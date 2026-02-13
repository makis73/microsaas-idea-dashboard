#!/usr/bin/env python3
"""
Enhanced Micro SaaS Idea Analyzer
Provides detailed analysis, links, and feasibility assessment for each post
"""

import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Any

def analyze_reddit_post(post_data: Dict) -> Dict:
    """Analyze a Reddit post for micro SaaS potential"""
    title = post_data.get('title', '')
    score = post_data.get('score', 0)
    comments = post_data.get('num_comments', 0)
    url = post_data.get('url', '')
    reddit_url = f"https://reddit.com{post_data.get('permalink', '')}"
    
    analysis = {
        "title": title,
        "reddit_url": reddit_url,
        "score": score,
        "comments": comments,
        "analysis": "",
        "feasibility": 0,
        "audience_potential": 0,
        "business_model_suggestions": []
    }
    
    # AI Content Optimization posts
    if "chatgpt" in title.lower() or "ranking" in title.lower() or "ai" in title.lower():
        analysis["analysis"] = "High interest in AI content optimization. Many creators struggle with ranking in AI search results."
        analysis["feasibility"] = 8  # 1-10 scale
        analysis["audience_potential"] = 9
        analysis["business_model_suggestions"] = [
            "Freemium SaaS ($19-49/month)",
            "API access for agencies",
            "One-time audit tool"
        ]
        analysis["micro_saas_ideas"] = [
            "AI Content Score Analyzer",
            "ChatGPT Optimization Dashboard",
            "AI SEO Keyword Research Tool"
        ]
    
    # Launch/Indie Hacker posts
    elif "launch" in title.lower() or "shaking" in title.lower():
        analysis["analysis"] = "Strong emotional response to launching. Indie hacker community is highly engaged."
        analysis["feasibility"] = 7
        analysis["audience_potential"] = 8
        analysis["business_model_suggestions"] = [
            "Freemium launch tracker",
            "Community features ($9/month)",
            "Analytics add-ons"
        ]
        analysis["micro_saas_ideas"] = [
            "Launch Day Dashboard",
            "Indie Hacker Analytics",
            "Community Engagement Tracker"
        ]
    
    # Business/Co-founder issues
    elif "co-founders" in title.lower() or "pay cut" in title.lower():
        analysis["analysis"] = "Common pain point in startup dynamics. Legal/business agreements are often overlooked."
        analysis["feasibility"] = 6
        analysis["audience_potential"] = 7
        analysis["business_model_suggestions"] = [
            "Template marketplace",
            "Document generator SaaS",
            "Consultation add-ons"
        ]
        analysis["micro_saas_ideas"] = [
            "Co-founder Agreement Builder",
            "Startup Legal Doc Generator",
            "Equity Calculator Tool"
        ]
    
    # Default analysis for other posts
    else:
        analysis["analysis"] = "General SaaS discussion. Look for recurring pain points or specific tool requests."
        analysis["feasibility"] = 5
        analysis["audience_potential"] = 6
        analysis["business_model_suggestions"] = ["Freemium model", "Pay-per-use"]
        analysis["micro_saas_ideas"] = ["Problem-specific utility tool"]
    
    return analysis

def analyze_hn_story(story_data: Dict) -> Dict:
    """Analyze a Hacker News story for micro SaaS potential"""
    title = story_data.get('title', 'No title')
    score = story_data.get('score', 0)
    hn_url = f"https://news.ycombinator.com/item?id={story_data.get('id', '')}"
    
    analysis = {
        "title": title,
        "hn_url": hn_url,
        "score": score,
        "analysis": "",
        "feasibility": 0,
        "audience_potential": 0,
        "business_model_suggestions": []
    }
    
    # AI/ML topics
    if "gpt" in title.lower() or "gemini" in title.lower() or "ai" in title.lower():
        analysis["analysis"] = "AI tools and models are highly trending. Opportunities in tooling around AI APIs."
        analysis["feasibility"] = 8
        analysis["audience_potential"] = 9
        analysis["business_model_suggestions"] = [
            "API wrapper SaaS",
            "AI workflow automation",
            "Model comparison tools"
        ]
        analysis["micro_saas_ideas"] = [
            "AI API Cost Optimizer",
            "Multiple AI Provider Dashboard",
            "AI Response Quality Analyzer"
        ]
    
    # UI/UX/Dark patterns
    elif "tip" in title.lower() or "dark pattern" in title.lower() or "ui" in title.lower():
        analysis["analysis"] = "Growing concern about ethical design. Tools for detecting/avoiding dark patterns."
        analysis["feasibility"] = 7
        analysis["audience_potential"] = 8
        analysis["business_model_suggestions"] = [
            "Browser extension freemium",
            "Agency/enterprise plans",
            "Consulting services"
        ]
        analysis["micro_saas_ideas"] = [
            "Dark Pattern Scanner",
            "Ethical Design Checklist Tool",
            "UI Accessibility Checker"
        ]
    
    # Developer tools
    elif "macos" in title.lower() or "window" in title.lower() or "developer" in title.lower():
        analysis["analysis"] = "Developer pain points around tools and workflows. Niche but loyal audience."
        analysis["feasibility"] = 6
        analysis["audience_potential"] = 7
        analysis["business_model_suggestions"] = [
            "One-time purchase",
            "Subscription for teams",
            "Open source + paid features"
        ]
        analysis["micro_saas_ideas"] = [
            "Developer Workflow Optimizer",
            "Tool Configuration Manager",
            "Cross-platform Utility"
        ]
    
    # Default analysis
    else:
        analysis["analysis"] = "General tech discussion. Evaluate based on engagement score and comments."
        analysis["feasibility"] = 5
        analysis["audience_potential"] = 6
        analysis["business_model_suggestions"] = ["Need more specific pain point"]
        analysis["micro_saas_ideas"] = ["Problem-specific solution"]
    
    return analysis

def fetch_reddit_posts():
    """Fetch and analyze Reddit r/SaaS posts"""
    print("🔍 Analyzing Reddit r/SaaS posts...")
    try:
        url = "https://www.reddit.com/r/SaaS/top/.json?limit=5"
        headers = {"User-Agent": "MicroSaaS-Analyzer/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            analyzed_posts = []
            
            for post in data['data']['children'][:3]:  # Top 3
                post_data = post['data']
                analysis = analyze_reddit_post(post_data)
                analyzed_posts.append(analysis)
            
            return analyzed_posts
        else:
            print(f"❌ Reddit API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching Reddit: {e}")
        return []

def fetch_hn_stories():
    """Fetch and analyze Hacker News top stories"""
    print("🔍 Analyzing Hacker News stories...")
    try:
        # Get top story IDs
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_url, timeout=10)
        
        if response.status_code == 200:
            story_ids = response.json()[:5]
            analyzed_stories = []
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_resp = requests.get(story_url, timeout=10)
                
                if story_resp.status_code == 200:
                    story_data = story_resp.json()
                    if story_data.get('type') == 'story' and story_data.get('title'):
                        analysis = analyze_hn_story(story_data)
                        analyzed_stories.append(analysis)
                
                if len(analyzed_stories) >= 3:
                    break
            
            return analyzed_stories
        else:
            print(f"❌ HN API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching HN: {e}")
        return []

def generate_enhanced_report(reddit_posts, hn_stories):
    """Generate enhanced report with analysis"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Enhanced Micro SaaS Idea Analysis
Generated: {timestamp}

## Summary
Found {len(reddit_posts)} Reddit posts and {len(hn_stories)} HN stories with micro SaaS potential.

## 🔥 Top Micro SaaS Opportunities

"""
    
    # Reddit section
    if reddit_posts:
        report += "### Reddit r/SaaS Analysis\n\n"
        for i, post in enumerate(reddit_posts, 1):
            report += f"""#### {i}. {post['title'][:80]}...
**Link:** [{post['reddit_url']}]({post['reddit_url']})
**Engagement:** ⬆️ {post['score']} points | 💬 {post['comments']} comments
**My Analysis:** {post['analysis']}
**Feasibility Score:** {post['feasibility']}/10
**Audience Potential:** {post['audience_potential']}/10
**Suggested Business Models:** {', '.join(post['business_model_suggestions'])}
**Micro SaaS Ideas:** {', '.join(post['micro_saas_ideas'])}
---
"""
    
    # HN section
    if hn_stories:
        report += "\n### Hacker News Analysis\n\n"
        for i, story in enumerate(hn_stories, 1):
            report += f"""#### {i}. {story['title'][:80]}...
**Link:** [{story['hn_url']}]({story['hn_url']})
**Engagement:** ⬆️ {story['score']} points
**My Analysis:** {story['analysis']}
**Feasibility Score:** {story['feasibility']}/10
**Audience Potential:** {story['audience_potential']}/10
**Suggested Business Models:** {', '.join(story['business_model_suggestions'])}
**Micro SaaS Ideas:** {', '.join(story['micro_saas_ideas'])}
---
"""
    
    # Recommendations
    report += "\n## 🎯 Recommended Focus Areas\n\n"
    
    all_items = reddit_posts + hn_stories
    if all_items:
        # Sort by feasibility * audience_potential
        sorted_items = sorted(all_items, key=lambda x: x['feasibility'] * x['audience_potential'], reverse=True)
        
        report += "### Top 3 Opportunities (Feasibility × Audience)\n\n"
        for i, item in enumerate(sorted_items[:3], 1):
            total_score = item['feasibility'] * item['audience_potential']
            report += f"{i}. **{item['title'][:50]}...** (Score: {total_score}/100)\n"
            report += f"   Ideas: {', '.join(item['micro_saas_ideas'][:2])}\n\n"
    
    report += "\n## 📈 Scoring Guide\n"
    report += "- **Feasibility (1-10):** How easy to build & maintain\n"
    report += "- **Audience Potential (1-10):** Market size & interest\n"
    report += "- **Total Score:** Feasibility × Audience Potential (max 100)\n"
    
    report += "\n---\n*Analysis generated by Micro SaaS Idea Analyzer*"
    
    return report

def save_json_report(reddit_posts, hn_stories):
    """Save analysis as JSON for dashboard"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "reddit_posts": reddit_posts,
        "hn_stories": hn_stories,
        "summary": {
            "total_opportunities": len(reddit_posts) + len(hn_stories),
            "avg_feasibility": 0,
            "avg_audience_potential": 0
        }
    }
    
    # Calculate averages
    all_items = reddit_posts + hn_stories
    if all_items:
        report["summary"]["avg_feasibility"] = sum(item['feasibility'] for item in all_items) / len(all_items)
        report["summary"]["avg_audience_potential"] = sum(item['audience_potential'] for item in all_items) / len(all_items)
    
    # Save JSON
    reports_dir = "enhanced_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"{reports_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    return filename

def main():
    print("🚀 Starting Enhanced Micro SaaS Idea Analyzer...")
    print("="*50)
    
    # Fetch and analyze data
    reddit_posts = fetch_reddit_posts()
    hn_stories = fetch_hn_stories()
    
    if not reddit_posts and not hn_stories:
        print("❌ No data fetched. Check internet connection.")
        return
    
    # Generate enhanced report
    report = generate_enhanced_report(reddit_posts, hn_stories)
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save reports
    txt_filename = f"enhanced_reports/analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    json_filename = save_json_report(reddit_posts, hn_stories)
    
    os.makedirs("enhanced_reports", exist_ok=True)
    with open(txt_filename, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Enhanced report saved to: {txt_filename}")
    print(f"✅ JSON data saved to: {json_filename}")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Reddit posts analyzed: {len(reddit_posts)}")
    print(f"   HN stories analyzed: {len(hn_stories)}")
    
    if reddit_posts or hn_stories:
        all_items = reddit_posts + hn_stories
        avg_feasibility = sum(item['feasibility'] for item in all_items) / len(all_items)
        avg_audience = sum(item['audience_potential'] for item in all_items) / len(all_items)
        
        print(f"   Avg feasibility score: {avg_feasibility:.1f}/10")
        print(f"   Avg audience potential: {avg_audience:.1f}/10")
        print(f"   Best opportunity score: {max(item['feasibility'] * item['audience_potential'] for item in all_items)}/100")
    
    return {
        "success": True,
        "reddit_count": len(reddit_posts),
        "hn_count": len(hn_stories),
        "report_file": txt_filename,
        "json_file": json_filename
    }

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result.get('success') else 1)