from googleapiclient.discovery import build

# Replace with your actual API key
api_key = 'AIzaSyBKw7WKvJxheeeDh8jdruGUYe8tzEDBqug'

# Build the YouTube API client using your API key
youtube = build('youtube', 'v3', developerKey=api_key)

def analyze_video_comments(video_url):
    # Extract video ID from the URL (Assuming the URL is in the format "https://www.youtube.com/watch?v=video_id")
    video_id = video_url.split('v=')[-1]

    # Call the YouTube API to get video comments
    video_response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()

    # Check if video response is valid
    if 'items' not in video_response or len(video_response['items']) == 0:
        return {'error': 'Video not found or has no comments'}

    # Extract relevant information from the response
    video_info = video_response['items'][0]
    video_title = video_info['snippet']['title']
    video_description = video_info['snippet']['description']
    video_comments_count = video_info['statistics'].get('commentCount', 0)

    # Get video comments
    comment_response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Adjust the max results to your needs
    ).execute()

    comments = []
    for item in comment_response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return {
        'title': video_title,
        'description': video_description,
        'comments_count': video_comments_count,
        'comments': comments
    }
