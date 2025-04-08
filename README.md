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

The fake follower detection system uses a machine learning model hosted on FastAPI. It analyzes:
- Username characteristics (length, digits).
- Profile completeness (bio length, profile picture).
- Following/follower ratios.
- Posting frequency and patterns.

The model returns a percentage score indicating the likelihood of fake followers in an account.

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

## 📞 Contact

For questions or feedback:
- Email: contact@influenceiq.com
- Twitter: [@InfluenceIQ](https://twitter.com/InfluenceIQ)
- Website: [www.influenceiq.com](https://www.influenceiq.com)

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
[8] https://github.com/othneildrew/Best-README-Template
[9] https://www.linkedin.com/pulse/create-cool-github-profile-readmemd-muhammedh-shadir
[10] https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc
[11] https://github.com/banesullivan/README
[12] https://gprm.itsvg.in
[13] https://www.readme-templates.com
[14] https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
[15] https://www.reddit.com/r/github/comments/uulygm/what_are_some_really_nice_github_profile_readmes/
[16] https://github.com/durgeshsamariya/awesome-github-profile-readme-templates
[17] https://github.com/jehna/readme-best-practices
[18] https://www.youtube.com/watch?v=7FHiew0_NLQ
[19] https://www.youtube.com/watch?v=rCt9DatF63I
[20] https://dev.to/mfts/how-to-write-a-perfect-readme-for-your-github-project-59f2

---
Answer from Perplexity: https://www.perplexity.ai/search/ansh-influence-ai-vK9Izg2oSi2tv5lrTg7lGA?utm_source=copy_output
