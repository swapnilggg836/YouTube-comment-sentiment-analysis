# 🎯 YouTube Sentiment Analyzer

> **Analyze the emotional pulse of any YouTube video** — instantly understand what viewers truly feel through AI-powered sentiment analysis of comments.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Author](#-author)

---

## 🌟 Overview

**YouTube Sentiment Analyzer** is a full-stack web application that lets you paste any YouTube video URL and instantly receive a detailed sentiment breakdown of its comment section. It uses **NLP (Natural Language Processing)** to classify viewer comments into **Positive**, **Negative**, and **Neutral** categories, giving content creators, marketers, and researchers actionable insights into audience sentiment.

The app fetches up to **600 real-time comments** from YouTube, filters out spam, emojis-only content, and hyperlinks, then runs each comment through a sentiment scoring engine — finally presenting results as beautiful pie charts, bar graphs, and paginated comment lists.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔗 **YouTube URL Parsing** | Accepts both `youtube.com/watch?v=` and `youtu.be/` short URL formats |
| 🤖 **AI Sentiment Analysis** | Powered by VADER NLP for accurate compound polarity scoring |
| 🧹 **Smart Comment Filtering** | Removes hyperlinks, emoji-only comments, and uploader self-replies |
| 📊 **Visual Charts** | Auto-generated Pie Chart and Bar Chart showing sentiment distribution |
| 📋 **Paginated Comment Browser** | Browse 20 comments at a time per sentiment category |
| 📎 **Copy to Clipboard** | One-click copy any individual comment |
| ⚡ **Real-time Results** | Live analysis with average polarity score |
| 📱 **Responsive UI** | Clean, modern React interface |

---

## 🛠 Tech Stack

### 🔙 Backend

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.9+ | Core programming language |
| **Flask** | 3.x | Lightweight REST API web framework |
| **Flask-CORS** | 5.x | Cross-Origin Resource Sharing — allows React frontend to call the Flask API |
| **Google API Python Client** | 2.x | Official library to interact with the **YouTube Data API v3** |
| **VADER Sentiment** | 3.3+ | Rule-based NLP model for social media text sentiment scoring |
| **Matplotlib** | 3.x | Chart generation — renders Pie and Bar charts as in-memory PNG images |
| **emoji** | 2.x | Detects and counts emoji characters in comments for filtering |

#### Why VADER?
VADER (**Valence Aware Dictionary and sEntiment Reasoner**) is specifically designed for **social media text** — it understands slang, ALL CAPS, punctuation like `!!!`, emoticons, and short phrases typical in YouTube comments. It produces a `compound` score between `-1.0` (most negative) and `+1.0` (most positive).

- **Positive**: `compound >= 0.05`
- **Neutral**: `-0.05 < compound < 0.05`
- **Negative**: `compound <= -0.05`

---

### 🖥 Frontend

| Technology | Version | Purpose |
|---|---|---|
| **React** | 19.x | Component-based UI library |
| **Axios** | 1.x | Promise-based HTTP client for calling the Flask REST API |
| **Chart.js** | 4.x | Powerful canvas-based charting library |
| **react-chartjs-2** | 5.x | React wrapper for Chart.js |
| **Create React App** | 5.x | Zero-config React project scaffolding |

---

### 🌐 External APIs

| Service | Purpose |
|---|---|
| **YouTube Data API v3** | Fetches video metadata and up to 600 paginated comment threads |

---

## 🏗 Project Architecture

```
+----------------------------------------------------------+
|                      USER BROWSER                         |
|                                                           |
|   +---------------------------------------------------+   |
|   |           React Frontend (Port 3000)              |   |
|   |                                                   |   |
|   |   +-----------+    +------------+                 |   |
|   |   |   App.js  |    |  Chart.js  |                 |   |
|   |   | (Main UI) |    | (Visuals)  |                 |   |
|   |   +-----------+    +------------+                 |   |
|   +----------------------------+----------------------+   |
+--------------------------------|-------------------------+
                                 |  HTTP POST /analyze
                                 |  { video_url: "..." }
                                 v
+----------------------------------------------------------+
|          Flask REST API Backend (Port 5000)               |
|                                                           |
|   +---------------------------------------------------+   |
|   |                    app.py                         |   |
|   |                                                   |   |
|   |  1. Extract Video ID from URL                     |   |
|   |  2. Fetch up to 600 comments (YouTube API)        |   |
|   |  3. Filter irrelevant comments                    |   |
|   |  4. Run VADER Sentiment Analysis                  |   |
|   |  5. Generate Pie & Bar charts (Matplotlib)        |   |
|   |  6. Return JSON with charts + comment lists       |   |
|   +----------------------------+----------------------+   |
+--------------------------------|-------------------------+
                                 |  API Request
                                 v
               +--------------------------------+
               |   YouTube Data API v3          |
               |   (Google Cloud Console)        |
               +--------------------------------+
```

---

## How It Works

### Step-by-step Data Flow

```
1. User enters a YouTube URL
        |
        v
2. Frontend validates URL format (regex match for video ID)
        |
        v
3. Axios sends POST request to Flask backend at /analyze
        |
        v
4. Backend extracts 11-char video ID from URL
        |
        v
5. YouTube API fetches video metadata (channel ID, title)
        |
        v
6. YouTube API paginates through comment threads (100/page, max 600)
   -> Filters OUT comments by the video uploader (to avoid bias)
        |
        v
7. Comment filtering pipeline:
   -> Remove pure-hyperlink comments
   -> Remove emoji-heavy comments (emoji > 35% of total characters)
   -> Remove empty / whitespace-only strings
        |
        v
8. VADER Sentiment Analyzer scores each filtered comment
   -> Compound score >=  0.05  = POSITIVE
   -> Compound score <= -0.05  = NEGATIVE
   -> Else                     = NEUTRAL
        |
        v
9. Matplotlib generates Bar Chart + Pie Chart -> encoded as base64 PNG
        |
        v
10. Flask returns JSON response with counts, scores, comments & charts
        |
        v
11. React renders summary stats, charts, and paginated comment lists
```

---

## 📁 Project Structure

```
sentiment/
|
+-- README.md                        <- You are here
|
+-- backend/                         <- Python Flask REST API
|   +-- app.py                       <- Main Flask application & all core logic
|   |     fetch_and_analyze_comments()   <- Orchestrator function
|   |     filter_relevant_comments()     <- Comment cleaning/filtering
|   |     analyze_sentiments()           <- VADER sentiment scoring
|   |     generate_bar_chart()           <- Matplotlib bar chart -> base64
|   |     generate_pie_chart()           <- Matplotlib pie chart -> base64
|   |     POST /analyze                  <- REST endpoint
|   |
|   +-- sentiment.py                 <- Standalone YouTube comment fetcher (utility)
|   +-- requirements.txt             <- Python dependencies
|   +-- ytcomments.txt               <- Sample comments file
|   +-- venv/                        <- Python virtual environment (not committed)
|
+-- frontend/                        <- React Single Page Application
    +-- public/                      <- Static assets & index.html
    +-- src/
    |   +-- App.js                   <- Main component: URL input, API call, results
    |   +-- App.css                  <- Application styles
    |   +-- index.js                 <- React DOM entry point
    |   +-- components/
    |       +-- Chart.js             <- Chart.js wrapper component
    |       +-- CommentList.js       <- Comment listing component
    +-- package.json                 <- npm dependencies & scripts
    +-- .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9 or higher
- **Node.js** 18+ and **npm**
- A valid **YouTube Data API v3** key from [Google Cloud Console](https://console.cloud.google.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-sentiment-analyzer.git
cd youtube-sentiment-analyzer
```

---

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

#### Configure your API Key

Open `app.py` and replace the placeholder with your YouTube API key:

```python
# Line 16 in app.py
API_KEY = 'YOUR_YOUTUBE_DATA_API_KEY_HERE'
```

> **Security Note**: For production, use environment variables (.env file) instead of hardcoding API keys.

#### Start the Flask Server

```bash
python app.py
```

The backend will start at `http://127.0.0.1:5000`

---

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install npm dependencies
npm install

# Start the development server
npm start
```

The React app will open at `http://localhost:3000`

---

### 4. Using the Application

1. Open `http://localhost:3000` in your browser
2. Paste any YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Click **Analyze**
4. Wait for the backend to fetch and process comments (may take 10-30 seconds)
5. View the sentiment summary, charts, and browse categorized comments

---

## 📡 API Reference

### `POST /analyze`

Analyzes sentiment of comments for a given YouTube video.

**Request Body:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Success Response:**
```json
{
  "positive_count": 245,
  "negative_count": 78,
  "neutral_count": 134,
  "avg_polarity": 0.312,
  "polarity": [0.85, -0.42, 0.0],
  "positive_comments": ["Great video!", "Love this!"],
  "negative_comments": ["This is terrible..."],
  "neutral_comments": ["Interesting."],
  "bar_chart": "<base64-encoded-PNG>",
  "pie_chart": "<base64-encoded-PNG>"
}
```

**Error Response:**
```json
{
  "error": "No video URL provided"
}
```

---

## Python Dependencies (requirements.txt)

| Package | Purpose |
|---|---|
| `flask` | Web framework for the REST API |
| `flask-cors` | Enables cross-origin requests from the React frontend |
| `google-api-python-client` | YouTube Data API v3 client |
| `vaderSentiment` | NLP sentiment analyzer optimized for social media |
| `matplotlib` | Chart rendering (Pie & Bar charts) |
| `emoji` | Emoji detection and counting |

---

## Frontend Dependencies (package.json)

| Package | Purpose |
|---|---|
| `react` | Core UI library |
| `react-dom` | React DOM rendering |
| `axios` | HTTP client for API calls |
| `chart.js` | Canvas-based charting |
| `react-chartjs-2` | React bindings for Chart.js |

---

## 👤 Author

**Swapnil Gaikwad**

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

> **Tip**: For best results, analyze videos with at least 100+ comments. Videos with disabled comments will not return any data.
