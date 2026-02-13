# 🤖 Automated Tournament Scraping Guide

## How It Works

Your fantasy league now automatically scrapes tournament results from PDGA.com using your `tournaments.txt` schedule file!

## The System

### 1. Tournament Schedule (`tournaments.txt`)
This file contains your season's tournament schedule:
```
Supreme Flight Open,ES,February 27 - March 1,
Big Easy Open,ES,March 13 - 15,
...
```

**Format:** `Tournament Name, Tier Code, Dates,`

**Tier Codes:**
- `ES` = Elite Series (1x multiplier)
- `ESP` or `ESp` = Elite Series Plus (1.5x multiplier)
- `M` = Major (2x multiplier)

### 2. Tournament Parser (`tournament_parser.py`)
Reads `tournaments.txt` and provides:
- Tournament name and dates
- Tier multipliers
- Date range searching
- Tournament lookup by name

### 3. Web Scraper (`update_league.py`)
**Every week (or when you run it), the scraper:**

1. **Loads the schedule** from `tournaments.txt`
2. **Finds recent tournaments** (past 14 days)
3. **For each tournament:**
   - Searches PDGA.com for the event
   - Finds the PDGA event ID
   - Scrapes the MPO division results
   - Extracts player placements and PDGA numbers
4. **Processes fantasy scores:**
   - Calculates points (placement × tier × underdog bonus)
   - Selects best 3 players per team
   - Updates standings and player stats
5. **Saves all data** to JSON files

## Automatic Weekly Updates

### GitHub Actions Workflow
The `.github/workflows/update-league.yml` file runs automatically:

```yaml
schedule:
  - cron: '0 6 * * 1'  # Every Monday at 6 AM UTC
```

**What happens:**
1. Monday morning, GitHub Actions triggers
2. Runs `python update_league.py`
3. Scraper checks tournaments from past 14 days
4. Finds finished tournaments from your schedule
5. Scrapes PDGA for results
6. Updates all JSON files
7. Commits changes to repository
8. GitHub Pages deploys updated website

## How Tournament Matching Works

### Step-by-Step Process

**1. Date Range Check**
```python
# Looks for tournaments that ended in past 14 days
end_date = today
start_date = today - 14 days

# From tournaments.txt: "Big Easy Open,ES,March 13 - 15,"
# If today is March 16-29, this tournament is in range!
```

**2. PDGA Search**
```python
# Searches PDGA.com for "Big Easy Open"
# Looks for event page: /tour/event/12345
# Extracts event ID: 12345
```

**3. Results Scraping**
```python
# Fetches: https://www.pdga.com/tour/event/12345
# Finds MPO division results table
# Parses each row:
#   - Placement (1st, 2nd, T3, etc.)
#   - Player name
#   - PDGA number
```

**4. Fantasy Scoring**
```python
# For each team:
#   For each player on roster:
#     If player in results:
#       score = placement × tier_multiplier
#       if underdog: score × 2
#   
#   Select 3 best scores
#   Add to team total
```

## Testing Locally

### Test the Tournament Parser
```bash
python3 tournament_parser.py
```

**Output:**
```
✅ Loaded 19 tournaments from schedule

================================================================================
2025 DGPT Tournament Schedule
================================================================================

 1. Supreme Flight Open
    🔴 Elite
    February 27 - March 1
    Start: 2025-02-27
...
```

### Test Web Scraping
```bash
# Install dependencies first
pip install -r requirements.txt

# Run the full update
python3 update_league.py
```

**Output:**
```
================================================================================
🥏 Starting Fantasy Disc Golf League Update
================================================================================
   Checking for tournaments from the past 14 days...

   📅 Looking for tournaments between 2025-03-01 and 2025-03-15
   Found 2 scheduled tournament(s) in range

   🥏 Processing: Big Easy Open
      Tier: DGPT - Elite Series (ES)
      Dates: March 13 - 15
      Searching PDGA for: Big Easy Open
      ✅ Found PDGA event ID: 98765
      Fetching results from: https://www.pdga.com/tour/event/98765
      ✅ Found 156 MPO results

📊 Updating fantasy scores for Week 1

   Team: Team Alpha
      Paul McBeth: 1st at Big Easy Open = 3.0 pts
      Eagle McMahon: 5th at Big Easy Open = 15.0 pts
      ...
      Top 3 this week:
         1. Paul McBeth: 3.0 pts
         2. Ricky Wysocki: 6.0 pts
         3. Eagle McMahon: 15.0 pts
      Team week total: 24.0 pts

================================================================================
✅ Update Complete!
================================================================================
   Current Season Week: 1

📊 Current Standings:
   1. Team Alpha: 24.0 pts (1 weeks)
   2. Team Beta: 31.5 pts (1 weeks)
```

## Customizing the Scraper

### Change Lookback Period
Edit `update_league.py`, line in `run_update()`:
```python
recent_tournaments = self.scraper.get_recent_mpo_tournaments(days_back=14)
# Change 14 to any number of days
```

### Add More Divisions
Currently only MPO is scraped. To add FPO:

1. Modify `get_tournament_results_by_event_id()`:
```python
def get_tournament_results_by_event_id(self, event_id: str, division: str = 'MPO')
# Change division parameter in function calls
```

2. Update scraping logic to handle multiple divisions

### Rate Limiting
The scraper includes delays to be respectful to PDGA:
```python
time.sleep(3)  # Wait 3 seconds between tournaments
```

Adjust this if you get rate-limited or want faster scraping.

## Troubleshooting

### "No tournaments found in date range"
- Check your tournaments.txt dates
- Make sure you're in the right date range
- Verify tournament has ended (past the end date)

### "Could not find PDGA event ID"
- Tournament name might not match PDGA exactly
- Try manual search on PDGA.com to find the event
- Update tournament name in tournaments.txt to match PDGA

### "Could not find MPO results section"
PDGA website structure may have changed:
1. Visit the tournament page manually
2. Inspect the HTML structure
3. Update CSS selectors in `get_tournament_results_by_event_id()`

### "No results found"
- Tournament might not have posted final results yet
- PDGA might be updating their page
- Try again in a few hours or next day

### Rate Limiting / Blocked
If you get HTTP 429 or 403 errors:
- Increase sleep time between requests
- Run less frequently
- Consider using PDGA API if available

## Manual Testing a Specific Tournament

Want to test scraping for a specific event?

```bash
python3
```

```python
from update_league import PDGAScraper

scraper = PDGAScraper()

# Test searching for a tournament
event_id = scraper.search_pdga_tournament("Big Easy Open")
print(f"Event ID: {event_id}")

# Test getting results
if event_id:
    results = scraper.get_tournament_results_by_event_id(event_id)
    print(f"Found {len(results)} results")
    
    # Show first 5
    for result in results[:5]:
        print(f"{result['placement']}. {result['name']} (#{result['pdga_number']})")
```

## Advanced: Live Scoring

Want to update scores during a tournament (live results)?

```python
from update_league import PDGAScraper

scraper = PDGAScraper()

# Fetch current standings
tournament = scraper.get_live_tournament_results("Jonesboro Open")

if tournament:
    print(f"Live results for {tournament['name']}")
    for result in tournament['results'][:10]:
        print(f"{result['placement']}. {result['name']}")
```

Run this script during a tournament to see current standings!

## Data Flow Diagram

```
tournaments.txt
      ↓
tournament_parser.py (reads schedule)
      ↓
update_league.py (main script)
      ↓
1. Find tournaments in date range
      ↓
2. Search PDGA.com for each tournament
      ↓
3. Scrape MPO results
      ↓
4. Calculate fantasy points
      ↓
5. Select top 3 per team
      ↓
6. Update JSON files
      ↓
data/*.json (rosters, standings, player_stats)
      ↓
GitHub commit & push
      ↓
GitHub Pages deploys
      ↓
Website updates!
```

## Monitoring

### Check Update Status
Go to your GitHub repository → **Actions** tab

You'll see:
- ✅ Green check = Update succeeded
- ❌ Red X = Update failed
- 🟡 Yellow dot = Update running

Click on any run to see detailed logs.

### Enable Email Notifications
GitHub Settings → Notifications → Actions
- Choose "Send notifications for failed workflows only"
- Get emailed if scraping breaks

## Best Practices

1. **Test locally first** before pushing changes
2. **Check logs** in GitHub Actions after each run
3. **Monitor PDGA website** for structure changes
4. **Update selectors** if scraping breaks
5. **Be respectful** with rate limiting
6. **Keep tournaments.txt updated** with correct names

## Future Enhancements

Ideas for improvement:
- Cache PDGA event IDs to reduce searches
- Add retry logic for failed scrapes
- Implement PDGA API if they release one
- Support multiple divisions (FPO, MP40, etc.)
- Add email notifications for updates
- Create a backup manual entry system
- Add tournament preview feature

---

**Your league is now fully automated! 🎉**
