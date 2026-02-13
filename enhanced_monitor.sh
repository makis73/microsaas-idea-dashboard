#!/bin/bash

# Enhanced Micro SaaS Monitor with AI Analysis
# Runs analysis and updates JSON for interactive dashboard

set -e

echo "🚀 Starting Enhanced Micro SaaS Analyzer..."
echo ""

# Create directories
mkdir -p enhanced_reports
mkdir -p monitor_reports

# Check Python requirements
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is required but not installed"
    echo "   Install with: brew install python"
    exit 1
fi

echo "📦 Checking Python dependencies..."
if ! python3 -c "import requests" 2>/dev/null; then
    echo "   Installing requests module..."
    pip3 install requests
fi

echo "🔍 Running enhanced analyzer..."
python3 analyze_ideas.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Enhanced analysis complete!"
    
    # Find the latest JSON report
    latest_json=$(ls -t enhanced_reports/analysis_*.json 2>/dev/null | head -1)
    
    if [ -n "$latest_json" ]; then
        # Create a symlink for latest.json
        ln -sf "$(basename "$latest_json")" enhanced_reports/latest.json
        
        # Find the latest markdown report
        latest_md=$(ls -t enhanced_reports/analysis_*.md 2>/dev/null | head -1)
        
        echo ""
        echo "📊 Reports generated:"
        echo "   JSON (for dashboard): enhanced_reports/$(basename "$latest_json")"
        echo "   Markdown: enhanced_reports/$(basename "$latest_md")"
        echo "   Latest link: enhanced_reports/latest.json"
        
        # Extract summary from JSON
        total=$(python3 -c "
import json
import sys
try:
    with open('$latest_json', 'r') as f:
        data = json.load(f)
    print(f\"Total opportunities: {data['summary']['total_opportunities']}\")
    print(f\"Average feasibility: {data['summary']['avg_feasibility']:.1f}/10\")
    print(f\"Average audience potential: {data['summary']['avg_audience_potential']:.1f}/10\")
    
    # Find top idea
    all_ideas = data['reddit_posts'] + data['hn_stories']
    if all_ideas:
        top_idea = max(all_ideas, key=lambda x: x['feasibility'] * x['audience_potential'])
        total_score = top_idea['feasibility'] * top_idea['audience_potential']
        print(f\"Top opportunity score: {total_score}/100\")
        print(f\"Top idea: {top_idea['title'][:60]}...\")
except Exception as e:
    print(f\"Error: {e}\")
" 2>/dev/null)
        
        echo ""
        echo "📈 Summary:"
        echo "$total"
        
    else
        echo "⚠️  No JSON report generated"
    fi
    
    echo ""
    echo "🌐 To view enhanced dashboard:"
    echo "   open enhanced_dashboard.html"
    echo "   or visit: file://$(pwd)/enhanced_dashboard.html"
    
else
    echo "❌ Enhanced analysis failed"
    exit 1
fi

echo ""
echo "🔄 Also running simple monitor for comparison..."
./monitor_simple.sh

echo ""
echo "🎉 All done! Enhanced dashboard is ready."
echo "   Next run: $(date -v+6H '+%H:%M') (every 6 hours recommended)"