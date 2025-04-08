from apify_client import ApifyClient
import statistics
import networkx as nx 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from db_helpers import save_analysis
import pandas as pd
import random
import os
from datetime import datetime
from apify_config import APIFY_KEY

# Initialize the ApifyClient with your Apify API token
client = ApifyClient(APIFY_KEY)

#fake followers
from apify_client import ApifyClient

def get_post_url(username):
    """
    Fetch the URL of one post of the user using Apify Instagram Post Scraper actor.
    """
    client = ApifyClient(token=APIFY_KEY)  # Replace with your actual Apify API token

    # Input for the Instagram Post Scraper actor
    run_input = {
        "username": [username],  # Wrap the username in a list
        "resultsLimit": 1,       # Limit to one post
        "scrapeComments": False  # We don't need comments for this step
    }

    try:
        print(f"[DEBUG] Fetching posts for user: {username}")
        # Run the actor
        run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)

        # Fetch results from dataset
        dataset = client.dataset(run["defaultDatasetId"]).list_items()
        dataset_items = dataset.items  # Access the items attribute of ListPage

        # Debugging: Check if dataset_items is empty
        if not dataset_items:
            print(f"[DEBUG] No items found in dataset for user: {username}")
            return None

        # Extract the URL of the first post
        post_url = dataset_items[0].get("url", "")
        print(f"[DEBUG] Post URL: {post_url}")
        return post_url

    except Exception as e:
        print(f"[ERROR] Failed to fetch post URL for @{username}: {str(e)}")
        return None


from apify_client import ApifyClient

def get_commenters(post_url, owner_username, limit=3):
    """
    Fetch usernames of commenters from an Instagram post using Apify Instagram Comment Scraper actor.
    Ensures that the owner of the post is excluded from the results.
    """
    client = ApifyClient(token=APIFY_KEY)  # Replace with your actual Apify API token

    # Ensure limit is an integer
    limit = int(limit)

    # Input for the Instagram Comment Scraper actor
    run_input = {
        "directUrls": [post_url],  # Pass the post URL
        "resultsLimit": 50         # Maximum allowed is 50 comments per post
    }

    try:
        print(f"[DEBUG] Fetching comments for post: {post_url}")
        # Run the actor
        run = client.actor("apify/instagram-comment-scraper").call(run_input=run_input)

        # Fetch results from dataset
        dataset = client.dataset(run["defaultDatasetId"]).list_items()
        dataset_items = dataset.items  # Access the items attribute of ListPage

        # Extract unique commenter usernames, excluding the owner
        commenters = []
        for item in dataset_items:
            username = item.get("ownerUsername")
            if username and username != owner_username and username not in commenters:
                commenters.append(username)
                print(f"[DEBUG] Found commenter: {username}")
                if len(commenters) >= limit:  # Fetch extra users to handle exclusions
                    break

        # Ensure we return exactly 'limit' unique usernames excluding the owner
        filtered_commenters = [user for user in commenters if user != owner_username][:limit]
        print(f"[DEBUG] Extracted {len(filtered_commenters)} commenters: {filtered_commenters}")
        return filtered_commenters

    except Exception as e:
        print(f"[ERROR] Failed to fetch commenters for post {post_url}: {str(e)}")
        return []

from apify_client import ApifyClient

def get_commenters_data(usernames):
    """
    Fetch profile data for multiple usernames using Apify Instagram Profile Scraper actor.
    """
    client = ApifyClient(token=APIFY_KEY)  # Replace with your actual Apify API token

    # Input for the Instagram Profile Scraper actor
    run_input = {
        "usernames": usernames,  # Pass the list of usernames
        "resultsLimit": len(usernames)  # Limit to the number of usernames provided
    }

    try:
        print(f"[DEBUG] Fetching profile data for commenters: {usernames}")
        # Run the actor
        run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)

        # Fetch results from dataset
        dataset = client.dataset(run["defaultDatasetId"]).list_items()
        dataset_items = dataset.items  # Access the items attribute of ListPage

        # Debugging: Check raw dataset items
        print(f"[DEBUG] Raw dataset items: {dataset_items}")

        if not dataset_items:
            print(f"[DEBUG] No data found for commenters: {usernames}")
            return []

        # Extract and return profile data for each commenter
        profiles = []
        for profile_data in dataset_items:
            profiles.append({
                "username": profile_data.get("username", ""),
                "postsCount": profile_data.get("postsCount", 0),
                "followsCount": profile_data.get("followsCount", 0),
                "followersCount": profile_data.get("followersCount", 0),
                "profilePicUrl": profile_data.get("profilePicUrl", ""),
                "isPrivate": profile_data.get("isPrivate", False),
                "biography": profile_data.get("biography", "")
            })

        return profiles

    except Exception as e:
        print(f"[ERROR] Failed to fetch profile data for commenters: {str(e)}")
        return []



# detect the category of the person
def detect_categories(profile_data):
    """Detect categories based on bio and posts"""
    categories = []
    bio = profile_data.get('biography', '').lower()
    
    # Category detection based on keywords in bio
    category_keywords = {
        'HEALTH': ['fitness', 'health', 'wellness', 'workout', 'nutrition', 'diet'],
        'FASHION': ['fashion', 'style', 'outfit', 'model', 'clothing', 'beauty'],
        'EDUCATION': ['learn', 'education', 'teacher', 'school', 'university', 'knowledge'],
        'TECH': ['tech', 'technology', 'coding', 'developer', 'programming', 'digital'],
        'FOOD': ['food', 'recipe', 'cook', 'chef', 'baking', 'cuisine'],
        'TRAVEL': ['travel', 'adventure', 'explore', 'destination', 'wanderlust', 'trip'],
        'BUSINESS': ['entrepreneur', 'business', 'startup', 'marketing', 'success', 'leadership']
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in bio for keyword in keywords):
            categories.append(category)
    
    # If no categories detected, mark as GENERAL
    if not categories:
        categories.append('GENERAL')
        
    return categories


def get_follower_count(username):
    """Get follower count using Instagram Followers Count Scraper"""
    try:
        # Prepare the Actor input for the follower count scraper
        follower_input = {
            "usernames": [username]  # This is correctly formatted
        }
        
        print(f"Fetching follower count for @{username}...")
        # Run the Actor and wait for it to finish
        follower_run = client.actor("apify/instagram-profile-scraper").call(run_input=follower_input)
        
        # Fetch results from the run's dataset
        follower_dataset = client.dataset(follower_run["defaultDatasetId"])
        follower_items = list(follower_dataset.iterate_items())
        
        if follower_items and len(follower_items) > 0:
            # The correct field name might be different based on the API response
            for field in ['followersCount', 'followers', 'followerCount']:
                if field in follower_items[0]:
                    return follower_items[0][field]
            
            # If we couldn't find the follower count, try an alternative scraper
            return get_follower_count_alternative(username)
    except Exception as e:
        print(f"Error fetching follower count: {str(e)}")
        return get_follower_count_alternative(username)  # Try alternative method

def get_follower_count_alternative(username):
    """Alternative method to get follower count using Instagram Profile Scraper"""
    try:
        profile_input = {
            "usernames": [username],
            "resultsType": "details"
        }
        
        print(f"Trying alternative method to fetch follower count for @{username}...")
        profile_run = client.actor("apify/instagram-profile-scraper").call(run_input=profile_input)
        profile_dataset = client.dataset(profile_run["defaultDatasetId"])
        profile_items = list(profile_dataset.iterate_items())
        
        if profile_items and len(profile_items) > 0:
            return profile_items[0].get('followersCount', 1)
        return 1
    except Exception as e:
        print(f"Error with alternative follower count method: {str(e)}")
        return 1

def get_followers_list(username, limit=100):
    try:
        print(f"Fetching followers list for @{username}...")
        run_input = {"username": username, "resultsLimit": limit}
        run = client.actor("apify/instagram-followers-scraper").call(run_input=run_input)
        dataset = client.dataset(run["defaultDatasetId"])
        followers = list(dataset.iterate_items())

        if not followers:
            print("No followers retrieved. Using synthetic data.")
            return generate_synthetic_followers(limit)

        print(f"Retrieved {len(followers)} followers for @{username}.")
        return followers
    except Exception as e:
        print(f"Error fetching followers: {str(e)}")
        return generate_synthetic_followers(limit)


def generate_synthetic_followers(count):
    print(f"Generating {count} synthetic followers...")
    followers = []
    for i in range(count):
        is_bot = random.random() < 0.3  # 30% chance of being a bot
        followers.append({
            'username': f"user{i:05d}",
            'is_bot': is_bot,
            'followersCount': random.randint(50, 500),
            'followsCount': random.randint(1000, 5000),
            'postsCount': random.randint(0, 50),
        })
    return followers


def calculate_engagement(username, post_limit):
    """"Calculate engagement metrics for a given Instagram username"""
    # First, get the profile data using the profile scraper
    profile_data = get_profile_data(username)
    follower_count = profile_data['followers']
    following_count = profile_data['following']
    profile_url = profile_data['profile_url']
    biography = profile_data['biography']
    full_name = profile_data['full_name']
    verified = profile_data['verified']
    

    
    # Prepare the Actor input for post data
    run_input = {
        "username": [username],
        "resultsLimit": post_limit,
        "scrapeComments": True,
        "commentsLimit": 10
    }
    
    print(f"Fetching post data for @{username}...")
    # Run the Actor and wait for it to finish
    run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)
    
    # Fetch results from the run's dataset
    dataset = client.dataset(run["defaultDatasetId"])
    items = list(dataset.iterate_items())
    
    if not items:
        return None
    
    # Extract engagement data
    likes = []
    comments = []
    shares = []
    saves = []
    for item in items:
        # Try different property names based on Apify's current data structure
        like_count = item.get('likesCount', 0)
        if like_count == 0:
            like_count = item.get('likes', 0)
        
        comment_count = item.get('commentsCount', 0)
        if comment_count == 0:
            comment_count = len(item.get('comments', []))
        
        # Estimate shares and saves
        share_count = item.get('sharesCount', int(like_count * random.uniform(0.05, 0.1)))
        save_count = item.get('savesCount', int(like_count * random.uniform(0.08, 0.15)))
        
        likes.append(like_count)
        comments.append(comment_count)
        shares.append(share_count)
        saves.append(save_count)
    
    # Calculate metrics
    avg_likes = statistics.mean(likes) if likes else 0
    avg_comments = statistics.mean(comments) if comments else 0
    avg_shares = statistics.mean(shares) if shares else 0
    avg_saves = statistics.mean(saves) if saves else 0

    total_engagement = sum(likes) + sum(comments) + sum(shares) + sum(saves)
    posts_analyzed = len(items)
    
    # Calculate engagement score using the formula: (total likes + total comments) / (followers × posts) × 100
    engagement_score = (total_engagement / (follower_count * posts_analyzed)) * 100 if follower_count and posts_analyzed else 0
    
    return {
        'username': username,
        'followers': follower_count,
        'following': following_count,
        'profile_url': profile_url,
        'biography': biography,
        'full_name': full_name,
        'verified': verified,
        'posts_analyzed': posts_analyzed,
        'avg_likes': avg_likes,
        'avg_comments': avg_comments,
        'avg_shares': avg_shares,
        'avg_saves': avg_saves,
        'engagement_score': engagement_score,
        'total_likes': sum(likes),
        'total_comments': sum(comments),
        'total_shares': sum(shares),
        'total_saves': sum(saves)
    }

def detect_fake_followers(followers_data):
    """Analyze followers to detect fake/bot accounts"""
    # Create a DataFrame for analysis
    df = pd.DataFrame(followers_data)
    
    # Add detection criteria
    df['follower_ratio'] = df['followsCount'] / df['followersCount'].apply(lambda x: max(x, 1))
    df['username_generic'] = df['username'].str.contains(r'user\d+') | df['username'].str.contains(r'[a-z]+\d{5,}')
    df['low_posts'] = df['postsCount'] < 5
    
    # Classify as bot based on multiple criteria
    df['is_bot_detected'] = (
        (df['follower_ratio'] > 10) |  # Following many, followed by few
        (df['username_generic'] & df['low_posts']) |  # Generic username and few posts
        (df['followsCount'] > 3000) |  # Following too many accounts
        (df['postsCount'] == 0)  # No posts at all
    )
    
    # Calculate fake follower percentage
    fake_percentage = df['is_bot_detected'].mean() * 100
    
    return {
        'followers_analyzed': len(df),
        'fake_followers_count': df['is_bot_detected'].sum(),
        'fake_followers_percentage': fake_percentage,
        'follower_data': df
    }

def create_network_graph(followers_data, username, output_dir="static/reports"):
    """Create and visualize the network graph of followers"""
    if not followers_data:
        print(f"No follower data available for @{username}. Skipping graph generation.")
        return None

    try:
        # Create a directed graph
        G = nx.DiGraph()
        G.add_node(username, type='main')  # Add main user node

        # Add followers as nodes and edges
        for follower in followers_data:
            follower_name = follower['username']
            is_bot = follower.get('is_bot_detected', follower.get('is_bot', False))
            G.add_node(follower_name, type='bot' if is_bot else 'real')
            G.add_edge(follower_name, username)  # Follower follows the main user

        # Set up the plot
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, k=0.3, iterations=50)

        # Define node colors based on type
        node_colors = []
        for node in G.nodes():
            if G.nodes[node].get('type') == 'main':
                node_colors.append('gold')  # Main user
            elif G.nodes[node].get('type') == 'bot':
                node_colors.append('red')  # Fake follower
            else:
                node_colors.append('lightblue')  # Real follower

        # Draw nodes and edges
        nx.draw(
            G,
            pos,
            with_labels=False,
            node_color=node_colors,
            node_size=[300 if n == username else 100 for n in G.nodes()],
            alpha=0.8,
            edge_color='gray',
            arrows=True,
            arrowsize=10
        )

        # Add labels only to the main user node
        labels = {username: username}
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')

        # Add a legend to explain the colors
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Main User', markersize=10, markerfacecolor='gold'),
            plt.Line2D([0], [0], marker='o', color='w', label='Fake Follower', markersize=10, markerfacecolor='red'),
            plt.Line2D([0], [0], marker='o', color='w', label='Real Follower', markersize=10, markerfacecolor='lightblue')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

        # Save the graph to a file
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/{username}_network_graph.png"
        
        plt.title(f"Follower Network for @{username}", fontsize=16)
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"Network graph saved at {output_file}")
        return output_file  # Return the file path
    except Exception as e:
        print(f"Failed to create network graph: {str(e)}")
        return None  # Return None in case of error


    

def analyze_instagram_influence(username, post_limit=10, follower_limit=100):
    print(f"Starting analysis for @{username} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Get profile data
    profile_data = get_profile_data(username)
    if not profile_data or not profile_data.get("followers"):
        print(f"Failed to retrieve profile data for @{username}.")
        return {"error": "Failed to retrieve profile data"}

    # Step 2: Fetch followers list
    followers_list = get_followers_list(username, follower_limit)
    if not followers_list:
        print(f"No followers retrieved for @{username}. Skipping network graph creation.")
    
    # Step 3: Generate network graph
    graph_path = create_network_graph(followers_list, username) if followers_list else None

    # Prepare results
    results = {
        "username": username,
        "followers": profile_data["followers"],
        "network_graph": graph_path,
    }

        # After detecting categories
    categories = detect_categories(profile_data)
    print(f"Detected categories: {categories}")

    # Add to results dictionary
    results["categories"] = categories

    # When calling save_analysis, explicitly pass the categories
    save_analysis(username, results, results.get('categories', []))

    return results




# new additional functions
def get_profile_data(username):
    """Get profile data including followers, following, profile URL and business address"""
    try:
        profile_input = {
            "usernames": [username],
            "resultsType": "details"
        }
        print(f"Fetching profile data for @{username}...")
        profile_run = client.actor("apify/instagram-profile-scraper").call(run_input=profile_input)
        profile_dataset = client.dataset(profile_run["defaultDatasetId"])
        profile_items = list(profile_dataset.iterate_items())
        

        #debug statement
        # print("apify response: ", profile_items)

        if profile_items and len(profile_items) > 0:
            # Extract business address if available
            business_address = {}
            if 'businessAddress' in profile_items[0]:
                address = profile_items[0]['businessAddress']
                business_address = {
                    'street': address.get('street_address', ''),
                    'city': address.get('city_name', ''),
                    'zip_code': address.get('zip_code', ''),
                    'latitude': address.get('latitude', 0),
                    'longitude': address.get('longitude', 0)
                }
            
            return {
                'followers': profile_items[0].get('followersCount', 0),
                'following': profile_items[0].get('followsCount', 0),
                'profile_url': profile_items[0].get('url', f"https://www.instagram.com/{username}/"),
                'biography': profile_items[0].get('biography', ''),
                'full_name': profile_items[0].get('fullName', ''),
                'verified': profile_items[0].get('verified', False),
                'posts_count': profile_items[0].get('postsCount', 0),
                'business_address': business_address,
                'latest_posts': profile_items[0].get('latestPosts', []),
                'profile_pic_url': profile_items[0].get('profilePicUrl', '')
            }
        else:
            return {'followers': 0, 'following': 0, 'profile_url': f"https://www.instagram.com/{username}/", 
                    'biography': '', 'full_name': '', 'verified': False, 'posts_count': 0, 
                    'profile_pic_url': '',
                    'business_address': {}, 'latest_posts': []}
    except Exception as e:
        print(f"Error fetching profile data: {str(e)}")
        return {'followers': 0, 'following': 0, 'profile_url': f"https://www.instagram.com/{username}/", 
                'biography': '', 'full_name': '', 'verified': False, 'posts_count': 0,
                'profile_pic_url': '', 
                'business_address': {}, 'latest_posts': []}


def calculate_engagement_from_posts(profile_data, post_limit=10):
    """Calculate engagement metrics using actual posts data from Instagram Profile Scraper"""
    followers = profile_data['followers']
    latest_posts = profile_data.get('latest_posts', [])[:post_limit]
    
    if not latest_posts:
        return None
    
    total_likes = 0
    total_comments = 0
    total_shares = 0
    total_saves = 0
    post_types = {}
    
    for post in latest_posts:
        likes = post.get('likesCount', 0)
        comments = post.get('commentsCount', 0)
        
        # Estimate shares and saves based on likes (since they're not directly available)
        shares = int(likes * random.uniform(0.05, 0.1))
        saves = int(likes * random.uniform(0.08, 0.15))
        
        # Track engagement by post type
        post_type = post.get('typeName', 'unknown')
        if post_type not in post_types:
            post_types[post_type] = {'count': 0, 'engagement': 0}
        
        post_types[post_type]['count'] += 1
        post_types[post_type]['engagement'] += likes + comments + shares + saves
        
        total_likes += likes
        total_comments += comments
        total_shares += shares
        total_saves += saves
    
    posts_analyzed = len(latest_posts)
    total_engagement = total_likes + total_comments + total_shares + total_saves
    
    # Calculate different engagement rate formulas
    
    # 1. Standard ER by followers (ER post)
    er_post = (total_engagement / (followers * posts_analyzed)) * 100 if followers and posts_analyzed else 0
    
    # 2. Adjusted formula for fair comparison across different account sizes
    er_adjusted = (total_engagement / (followers**0.85 * posts_analyzed)) * 100 if followers and posts_analyzed else 0
    
    # 3. Weighted engagement (formula from influence_calculator.py)
    weighted_engagement = (
        total_likes * 0.35 +
        total_comments * 0.25 +
        total_shares * 0.25 +
        total_saves * 0.15
    )
    er_weighted = (weighted_engagement / (followers * posts_analyzed)) * 100 if followers and posts_analyzed else 0
    
    # Calculate engagement by post type
    er_by_type = {}
    for post_type, data in post_types.items():
        if data['count'] > 0:
            er_by_type[post_type] = (data['engagement'] / (followers * data['count'])) * 100
    
    return {
        'posts_analyzed': posts_analyzed,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_shares': total_shares,
        'total_saves': total_saves,
        'avg_likes': total_likes / posts_analyzed if posts_analyzed else 0,
        'avg_comments': total_comments / posts_analyzed if posts_analyzed else 0,
        'avg_shares': total_shares / posts_analyzed if posts_analyzed else 0,
        'avg_saves': total_saves / posts_analyzed if posts_analyzed else 0,
        'engagement_score': er_post,
        'engagement_score_adjusted': er_adjusted,
        'engagement_score_weighted': er_weighted,
        'engagement_by_type': er_by_type
    }
