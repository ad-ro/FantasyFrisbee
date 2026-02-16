#!/usr/bin/env python3
"""
Diagnostic Script for Fantasy Disc Golf League Scraper
Tests each component to identify issues
"""

import sys
import json
from datetime import datetime, timedelta

def test_imports():
    """Test if all required packages are installed"""
    print("=" * 80)
    print("TEST 1: Checking Required Packages")
    print("=" * 80)
    
    required = {
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package} - installed")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n  ⚠️  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n  ✅ All packages installed!\n")
    return True


def test_tournament_schedule():
    """Test if tournaments2025.txt can be read"""
    print("=" * 80)
    print("TEST 2: Reading Tournament Schedule")
    print("=" * 80)
    
    try:
        with open('tournaments2025.txt', 'r') as f:
            content = f.read()
        
        if not content.strip():
            print("  ❌ tournaments2025.txt is empty!")
            return False
        
        # Count tournaments
        lines = [l for l in content.split(',') if l.strip()]
        num_tournaments = len(lines) // 3
        
        print(f"  ✅ tournaments2025.txt found")
        print(f"  ✅ Contains {num_tournaments} tournaments")
        
        # Show first tournament
        if num_tournaments > 0:
            print(f"\n  First tournament:")
            print(f"    Name: {lines[0].strip()}")
            print(f"    Tier: {lines[1].strip()}")
            print(f"    Dates: {lines[2].strip()}")
        
        return True
        
    except FileNotFoundError:
        print("  ❌ tournaments2025.txt not found!")
        print("  Make sure tournaments2025.txt is in the same directory")
        return False
    except Exception as e:
        print(f"  ❌ Error reading tournaments2025.txt: {e}")
        return False


def test_tournament_parser():
    """Test if tournament parser works"""
    print("\n" + "=" * 80)
    print("TEST 3: Tournament Parser")
    print("=" * 80)
    
    try:
        from tournament_parser import TournamentSchedule
        
        schedule = TournamentSchedule()
        
        if not schedule.tournaments:
            print("  ❌ No tournaments loaded by parser")
            return False
        
        print(f"  ✅ Parsed {len(schedule.tournaments)} tournaments")
        
        # Test date range function
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        recent = schedule.get_tournaments_in_date_range(start_date, end_date)
        print(f"  ✅ Found {len(recent)} tournaments in past 30 days")
        
        if recent:
            print(f"\n  Most recent tournament:")
            t = recent[-1]
            print(f"    Name: {t['name']}")
            print(f"    Tier: {t['tier']}")
            print(f"    Dates: {t['dates_raw']}")
        
        return True
        
    except ImportError:
        print("  ❌ Cannot import tournament_parser.py")
        return False
    except Exception as e:
        print(f"  ❌ Error in tournament parser: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_network_connectivity():
    """Test if we can reach PDGA website"""
    print("\n" + "=" * 80)
    print("TEST 4: Network Connectivity to PDGA")
    print("=" * 80)
    
    try:
        import requests
        
        print("  Testing connection to pdga.com...")
        response = requests.get('https://www.pdga.com', timeout=10)
        
        print(f"  ✅ Connected! Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ PDGA website is accessible")
            return True
        else:
            print(f"  ⚠️  Unusual status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ❌ Connection timeout - network issue or PDGA is down")
        return False
    except requests.exceptions.ConnectionError:
        print("  ❌ Connection error - check your internet connection")
        return False
    except Exception as e:
        print(f"  ❌ Network error: {e}")
        return False


def test_pdga_search():
    """Test searching for a known tournament"""
    print("\n" + "=" * 80)
    print("TEST 5: PDGA Tournament Search")
    print("=" * 80)
    
    try:
        from update_league import PDGAScraper
        import requests
        from bs4 import BeautifulSoup
        
        scraper = PDGAScraper()
        
        # Try to search for a well-known tournament
        print("  Searching for 'USDGC' on PDGA...")
        
        search_url = f"{scraper.base_url}/tour/search"
        params = {'title': 'USDGC'}
        
        response = scraper.session.get(search_url, params=params, timeout=10)
        print(f"  Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  ⚠️  Non-200 status code")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find any tournament links
        import re
        event_links = soup.find_all('a', href=re.compile(r'/tour/event/\d+'))
        
        print(f"  Found {len(event_links)} event links")
        
        if event_links:
            print("  ✅ PDGA search is working!")
            print(f"\n  Sample event link: {event_links[0].get('href')}")
            
            # Try to extract event ID
            href = event_links[0]['href']
            event_match = re.search(r'/tour/event/(\d+)', href)
            if event_match:
                print(f"  ✅ Event ID extraction works: {event_match.group(1)}")
            
            return True
        else:
            print("  ⚠️  No event links found in search results")
            print("\n  This likely means PDGA's HTML structure has changed")
            print("  You'll need to inspect the page manually and update selectors")
            
            # Save HTML for inspection
            with open('debug_search_results.html', 'w') as f:
                f.write(response.text)
            print("\n  💾 Saved HTML to debug_search_results.html for inspection")
            
            return False
            
    except Exception as e:
        print(f"  ❌ Error during search test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdga_results_page():
    """Test scraping a known tournament results page"""
    print("\n" + "=" * 80)
    print("TEST 6: PDGA Results Page Scraping")
    print("=" * 80)
    
    try:
        from update_league import PDGAScraper
        import requests
        from bs4 import BeautifulSoup
        import re
        
        scraper = PDGAScraper()
        
        # Use Supreme Flight 2024 as test event (event ID from your HTML: 88276)
        test_event_id = "88276"
        
        print(f"  Testing with event ID: {test_event_id} (Supreme Flight 2024)")
        print(f"  URL: {scraper.base_url}/tour/event/{test_event_id}")
        
        response = scraper.session.get(f"{scraper.base_url}/tour/event/{test_event_id}", timeout=15)
        
        if response.status_code != 200:
            print(f"  ⚠️  Status code: {response.status_code}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for MPO division header
        print("\n  Looking for MPO division...")
        
        division_header = soup.find('h3', {'class': 'division', 'id': 'MPO'})
        
        if not division_header:
            print("  ❌ Could not find MPO division header with id='MPO'")
            print("\n  PDGA page structure may have changed")
            
            # Save HTML for inspection
            with open('debug_results_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("\n  💾 Saved HTML to debug_results_page.html for inspection")
            
            return False
        
        print("  ✅ Found MPO division header")
        
        # Find results table
        details_section = division_header.find_parent('details')
        if details_section:
            results_table = details_section.find('table', class_='results')
        else:
            results_table = division_header.find_next('table', class_='results')
        
        if not results_table:
            print("  ❌ Could not find results table")
            return False
        
        print("  ✅ Found results table")
        
        # Try to parse rows
        tbody = results_table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
        else:
            rows = results_table.find_all('tr')[1:]
        
        print(f"  Found {len(rows)} result rows")
        
        if len(rows) == 0:
            print("  ⚠️  No rows found - table structure may have changed")
            return False
        
        # Try to parse first few rows
        parsed_count = 0
        for row in rows[:5]:
            try:
                # Find placement
                place_cell = row.find('td', class_='place')
                if not place_cell:
                    continue
                
                placement = place_cell.get_text().strip()
                
                # Find player cell
                player_cell = row.find('td', class_='player')
                if not player_cell:
                    continue
                
                player_link = player_cell.find('a')
                if not player_link:
                    continue
                
                player_name = player_link.get_text().strip()
                
                # Extract PDGA number from link
                href = player_link.get('href', '')
                pdga_match = re.search(r'/player/(\d+)', href)
                
                if pdga_match:
                    pdga_number = pdga_match.group(1)
                    parsed_count += 1
                    
                    if parsed_count <= 3:
                        print(f"  ✅ Parsed: {placement}. {player_name} (PDGA #{pdga_number})")
            
            except Exception as e:
                continue
        
        if parsed_count > 0:
            print(f"\n  ✅ Successfully parsed {parsed_count}/5 test rows")
            print("  ✅ Results page parsing is working!")
            return True
        else:
            print("  ⚠️  Could not parse any rows")
            print("  HTML structure may have changed")
            return False
        
    except Exception as e:
        print(f"  ❌ Error during results test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_scraper():
    """Test the full scraper with current data"""
    print("\n" + "=" * 80)
    print("TEST 7: Full Scraper Test")
    print("=" * 80)
    
    try:
        from update_league import PDGAScraper
        
        scraper = PDGAScraper()
        
        print("  Running full tournament scraper...")
        print("  (This may take a minute)")
        
        tournaments = scraper.get_recent_mpo_tournaments(days_back=60)  # Look back 60 days
        
        print(f"\n  Found {len(tournaments)} tournaments with results")
        
        if len(tournaments) == 0:
            print("\n  ⚠️  No tournaments found. This could mean:")
            print("     - No tournaments finished in past 60 days")
            print("     - Tournament names don't match PDGA exactly")
            print("     - PDGA search isn't finding the tournaments")
            print("     - Dates in tournaments2025.txt are in the future")
            return False
        
        # Show details of first tournament
        if tournaments:
            t = tournaments[0]
            print(f"\n  First tournament scraped:")
            print(f"    Name: {t['name']}")
            print(f"    Tier: {t['tier']}")
            print(f"    Results: {len(t.get('results', []))} players")
            
            if t.get('results'):
                print(f"\n    Sample results:")
                for result in t['results'][:3]:
                    print(f"      {result['placement']}. {result['name']} (PDGA #{result['pdga_number']})")
        
        print("\n  ✅ Scraper is working!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error during full scraper test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all diagnostic tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "FANTASY DISC GOLF SCRAPER DIAGNOSTICS" + " " * 21 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    results = {}
    
    # Run all tests
    results['imports'] = test_imports()
    
    if results['imports']:
        results['schedule'] = test_tournament_schedule()
        results['parser'] = test_tournament_parser()
        results['network'] = test_network_connectivity()
        
        if results['network']:
            results['search'] = test_pdga_search()
            results['results_page'] = test_pdga_results_page()
            results['full_scraper'] = test_full_scraper()
    
    # Summary
    print("\n" + "=" * 80)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if not results.get('imports'):
        print("\n  1. Install missing packages:")
        print("     pip install requests beautifulsoup4 lxml")
    
    elif not results.get('schedule'):
        print("\n  1. Make sure tournaments2025.txt is in the current directory")
        print("     and contains tournament data")
    
    elif not results.get('network'):
        print("\n  1. Check your internet connection")
        print("  2. Verify PDGA.com is accessible in your browser")
    
    elif not results.get('search') or not results.get('results_page'):
        print("\n  1. PDGA website structure has likely changed")
        print("  2. Check debug HTML files created:")
        print("     - debug_search_results.html")
        print("     - debug_results_page.html")
        print("\n  3. Update CSS selectors in update_league.py:")
        print("     - search_pdga_tournament() function")
        print("     - get_tournament_results_by_event_id() function")
        print("\n  4. See AUTOMATED_SCRAPING.md for detailed instructions")
    
    elif not results.get('full_scraper'):
        print("\n  1. Check if tournaments2025.txt dates are correct")
        print("  2. Verify tournament names match PDGA exactly")
        print("  3. Try increasing days_back parameter")
        print("  4. Check if tournaments have posted final results on PDGA")
    
    else:
        print("\n  ✅ All tests passed! Your scraper is working correctly.")
        print("\n  If you're still not seeing data:")
        print("     - Make sure tournaments have finished and results are posted")
        print("     - Run: python3 update_league.py")
        print("     - Check GitHub Actions logs if using automation")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
