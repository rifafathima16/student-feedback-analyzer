from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.secret_key = 'dev-secret'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017')
db = client['feedback_db']
feedbacks_collection = db['feedbacks']

analyzer = SentimentIntensityAnalyzer()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Gather form data
        student_name = request.form.get('name')  # optional
        subject = request.form.get('subject')
        faculty = request.form.get('faculty')
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()

        # Basic validation: comment must not be empty
        if not comment:
            flash('Comment cannot be empty.', 'error')
            # Re-render form preserving entered values
            return render_template('index.html',
                                   name=student_name,
                                   subject=subject,
                                   faculty=faculty,
                                   rating=rating)

        # Sentiment analysis on comment
        score = analyzer.polarity_scores(comment)['compound']
        if score >= 0.05:
            sentiment = 'Positive'
        elif score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        from datetime import datetime
        feedback_doc = {
            'name': student_name,
            'subject': subject,
            'faculty': faculty,
            'rating': int(rating) if rating else None,
            'comment': comment,
            'score': score,
            'sentiment': sentiment,
            'timestamp': datetime.utcnow()
        }
        feedbacks_collection.insert_one(feedback_doc)
        return render_template('thankyou.html')
    # For GET requests, just render the form
    return render_template('index.html')

def get_suggestions(feedbacks):
    """Generate rule‑based improvement suggestions based on negative comments.
    Returns a list of up to 5 suggestion strings. If the majority of feedback is
    positive, returns an encouraging message instead.
    """
    # Mapping of keywords (lowercase) to suggestion text
    keyword_map = {
        ('fast', 'speed'): "Slow down and recap often.",
        ('boring',): "Add interactive activities and examples.",
        ('confusing', 'unclear'): "Use simpler explanations and diagrams.",
        ('notes',): "Share study material with students.",
        ('doubt',): "Allocate dedicated Q&A time.",
        ('assignment',): "Provide clearer assignment instructions.",
    }

    # Count suggestions occurrences
    suggestion_counts = {}
    # Analyze only negative feedbacks
    for fb in feedbacks:
        if fb.get('sentiment') != 'Negative':
            continue
        comment = fb.get('comment', '').lower()
        for keywords, suggestion in keyword_map.items():
            if any(kw in comment for kw in keywords):
                suggestion_counts[suggestion] = suggestion_counts.get(suggestion, 0) + 1
    # If no negative feedbacks or positive dominates, give encouraging message
    total = len(feedbacks)
    pos = sum(1 for f in feedbacks if f.get('sentiment') == 'Positive')
    if total == 0 or pos > total / 2:
        return ["Great job! The feedback is largely positive. Keep up the good work!"]
    # Sort suggestions by frequency and take top 5
    sorted_suggestions = sorted(suggestion_counts.items(), key=lambda kv: kv[1], reverse=True)
    return [s for s, _ in sorted_suggestions[:5]]

@app.route('/dashboard')
def dashboard():
    # Optional faculty filter via query param
    selected_faculty = request.args.get('faculty')

    # Base query
    query = {}
    if selected_faculty:
        query['faculty'] = selected_faculty

    # Retrieve all matching feedbacks
    feedbacks = list(feedbacks_collection.find(query))

    # Compute overall stats
    total = len(feedbacks)
    pos = [f for f in feedbacks if f.get('sentiment') == 'Positive']
    neu = [f for f in feedbacks if f.get('sentiment') == 'Neutral']
    neg = [f for f in feedbacks if f.get('sentiment') == 'Negative']
    pos_count, neu_count, neg_count = len(pos), len(neu), len(neg)
    # Avoid division by zero
    pos_pct = round(pos_count / total * 100, 1) if total else 0
    neu_pct = round(neu_count / total * 100, 1) if total else 0
    neg_pct = round(neg_count / total * 100, 1) if total else 0

    # Average rating (ignore missing ratings)
    ratings = [f.get('rating') for f in feedbacks if f.get('rating') is not None]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    # Recent 10 feedbacks (sorted by timestamp descending)
    recent_feedbacks = sorted(feedbacks, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]

    # Faculty list for dropdown (distinct values)
    faculty_list = feedbacks_collection.distinct('faculty')

    # Generate suggestions
    suggestions = get_suggestions(feedbacks)

    return render_template(
        'dashboard.html',
        total=total,
        pos_count=pos_count,
        neu_count=neu_count,
        neg_count=neg_count,
        pos_pct=pos_pct,
        neu_pct=neu_pct,
        neg_pct=neg_pct,
        avg_rating=avg_rating,
        recent_feedbacks=recent_feedbacks,
        faculty_list=faculty_list,
        selected_faculty=selected_faculty,
        suggestions=suggestions,
    )


if __name__ == '__main__':
    app.run(debug=True)
