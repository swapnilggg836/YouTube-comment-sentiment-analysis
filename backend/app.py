from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
import re
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# API Key for YouTube API
API_KEY = 'AIzaSyBKw7WKvJxheeeDh8jdruGUYe8tzEDBqug'

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Helper function to fetch comments and perform sentiment analysis
def fetch_and_analyze_comments(video_url):
    # Extract video ID from URL
    video_id = video_url.split('v=')[-1]

    # Fetch video information
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Get uploader channel ID
    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']

    comments = []
    nextPageToken = None
    while len(comments) < 600:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # Fetch up to 100 comments per request
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            if comment['authorChannelId']['value'] != uploader_channel_id:
                comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    # Filter relevant comments (remove emojis, hyperlinks, etc.)
    relevant_comments = filter_relevant_comments(comments)
    
    # Analyze sentiment
    polarity, positive_comments, negative_comments, neutral_comments = analyze_sentiments(relevant_comments)

    # Generate sentiment summary
    sentiment_summary = {
        'positive_count': len(positive_comments),
        'negative_count': len(negative_comments),
        'neutral_count': len(neutral_comments),
        'avg_polarity': sum(polarity) / len(polarity) if polarity else 0,
        'positive_comments': positive_comments,
        'negative_comments': negative_comments,
        'neutral_comments': neutral_comments,
        'polarity': polarity
    }

    # Generate charts as base64 encoded images
    sentiment_summary['bar_chart'] = generate_bar_chart(positive_comments, negative_comments, neutral_comments)
    sentiment_summary['pie_chart'] = generate_pie_chart(positive_comments, negative_comments, neutral_comments)

    return sentiment_summary

def filter_relevant_comments(comments):
    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    threshold_ratio = 0.65
    relevant_comments = []

    for comment_text in comments:
        comment_text = comment_text.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))

        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)
    
    return relevant_comments

def analyze_sentiments(comments):
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    sentiment_analyzer = SentimentIntensityAnalyzer()

    for comment in comments:
        sentiment_dict = sentiment_analyzer.polarity_scores(comment)
        polarity.append(sentiment_dict['compound'])

        if sentiment_dict['compound'] > 0.05:
            positive_comments.append(comment)
        elif sentiment_dict['compound'] < -0.05:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)
    
    return polarity, positive_comments, negative_comments, neutral_comments

def generate_bar_chart(positive_comments, negative_comments, neutral_comments):
    labels = ['Positive', 'Negative', 'Neutral']
    comment_counts = [len(positive_comments), len(negative_comments), len(neutral_comments)]

    fig, ax = plt.subplots()
    ax.bar(labels, comment_counts, color=['blue', 'red', 'grey'])
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Comment Count')
    ax.set_title('Sentiment Analysis of Comments')

    # Convert plot to base64 image
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

    return img_base64

def generate_pie_chart(positive_comments, negative_comments, neutral_comments):
    labels = ['Positive', 'Negative', 'Neutral']
    comment_counts = [len(positive_comments), len(negative_comments), len(neutral_comments)]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(comment_counts, labels=labels, autopct='%1.1f%%')
    ax.set_title('Sentiment Distribution')

    # Convert plot to base64 image
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

    return img_base64

# API endpoint to analyze comments
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    sentiment_summary = fetch_and_analyze_comments(video_url)
    return jsonify(sentiment_summary)

if __name__ == '__main__':
    app.run(debug=True)
    
