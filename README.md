# Micro SaaS Idea Dashboard

A dashboard for tracking trending micro SaaS ideas from multiple sources.

## Features

- **Automated Monitoring**: Checks Product Hunt, Reddit r/SaaS, Hacker News, and more
- **Daily Reports**: Generates morning and afternoon reports
- **Trend Analysis**: Identifies patterns and pain points
- **Simple Web Interface**: View all reports in one place

## Sources Monitored

1. **Product Hunt** - Daily product launches
2. **Reddit r/SaaS** - Pain points and discussions
3. **Hacker News** - Tech trends and "Ask HN" posts
4. **Indie Hackers** - Success stories and questions
5. **Twitter #buildinpublic** - Real-time maker updates

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/makis73/microsaas-idea-dashboard.git
cd microsaas-idea-dashboard
```

### 2. Run the monitoring system
```bash
./monitor_simple.sh
```

### 3. Open the dashboard
```bash
open dashboard.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Automated Monitoring

The system uses OpenClaw cron jobs to run:
- **9:00 AM** - Morning check
- **5:00 PM** - Afternoon check

Reports are saved to `monitor_reports/` folder.

## Dashboard Structure

```
microsaas-idea-dashboard/
├── dashboard.html          # Main dashboard
├── style.css              # Dashboard styles
├── script.js              # Dashboard functionality
├── monitor_simple.sh      # Monitoring script
├── monitor_microsaas.py   # Advanced monitoring (Python)
├── monitor_reports/       # Generated reports
├── config.json            # Configuration file
└── README.md              # This file
```

## Configuration

Edit `config.json` to:
- Add API keys (Product Hunt, Twitter, etc.)
- Change monitoring frequency
- Add new sources to monitor

## Adding New Sources

1. Add source to `monitor_simple.sh`
2. Update `dashboard.html` to display new data
3. Test with `./monitor_simple.sh`

## License

MIT