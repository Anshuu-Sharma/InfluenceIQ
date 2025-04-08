import re
import math




def extract_number(text):
    """Convert text numbers to integers"""
    if isinstance(text, (int, float)):
        return int(text)
    return int(re.sub(r"[^0-9]", "", str(text))) if text else 0

def calculate_influence_metrics(profile_data, engagement_data):
    """Calculate metrics with improved 2025 formula"""
    followers = profile_data.get('followers', 0)
    posts_analyzed = engagement_data.get('posts_analyzed', 12)
    
    # Handle division by zero
    safe_divisor = max(followers, 1)
    
    # Calculate weighted engagement using the 2025 formula
    weighted_engagement = (
        engagement_data.get('total_likes', 0) * 0.35 +
        engagement_data.get('total_comments', 0) * 0.25 +
        engagement_data.get('total_shares', 0) * 0.25 +
        engagement_data.get('total_saves', 0) * 0.15
    )
    
    # Calculate engagement rate per post
    engagement_rate = (weighted_engagement / posts_analyzed) / safe_divisor * 100
    # Calculate post frequency (posts per day assuming 30-day period)
    post_frequency = posts_analyzed / 30
    
    return {
        'engagement_rate': round(engagement_rate, 2),
        'post_frequency': round(post_frequency, 2),
        'avg_shares': round(engagement_data.get('avg_shares', 0), 2),
        'avg_saves': round(engagement_data.get('avg_saves', 0), 2)
    }

def estimate_fake_followers(profile_data, engagement_data):
    """Improved fake follower estimation using engagement patterns"""
    followers = profile_data.get('followers', 0)
    
    # Calculate engagement per follower
    engagement_per_follower = (
        engagement_data.get('total_likes', 0) +
        engagement_data.get('total_comments', 0) +
        engagement_data.get('total_saves', 0) +
        engagement_data.get('total_shares', 0)
    ) / max(followers, 1)
    
    # More nuanced fake follower estimation based on engagement patterns
    if engagement_per_follower < 0.005:
        return min(90, 80 - (engagement_per_follower * 1000))  # Very low engagement suggests up to 80-90% fake
    elif engagement_per_follower < 0.01:
        return min(70, 60 - (engagement_per_follower * 1000))  # Low engagement suggests up to 60-70% fake
    elif engagement_per_follower < 0.03:
        return min(50, 40 - (engagement_per_follower * 500))   # Below average engagement suggests up to 40-50% fake
    elif engagement_per_follower < 0.05:
        return min(30, 20 - (engagement_per_follower * 200))   # Average engagement suggests up to 20-30% fake
    else:
        return max(5, min(20, 15 - (engagement_per_follower * 100)))  # Good engagement still has some fake followers (5-20%)

def calculate_influence_score(metrics):
    weights = {
        'engagement': 0.40,
        'authenticity': 0.30,
        'content_quality': 0.20,
        'reach': 0.10
    }
    
    raw_score = (
        metrics.get('engagement', 0) * weights['engagement'] +
        metrics.get('authenticity', 0) * weights['authenticity'] +
        metrics.get('content_quality', 0) * weights['content_quality'] +
        metrics.get('reach', 0) * weights['reach']
    )
    
    # Improved normalization
    normalized_score = 100 * (1 - math.exp(-raw_score / 60))
    return round(max(0, min(100, normalized_score)), 2)




# fastapi
import pandas as pd
import requests

def estimate_fake_followers_from_commenters(commenters_data):
    """Analyze commenters by sending data to local FastAPI classifier"""
    
    print(f"[DEBUG] Analyzing {len(commenters_data)} commenters with ML model")
    
    # Convert raw follower data to required API input format
    input_payload = []
    for follower in commenters_data:
        formatted = {
            "username": follower['username'],
            "posts": follower['posts'],
            "following": follower['following'],
            "followers": follower['followers'],
            "has_profile_pic": follower['has_profile_pic'],
            "private": follower['private'],
            "follower_following_ratio": follower['follower_following_ratio'],
            "bio_length": follower['bio_length'],
            "username_length": follower['username_length'],
            "digits_in_username": follower['digits_in_username']
        }
        input_payload.append(formatted)
    
    try:
        # Send request to FastAPI endpoint
        print(f"[DEBUG] Sending request to FastAPI endpoint")
        response = requests.post("http://localhost:8000/predict", json=input_payload)
        response.raise_for_status()
        predictions = response.json()['predictions']
        print(f"[DEBUG] Received predictions: {predictions}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch predictions from API: {str(e)}")
        return -1

    # Convert to DataFrame for analysis
    df = pd.DataFrame(input_payload)
    df['is_fake'] = predictions

    # Calculate fake follower percentage
    fake_percentage = df['is_fake'].mean() * 100
    real_percentage = 100 - fake_percentage
    
    print(f"[DEBUG] ML model fake follower percentage: {fake_percentage:.2f}%")
    print(f"[DEBUG] ML model real follower percentage: {real_percentage:.2f}%")
    
    return fake_percentage
