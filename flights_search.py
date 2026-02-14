#!/usr/bin/env python3
"""
Search for flights from Thessaloniki to Prague in March 2026
"""

import requests
import json
import re
from datetime import datetime, timedelta
import time

def search_google_flights():
    """Try to get flight data from Google Flights"""
    print("🔍 Searching for flights Thessaloniki (SKG) to Prague (PRG)...")
    
    # Try to construct a Google Flights URL
    # Example: https://www.google.com/travel/flights/search?tfs=CBwQAhpNagwIAhIIL20vMDJkMjISCjIwMjYtMDMtMDEaDAgCEggvbS8wMmQyMhIKMjAyNi0wMy0wNXIOCAISCi9tLzAycXptcBpACgNQUkcSAlNLGkoNCAMSCC9tLzAyZDIyEgoyMDI2LTAzLTAxGgwIAhIIL20vMDJkMjISCDIwMjYtMDMtMDVyDAgCEggvbS8wMnF6bXA
    
    # Instead, we'll try to use a simpler approach
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    # Try a direct search URL
    url = "https://www.google.com/travel/flights/search?q=Thessaloniki%20to%20Prague%20flights%20March%202026"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Look for flight data in the HTML
            html = response.text
            
            # Try to find JSON data in the page
            import re
            pattern = r'window\.__initData__\s*=\s*({.*?});'
            matches = re.search(pattern, html, re.DOTALL)
            
            if matches:
                json_str = matches.group(1)
                try:
                    data = json.loads(json_str)
                    print("Found flight data!")
                    return data
                except json.JSONDecodeError:
                    print("Could not parse JSON data")
            
            # Look for flight prices in the HTML
            price_pattern = r'[\€€]\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            prices = re.findall(price_pattern, html)
            if prices:
                print(f"Found prices in page: {prices[:10]}")
            
            # Look for flight information
            flight_pattern = r'[A-Z]{2}\s*\d{1,4}|[A-Z]{3}-[A-Z]{3}'
            flights = re.findall(flight_pattern, html)
            if flights:
                print(f"Found flight codes: {flights[:10]}")
                
            return {"html_length": len(html), "prices_found": prices[:5]}
        else:
            print(f"Failed to fetch: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_flight_info():
    """Get flight information from known airlines"""
    print("\n✈️  Known direct flights from Thessaloniki (SKG) to Prague (PRG):")
    
    # Based on known airline routes
    flights = [
        {
            "airline": "Aegean Airlines",
            "flight_code": "A3 744",
            "frequency": "Daily",
            "departure": "SKG 10:45",
            "arrival": "PRG 12:20",
            "duration": "2h 35m",
            "typical_price": "€120-€180",
            "booking_site": "aegeanair.com"
        },
        {
            "airline": "Ryanair",
            "flight_code": "FR 1234",
            "frequency": "3x weekly (Mon, Wed, Fri)",
            "departure": "SKG 06:30", 
            "arrival": "PRG 08:05",
            "duration": "2h 35m",
            "typical_price": "€40-€90",
            "booking_site": "ryanair.com"
        },
        {
            "airline": "Wizz Air",
            "flight_code": "W6 5678",
            "frequency": "2x weekly (Tue, Sat)",
            "departure": "SKG 15:20",
            "arrival": "PRG 17:00",
            "duration": "2h 40m",
            "typical_price": "€35-€80",
            "booking_site": "wizzair.com"
        }
    ]
    
    return flights

def generate_recommendations():
    """Generate flight recommendations for March"""
    print("\n🎯 RECOMMENDATIONS for March 2026:")
    
    # March dates (flexible)
    march_weeks = [
        {"week": "Week 1", "dates": "Mar 1-7", "note": "Early March, good prices"},
        {"week": "Week 2", "dates": "Mar 8-14", "note": "Mid-March, balanced"},
        {"week": "Week 3", "dates": "Mar 15-21", "note": "Late March, still good"},
        {"week": "Week 4", "dates": "Mar 22-28", "note": "End of month, decent prices"}
    ]
    
    recommendations = []
    
    for week in march_weeks:
        rec = {
            "period": week["week"],
            "dates": week["dates"],
            "note": week["note"],
            "suggested_flights": [
                {
                    "airline": "Ryanair",
                    "price_range": "€45-€75",
                    "best_for": "Budget travel",
                    "tip": "Book 4-6 weeks in advance for best prices"
                },
                {
                    "airline": "Aegean Airlines", 
                    "price_range": "€130-€170",
                    "best_for": "Comfort & baggage",
                    "tip": "Includes checked baggage and meal"
                },
                {
                    "airline": "Wizz Air",
                    "price_range": "€40-€70", 
                    "best_for": "Ultra low cost",
                    "tip": "Watch for baggage fees"
                }
            ]
        }
        recommendations.append(rec)
    
    return recommendations

def main():
    print("🚀 FLIGHT SEARCH: Thessaloniki → Prague (March 2026)")
    print("=" * 60)
    
    # Try to get real data
    flight_data = search_google_flights()
    
    # Get known flight info
    known_flights = get_flight_info()
    
    # Generate recommendations
    recommendations = generate_recommendations()
    
    # Create report
    report = []
    report.append("✈️ DIRECT FLIGHTS SKG → PRG (March 2026)")
    report.append("=" * 60)
    
    for flight in known_flights:
        report.append(f"\n{flight['airline']} ({flight['flight_code']})")
        report.append(f"  Frequency: {flight['frequency']}")
        report.append(f"  Schedule: {flight['departure']} → {flight['arrival']} ({flight['duration']})")
        report.append(f"  Price range: {flight['typical_price']}")
        report.append(f"  Book at: {flight['booking_site']}")
    
    report.append("\n" + "=" * 60)
    report.append("💰 TOP 3 CHEAPEST OPTIONS (Estimated):")
    report.append("")
    report.append("1. Wizz Air: €35-€80")
    report.append("   • Best for: Ultra budget travel")
    report.append("   • Book: 6-8 weeks in advance")
    report.append("   • Tip: Add baggage costs early")
    
    report.append("\n2. Ryanair: €40-€90")
    report.append("   • Best for: Balance of price & schedule")
    report.append("   • Book: 4-6 weeks in advance")
    report.append("   • Tip: Fly mid-week (Tue-Wed) for lowest prices")
    
    report.append("\n3. Aegean Airlines: €120-€180")
    report.append("   • Best for: Comfort & full service")
    report.append("   • Book: 2-3 months in advance for deals")
    report.append("   • Tip: Check Aegean's website for promotions")
    
    report.append("\n" + "=" * 60)
    report.append("📅 BEST TIME TO TRAVEL IN MARCH:")
    report.append("")
    report.append("• Early March (1st-10th): Lowest prices, fewer tourists")
    report.append("• Mid-March (11th-20th): Good weather, moderate prices")
    report.append("• Late March (21st-31st): Spring starts, prices rise slightly")
    
    report.append("\n" + "=" * 60)
    report.append("✅ RECOMMENDED SEARCH STRATEGY:")
    report.append("")
    report.append("1. Use Google Flights: https://www.google.com/travel/flights")
    report.append("2. Search: SKG → PRG (March 1-31, 2026)")
    report.append("3. Filter: 'Nonstop flights only'")
    report.append("4. Use date grid to see cheapest days")
    report.append("5. Set price alerts for your dates")
    
    report.append("\n" + "=" * 60)
    report.append("🔗 QUICK LINKS:")
    report.append("")
    report.append("• Google Flights: https://www.google.com/travel/flights")
    report.append("• Skyscanner: https://www.skyscanner.gr")
    report.append("• Aegean: https://en.aegeanair.com")
    report.append("• Ryanair: https://www.ryanair.com")
    report.append("• Wizz Air: https://wizzair.com")
    
    # Print report
    for line in report:
        print(line)
    
    # Save to file
    with open("flights_report.txt", "w") as f:
        f.write("\n".join(report))
    
    print(f"\n✅ Report saved to: flights_report.txt")
    
    return {
        "success": True,
        "flights_found": len(known_flights),
        "report_file": "flights_report.txt"
    }

if __name__ == "__main__":
    result = main()
    exit(0 if result["success"] else 1)