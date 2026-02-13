#!/usr/bin/env python3
"""
Tournament Schedule Parser
Parses tournaments.txt and provides tournament information for the fantasy league
"""

import json
from datetime import datetime
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
                content = f.read()
            
            # Split by comma and process each tournament
            entries = [e.strip() for e in content.split(',') if e.strip()]
            
            # Process in groups of 3 (name, tier, dates)
            for i in range(0, len(entries), 3):
                if i + 2 >= len(entries):
                    break
                
                name = entries[i].strip()
                tier_abbr = entries[i + 1].strip()
                dates = entries[i + 2].strip()
                
                # Parse the tier
                tier = TIER_MAP.get(tier_abbr, 'B-Tier')
                
                # Parse dates
                start_date, end_date = self.parse_dates(dates)
                
                tournament = {
                    'name': name,
                    'tier_abbr': tier_abbr,
                    'tier': tier,
                    'dates_raw': dates,
                    'start_date': start_date,
                    'end_date': end_date,
                }
                
                tournaments.append(tournament)
            
            print(f"✅ Loaded {len(tournaments)} tournaments from schedule")
            return tournaments
            
        except FileNotFoundError:
            print(f"⚠️  Warning: {self.schedule_file} not found")
            return []
        except Exception as e:
            print(f"❌ Error loading schedule: {e}")
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
                'A-Tier': '⚪ A-Tier',
                'B-Tier': '⚫ B-Tier'
            }.get(t['tier'], t['tier'])
            
            print(f"\n{i:2d}. {t['name']}")
            print(f"    {tier_display}")
            print(f"    {t['dates_raw']}")
            if t['start_date']:
                print(f"    Start: {t['start_date'].strftime('%Y-%m-%d')}")
        
        print("\n" + "=" * 80)


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
        test_tournament = schedule.find_tournament_by_name("jonesboro")
        if test_tournament:
            print(f"Found: {test_tournament['name']} - {test_tournament['tier']}")
        
        # Test upcoming tournaments
        print("\n\n📅 Upcoming tournaments (next 60 days):")
        upcoming = schedule.get_upcoming_tournaments(days_ahead=60)
        for t in upcoming[:5]:
            print(f"  • {t['name']} - {t['start_date'].strftime('%B %d')}")
        
        # Test date range
        print("\n\n📆 Tournaments in March:")
        march_start = datetime(2025, 3, 1)
        march_end = datetime(2025, 3, 31)
        march_tournaments = schedule.get_tournaments_in_date_range(march_start, march_end)
        for t in march_tournaments:
            print(f"  • {t['name']}")
    
    else:
        print("\n❌ No tournaments loaded. Make sure tournaments.txt exists!")


if __name__ == "__main__":
    main()
