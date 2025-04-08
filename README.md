# InfluenceIQ: Instagram Analytics & Fake Follower Detection

## 🚀 Overview

**InfluenceIQ** is an advanced Instagram analytics platform that leverages machine learning to provide detailed insights into Instagram profiles. It helps influencers, brands, and marketers make data-driven decisions by analyzing engagement metrics, detecting fake followers, and visualizing network graphs.

---

## ✨ Features

- **Profile Analytics**: Analyze follower count, following, posts, engagement rates, and more.
- **Fake Follower Detection**: Powered by a custom machine learning model hosted on FastAPI.
- **Commenter Analysis**: Extract and analyze profiles of users commenting on posts.
- **Network Visualization**: Interactive graphs showing follower relationships.
- **Leaderboard**: Compare top influencers across categories.
- **Category Detection**: Automatic classification of accounts into niches like fashion, travel, tech, etc.

---

## 🛠️ Technology Stack

- **Backend**: Flask (main app), FastAPI (ML model serving)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Scikit-learn
- **Data Processing**: Pandas
- **Visualization**: Matplotlib, NetworkX
- **Database**: AWS DynamoDB
- **Cloud Storage**: AWS S3
- **API Integration**: Apify for Instagram data scraping

---

## 📊 Screenshots
![Screenshot 2025-04-08 at 8 56 18 PM](https://github.com/user-attachments/assets/43b8b893-3ba4-4dd1-a60a-c08b8c055128)
![Screenshot 2025-04-08 at 8 56 51 PM](https://github.com/user-attachments/assets/4eec0b3f-7a6c-4767-ac01-8131cf1a67c7)
![Screenshot 2025-04-08 at 8 57 12 PM](https://github.com/user-attachments/assets/ef2caa83-5e29-4450-a6a0-aac0fa69c301)


  
  


---

## 🧠 How It Works

1. **Data Collection**:
   - Use Apify actors to scrape public Instagram data.
   - Extract profiles, posts, followers, and engagement metrics.

2. **Profile Analysis**:
   - Calculate engagement rates and influence scores.
   - Detect fake followers using a FastAPI-hosted ML model.

3. **Network Analysis**:
   - Generate visual representations of follower relationships.

4. **Commenter Analysis**:
   - Extract usernames of commenters from posts.
   - Analyze their profiles using machine learning.

---

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Apify API token
- AWS credentials

### Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/influenceiq.git
cd influenceiq

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export APIFY_TOKEN="your_apify_token"
export AWS_ACCESS_KEY="your_aws_access_key"
export AWS_SECRET_KEY="your_aws_secret_key"

# Start the application
python app.py
```

---

## 🌐 Usage

### Analyze Profiles
1. Navigate to the homepage.
2. Enter an Instagram username to analyze.
3. View comprehensive analytics including:
   - Profile statistics (followers, following, posts).
   - Engagement metrics (likes/comments per post).
   - Fake follower percentage (ML-powered detection).
   - Network graph visualization.

### Leaderboard
1. Navigate to `/leaderboard/view` to see top influencers.
2. Filter by category using the dropdown menu.
3. Sort by influence score, engagement rate, or follower count.

### Categories
Profiles are automatically categorized into niches:
- Fashion & Style
- Travel & Adventure
- Technology & Gadgets
- Food & Cooking
- Business & Entrepreneurship

Access category-specific leaderboards via `/leaderboard/category/[CATEGORY_ID]`.

---

## 🧠 Machine Learning Model

# 🚨 Fake Followers Detection API

This project provides a REST API that estimates the percentage of fake followers for Instagram profiles based solely on followers' metadata. It is built using **FastAPI**, a high-performance web framework for building APIs with Python.

---

## 🔍 Overview

Instagram users and influencers often attract fake followers—either bots or inactive accounts. This project uses machine learning and heuristics to detect such fake followers from profile and follower data.

---

## ⚙️ How It Works

### 1. 📦 Data Collection
- Follower metadata is gathered from Instagram-like sources via tools like **Apify** or scrapers.
- Typical data per follower includes:
  - `username`
  - `followersCount`
  - `followsCount`
  - `postsCount`

### 2. 🧠 Model (ML-based Classifier)
- A machine learning model (e.g., RandomForestClassifier or XGBoost) was trained on a labeled dataset containing real and fake accounts.
- The features used include:
  - Number of posts
  - Followers/following count
  - Profile privacy
  - Presence of a profile picture
  - Bio length
  - Username length and numeric patterns

### 3. 🔗 API Endpoint
- The trained model and/or heuristic logic is served using FastAPI.
- The user sends a JSON of followers to the `/predict_fake_followers` endpoint.
- The API processes the data and returns:
  - Total followers analyzed
  - Estimated fake follower percentage

---


## 📈 Influence Score Calculation

The influence score is calculated using a weighted formula:
1. Engagement rate (35%)
2. Authenticity (25%)
3. Content quality (25%)
4. Reach (15%)

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


This README provides everything needed for users and contributors to understand and use your project effectively while showcasing its capabilities in an interactive and professional manner!

Citations:
[1] https://www.hatica.io/blog/best-practices-for-github-readme/
[2] https://www.sitepoint.com/github-profile-readme/
[3] https://everhour.com/blog/github-readme-template/
[4] https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
[5] https://github.com/matiassingers/awesome-readme
[6] https://tilburgsciencehub.com/topics/collaborate-share/share-your-work/content-creation/readme-best-practices/
[7] https://github.com/abhisheknaiidu/awesome-github-profile-readme

