# db_helpers.py
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import json
from datetime import datetime
from aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, DYNAMODB_TABLE

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

table = dynamodb.Table(DYNAMODB_TABLE)

# 1 april ansh
def update_existing_data_with_categories():
    """Update existing data with categories based on usernames"""
    from data_extractor import detect_categories
    
    response = table.scan()
    items = response.get('Items', [])
    
    for item in items:
        username = item.get('username')
        if username and 'categories' not in item:
            # Create a mock profile with just the username to detect categories
            mock_profile = {'username': username}
            categories = detect_categories(mock_profile)
            
            # Update the item with categories
            table.update_item(
                Key={'username': username},
                UpdateExpression="SET categories = :c",
                ExpressionAttributeValues={':c': categories}
            )
            print(f"Updated {username} with categories: {categories}")
    
    print("Finished updating existing data with categories")



def save_analysis(username, analysis_data, categories=None):
    """Convert all float values to Decimal before saving to DynamoDB"""
    # Convert float values to Decimal using json serialization
    # json_str = json.dumps(analysis_data)
    # decimal_data = json.loads(json_str, parse_float=Decimal)
    
    item = {
        'username': username,  # Partition key
        'influenceScore': Decimal(str(analysis_data.get('influence_score', 0))),  # Sort key as Decimal
        'timestamp': datetime.now().isoformat(),
        'engagementRate': Decimal(str(analysis_data.get('engagement_rate', 0))),
        'followers': int(analysis_data.get('followers', 0)),
        'graphUrl': analysis_data.get('network_graph', ''),
        'categories': categories if isinstance(categories, list) else [str(categories)] if categories else []
    }

    # 1 april ansh
    # Add categories if provided
    print(f"Saving item to DynamoDB: {item}")
    
    try:
        response = table.put_item(Item=item)
        print(f"Successfully saved analysis for {username}")
        return response
    except Exception as e:
        print(f"Error saving to DynamoDB: {str(e)}")
        raise

def get_leaderboard(sort_by='influenceScore', category=None, limit=20):
    try:
        print(f"Getting leaderboard with category filter: {category}")
        # Use scan operation to get all items
        response = table.scan()
        items = response.get('Items', [])
        print(f"Retrieved {len(items)} items from DynamoDB")
        for item in items:
            print(f"Raw item from DynamoDB: {item}")
        
        # Create a dictionary to store the latest entry for each username
        latest_entries = {}
        
        for item in items:
            username = item.get('username', '')
            timestamp = item.get('timestamp', '')
            
            # If this username isn't in our dictionary yet, or this entry is newer
            if username not in latest_entries or timestamp > latest_entries[username].get('timestamp', ''):
                latest_entries[username] = item
        
        # Convert dictionary values to list
        unique_items = list(latest_entries.values())

         # Debug: Print items before filtering
        print(f"Items before filtering: {len(unique_items)}")

        # Filter by category if specified
        if category:
            filtered_items = [item for item in unique_items if category in item.get('categories', [])]
            print(f"Items matching category '{category}': {len(filtered_items)}")
            for item in filtered_items:
                print(f"Matched item: {item}")
            unique_items = filtered_items
        
        # Map DynamoDB attribute names to frontend expected names
        mapped_items = []
        for item in unique_items:
            mapped_item = {
                'username': item.get('username', ''),
                'influence_score': float(item.get('influenceScore', 0)),
                'engagement_rate': float(item.get('engagementRate', 0)),
                'followers': int(item.get('followers', 0)),
                'timestamp': item.get('timestamp', ''),
                'categories': item.get('categories', ['GENERAL'])
            }
            mapped_items.append(mapped_item)
        
        # Sort based on the requested field
        sort_field_map = {
            'influence_score': 'influence_score',
            'engagement_rate': 'engagement_rate',
            'followers': 'followers',
            'influenceScore': 'influence_score'
        }
        sort_field = sort_field_map.get(sort_by, 'influence_score')
        
        # Sort in Python
        mapped_items.sort(key=lambda x: x.get(sort_field, 0), reverse=True)
        
        return mapped_items[:limit]
    except Exception as e:
        print(f"Error getting leaderboard: {str(e)}")
        return []


def add_precomputed_influencers():
    """Add precomputed top influencers to DynamoDB."""
    precomputed_influencers = [
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

    for influencer in precomputed_influencers:
        save_analysis(
            username=influencer['username'],
            analysis_data={
                'influence_score': influencer['influence_score'],
                'engagement_rate': influencer['engagement_rate'],
                'followers': influencer['followers'],
                'network_graph': None,  # No graph for precomputed influencers
            },
            categories=influencer['categories']
        )
    print("Precomputed influencers added successfully.")


def get_precomputed_influencers(limit=10):
    """Fetch precomputed top influencers from DynamoDB."""
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        # Sort by influence score and limit the results
        sorted_items = sorted(items, key=lambda x: float(x['influenceScore']), reverse=True)
        return sorted_items[:limit]
    except Exception as e:
        print(f"Error fetching precomputed influencers: {str(e)}")
        return []

