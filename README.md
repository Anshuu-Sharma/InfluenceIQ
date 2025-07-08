# InfluenceIQ: Instagram Analytics
## 🚀 Overview

**InfluenceIQ** is an advanced Instagram analytics platform that provide detailed insights into Instagram profiles. It helps influencers, brands, and marketers make data-driven decisions by analyzing engagement metrics.

---

## ✨ Features

- **Profile Analytics**: Analyze follower count, following, posts, engagement rates, and more.
- **Commenter Analysis**: Extract and analyze profiles of users commenting on posts.
- **Leaderboard**: Compare top influencers across categories.
- **Category Detection**: Automatic classification of accounts into niches like fashion, travel, tech, etc.

---

## 🛠️ Technology Stack

- **Backend**: Flask (main app)
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
![Screenshot 2025-04-08 at 8 57 12 PM](https://github.com/user-attachments/assets/ef2caa83-5e29-4450-a6a0-aac0fa69c301)


  
  


---

## 🧠 How It Works

1. **Data Collection**:
   - Use Apify actors to scrape public Instagram data.
   - Extract profiles, posts, followers, and engagement metrics.

2. **Profile Analysis**:
   - Calculate engagement rates and influence scores.

3. **Commenter Analysis**:
   - Extract usernames of commenters from posts.

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
