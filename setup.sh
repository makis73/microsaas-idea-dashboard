#!/bin/bash

# Micro SaaS Idea Dashboard - Setup Script

set -e

echo "🚀 Setting up Micro SaaS Idea Dashboard..."
echo ""

# Check requirements
echo "📋 Checking requirements..."
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is required but not installed"
    echo "   Install with: brew install python"
    exit 1
fi

if ! command -v gh &>/dev/null; then
    echo "❌ GitHub CLI is required but not installed"
    echo "   Install with: brew install gh"
    exit 1
fi

echo "✅ Requirements met"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p monitor_reports logs backups
echo "✅ Directories created"
echo ""

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if pip3 list | grep -q requests; then
    echo "✅ requests already installed"
else
    pip3 install requests
    echo "✅ requests installed"
fi
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x monitor_simple.sh
chmod +x setup.sh
echo "✅ Scripts are executable"
echo ""

# Test the monitor
echo "🧪 Testing monitor script..."
if ./monitor_simple.sh; then
    echo "✅ Monitor test successful"
else
    echo "❌ Monitor test failed"
    echo "   Check Python installation and try again"
    exit 1
fi
echo ""

# Set up cron jobs (optional)
echo "⏰ Setting up cron jobs..."
read -p "Do you want to set up automatic monitoring? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "To set up cron jobs, run:"
    echo "  openclaw cron add --name 'Micro SaaS Morning' --schedule '0 9 * * *' --message 'Run micro SaaS monitor'"
    echo "  openclaw cron add --name 'Micro SaaS Afternoon' --schedule '0 17 * * *' --message 'Run micro SaaS monitor'"
    echo ""
    echo "Or use the OpenClaw dashboard to configure cron jobs."
fi
echo ""

# Open the dashboard
echo "🌐 Opening dashboard..."
echo "To view the dashboard:"
echo "1. Open dashboard.html in your browser"
echo "2. Or run: python3 -m http.server 8000"
echo "3. Then visit: http://localhost:8000"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "📊 Next steps:"
echo "1. Run ./monitor_simple.sh to generate your first report"
echo "2. Open dashboard.html to view the dashboard"
echo "3. Add API keys to config.json for enhanced monitoring"
echo "4. Push to GitHub: git add . && git commit -m 'Initial setup' && git push"
echo ""

# Ask to open dashboard
read -p "Open dashboard now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &>/dev/null; then
        open dashboard.html
    elif command -v xdg-open &>/dev/null; then
        xdg-open dashboard.html
    else
        echo "Could not open browser automatically"
        echo "Please open dashboard.html manually"
    fi
fi

echo ""
echo "✅ Dashboard setup complete!"