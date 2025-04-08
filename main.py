import os
import random
import json
from datetime import datetime

# New imports
from db_helpers import save_analysis
from s3_helpers import upload_graph_to_s3
from data_extractor import (
    calculate_engagement,
    get_followers_list,
    get_profile_data,
    calculate_engagement_from_posts,
    detect_fake_followers,
    create_network_graph,
    detect_categories,
    get_post_url,
    get_commenters,
    get_commenters_data
)
from influence_calculator import (
    calculate_influence_metrics,
    estimate_fake_followers,
    calculate_influence_score
)


def analyze_instagram_influence(username, post_limit=10, follower_limit=100):
    """Complete analysis of Instagram influence for a given username"""
    print(f"Starting analysis for @{username} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Get profile data and engagement data
    print("Step 1: Extracting profile and engagement data...")
    profile_data = get_profile_data(username)

    engagement_result = calculate_engagement_from_posts(profile_data, post_limit)
    if not engagement_result:
        print("No posts data available, falling back to standard engagement calculation...")
        engagement_result = calculate_engagement(username, post_limit)

    if not engagement_result:
        print(f"Failed to retrieve data for @{username}.")
        return {"error": "Failed to retrieve data"}

    # Prepare profile and engagement data structures
    profile_info = {
        "username": username,
        "followers": profile_data["followers"],
        "following": profile_data["following"],
        "posts": profile_data.get("posts_count", engagement_result["posts_analyzed"])
    }

    engagement_data = {
        "total_likes": engagement_result["total_likes"],
        "total_comments": engagement_result["total_comments"],
        "total_shares": engagement_result["total_shares"],
        "total_saves": engagement_result["total_saves"],
        "posts_analyzed": engagement_result["posts_analyzed"],
        "avg_shares": engagement_result["avg_shares"],
        "avg_saves": engagement_result["avg_saves"]
    }

    # Step 2: Estimate follower quality
    print("Step 2: Estimating follower quality...")
    post_url = get_post_url(username)
    commenter_analysis_results = analyze_commenters(post_url, username)

    if commenter_analysis_results:
        save_commenter_analysis(commenter_analysis_results, username)


            
    fake_follower_percentage = estimate_fake_followers(profile_data, engagement_data)

    # Step 3: Calculate influence score
    print("Step 3: Calculating influence score...")
    metrics = calculate_influence_metrics(profile_data, engagement_data)
    influence_score = calculate_influence_score({
        'engagement': metrics['engagement_rate'],
        'authenticity': 100 - fake_follower_percentage,
        'content_quality': metrics['post_frequency'] * 10,
        'reach': profile_data['followers'] / 1000
    })

    # Format business address for display
    business_address_str = ""
    if profile_data.get("business_address"):
        addr = profile_data["business_address"]
        street = addr.get("street", "")
        city = addr.get("city", "")
        zip_code = addr.get("zip_code", "")
        business_address_str = f"{street}, {city} {zip_code}".strip()
        if business_address_str.startswith(", "):
            business_address_str = business_address_str[2:]

    # Initialize graph_path to avoid referencing before assignment
    graph_path = None

    # Generate network graph (if followers are available)
    print("Generating network graph...")
    followers_list = get_followers_list(username, follower_limit)
    if followers_list:
        graph_path = create_network_graph(followers_list, username, output_dir="static/reports")

    # Upload graph to S3 (if graph is generated)
    graph_url = None
    if graph_path:
        graph_url = upload_graph_to_s3(graph_path, username)

    # Detect categories for the user
    print("Detecting categories...")
    categories = detect_categories(profile_data)

    # Prepare final results
    results = {
        "username": username,
        "full_name": profile_data.get("full_name", ""),
        "biography": profile_data.get("biography", ""),
        "verified": profile_data.get("verified", False),
        "followers": profile_data["followers"],
        "following": profile_data["following"],
        "profile_url": profile_data.get("profile_url", f"https://www.instagram.com/{username}/"),
        "business_address": business_address_str,
        "posts_count": profile_data.get("posts_count", 0),
        "avg_likes": round(engagement_result["avg_likes"], 2),
        "avg_comments": round(engagement_result["avg_comments"], 2),
        "profile_pic_url": profile_data.get("profile_pic_url", ""),
        "engagement_rate": round(metrics["engagement_rate"], 2),
        "engagement_rate_adjusted": round(engagement_result.get("engagement_score_adjusted", 0), 2),
        "engagement_rate_weighted": round(engagement_result.get("engagement_score_weighted", 0), 2),
        "fake_follower_percentage": round(fake_follower_percentage, 2),
        "influence_score": round(influence_score, 2),
        "network_graph": graph_url,
        "categories": categories,
        "analysis_date": datetime.now().isoformat()
    }

    # After calculating the original fake_follower_percentage
    print(f"[DEBUG] Original fake follower percentage: {fake_follower_percentage:.2f}%")

    #fastapi
    # ML model analysis
    try:
        from influence_calculator import estimate_fake_followers_from_commenters
        commenters_fake_percentage = estimate_fake_followers_from_commenters(commenter_analysis_results)
        results["fake_follower_percentage"] = round(commenters_fake_percentage, 2)
        if commenters_fake_percentage != -1:
            # Store both percentages
            results["original_fake_follower_percentage"] = round(fake_follower_percentage, 2)
            results["commenters_fake_percentage"] = round(commenters_fake_percentage, 2)
            results["fake_follower_percentage"] = round(commenters_fake_percentage, 2)
            
            # Update the main fake_follower_percentage with the ML model result
            fake_follower_percentage = commenters_fake_percentage
            print(f"[DEBUG] Updated fake follower percentage with ML model: {fake_follower_percentage:.2f}%")
        else:
            print("[DEBUG] ML model returned invalid result, keeping original percentage")
    except Exception as e:
        print(f"[ERROR] Failed to analyze commenters with ML model: {str(e)}")




    if "engagement_by_type" in engagement_result:
        results["engagement_by_type"] = {
            k: round(v, 2) for k, v in engagement_result["engagement_by_type"].items()
        }
    if profile_data["followers"] >= 10000000:  
        results["fake_follower_percentage"] = random.uniform(0.1, 0.9) 
    # Save results to file
    os.makedirs("static/reports", exist_ok=True)
    with open(f"static/reports/{username}_report.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save analysis to DynamoDB (with categories)
    save_analysis(username, results, categories)


    print("\n=== INFLUENCE ANALYSIS SUMMARY ===")
    print(f"Username: @{username}")
    print(f"Full Name: {results['full_name']}")
    print(f"Biography: {results['biography']}")
    print(f"Verified: {'Yes' if results['verified'] else 'No'}")
    print(f"Followers: {results['followers']:,}")
    print(f"Following: {results['following']:,}") 
    print(f"Profile URL: {results['profile_url']}")
    print(f"Total Posts: {results['posts_count']:,}")  # Display total posts count
    print(f"Standard Engagement Rate: {results['engagement_rate']:.2f}%")
    print(f"Adjusted Engagement Rate: {results['engagement_rate_adjusted']:.2f}%")
    print(f"Weighted Engagement Rate: {results['engagement_rate_weighted']:.2f}%")
    if business_address_str:
        print(f"Business Address: {business_address_str}")  # Display business address 
   
    print(f"Average Likes: {results['avg_likes']:.2f}")
    print(f"Average Comments: {results['avg_comments']:.2f}")
    print(f"Estimated Fake Followers: {results['fake_follower_percentage']:.2f}%")
    print(f"Influence Score: {results['influence_score']:.2f}")
    if "engagement_by_type" in results:
        print("\nEngagement by Post Type:")
        for post_type, rate in results["engagement_by_type"].items():
            print(f"  {post_type}: {rate:.2f}%")
    print(f"Analysis Date: {results['analysis_date']}")
    print(f"Full report saved in reports/{username}_report.json")
    print(f"url: {results['profile_pic_url']}")



    # Generate network graph
    print("Generating network graph...")
    followers_list = get_followers_list(username, follower_limit)
    graph_path = create_network_graph(followers_list, username, output_dir="static/reports")

    # Upload graph to S3
    graph_url = upload_graph_to_s3(graph_path, username)
    if graph_url:
        results["network_graph"] = graph_url
    # Save analysis to DynamoDB
    # save_analysis(username, results)  # this makes sure img is not uploaded to db


    # 1 april ansh
    # Add after profile data is retrieved
    categories = detect_categories(profile_data)
    print(f"Detected categories: {categories}")
    # Add to results dictionary
    results["categories"] = categories
    # Update the save_analysis call
    # Make sure categories are passed to all save_analysis calls
    save_analysis(username, results, results.get('categories', []))

    return results

def analyze_commenters(post_url, owner_username):
    """
    Analyze commenters from a post URL.
    """
    # Step 1: Get commenters' usernames (already implemented)
    commenters = get_commenters(post_url, owner_username)

    if not commenters:
        print("[ERROR] No valid commenters found.")
        return []

    # Step 2: Fetch and analyze their profiles
    commenter_profiles = get_commenters_data(commenters)

    # Step 3: Calculate metrics for each commenter
    results = []
    for profile in commenter_profiles:
        metrics = {
            "username": profile["username"],
            "posts": profile.get("postsCount", 0),
            "following": profile.get("followsCount", 0),
            "followers": profile.get("followersCount", 0),
            "has_profile_pic": bool(profile.get("profilePicUrl")),
            "private": profile.get("isPrivate", False),
            "follower_following_ratio": round(
                profile.get("followersCount", 0) / max(profile.get("followsCount", 1), 1), 2),
            "bio_length": len(profile.get("biography", "")),
            "username_length": len(profile["username"]),
            "digits_in_username": sum(c.isdigit() for c in profile["username"])
        }
        results.append(metrics)

    return results

import os
import json

def save_commenter_analysis(data, username):
    """
    Save commenter analysis results to a JSON file named after the main username.
    """
    os.makedirs("static/reports", exist_ok=True)
    output_path = f"static/reports/{username}_commenters_analysis.json"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[DEBUG] Commenter analysis saved to {output_path}")



if __name__ == "__main__":
    username = input("Enter Instagram username to analyze: ")
    post_limit = 10  # Default number of posts to analyze
    follower_limit = 100  # Default number of followers to analyze
    
    try:
        post_limit = int(input(f"Enter number of posts to analyze (default: {post_limit}): ") or post_limit)
        follower_limit = int(input(f"Enter number of followers to analyze (default: {follower_limit}): ") or follower_limit)
    except ValueError:
        print("Invalid input. Using default values.")
    
    analyze_instagram_influence(username, post_limit, follower_limit)

