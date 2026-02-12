// Micro SaaS Idea Dashboard - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Update last updated time
    updateLastUpdated();
    
    // Load reports
    loadReports();
    
    // Update stats
    updateStats();
    
    // Set next check time
    updateNextCheck();
    
    // Update dashboard every 30 seconds
    setInterval(updateDashboard, 30000);
});

function updateLastUpdated() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('lastUpdated').textContent = 
        `Last updated: ${now.toLocaleDateString('en-US', options)}`;
}

async function loadReports() {
    const reportsList = document.getElementById('reportsList');
    
    try {
        // In a real implementation, this would fetch from an API
        // For now, we'll simulate with sample data
        
        const sampleReports = [
            {
                title: "Morning Report - Reddit r/SaaS trending",
                time: "Today 9:15 AM",
                preview: "Found 3 interesting discussions about AI automation tools and developer pain points..."
            },
            {
                title: "Hacker News Analysis",
                time: "Yesterday 5:30 PM",
                preview: "Top stories about AI agents and developer tools. Pattern: automation tools getting traction..."
            },
            {
                title: "Product Hunt Weekly Trend",
                time: "Yesterday 9:00 AM",
                preview: "Micro SaaS tools for content creation and API monitoring trending this week..."
            }
        ];
        
        reportsList.innerHTML = '';
        
        sampleReports.forEach(report => {
            const reportItem = document.createElement('div');
            reportItem.className = 'report-item';
            reportItem.innerHTML = `
                <div class="report-header">
                    <div class="report-title">${report.title}</div>
                    <div class="report-time">${report.time}</div>
                </div>
                <div class="report-preview">${report.preview}</div>
            `;
            reportsList.appendChild(reportItem);
        });
        
    } catch (error) {
        reportsList.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Unable to load reports. Try running the monitor script first.</p>
            </div>
        `;
    }
}

function updateStats() {
    // Update today's reports count
    const today = new Date().toISOString().split('T')[0];
    const todayReports = Math.floor(Math.random() * 3) + 1; // Simulate 1-3 reports
    document.getElementById('todayReports').textContent = todayReports;
    
    // Simulate data from different sources
    document.getElementById('phCount').textContent = `${Math.floor(Math.random() * 10) + 5}`;
    document.getElementById('redditCount').textContent = `${Math.floor(Math.random() * 20) + 10}`;
    document.getElementById('hnCount').textContent = `${Math.floor(Math.random() * 15) + 8}`;
}

function updateNextCheck() {
    const now = new Date();
    const nextCheck = new Date(now);
    
    // If it's before 9 AM, next check is 9 AM
    if (now.getHours() < 9) {
        nextCheck.setHours(9, 0, 0, 0);
    } 
    // If it's between 9 AM and 5 PM, next check is 5 PM
    else if (now.getHours() < 17) {
        nextCheck.setHours(17, 0, 0, 0);
    } 
    // If it's after 5 PM, next check is tomorrow 9 AM
    else {
        nextCheck.setDate(nextCheck.getDate() + 1);
        nextCheck.setHours(9, 0, 0, 0);
    }
    
    const timeString = nextCheck.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    document.getElementById('nextCheck').textContent = timeString;
}

function updateDashboard() {
    updateLastUpdated();
    updateStats();
    updateNextCheck();
}

// Action Functions
function runMonitor() {
    alert('Running monitor script... Check the terminal for output.');
    // In a real implementation, this would make an API call to run the script
    console.log('Monitor script would be executed here');
}

function openReportsFolder() {
    alert('Opening reports folder...');
    // In a real implementation, this would open the file explorer
    console.log('Would open monitor_reports/ folder');
}

function viewLatestReport() {
    alert('Opening latest report...');
    // In a real implementation, this would open the latest report file
    console.log('Would open latest report file');
}

// Add some interactive effects
document.querySelectorAll('.stat-card, .pattern-card, .report-item').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.cursor = 'pointer';
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        runMonitor();
    }
    if (e.ctrlKey && e.key === 'o') {
        e.preventDefault();
        openReportsFolder();
    }
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        viewLatestReport();
    }
});

// Add notification for new data
function showNotification(message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Micro SaaS Dashboard', {
            body: message,
            icon: 'https://cdn-icons-png.flaticon.com/512/2721/2721266.png'
        });
    }
}

// Request notification permission on load
if ('Notification' in window) {
    Notification.requestPermission();
}

// Export function to generate report summary (for cron job integration)
function generateReportSummary() {
    return {
        timestamp: new Date().toISOString(),
        stats: {
            productHunt: document.getElementById('phCount').textContent,
            reddit: document.getElementById('redditCount').textContent,
            hackerNews: document.getElementById('hnCount').textContent,
            reportsToday: document.getElementById('todayReports').textContent
        }
    };
}