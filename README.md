# 🥏 Fantasy Disc Golf League

A GitHub Pages website for tracking your fantasy disc golf league with automatic weekly updates from PDGA tournament results.

## 📋 League Rules

- Each player selects 7 professional disc golfers (MPO division only)
- The 7th pick must be ranked outside the top 50 (the "underdog")
- The underdog pick scores **double points**
- **WEEKLY SCORING: Only your best 3 players count each week**
- Scoring: **Placement × Event Tier Multiplier**
  - Elite Series: 3x multiplier
  - Major: 2.5x multiplier
  - A-Tier: 2x multiplier
  - B-Tier: 1x multiplier
- **Lower total score wins** at the end of the season
- Example: 1st place at an Elite event = 1 × 3 = 3 points

### How Weekly Top-3 Works

Each week:
1. All tournament results are collected
2. Every player's score is calculated with tier multipliers
3. For each team, the **3 lowest scores** are selected
4. Those 3 scores are added to the team's season total
5. Individual player stats are tracked (season total, times counted, etc.)

See [WEEKLY_SCORING_GUIDE.md](WEEKLY_SCORING_GUIDE.md) for detailed examples and strategy!

## 🚀 Setup Instructions

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/yourusername/fantasy-disc-golf.git
cd fantasy-disc-golf
```

### 2. Configure Your Tournament Schedule

The `tournaments.txt` file contains your season schedule. It's already populated with the 2025 DGPT schedule, but you can customize it:

```
Tournament Name,Tier Code,Dates,
```

**Tier Codes:** ES (Elite), M (Major), A (A-Tier), B (B-Tier)

**The scraper will automatically:**
- Check this schedule every week
- Search PDGA.com for finished tournaments
- Scrape results and update scores

See [AUTOMATED_SCRAPING.md](AUTOMATED_SCRAPING.md) for details!

### 3. Configure Your League Rosters

Edit `data/rosters.json` to add your teams and players:

```json
{
  "teams": [
    {
      "team_name": "Your Team Name",
      "owner": "Your Name",
      "players": [
        {
          "name": "Paul McBeth",
          "pdga_number": 27523,
          "is_underdog": false,
          "current_score": 0.0
        },
        // ... 6 more players
        {
          "name": "Your Underdog Pick",
          "pdga_number": 12345,
          "is_underdog": true,
          "current_score": 0.0
        }
      ]
    }
  ]
}
```

**Important:** The 7th player in each team's roster should have `"is_underdog": true`.

### 3. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** (under "Code and automation")
3. Under "Source", select **Deploy from a branch**
4. Choose **main** branch and **/ (root)** folder
5. Click **Save**

Your site will be available at: `https://yourusername.github.io/fantasy-disc-golf/`

### 4. Test the Automated Scraper

**Good news: The scraper is already fully implemented!** 🎉

It automatically:
1. Reads your `tournaments.txt` schedule
2. Searches PDGA.com for tournaments that finished recently
3. Scrapes MPO division results
4. Calculates fantasy scores with tier multipliers
5. Selects weekly top-3 players per team
6. Updates all data files

**Test it locally:**
```bash
pip3 install -r requirements.txt
python3 update_league.py
```

**What you'll see:**
```
🥏 Starting Fantasy Disc Golf League Update
📅 Looking for tournaments...
🥏 Processing: Big Easy Open
   ✅ Found PDGA event ID: 98765
   ✅ Found 156 MPO results
📊 Updating fantasy scores for Week 1
   Team: Team Alpha
      Paul McBeth: 1st = 3.0 pts
      ...
✅ Update Complete!
```

**Troubleshooting:**
- If no tournaments found, check dates in `tournaments.txt`
- If scraping fails, PDGA website structure may have changed
- See [AUTOMATED_SCRAPING.md](AUTOMATED_SCRAPING.md) for details

### 5. Configure Automatic Updates

The GitHub Action (`.github/workflows/update-league.yml`) is set to run:
- **Every Monday at 6 AM UTC**
- Can also be triggered manually from the Actions tab

To change the schedule, edit the cron expression:
```yaml
schedule:
  - cron: '0 6 * * 1'  # Minute Hour Day Month Weekday
```

Example schedules:
- `'0 6 * * 1'` - Every Monday at 6 AM UTC
- `'0 6 * * 1,4'` - Monday and Thursday at 6 AM UTC
- `'0 6 * * *'` - Every day at 6 AM UTC

## 📁 Project Structure

```
fantasy-disc-golf/
├── index.html              # Main website page
├── styles.css              # Styling
├── app.js                  # Frontend JavaScript
├── update_league.py        # Python scraper and updater
├── data/
│   ├── rosters.json        # Team rosters and player stats
│   ├── standings.json      # Current standings with weekly breakdown
│   ├── player_stats.json   # Individual player leaderboard
│   └── recent_tournaments.json  # Recent tournament results
└── .github/
    └── workflows/
        └── update-league.yml  # GitHub Actions automation
```

## 🔧 Customization

### Modify Scoring System

Edit the multipliers in `update_league.py`:

```python
TIER_MULTIPLIERS = {
    'DGPT - Elite Series': 3.0,
    'Major': 2.5,
    'DGPT - Silver Series': 2.0,
    'A-Tier': 2.0,
    'B-Tier': 1.0,
}
```

### Change Website Styling

Edit `styles.css` to customize colors, fonts, and layout:

```css
:root {
    --primary-color: #2c5f8d;    /* Main theme color */
    --secondary-color: #4a9eff;  /* Accent color */
    --accent-color: #ff6b35;     /* Highlight color */
}
```

### Add More Teams

Simply add more team objects to `data/rosters.json`.

## 🐛 Troubleshooting

### Data Not Updating

1. Check the Actions tab for workflow run status
2. Look for error messages in the workflow logs
3. Verify PDGA scraping is working: `python3 update_league.py`

### GitHub Pages Not Showing Updates

1. Make sure you've committed and pushed changes
2. Check that GitHub Pages is enabled in repository settings
3. Clear browser cache and hard refresh (Ctrl+Shift+R)

### PDGA Website Changes

If the PDGA website structure changes, you'll need to update the scraper:
1. Inspect the current PDGA tournament pages
2. Update the scraping logic in `update_league.py`
3. Test thoroughly before deploying

## 📝 Manual Updates

To manually trigger an update:
1. Go to the **Actions** tab in your repository
2. Select **Update Fantasy League** workflow
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

## 🤝 Contributing

Feel free to submit issues or pull requests for:
- Bug fixes
- Feature improvements
- Better PDGA scraping methods
- UI/UX enhancements

## 📄 License

MIT License - feel free to use and modify for your own leagues!

## 🔗 Useful Links

- [PDGA Official Site](https://www.pdga.com)
- [PDGA Tour Events](https://www.pdga.com/tour/search)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Happy disc golfing! 🥏**
