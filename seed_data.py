# Seed script to generate 1,000 realistic fake student feedback records
# Run this script after the virtual environment is activated: python seed_data.py

import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# MongoDB connection (same as app)
client = MongoClient('mongodb://localhost:27017')
db = client['feedback_db']
collection = db['feedbacks']

# Clear existing data safely
collection.delete_many({})

# Fixed lists
faculty_names = [
    'Dr. Smith',
    'Prof. Johnson',
    'Dr. Lee',
    'Prof. Patel',
    'Dr. Martinez'
]
subjects = [
    'Mathematics',
    'Science',
    'History',
    'Literature',
    'Computer Science',
    'Art'
]
# 40 example comment sentences (mix of sentiment)
comments = [
    # Positive
    'The professor explained the concepts very clearly.',
    'I really enjoyed the course material and the assignments.',
    'Great class! Learned a lot and felt engaged.',
    'The lectures were inspiring and well-structured.',
    'I appreciated the prompt feedback on my work.',
    'Fantastic teaching style, made difficult topics easy.',
    'The lab sessions were hands-on and very helpful.',
    'I felt motivated throughout the semester.',
    'The professor was approachable and supportive.',
    'Excellent resources and reading material.',
    # Neutral
    'The class was okay, nothing exceptional.',
    'Content was covered as expected.',
    'The pacing was average.',
    'I attended most lectures.',
    'Assignments were standard.',
    'The course met my basic expectations.',
    'It was a regular semester.',
    'The professor was neutral in tone.',
    'Materials were sufficient.',
    'Overall, the experience was fine.',
    # Negative
    'The lectures were boring and hard to follow.',
    'I struggled to understand the material.',
    'The professor did not provide clear explanations.',
    'Assignments were overly difficult and unclear.',
    'The class felt disorganized.',
    'Feedback was delayed and vague.',
    'I did not feel engaged in the course.',
    'The course workload was unreasonable.',
    'The professor seemed uninterested.',
    'Overall, I was disappointed with this class.'
]

analyzer = SentimentIntensityAnalyzer()

# Helper to generate a random datetime within the last 6 months
def random_timestamp():
    now = datetime.utcnow()
    days_back = random.randint(0, 180)  # ~6 months
    seconds_back = random.randint(0, 86400)
    return now - timedelta(days=days_back, seconds=seconds_back)

records = []
for i in range(1000):
    name = f'Student_{i+1}'
    subject = random.choice(subjects)
    faculty = random.choice(faculty_names)
    rating = random.randint(1, 5)
    comment = random.choice(comments)
    # VADER sentiment score
    score = analyzer.polarity_scores(comment)['compound']
    if score >= 0.05:
        sentiment = 'Positive'
    elif score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    doc = {
        'name': name,
        'subject': subject,
        'faculty': faculty,
        'rating': rating,
        'comment': comment,
        'score': score,
        'sentiment': sentiment,
        'timestamp': random_timestamp()
    }
    records.append(doc)

# Bulk insert for efficiency
collection.insert_many(records)
print(f'Inserted {len(records)} fake feedback records.')
