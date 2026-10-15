// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const pageSize = 20;

  const handleInputChange = (e) => {
    setVideoUrl(e.target.value);
  };

  const normalizeUrl = (url) => {
    const match = url.match(/(?:v=|\.be\/)([\w-]{11})/);
    return match ? match[1] : null;
  };

  const handleAnalyze = async () => {
    const videoId = normalizeUrl(videoUrl);
    if (!videoId) {
      setError('Invalid YouTube URL');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', {
        video_url: `https://www.youtube.com/watch?v=${videoId}`
      });
      setResult(response.data);
      setError('');
      setPage(0);
    } catch (error) {
      setError('Failed to analyze the video. Please check the URL or try again later.');
      setResult(null);
    }
  };

  const paginatedComments = (comments) => {
    return comments.slice(page * pageSize, (page + 1) * pageSize);
  };

  const CommentList = ({ sentiment, comments }) => {
    const colors = {
      positive: '#d1e7dd',
      negative: '#f8d7da',
      neutral: '#e2e3e5',
    };

    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text);
      alert('Comment copied to clipboard!');
    };

    return (
      <div className="comment-section">
        <h3>{sentiment.toUpperCase()} Comments</h3>
        {paginatedComments(comments).map((comment, i) => (
          <div
            key={i}
            className="comment-box"
            style={{ backgroundColor: colors[sentiment] }}
          >
            <p>{comment}</p>
            <button className="copy-btn" onClick={() => copyToClipboard(comment)}>
              📋
            </button>
          </div>
        ))}
        {comments.length > (page + 1) * pageSize && (
          <button
            className="show-more-btn"
            onClick={() => setPage(page + 1)}
          >
            Show More
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <h1> YouTube Sentiment Analyzer</h1>
      </nav>

      <div className="content-container">
        <input
          type="text"
          placeholder="Enter YouTube video URL"
          value={videoUrl}
          onChange={handleInputChange}
        />
        <button onClick={handleAnalyze}>Analyze</button>

        {error && <p className="error-text">{error}</p>}

        {result && (
          <div className="result-container">
            <h2>Sentiment Summary</h2>
            <p>👍 Positive Comments: {result.positive_count}</p>
            <p>👎 Negative Comments: {result.negative_count}</p>
            <p>😐 Neutral Comments: {result.neutral_count}</p>
            <p>📈 Average Polarity: {result.avg_polarity.toFixed(3)}</p>

            <h3>📊 Sentiment Distribution</h3>
            <img src={`data:image/png;base64,${result.pie_chart}`} alt="Pie Chart" />

            <h3>📊 Bar Chart</h3>
            <img src={`data:image/png;base64,${result.bar_chart}`} alt="Bar Chart" />

            <CommentList sentiment="positive" comments={result.positive_comments} />
            <CommentList sentiment="negative" comments={result.negative_comments} />
            <CommentList sentiment="neutral" comments={result.neutral_comments} />
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Created By Swapnil Gaikwad</p>
      </footer>
    </div>
  );
}

export default App;
