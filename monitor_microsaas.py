#!/usr/bin/env python3
"""
Micro SaaS Idea Monitor
Checks Product Hunt, Reddit, Twitter for trending micro SaaS ideas
"""

import json
import os
import sys
from datetime import datetime
import requests

def check_producthunt():
    """Check Product Hunt trending products"""
    print("📊 Checking Product Hunt...")
    try:
        # This is a simplified check - in production you'd use Product Hunt API
        # or scrape the site properly
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "source": "Product Hunt",
            "date": today,
            "status": "API key needed for proper monitoring",
            "note": "Get Product Hunt API key or use RSS: https://www.producthunt.com/feed"
        }
    except Exception as e:
        return {"source": "Product Hunt", "error": str(e)}

def check_reddit_saas():
    """Check r/SaaS top posts"""
    print("📊 Checking Reddit r/SaaS...")
    try:
        url = "https://www.reddit.com/r/SaaS/top/.json?limit=10"
        headers = {"User-Agent": "MicroSaaS-Monitor/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            for post in data['data']['children'][:5]:
                post_data = post['data']
                posts.append({
                    "title": post_data['title'],
                    "score": post_data['score'],
                    "comments": post_data['num_comments'],
                    "url": f"https://reddit.com{post_data['permalink']}"
                })
            return {
                "source": "Reddit r/SaaS",
                "posts": posts,
                "checked_at": datetime.now().isoformat()
            }
        else:
            return {"source": "Reddit r/SaaS", "error": f"Status: {response.status_code}"}
    except Exception as e:
        return {"source": "Reddit r/SaaS", "error": str(e)}

def check_hackernews_ask():
    """Check Hacker News Ask HN posts"""
    print("📊 Checking Hacker News Ask HN...")
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            story_ids = response.json()[:10]
            ask_posts = []
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_resp = requests.get(story_url, timeout=10)
                
                if story_resp.status_code == 200:
                    story = story_resp.json()
                    # Look for Ask HN posts
                    if story.get('type') == 'story' and 'Ask HN:' in story.get('title', ''):
                        ask_posts.append({
                            "title": story['title'],
                            "score": story.get('score', 0),
                            "url": f"https://news.ycombinator.com/item?id={story_id}",
                            "time": datetime.fromtimestamp(story.get('time', 0)).isoformat()
                        })
                        if len(ask_posts) >= 3:
                            break
            
            return {
                "source": "Hacker News Ask HN",
                "posts": ask_posts,
                "checked_at": datetime.now().isoformat()
            }
        else:
            return {"source": "Hacker News", "error": f"Status: {response.status_code}"}
    except Exception as e:
        return {"source": "Hacker News", "error": str(e)}

def generate_report(results):
    """Generate a readable report"""
    report_lines = []
    report_lines.append(f"# Micro SaaS Idea Monitor Report")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    for result in results:
        report_lines.append(f"## {result['source']}")
        
        if 'error' in result:
            report_lines.append(f"❌ Error: {result['error']}")
        elif 'posts' in result:
            for i, post in enumerate(result['posts'], 1):
                report_lines.append(f"{i}. **{post['title']}**")
                if 'score' in post:
                    report_lines.append(f"   ⬆️ {post.get('score', 0)} points | 💬 {post.get('comments', 0)} comments")
                if 'url' in post:
                    report_lines.append(f"   🔗 {post['url']}")
                report_lines.append("")
        elif 'note' in result:
            report_lines.append(f"ℹ️ {result['note']}")
        
        report_lines.append("")
    
    return "\n".join(report_lines)

def save_report(report_text):
    """Save report to file"""
    reports_dir = "monitor_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"{reports_dir}/report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(filename, 'w') as f:
        f.write(report_text)
    
    return filename

def main():
    print("🚀 Starting Micro SaaS Idea Monitor...")
    
    # Run all checks
    results = [
        check_producthunt(),
        check_reddit_saas(),
        check_hackernews_ask()
    ]
    
    # Generate report
    report = generate_report(results)
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save report
    saved_file = save_report(report)
    print(f"\n✅ Report saved to: {saved_file}")
    
    # Check if there are interesting posts
    interesting_count = 0
    for result in results:
        if 'posts' in result and len(result['posts']) > 0:
            interesting_count += len(result['posts'])
    
    if interesting_count > 0:
        print(f"🎯 Found {interesting_count} potentially interesting posts")
        return {"interesting_posts": interesting_count, "report_file": saved_file}
    else:
        print("ℹ️ No interesting posts found this time")
        return {"interesting_posts": 0, "report_file": saved_file}

if __name__ == "__main__":
    result = main()
    # Exit with code based on findings (0 = nothing interesting, 1 = found posts)
    sys.exit(0 if result['interesting_posts'] == 0 else 1)