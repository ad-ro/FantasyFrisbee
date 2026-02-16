# 🆔 Event ID Scraping Guide

## What's New

Your scraper now supports **direct event ID scraping** for faster and more reliable results!

## Benefits of Event IDs

✅ **Faster** - No searching required  
✅ **More Reliable** - No name matching issues  
✅ **Exact Results** - Always gets the right tournament  
✅ **No Rate Limiting** - Fewer requests to PDGA  

## tournaments.txt Format

### New Format (with Event IDs):
```
Tournament Name,Tier,Dates,EventID
Supreme Flight Open,ES,February 27 - March 1,88276
Big Easy Open,ES,March 13 - 15,89123
```

### Old Format (still supported):
```
Tournament Name,Tier,Dates,
Supreme Flight Open,ES,February 27 - March 1,
```

**Note:** Event ID is optional but highly recommended!

## Finding Event IDs

### Method 1: From PDGA Website

1. Go to https://www.pdga.com/tour/search
2. Search for your tournament
3. Click on the tournament
4. Look at URL: `https://www.pdga.com/tour/event/88276`
5. Event ID is: `88276`

### Method 2: From Previous Year

If the tournament happened last year:
- 2024 Supreme Flight: Event ID `88276`
- 2025 Supreme Flight: Event ID will be different
- Check PDGA for current year's ID

### Method 3: Let the Scraper Find It

Run without event ID and the scraper will:
1. Search for tournament by name
2. Find the event ID
3. Tell you to add it to tournaments.txt

```
💡 Tip: Add event ID 89123 to tournaments.txt for faster scraping
```

## How to Add Event IDs

### Update tournaments.txt

```bash
# Open file
nano tournaments.txt

# Add event ID after dates (4th field)
# Before:
Supreme Flight Open,ES,February 27 - March 1,

# After:
Supreme Flight Open,ES,February 27 - March 1,88276
```

### Bulk Update

Create a helper script to add IDs:

```python
# add_event_ids.py
schedule = TournamentSchedule()

# Manual mapping
event_ids = {
    'Supreme Flight Open': '88276',
    'Big Easy Open': '89123',
    # Add more...
}

# Would need to rewrite tournaments.txt with IDs
```

## Using Event ID Scraper

### Scrape Single Tournament

```bash
# By event ID
python3 scrape_by_event_id.py 88276

# Output:
================================================================================
SCRAPING SINGLE TOURNAMENT
================================================================================

1. Fetching: https://www.pdga.com/tour/event/88276
   ✅ Response: 200

2. Parsing HTML...
   ✅ Tournament: DGPT - Discraft Supreme Flight Open

3. Finding MPO division...
   ✅ Found: MPO · Mixed Pro Open (108)

4. Finding results table...
   ✅ Found results table

5. Parsing player results...
   Found 108 rows
   ✅ Successfully parsed 108 players

RESULTS SUMMARY
================================================================================
Tournament: DGPT - Discraft Supreme Flight Open
Event ID: 88276
Total Players: 108

TOP 10 FINISHERS:
  1. Ezra Robinson               PDGA #50671
  2. Anthony Barela              PDGA #44382
  3. Paul McBeth                 PDGA #27523
  ...

✅ Results saved to: event_88276_results.json
```

### Scrape All Scheduled Tournaments

```bash
# Scrape all tournaments with event IDs
python3 scrape_by_event_id.py --all

# Interactive mode
python3 scrape_by_event_id.py
```

### Interactive Mode

```bash
python3 scrape_by_event_id.py

PDGA TOURNAMENT SCRAPER
================================================================================

Options:
  1. Scrape by event ID
  2. Scrape all tournaments with IDs from schedule
  3. Show schedule
  4. Exit

Select option (1-4): 1
Enter PDGA event ID: 88276
```

## Testing Event ID Parsing

```bash
# Test with tournament_parser.py
python3 tournament_parser.py

# Output will show:
✅ Loaded 19 tournaments from schedule (1 with event IDs)

# Then test scraping:
🔍 Testing name search:
Found: Supreme Flight Open
  Tier: DGPT - Elite Series
  Event ID: 88276

📥 Testing scraping by event ID...
[scrapes the tournament]

✅ Scraping test successful!
   Tournament: DGPT - Discraft Supreme Flight Open
   Players scraped: 108
```

## Integration with update_league.py

The main scraper now automatically uses event IDs:

```python
# In get_recent_mpo_tournaments():

event_id = scheduled_tournament.get('event_id')

if event_id:
    # Direct scraping (fast & reliable)
    print(f"Using event ID: {event_id}")
    results = self.get_tournament_results_by_event_id(event_id)
else:
    # Fallback to search (slower)
    print(f"No event ID - searching by name...")
    event_id = self.search_pdga_tournament(name)
```

## Example Workflow

### Initial Setup (One Time)

```bash
# 1. Get event IDs for known tournaments
python3 scrape_by_event_id.py --schedule

# 2. Look up each tournament on PDGA
# 3. Add event IDs to tournaments.txt

# tournaments.txt becomes:
Supreme Flight Open,ES,February 27 - March 1,88276
Big Easy Open,ES,March 13 - 15,89123
Queen City Classic,ES,March 27 - 29,89456
```

### Weekly Updates (Automatic)

```bash
# Scraper now uses event IDs automatically
python3 update_league.py

# Output:
🥏 Processing: Supreme Flight Open
   Using event ID: 88276  ← Much faster!
   ✅ Successfully scraped 108 results
```

### Adding New Tournament Event IDs

When a new tournament finishes:

```bash
# 1. Scraper finds it by name (slower)
🥏 Processing: New Tournament
   No event ID - searching by name...
   ✅ Found PDGA event ID: 99999
   💡 Tip: Add event ID 99999 to tournaments.txt

# 2. Add the ID to tournaments.txt
New Tournament,ES,June 1 - 3,99999

# 3. Next time it's instant!
```

## Command Reference

### scrape_by_event_id.py

```bash
# Interactive mode
python3 scrape_by_event_id.py

# Scrape specific event
python3 scrape_by_event_id.py 88276

# Scrape all scheduled events with IDs
python3 scrape_by_event_id.py --all

# Show schedule
python3 scrape_by_event_id.py --schedule

# Help
python3 scrape_by_event_id.py --help
```

### tournament_parser.py

```bash
# Test parsing and event ID scraping
python3 tournament_parser.py
```

### update_league.py

```bash
# Regular fantasy league update (uses event IDs automatically)
python3 update_league.py
```

## Troubleshooting

### "No tournaments with event IDs"

**Solution:** Add event IDs to tournaments.txt

```
Before: Supreme Flight Open,ES,February 27 - March 1,
After:  Supreme Flight Open,ES,February 27 - March 1,88276
```

### Event ID Not Working

**Check:**
1. Event ID is correct (visit URL to verify)
2. Tournament has finished and results are posted
3. Event ID is in tournaments.txt in correct position

### Wrong Tournament Scraped

**Cause:** Incorrect event ID

**Solution:**
1. Verify event ID at https://www.pdga.com/tour/event/XXXXX
2. Make sure it's the correct year
3. Update tournaments.txt

## Performance Comparison

### Without Event IDs:
```
🥏 Processing: Supreme Flight Open
   Searching PDGA for: Supreme Flight Open... (3 seconds)
   ✅ Found PDGA event ID: 88276
   Fetching results... (2 seconds)
Total: ~5 seconds per tournament
```

### With Event IDs:
```
🥏 Processing: Supreme Flight Open
   Using event ID: 88276
   Fetching results... (2 seconds)
Total: ~2 seconds per tournament
```

**60% faster!** ⚡

## Best Practices

1. ✅ **Add event IDs for all tournaments you'll scrape repeatedly**
2. ✅ **Update tournaments.txt at season start with all event IDs**
3. ✅ **Test event IDs with scrape_by_event_id.py before adding**
4. ✅ **Keep a backup of working event IDs**
5. ✅ **Document where you found each event ID**

## FAQ

**Q: Do I need event IDs for all tournaments?**  
A: No, but it makes scraping faster and more reliable.

**Q: Can I mix tournaments with and without event IDs?**  
A: Yes! The scraper will use IDs when available, search by name otherwise.

**Q: What if PDGA changes event IDs?**  
A: Very rare, but if it happens, update tournaments.txt with new ID.

**Q: How do I find event IDs for past tournaments?**  
A: Search PDGA.com, find the tournament page, get ID from URL.

**Q: Can I use event IDs from previous years?**  
A: No, each year's tournament gets a new event ID.

## Summary

Event IDs make scraping:
- ⚡ **60% faster**
- ✅ **More reliable**
- 🎯 **Always accurate**
- 🔧 **Easier to maintain**

Add them to tournaments.txt for best results!

---

**Next Steps:**

1. Run `python3 scrape_by_event_id.py 88276` to test
2. Add event IDs to tournaments.txt
3. Run `python3 update_league.py` to see the speed improvement!
