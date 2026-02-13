# 🎯 Tournament Integration Summary

## What Was Added

Your fantasy disc golf league now has **fully automated tournament scraping** integrated with your `tournaments.txt` schedule file!

## Key Components

### 1. Tournament Schedule (`tournaments.txt`)
```
Supreme Flight Open,ES,February 27 - March 1,
Big Easy Open,ES,March 13 - 15,
Queen City Classic,ES,March 27 - 29,
...
```

✅ Already contains your full 2025 DGPT schedule
✅ Includes tier codes for proper multipliers
✅ Parser reads dates and tournament info

### 2. Tournament Parser (`tournament_parser.py`)
**NEW FILE** - Handles schedule management:
- Parses `tournaments.txt` format
- Converts tier codes (ES, M, A, B) to multipliers
- Finds tournaments by name or date range
- Provides tournament info to scraper

**Test it:**
```bash
python3 tournament_parser.py
```

### 3. Enhanced Scraper (`update_league.py`)
**COMPLETELY REWRITTEN** with:
- ✅ Full PDGA.com web scraping
- ✅ Tournament search by name
- ✅ MPO results extraction
- ✅ Player PDGA number matching
- ✅ Weekly top-3 scoring
- ✅ Comprehensive error handling
- ✅ Rate limiting (respects PDGA servers)

### 4. Documentation
- **AUTOMATED_SCRAPING.md** - Complete scraping guide
- **README.md** - Updated with scraping info
- **QUICK_REFERENCE.md** - Scoring rules
- **WEEKLY_SCORING_GUIDE.md** - Top-3 system details

## How It Works End-to-End

```
1. MONDAY MORNING (GitHub Actions triggers)
   ↓
2. Run: python3 update_league.py
   ↓
3. Load tournaments.txt schedule
   ↓
4. Find tournaments that finished in past 14 days
   Example: "Big Easy Open" finished March 15
   ↓
5. Search PDGA.com for "Big Easy Open"
   ↓
6. Find event page: /tour/event/98765
   ↓
7. Scrape MPO division results table:
   - 1. Paul McBeth (PDGA #27523)
   - 2. Ricky Wysocki (PDGA #38008)
   - 3. Eagle McMahon (PDGA #48532)
   - ... (156 players total)
   ↓
8. Calculate fantasy scores:
   Paul: 1st × 3.0 (Elite) = 3.0 pts
   Ricky: 2nd × 3.0 (Elite) = 6.0 pts
   ↓
9. For each team, select best 3 players
   Team Alpha top 3: Paul (3), Ricky (6), Eagle (15) = 24 pts
   ↓
10. Update all JSON files:
    - standings.json (team totals + weekly breakdown)
    - rosters.json (player stats)
    - player_stats.json (leaderboard)
    - recent_tournaments.json (history)
   ↓
11. Commit changes to GitHub
   ↓
12. GitHub Pages deploys updated website
   ↓
13. Your league members see updated scores! 🎉
```

## What Gets Updated Automatically

### Team Standings
- Weekly top-3 scores added to season total
- Weeks counted tracked
- Average per week calculated

### Player Statistics
- Season total (all top-3 weeks combined)
- Times counted in top-3
- Tournaments played
- Average when counted

### Tournament History
- Recent tournaments with dates and tiers
- Fantasy-relevant finishes
- Player contributions

## Example Run Output

```bash
$ python3 update_league.py

================================================================================
🥏 Starting Fantasy Disc Golf League Update
================================================================================
   Checking for tournaments from the past 14 days...

   📅 Looking for tournaments between 2025-03-01 and 2025-03-15
   Found 2 scheduled tournament(s) in range

   🥏 Processing: Supreme Flight Open
      Tier: DGPT - Elite Series (ES)
      Dates: February 27 - March 1
      Searching PDGA for: Supreme Flight Open
      ✅ Found PDGA event ID: 98764
      Fetching results from: https://www.pdga.com/tour/event/98764
      ✅ Found 144 MPO results
      ✅ Successfully scraped 144 results

   🥏 Processing: Big Easy Open
      Tier: DGPT - Elite Series (ES)
      Dates: March 13 - 15
      Searching PDGA for: Big Easy Open
      ✅ Found PDGA event ID: 98765
      Fetching results from: https://www.pdga.com/tour/event/98765
      ✅ Found 156 MPO results
      ✅ Successfully scraped 156 results

   ✅ Found 2 tournament(s) with results

📊 Updating fantasy scores for Week 1

   Team: Team Alpha
      Paul McBeth: 1st at Supreme Flight Open = 3.0 pts
      Paul McBeth: 2nd at Big Easy Open = 6.0 pts
      Eagle McMahon: 5th at Supreme Flight Open = 15.0 pts
      Eagle McMahon: 3rd at Big Easy Open = 9.0 pts
      Ricky Wysocki: 4th at Big Easy Open = 12.0 pts
      Calvin Heimburg: 8th at Supreme Flight Open = 24.0 pts
      
      Top 3 this week:
         1. Paul McBeth: 9.0 pts
         2. Eagle McMahon: 24.0 pts
         3. Ricky Wysocki: 12.0 pts
      Team week total: 45.0 pts

   Team: Team Beta
      Simon Lizotte: 6th at Supreme Flight Open = 18.0 pts
      Kyle Klein: 3rd at Big Easy Open = 9.0 pts
      Isaac Robinson: 7th at Supreme Flight Open = 21.0 pts
      Anthony Barela: 11th at Big Easy Open = 33.0 pts
      
      Top 3 this week:
         1. Kyle Klein: 9.0 pts
         2. Simon Lizotte: 18.0 pts
         3. Isaac Robinson: 21.0 pts
      Team week total: 48.0 pts

================================================================================
✅ Update Complete!
================================================================================
   Current Season Week: 1

📊 Current Standings:
   1. Team Alpha: 45.0 pts (1 weeks)
   2. Team Beta: 48.0 pts (1 weeks)

================================================================================
```

## Testing the Integration

### 1. Parse Tournament Schedule
```bash
python3 tournament_parser.py
```
Should show all 19 tournaments from your schedule.

### 2. Test Scraping (when tournaments are live)
```bash
python3 update_league.py
```
Will search for and scrape any tournaments that finished in past 14 days.

### 3. Test Manual Tournament Fetch
```python
python3
>>> from update_league import PDGAScraper
>>> scraper = PDGAScraper()
>>> tournament = scraper.get_live_tournament_results("Jonesboro Open")
>>> print(f"Found {len(tournament['results'])} results")
```

## Maintenance & Monitoring

### When PDGA Website Changes
If scraping breaks:
1. Visit tournament page manually
2. Inspect HTML structure (right-click → Inspect)
3. Update CSS selectors in `update_league.py`:
   - `get_tournament_results_by_event_id()` function
   - Look for table parsing logic
4. Test with `python3 update_league.py`

### Check GitHub Actions
- Go to repository → Actions tab
- See run history and logs
- Green check = success, Red X = failure

### Update Tournament Schedule
When new tournaments are announced:
1. Add to `tournaments.txt`
2. Format: `Name,Tier,Dates,`
3. Commit and push
4. Scraper will automatically include them

## Customization Options

### Change Update Frequency
Edit `.github/workflows/update-league.yml`:
```yaml
schedule:
  - cron: '0 6 * * 1'     # Monday 6 AM
  - cron: '0 6 * * 4'     # Add Thursday 6 AM
```

### Adjust Lookback Period
Edit `update_league.py`:
```python
recent_tournaments = self.scraper.get_recent_mpo_tournaments(days_back=14)
# Change to 7, 21, 30, etc.
```

### Modify Rate Limiting
Edit `update_league.py`:
```python
time.sleep(3)  # Seconds between requests
# Increase if getting rate-limited
```

## Success Indicators

✅ **Everything Working If:**
- `python3 tournament_parser.py` shows your schedule
- `python3 update_league.py` finds and scrapes tournaments
- JSON files update with new data
- GitHub Actions runs successfully weekly
- Website shows updated scores

## Next Steps

1. ✅ Test locally: `python3 update_league.py`
2. ✅ Verify JSON files updated
3. ✅ Push to GitHub
4. ✅ Check GitHub Actions runs
5. ✅ Wait for Monday's automatic update
6. ✅ Monitor for first few weeks
7. ✅ Adjust selectors if PDGA changes

## Support Resources

- **AUTOMATED_SCRAPING.md** - Detailed scraping guide
- **README.md** - Full setup instructions
- **WEEKLY_SCORING_GUIDE.md** - Scoring system explained
- **QUICK_REFERENCE.md** - Rules cheat sheet

## Technical Details

**Dependencies:**
- `requests` - HTTP requests to PDGA
- `beautifulsoup4` - HTML parsing
- `lxml` - XML parsing (used by BS4)

**Data Flow:**
```
tournaments.txt → tournament_parser.py → update_league.py
                                              ↓
                                         PDGA.com
                                              ↓
                                    MPO Results Scraping
                                              ↓
                                    Fantasy Score Calc
                                              ↓
                                    data/*.json files
                                              ↓
                                       GitHub Pages
                                              ↓
                                      Your Website!
```

---

**Your fantasy league is now fully automated and integrated! 🎉🥏**

Every Monday, it will:
- Check your tournament schedule
- Scrape PDGA for finished tournaments
- Calculate fantasy scores
- Update all stats
- Deploy updated website

No manual work needed!
