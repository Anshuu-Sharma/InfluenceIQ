from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Add this
import os
from main import analyze_instagram_influence,analyze_commenters,save_commenter_analysis
from data_extractor import get_post_url, get_commenters, get_commenters_data
from db_helpers import get_leaderboard, save_analysis, update_existing_data_with_categories,table, get_precomputed_influencers

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Add CORS support


@app.route('/')
@app.route('/index/view')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Perform analysis (replace with your logic)
        result = analyze_instagram_influence(username)
        


        # Add categories to the result
        categories = result.get('categories', ['No category detected'])
        result['categories'] = categories

        return jsonify(result), 200
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return jsonify({'error': str(e)}), 500



@app.route('/leaderboard')
def leaderboard_api():
    sort_by = request.args.get('sort_by', 'influence_score')
    category = request.args.get('category')
    limit = int(request.args.get('limit', 20))
    
    try:
        results = get_leaderboard(sort_by, category, limit)
        return jsonify(results)
    except Exception as e:
        print(f"Leaderboard API error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/leaderboard/view')
def leaderboard_page():
    return render_template('leaderboard.html')

# 1 april ansh
# category code
@app.route('/categories')
def get_categories():
    """Get all available categories"""
    categories = [
        {"id": "HEALTH", "name": "Health & Wellness"},
        {"id": "FASHION", "name": "Fashion & Style"},
        {"id": "EDUCATION", "name": "Education"},
        {"id": "TECH", "name": "Technology"},
        {"id": "FOOD", "name": "Food & Cooking"},
        {"id": "TRAVEL", "name": "Travel"},
        {"id": "BUSINESS", "name": "Business"},
        {"id": "GENERAL", "name": "General"}
    ]
    return jsonify(categories)

@app.route('/leaderboard/category/<category>')
def category_leaderboard(category):
    return render_template('category_leaderboard.html', category=category)


@app.route('/admin/update-categories')
def update_categories():
    update_existing_data_with_categories()
    return "Categories updated successfully"

@app.route('/precomputed-influencers')
def precomputed_influencers():
    try:
        influencers = [
            {
            "username": "cristiano",
            "name": "Cristiano Ronaldo",
            "category": "Sports",
            "followers": 651507902,
            "influence_score": 100,
            "imageUrl": "/static/images/cristiano_ronaldo.jpeg",
            "verified": True,
            "avg_likes": 5000000,
            "avg_comments": 300000,
            "engagement_rate": 0.30,
            "fake_follower_percentage": 5.84
        },
        {
            'username': 'kyliejenner',
            "name": "Kylie Jenner",
            'influence_score': 97.2,
            'engagement_rate': 1.2,
            'followers': 394000000,
            'category': "Fashion & Beauty",
            "imageUrl": '/static/images/kylie_jenner.jpeg',
            "verified": True,
            "avg_likes": 2513252,
            "avg_comments": 6177,
            "engagement_rate": 0.25,
            "fake_follower_percentage": 7.44
        },
        {
            'username': 'selenagomez',
            'name': "Selena Gomez",
            'influence_score': 96.8,
            'engagement_rate': 1.5,
            'followers': 421000000,
            'category': "Music & Lifestyle",
            'imageUrl': '/static/images/selena_gomez.jpeg',
            "verified": True,
            "avg_likes": 2487642,
            "avg_comments": 12.1,
            "engagement_rate": 0.23,
            "fake_follower_percentage": 7.98
        },
        ]
        return jsonify(influencers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



#fastapi
# Add to imports
import threading
from ml_server import start_ml_server

# Add before app.run()
# Start ML server in a background thread
threading.Thread(target=start_ml_server).start()



@app.route('/admin/view-raw-data')
def view_raw_data():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=9000)  # Change port to 9000


