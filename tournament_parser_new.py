#!/usr/bin/env python3
"""
Tournament Schedule Parser
Parses tournaments.txt and provides tournament information for the fantasy league
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# Tier mapping from abbreviations to full names
TIER_MAP = {
    'ES': 'DGPT - Elite Series',
    'ESP': 'DGPT - Elite Series Plus',  # Elite Series Playoffs (alternate notation)
    'M': 'Major',

}


class TournamentSchedule:
    """Manages the tournament schedule for the season"""
    
    def __init__(self, schedule_file: str = "tournaments.txt"):
        self.schedule_file = schedule_file
        self.tournaments = self.load_schedule()
    
    def load_schedule(self) -> List[Dict]:
        """Load and parse the tournament schedule"""
        tournaments = []
        
        try:
            with open(self.schedule_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Split by comma
                parts = [p.strip() for p in line.split(',')]
                
                # Need at least name, tier, and dates
                if len(parts) < 3:
                    continue
                
                name = parts[0]
                tier_abbr = parts[1]
                dates = parts[2]
                
                # Event ID is optional (4th field)
                event_id = parts[3] if len(parts) >= 4 and parts[3] else None
                
                # Parse the tier
                tier = TIER_MAP.get(tier_abbr, 'ES')
                
                # Parse dates
                start_date, end_date = self.parse_dates(dates)
                
                tournament = {
                    'name': name,
                    'tier_abbr': tier_abbr,
                    'tier': tier,
                    'dates_raw': dates,
                    'start_date': start_date,
                    'end_date': end_date,
                    'event_id': event_id,
                }
                
                tournaments.append(tournament)
            
            # Count how many have event IDs
            with_ids = sum(1 for t in tournaments if t['event_id'])
            print(f"✅ Loaded {len(tournaments)} tournaments from schedule ({with_ids} with event IDs)")
            return tournaments
            
        except FileNotFoundError:
            print(f"⚠️  Warning: {self.schedule_file} not found")
            return []
        except Exception as e:
            print(f"❌ Error loading schedule: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def parse_dates(self, date_string: str) -> tuple:
        """
        Parse date string like "February 27 - March 1" or "April 9 - 12"
        Returns (start_date, end_date) as datetime objects
        """
        try:
            # Handle different date formats
            parts = date_string.split('-')
            
            if len(parts) == 2:
                start_str = parts[0].strip()
                end_str = parts[1].strip()
                
                # Assume current year (or next year if past)
                year = datetime.now().year
                
                # Parse start date
                start_date = datetime.strptime(f"{start_str} {year}", "%B %d %Y")
                
                # Handle end date (might be just a day number)
                if ' ' in end_str:
                    # Full date like "March 1"
                    end_date = datetime.strptime(f"{end_str} {year}", "%B %d %Y")
                else:
                    # Just a day number, use start month
                    month_name = start_str.split()[0]
                    end_date = datetime.strptime(f"{month_name} {end_str} {year}", "%B %d %Y")
                
                # If start date has passed and it's early in the year, might be next year
                now = datetime.now()
                if start_date < now and now.month <= 3:
                    # Tournament is probably next year
                    start_date = start_date.replace(year=year + 1)
                    end_date = end_date.replace(year=year + 1)
                
                return start_date, end_date
            
        except Exception as e:
            print(f"⚠️  Could not parse dates '{date_string}': {e}")
        
        return None, None
    
    def find_tournament_by_name(self, name: str) -> Optional[Dict]:
        """Find a tournament by name (case-insensitive partial match)"""
        name_lower = name.lower()
        
        for tournament in self.tournaments:
            if name_lower in tournament['name'].lower():
                return tournament
        
        return None
    
    def find_tournament_by_event_id(self, event_id: str) -> Optional[Dict]:
        """Find a tournament by its PDGA event ID"""
        for tournament in self.tournaments:
            if tournament.get('event_id') == str(event_id):
                return tournament
        
        return None
    
    def get_event_id(self, tournament_name: str) -> Optional[str]:
        """
        Get the event ID for a tournament by name
        Returns None if tournament not found or has no event ID
        """
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament:
            return tournament.get('event_id')
        return None
    
    def get_tournaments_with_event_ids(self) -> List[Dict]:
        """Get all tournaments that have event IDs"""
        return [t for t in self.tournaments if t.get('event_id')]
    
    def get_tournaments_without_event_ids(self) -> List[Dict]:
        """Get all tournaments that don't have event IDs yet"""
        return [t for t in self.tournaments if not t.get('event_id')]
    
    def get_tournaments_in_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get all tournaments that fall within a date range"""
        matching = []
        
        for tournament in self.tournaments:
            if tournament['start_date'] and tournament['end_date']:
                # Check if tournament overlaps with date range
                if (tournament['start_date'] <= end_date and 
                    tournament['end_date'] >= start_date):
                    matching.append(tournament)
        
        return matching
    
    def get_tier_for_tournament(self, name: str) -> str:
        """Get the tier for a tournament by name"""
        tournament = self.find_tournament_by_name(name)
        if tournament:
            return tournament['tier']
        return 'B-Tier'  # Default if not found
    
    def get_upcoming_tournaments(self, days_ahead: int = 30) -> List[Dict]:
        """Get tournaments coming up in the next N days"""
        now = datetime.now()
        future_date = now + timedelta(days=days_ahead)
        
        upcoming = []
        for tournament in self.tournaments:
            if tournament['start_date']:
                if now <= tournament['start_date'] <= future_date:
                    upcoming.append(tournament)
        
        return sorted(upcoming, key=lambda x: x['start_date'])
    
    def export_to_json(self, output_file: str = "data/tournament_schedule.json"):
        """Export the schedule to JSON format"""
        schedule_data = {
            'season': datetime.now().year,
            'last_updated': datetime.now().isoformat(),
            'tournaments': [
                {
                    'name': t['name'],
                    'tier': t['tier'],
                    'tier_abbr': t['tier_abbr'],
                    'dates': t['dates_raw'],
                    'start_date': t['start_date'].isoformat() if t['start_date'] else None,
                    'end_date': t['end_date'].isoformat() if t['end_date'] else None,
                    'event_id': t.get('event_id'),
                }
                for t in self.tournaments
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(schedule_data, f, indent=2)
        
        print(f"✅ Exported schedule to {output_file}")
    
    def print_schedule(self):
        """Print the tournament schedule in a readable format"""
        print("\n" + "=" * 80)
        print("2025 DGPT Tournament Schedule")
        print("=" * 80)
        
        for i, t in enumerate(self.tournaments, 1):
            tier_display = {
                'DGPT - Elite Series': '🔴 Elite',
                'Major': '🟠 Major',
                'DGPT - Silver Series': '🔵 Silver',

            }.get(t['tier'], t['tier'])
            
            print(f"\n{i:2d}. {t['name']}")
            print(f"    {tier_display}")
            print(f"    {t['dates_raw']}")
            if t['start_date']:
                print(f"    Start: {t['start_date'].strftime('%Y-%m-%d')}")
            if t.get('event_id'):
                print(f"    Event ID: {t['event_id']} ✅")
            else:
                print(f"    Event ID: [Not set]")
        
        print("\n" + "=" * 80)
        
        # Summary
        with_ids = sum(1 for t in self.tournaments if t.get('event_id'))
        without_ids = len(self.tournaments) - with_ids
        print(f"\nSummary:")
        print(f"  Total tournaments: {len(self.tournaments)}")
        print(f"  With event IDs: {with_ids} ✅")
        print(f"  Without event IDs: {without_ids}")
        print("=" * 80)


def scrape_tournament_by_event_id(event_id: str, division: str = 'MPO') -> Optional[Dict]:
    """
    Scrape tournament results directly by PDGA event ID
    
    Args:
        event_id: PDGA event ID (e.g., '88276')
        division: Division to scrape (default: 'MPO')
    
    Returns:
        Dictionary with tournament info and results, or None if failed
    """
    import requests
    from bs4 import BeautifulSoup
    import re
    
    print(f"\n{'='*80}")
    print(f"Scraping Tournament by Event ID: {event_id}")
    print(f"{'='*80}")
    
    try:
        # Build URL
        url = f"https://www.pdga.com/tour/event/{event_id}"
        
        print(f"\n1. Fetching: {url}")
        
        # Set up session with proper headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        print(f"   ✅ Response: {response.status_code}")
        
        # Parse HTML
        print(f"\n2. Parsing HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract tournament name
        title_tag = soup.find('title')
        tournament_name = title_tag.get_text().split('|')[0].strip() if title_tag else f"Event {event_id}"
        
        print(f"   ✅ Tournament: {tournament_name}")
        
        # Find division header
        print(f"\n3. Finding {division} division...")
        division_header = soup.find('h3', {'class': 'division', 'id': division})
        
        if not division_header:
            print(f"   ❌ Could not find {division} division")
            return None
        
        division_text = division_header.get_text()
        print(f"   ✅ Found: {division_text}")
        
        # Find results table
        print(f"\n4. Finding results table...")
        details_section = division_header.find_parent('details')
        
        if details_section:
            results_table = details_section.find('table', class_='results')
        else:
            results_table = division_header.find_next('table', class_='results')
        
        if not results_table:
            print(f"   ❌ Could not find results table")
            return None
        
        print(f"   ✅ Found results table")
        
        # Parse results
        print(f"\n5. Parsing player results...")
        tbody = results_table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
        else:
            rows = results_table.find_all('tr')[1:]
        
        print(f"   Found {len(rows)} rows")
        
        results = []
        
        for row in rows:
            try:
                # Find placement
                place_cell = row.find('td', class_='place')
                if not place_cell:
                    continue
                
                place_text = place_cell.get_text().strip()
                place_match = re.search(r'\d+', place_text)
                if not place_match:
                    continue
                placement = int(place_match.group())
                
                # Find player cell
                player_cell = row.find('td', class_='player')
                if not player_cell:
                    continue
                
                player_link = player_cell.find('a')
                if not player_link:
                    continue
                
                player_name = player_link.get_text().strip()
                
                # Extract PDGA number
                href = player_link.get('href', '')
                pdga_match = re.search(r'/player/(\d+)', href)
                
                if not pdga_match:
                    pdga_cell = row.find('td', class_='pdga-number')
                    if pdga_cell:
                        pdga_text = pdga_cell.get_text().strip()
                        pdga_match = re.search(r'\d+', pdga_text)
                        if pdga_match:
                            pdga_number = int(pdga_match.group())
                        else:
                            continue
                    else:
                        continue
                else:
                    pdga_number = int(pdga_match.group(1))
                
                results.append({
                    'placement': placement,
                    'pdga_number': pdga_number,
                    'name': player_name,
                    'tied': 'T' in place_text.upper()
                })
            
            except Exception:
                continue
        
        print(f"   ✅ Successfully parsed {len(results)} players")
        
        tournament = {
            'id': event_id,
            'name': tournament_name,
            'division': division,
            'results': results,
            'url': url
        }
        
        print(f"\n{'='*80}")
        print(f"✅ Successfully scraped {tournament_name}")
        print(f"   Event ID: {event_id}")
        print(f"   Players: {len(results)}")
        print(f"{'='*80}\n")
        
        return tournament
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def scrape_all_with_event_ids(schedule: TournamentSchedule) -> List[Dict]:
    """
    Scrape all tournaments that have event IDs
    
    Args:
        schedule: TournamentSchedule instance
    
    Returns:
        List of tournament dictionaries with results
    """
    import time
    
    tournaments_with_ids = schedule.get_tournaments_with_event_ids()
    
    print(f"\n{'='*80}")
    print(f"Scraping {len(tournaments_with_ids)} tournaments with event IDs")
    print(f"{'='*80}\n")
    
    results = []
    
    for i, tournament_info in enumerate(tournaments_with_ids, 1):
        event_id = tournament_info['event_id']
        
        print(f"\n[{i}/{len(tournaments_with_ids)}] {tournament_info['name']}")
        
        tournament = scrape_tournament_by_event_id(event_id)
        
        if tournament:
            # Add tier information
            tournament['tier'] = tournament_info['tier']
            tournament['tier_abbr'] = tournament_info['tier_abbr']
            tournament['dates_raw'] = tournament_info['dates_raw']
            tournament['date'] = tournament_info['end_date'].strftime('%Y-%m-%d') if tournament_info.get('end_date') else None
            tournament['location'] = 'USA'
            
            results.append(tournament)
        
        # Rate limiting
        if i < len(tournaments_with_ids):
            time.sleep(3)
    
    print(f"\n{'='*80}")
    print(f"✅ Scraped {len(results)}/{len(tournaments_with_ids)} successfully")
    print(f"{'='*80}\n")
    
    return results


def main():
    """Test the tournament schedule parser"""
    from datetime import timedelta
    
    schedule = TournamentSchedule()
    
    if schedule.tournaments:
        # Print full schedule
        schedule.print_schedule()
        
        # Export to JSON
        schedule.export_to_json()
        
        # Test finding by name
        print("\n\n🔍 Testing name search:")
        test_tournament = schedule.find_tournament_by_name("supreme flight")
        if test_tournament:
            print(f"Found: {test_tournament['name']}")
            print(f"  Tier: {test_tournament['tier']}")
            if test_tournament.get('event_id'):
                print(f"  Event ID: {test_tournament['event_id']}")
        
        # Test event ID lookup
        if test_tournament and test_tournament.get('event_id'):
            print(f"\n🆔 Testing event ID lookup:")
            found_by_id = schedule.find_tournament_by_event_id(test_tournament['event_id'])
            if found_by_id:
                print(f"Found by ID {test_tournament['event_id']}: {found_by_id['name']}")
                
                # Test scraping by event ID
                print(f"\n📥 Testing scraping by event ID...")
                tournament_data = scrape_tournament_by_event_id(test_tournament['event_id'])
                
                if tournament_data:
                    print(f"\n✅ Scraping test successful!")
                    print(f"   Tournament: {tournament_data['name']}")
                    print(f"   Players scraped: {len(tournament_data['results'])}")
                    
                    # Show top 5
                    if tournament_data['results']:
                        print(f"\n   Top 5 finishers:")
                        for result in tournament_data['results'][:5]:
                            print(f"      {result['placement']}. {result['name']} (#{result['pdga_number']})")
        
        # Test upcoming tournaments
        print("\n\n📅 Upcoming tournaments (next 60 days):")
        upcoming = schedule.get_upcoming_tournaments(days_ahead=60)
        for t in upcoming[:5]:
            event_id_text = f" (ID: {t['event_id']})" if t.get('event_id') else " [No ID]"
            print(f"  • {t['name']} - {t['start_date'].strftime('%B %d')}{event_id_text}")
        
        # Show tournaments without event IDs
        without_ids = schedule.get_tournaments_without_event_ids()
        if without_ids:
            print(f"\n\n⚠️  Tournaments without event IDs ({len(without_ids)}):")
            for t in without_ids:
                print(f"  • {t['name']}")
            print(f"\n   To add event IDs:")
            print(f"   1. Go to https://www.pdga.com/tour/search")
            print(f"   2. Search for each tournament")
            print(f"   3. Get event ID from URL: /tour/event/XXXXX")
            print(f"   4. Add to tournaments.txt after dates: Name,Tier,Dates,EventID")
    
    else:
        print("\n❌ No tournaments loaded. Make sure tournaments.txt exists!")


if __name__ == "__main__":
    main()
