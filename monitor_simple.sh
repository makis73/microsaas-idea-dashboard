#!/bin/bash

# Simple Micro SaaS Idea Monitor
# Checks basic sources and creates report

set -e

echo "🔍 Micro SaaS Idea Monitor - $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Create reports directory
REPORTS_DIR="monitor_reports"
mkdir -p "$REPORTS_DIR"

# Create report file
REPORT_FILE="$REPORTS_DIR/report_$(date '+%Y%m%d_%H%M').txt"

{
    echo "=== Micro SaaS Idea Monitor Report ==="
    echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Check Reddit r/SaaS (simplified)
    echo "=== Reddit r/SaaS ==="
    echo "Checking top posts..."
    
    # Try to get Reddit data
    REDDIT_URL="https://www.reddit.com/r/SaaS/top/.json?limit=5"
    if curl -s -H "User-Agent: MicroSaaS-Monitor" "$REDDIT_URL" 2>/dev/null | python3 -c "
import sys,json
try:
    data=json.load(sys.stdin)
    for post in data['data']['children'][:3]:
        title=post['data']['title'][:100]
        score=post['data']['score']
        comments=post['data']['num_comments']
        print(f'• {title}')
        print(f'  ⬆️ {score} points | 💬 {comments} comments')
        print()
except:
    print('Could not fetch Reddit data')
    print('Tip: Install python3 and requests module')
" 2>/dev/null; then
        echo "✅ Reddit check completed"
    else
        echo "❌ Could not fetch Reddit data"
        echo "   Install: pip3 install requests"
    fi
    
    echo ""
    echo "=== Hacker News ==="
    echo "Checking top stories..."
    
    # Check Hacker News
    if command -v python3 &>/dev/null; then
        python3 -c "
import sys,json,urllib.request,time
try:
    # Get top stories
    with urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json') as f:
        ids=json.load(f)[:5]
    
    print('Top 5 HN Stories:')
    for i,id in enumerate(ids, 1):
        with urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json') as f:
            story=json.load(f)
        title=story.get('title', 'No title')[:80]
        score=story.get('score', 0)
        print(f'{i}. {title}')
        print(f'   ⬆️ {score} points | https://news.ycombinator.com/item?id={id}')
        print()
except Exception as e:
    print(f'Error: {e}')
" 2>/dev/null || echo "❌ Could not fetch HN data"
    else
        echo "❌ Python3 not installed"
    fi
    
    echo ""
    echo "=== Monitoring Tips ==="
    echo "1. Product Hunt: Visit https://www.producthunt.com"
    echo "2. Indie Hackers: Visit https://www.indiehackers.com"
    echo "3. Twitter: Search #buildinpublic #microsaas"
    echo "4. Google Trends: https://trends.google.com"
    echo ""
    echo "=== Next Steps ==="
    echo "• Run this script twice daily (9 AM & 5 PM)"
    echo "• Review reports in: $REPORTS_DIR/"
    echo "• Look for patterns: 'pain', 'wish', 'alternative', 'tedious'"
    
} > "$REPORT_FILE"

echo ""
echo "✅ Report saved to: $REPORT_FILE"
echo ""
echo "📊 Report Preview:"
echo "------------------"
head -30 "$REPORT_FILE"