#!/usr/bin/env python3
"""
PDGA Fantasy Disc Golf League Scraper
Fetches tournament results and calculates fantasy points
Integrates with tournaments.txt schedule for automated scraping
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from bs4 import BeautifulSoup
import re

# Import tournament schedule parser
try:
    from tournament_parser import TournamentSchedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    print("⚠️  tournament_parser.py not found - tier detection will use defaults")

# Event tier multipliers
TIER_MULTIPLIERS = {
    'DGPT - Elite Series': 1.0,
    'Major': 2.0,
    'DGPT - Elite Series Plus': 1.5
}

# Simplified tier names for display
TIER_DISPLAY_NAMES = {
    'DGPT - Elite Series': 'Elite',
    'DGPT - Elite Series Plus' : 'Elite',
    'Major': 'Major',
}


class PDGAScraper:
    """Scraper for PDGA tournament data"""
    
    def __init__(self):
        self.base_url = "https://www.pdga.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Load tournament schedule
        if SCHEDULE_AVAILABLE:
            self.schedule = TournamentSchedule()
        else:
            self.schedule = None
    
    def search_pdga_tournament(self, tournament_name: str) -> Optional[str]:
        """
        Search PDGA for a tournament by name and return its event ID
        
        Args:
            tournament_name: Name of the tournament to search for
            
        Returns:
            PDGA event ID if found, None otherwise
        """
        try:
            # Try PDGA tour search
            search_url = f"{self.base_url}/tour/search"
            
            # Search with tournament name
            params = {
                'title': tournament_name,
                'OfficialName': tournament_name,
            }
            
            print(f"      Searching PDGA for: {tournament_name}")
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for event links - /tour/event/{event_id}
            event_links = soup.find_all('a', href=re.compile(r'/tour/event/\d+'))
            
            if event_links:
                # Extract event ID from first matching link
                href = event_links[0]['href']
                event_id = re.search(r'/tour/event/(\d+)', href)
                if event_id:
                    print(f"      ✅ Found PDGA event ID: {event_id.group(1)}")
                    return event_id.group(1)
            
            # Alternative: Try direct search in page content
            event_id_pattern = re.search(r'event[/_](\d{5,})', response.text)
            if event_id_pattern:
                return event_id_pattern.group(1)
            
            print(f"      ⚠️  Could not find PDGA event ID for '{tournament_name}'")
            return None
            
        except Exception as e:
            print(f"      ❌ Error searching for tournament: {e}")
            return None
    
    def get_tournament_results_by_event_id(self, event_id: str, division: str = 'MPO') -> List[Dict]:
        """
        Fetch results for a specific PDGA event ID
        
        Args:
            event_id: PDGA event ID
            division: Division to fetch (default: MPO)
            
        Returns:
            List of player results
        """
        try:
            results_url = f"{self.base_url}/tour/event/{event_id}"
            
            print(f"      Fetching results from: {results_url}")
            response = self.session.get(results_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find MPO division results
            results = []
            
            # Strategy 1: Look for division-specific section
            mpo_section = soup.find('div', {'id': division}) or soup.find('div', class_=re.compile(division, re.I))
            
            # Strategy 2: Look for results table with MPO
            if not mpo_section:
                tables = soup.find_all('table')
                for table in tables:
                    table_text = table.get_text().upper()
                    if 'MPO' in table_text or 'OPEN' in table_text:
                        mpo_section = table
                        break
            
            if not mpo_section:
                print(f"      ⚠️  Could not find {division} results section")
                return []
            
            # Find the results table
            results_table = mpo_section.find('table') if mpo_section.name != 'table' else mpo_section
            
            if not results_table:
                print(f"      ⚠️  Could not find results table")
                return []
            
            # Parse table rows
            rows = results_table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 2:
                        continue
                    
                    # Extract placement
                    place_text = cells[0].get_text().strip()
                    place_match = re.search(r'\d+', place_text)
                    if not place_match:
                        continue
                    placement = int(place_match.group())
                    
                    # Find player link to get PDGA number
                    player_link = row.find('a', href=re.compile(r'/player/\d+'))
                    
                    if player_link:
                        pdga_match = re.search(r'/player/(\d+)', player_link['href'])
                        if pdga_match:
                            pdga_number = int(pdga_match.group(1))
                            player_name = player_link.get_text().strip()
                            
                            results.append({
                                'placement': placement,
                                'pdga_number': pdga_number,
                                'name': player_name,
                                'tied': 'T' in place_text.upper()
                            })
                
                except Exception as e:
                    continue
            
            print(f"      ✅ Found {len(results)} {division} results")
            return results
            
        except Exception as e:
            print(f"      ❌ Error fetching tournament results: {e}")
            return []
    
    def get_recent_mpo_tournaments(self, days_back: int = 14) -> List[Dict]:
        """
        Fetch recent MPO tournaments using the schedule and scrape their results
        
        Args:
            days_back: How many days back to look for tournaments
            
        Returns:
            List of tournament dictionaries with results
        """
        if not self.schedule:
            print("   ⚠️  Tournament schedule not available - place tournaments.txt in root directory")
            return []
        
        tournaments = []
        
        # Get tournaments that ended in the last 'days_back' days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"\n   📅 Looking for tournaments between {start_date.date()} and {end_date.date()}")
        
        recent_tournaments = self.schedule.get_tournaments_in_date_range(start_date, end_date)
        
        if not recent_tournaments:
            print("   No tournaments found in date range")
            return []
        
        print(f"   Found {len(recent_tournaments)} scheduled tournament(s) in range")
        
        for scheduled_tournament in recent_tournaments:
            # Only process tournaments that have finished
            if scheduled_tournament['end_date'] and scheduled_tournament['end_date'] < end_date:
                print(f"\n   🥏 Processing: {scheduled_tournament['name']}")
                print(f"      Tier: {scheduled_tournament['tier']} ({scheduled_tournament['tier_abbr']})")
                print(f"      Dates: {scheduled_tournament['dates_raw']}")
                
                # Search for this tournament on PDGA
                event_id = self.search_pdga_tournament(scheduled_tournament['name'])
                
                if event_id:
                    # Fetch results
                    results = self.get_tournament_results_by_event_id(event_id, 'MPO')
                    
                    if results:
                        tournament = {
                            'id': event_id,
                            'name': scheduled_tournament['name'],
                            'tier': scheduled_tournament['tier'],
                            'tier_abbr': scheduled_tournament['tier_abbr'],
                            'date': scheduled_tournament['end_date'].strftime('%Y-%m-%d'),
                            'dates_raw': scheduled_tournament['dates_raw'],
                            'location': 'USA',
                            'results': results
                        }
                        
                        tournaments.append(tournament)
                        print(f"      ✅ Successfully scraped {len(results)} results")
                    else:
                        print(f"      ⚠️  No results found")
                else:
                    print(f"      ⚠️  Could not find event on PDGA")
                
                # Be nice to PDGA servers - rate limit
                time.sleep(3)
            else:
                print(f"\n   ⏭️  Skipping: {scheduled_tournament['name']} (not finished yet)")
        
        return tournaments
    
    def get_live_tournament_results(self, tournament_name: str) -> Optional[Dict]:
        """
        Fetch live or recent results for a specific tournament
        Useful for manual updates or testing
        
        Args:
            tournament_name: Name of the tournament
            
        Returns:
            Tournament dictionary with results
        """
        print(f"\n🔍 Searching for: {tournament_name}")
        
        # Get tournament info from schedule
        tournament_info = None
        if self.schedule:
            tournament_info = self.schedule.find_tournament_by_name(tournament_name)
        
        # Search PDGA for the event
        event_id = self.search_pdga_tournament(tournament_name)
        
        if not event_id:
            return None
        
        # Fetch results
        results = self.get_tournament_results_by_event_id(event_id, 'MPO')
        
        if not results:
            return None
        
        # Build tournament object
        tournament = {
            'id': event_id,
            'name': tournament_name,
            'tier': tournament_info['tier'] if tournament_info else 'A-Tier',
            'tier_abbr': tournament_info['tier_abbr'] if tournament_info else 'A',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'location': 'USA',
            'results': results
        }
        
        return tournament
    
    def calculate_placement_score(self, placement: int) -> float:
        """
        Calculate points based on tournament placement
        Lower placement = lower score (better)
        
        Args:
            placement: Player's finishing position
            
        Returns:
            Points for that placement
        """
        return float(placement)


class FantasyLeagueUpdater:
    """Updates fantasy league standings based on tournament results"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.scraper = PDGAScraper()
        self.rosters = self.load_rosters()
        self.standings = self.load_standings()
        self.tournaments = self.load_tournaments()
        self.player_stats = self.load_player_stats()
    
    def load_rosters(self) -> Dict:
        """Load team rosters from JSON"""
        with open(f"{self.data_dir}/rosters.json", 'r') as f:
            return json.load(f)
    
    def load_standings(self) -> Dict:
        """Load current standings from JSON"""
        with open(f"{self.data_dir}/standings.json", 'r') as f:
            return json.load(f)
    
    def load_tournaments(self) -> Dict:
        """Load tournament history from JSON"""
        with open(f"{self.data_dir}/recent_tournaments.json", 'r') as f:
            return json.load(f)
    
    def load_player_stats(self) -> Dict:
        """Load player statistics from JSON"""
        with open(f"{self.data_dir}/player_stats.json", 'r') as f:
            return json.load(f)
    
    def save_all_data(self):
        """Save all updated data to JSON files"""
        with open(f"{self.data_dir}/standings.json", 'w') as f:
            json.dump(self.standings, f, indent=2)
        
        with open(f"{self.data_dir}/rosters.json", 'w') as f:
            json.dump(self.rosters, f, indent=2)
        
        with open(f"{self.data_dir}/recent_tournaments.json", 'w') as f:
            json.dump(self.tournaments, f, indent=2)
        
        with open(f"{self.data_dir}/player_stats.json", 'w') as f:
            json.dump(self.player_stats, f, indent=2)
    
    def update_from_weekly_tournaments(self, tournaments: List[Dict]):
        """
        Update standings based on a week's worth of tournaments
        Only counts the best 3 players from each team for the week
        
        Args:
            tournaments: List of tournament dictionaries for the week
        """
        if not tournaments:
            return
        
        week_number = self.standings['current_week'] + 1
        self.standings['current_week'] = week_number
        
        print(f"\n📊 Updating fantasy scores for Week {week_number}")
        
        # Track this week's scores for each team
        for team in self.rosters['teams']:
            weekly_player_scores = []
            
            print(f"\n   Team: {team['team_name']}")
            
            # Calculate scores for each player across all tournaments this week
            for player in team['players']:
                week_score = 0.0
                tournaments_played_this_week = 0
                
                # Check all tournaments from this week
                for tournament in tournaments:
                    player_result = self.find_player_result(
                        tournament['results'], 
                        player['pdga_number']
                    )
                    
                    if player_result:
                        tier_multiplier = TIER_MULTIPLIERS.get(tournament.get('tier', 'B-Tier'), 1.0)
                        placement = player_result['placement']
                        base_score = self.scraper.calculate_placement_score(placement)
                        
                        # Apply tier multiplier
                        score = base_score * tier_multiplier
                        
                        # Double points for underdog (7th pick)
                        if player.get('is_underdog', False):
                            score *= 0.5
                        
                        week_score += score
                        tournaments_played_this_week += 1
                        
                        print(f"      {player['name']}: {placement}{self.ordinal_suffix(placement)} at {tournament['name']} = {score:.1f} pts")
                        
                        # Track individual tournament for this player
                        player.setdefault('weekly_scores', []).append({
                            'week': week_number,
                            'tournament': tournament['name'],
                            'placement': placement,
                            'score': score,
                            'tier': TIER_DISPLAY_NAMES.get(tournament['tier'], 'B-Tier'),
                            'counted': False  # Will be updated if in top 3
                        })
                
                # Update player's running totals
                if tournaments_played_this_week > 0:
                    player['tournaments_played'] = player.get('tournaments_played', 0) + tournaments_played_this_week
                
                # Track this player's weekly score for top-3 selection
                weekly_player_scores.append({
                    'player': player,
                    'week_score': week_score,
                    'tournaments_played': tournaments_played_this_week
                })
            
            # Sort players by weekly score and take best 3 (lowest scores)
            weekly_player_scores.sort(key=lambda x: x['week_score'] if x['tournaments_played'] > 0 else float('inf'))
            top_3_players = [p for p in weekly_player_scores if p['tournaments_played'] > 0][:3]
            
            # Calculate team's week score from top 3 players
            team_week_score = sum(p['week_score'] for p in top_3_players)
            
            print(f"      Top 3 this week:")
            for i, player_data in enumerate(top_3_players, 1):
                print(f"         {i}. {player_data['player']['name']}: {player_data['week_score']:.1f} pts")
            print(f"      Team week total: {team_week_score:.1f} pts")
            
            # Update which players were counted this week
            for player_data in top_3_players:
                player = player_data['player']
                player['season_total'] = player.get('season_total', 0.0) + player_data['week_score']
                player['times_counted'] = player.get('times_counted', 0) + 1
                
                # Mark their weekly scores as counted
                for score_entry in player.get('weekly_scores', []):
                    if score_entry['week'] == week_number:
                        score_entry['counted'] = True
            
            # Record weekly breakdown for this team
            team_standings = next((s for s in self.standings['standings'] if s['team_name'] == team['team_name']), None)
            if team_standings:
                team_standings.setdefault('weekly_breakdown', []).append({
                    'week': week_number,
                    'score': team_week_score,
                    'top_3_players': [
                        {
                            'name': p['player']['name'],
                            'score': p['week_score'],
                            'tournaments': p['tournaments_played']
                        } for p in top_3_players
                    ]
                })
        
        # Update player stats for leaderboard
        self.update_player_stats()
        
        # Recalculate team standings
        self.recalculate_standings()
        
        # Add tournaments to history
        for tournament in tournaments:
            self.add_tournament_to_history(tournament)
    
    def update_player_stats(self):
        """Update the player statistics leaderboard"""
        all_players = []
        
        for team in self.rosters['teams']:
            for player in team['players']:
                all_players.append({
                    'name': player['name'],
                    'pdga_number': player['pdga_number'],
                    'team': team['team_name'],
                    'owner': team['owner'],
                    'is_underdog': player.get('is_underdog', False),
                    'season_total': player.get('season_total', 0.0),
                    'tournaments_played': player.get('tournaments_played', 0),
                    'times_counted': player.get('times_counted', 0),
                    'average_when_counted': (
                        player.get('season_total', 0.0) / player.get('times_counted', 1)
                        if player.get('times_counted', 0) > 0 else 0.0
                    )
                })
        
        # Sort by season total (lower is better)
        all_players.sort(key=lambda x: x['season_total'] if x['season_total'] > 0 else float('inf'))
        
        self.player_stats['player_stats'] = all_players
        self.player_stats['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    
    def find_player_result(self, results: List[Dict], pdga_number: int) -> Optional[Dict]:
        """Find a player's result in tournament results"""
        for result in results:
            if result.get('pdga_number') == pdga_number:
                return result
        return None
    
    def recalculate_standings(self):
        """Recalculate team standings based on weekly top-3 scores"""
        for team_standing in self.standings['standings']:
            # Sum all weekly scores
            total_score = sum(week['score'] for week in team_standing.get('weekly_breakdown', []))
            team_standing['total_score'] = total_score
            team_standing['weeks_counted'] = len(team_standing.get('weekly_breakdown', []))
        
        # Sort by total score (lower is better)
        self.standings['standings'].sort(key=lambda x: x['total_score'])
        
        self.standings['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    
    def add_tournament_to_history(self, tournament: Dict):
        """Add tournament to recent tournaments list"""
        # Keep only last 10 tournaments
        if len(self.tournaments['tournaments']) >= 10:
            self.tournaments['tournaments'] = self.tournaments['tournaments'][-9:]
        
        # Extract fantasy-relevant results
        fantasy_results = []
        for team in self.rosters['teams']:
            for player in team['players']:
                result = self.find_player_result(tournament['results'], player['pdga_number'])
                if result:
                    fantasy_results.append({
                        'player': player['name'],
                        'finish': f"{result['placement']}{self.ordinal_suffix(result['placement'])} place",
                        'points': 0  # Will be calculated based on tier
                    })
        
        tournament_entry = {
            'name': tournament['name'],
            'date': tournament['date'],
            'location': tournament.get('location', 'USA'),
            'tier': TIER_DISPLAY_NAMES.get(tournament['tier'], 'B-Tier'),
            'fantasy_results': fantasy_results
        }
        
        self.tournaments['tournaments'].append(tournament_entry)
    
    @staticmethod
    def ordinal_suffix(n: int) -> str:
        """Get ordinal suffix for a number (st, nd, rd, th)"""
        if 11 <= n <= 13:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    
    def run_update(self):
        """Main update function - fetches new tournaments and updates standings"""
        print("=" * 80)
        print("🥏 Starting Fantasy Disc Golf League Update")
        print("=" * 80)
        print(f"   Checking for tournaments from the past 14 days...")
        
        # Fetch recent tournaments
        recent_tournaments = self.scraper.get_recent_mpo_tournaments(days_back=365)
        
        if not recent_tournaments:
            print("\n   ℹ️  No new tournaments found.")
            print("   This is normal if:")
            print("      • No tournaments finished in the past 14 days")
            print("      • PDGA website structure has changed (update selectors)")
            print("      • Network issues prevented scraping")
        else:
            print(f"\n   ✅ Found {len(recent_tournaments)} tournament(s) with results")
            
            # Process all tournaments from this week as a batch
            self.update_from_weekly_tournaments(recent_tournaments)
        
        # Save updated data
        self.save_all_data()
        
        print("\n" + "=" * 80)
        print("✅ Update Complete!")
        print("=" * 80)
        print(f"   Current Season Week: {self.standings['current_week']}")
        
        # Print standings summary
        print("\n📊 Current Standings:")
        for i, team in enumerate(self.standings['standings'][:5], 1):
            print(f"   {i}. {team['team_name']}: {team['total_score']:.1f} pts ({team['weeks_counted']} weeks)")
        
        print("\n" + "=" * 80)


def main():
    """Main entry point"""
    updater = FantasyLeagueUpdater()
    updater.run_update()


if __name__ == "__main__":
    main()
