# 🚀 Quick Start Guide

Get your fantasy disc golf league running in 5 steps!

## Step 1: Set Up Repository (5 minutes)

```bash
# Create a new repository on GitHub
# Clone it locally
git clone https://github.com/yourusername/fantasy-disc-golf.git
cd fantasy-disc-golf

# Copy all files from this project into your repository
```

## Step 2: Add Your Teams (10 minutes)

Edit `data/rosters.json`:

```json
{
  "teams": [
    {
      "team_name": "Team Alpha",
      "owner": "Your Name",
      "players": [
        {"name": "Paul McBeth", "pdga_number": 27523, "is_underdog": false, "current_score": 0.0},
        {"name": "Ricky Wysocki", "pdga_number": 38008, "is_underdog": false, "current_score": 0.0},
        {"name": "Eagle McMahon", "pdga_number": 48532, "is_underdog": false, "current_score": 0.0},
        {"name": "Calvin Heimburg", "pdga_number": 36851, "is_underdog": false, "current_score": 0.0},
        {"name": "Gannon Buhr", "pdga_number": 118661, "is_underdog": false, "current_score": 0.0},
        {"name": "Chris Dickerson", "pdga_number": 11963, "is_underdog": false, "current_score": 0.0},
        {"name": "Your Underdog", "pdga_number": 12345, "is_underdog": true, "current_score": 0.0}
      ]
    }
  ]
}
```

**Finding PDGA Numbers:**
1. Go to https://www.pdga.com
2. Search for player name
3. Click on their profile
4. PDGA number is in the URL: `pdga.com/player/27523`

## Step 3: Enable GitHub Pages (2 minutes)

1. Go to repository **Settings**
2. Click **Pages** in sidebar
3. Source: **Deploy from a branch**
4. Branch: **main** / folder: **/ (root)**
5. Click **Save**

Your site will be live at: `https://yourusername.github.io/fantasy-disc-golf/`

## Step 4: Implement PDGA Scraping (30-60 minutes)

### Option A: Quick Test Without Scraping

For testing, manually update `data/standings.json`:

```bash
python3 update_league.py  # Will run but won't fetch real data yet
```

### Option B: Implement Real Scraping

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Study PDGA website structure:**
- Visit https://www.pdga.com/tour/search
- Right-click → Inspect to see HTML structure
- Note the class names and element structure

3. **Update `pdga_scraper_helper.py`:**
- Update CSS selectors for tournament search
- Update selectors for results tables
- Test with recent tournament

4. **Test locally:**
```bash
python3 pdga_scraper_helper.py
```

5. **Integrate with main updater:**
- Copy working scraper code into `update_league.py`
- Test full update process

## Step 5: Commit and Deploy (2 minutes)

```bash
git add .
git commit -m "Initial fantasy disc golf league setup"
git push origin main
```

Visit your site in 1-2 minutes! 🎉

## Manual Updates

Trigger an update manually:
1. Go to **Actions** tab in GitHub
2. Click **Update Fantasy League**
3. Click **Run workflow**

## Automatic Updates

Already configured! Updates run every Monday at 6 AM UTC.

To change schedule, edit `.github/workflows/update-league.yml`:
```yaml
schedule:
  - cron: '0 6 * * 1'  # Change this line
```

## Testing Locally

Before pushing, test everything works:

```bash
# Test Python script
python3 update_league.py

# Serve website locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Troubleshooting

**Site not updating?**
- Check Actions tab for errors
- Make sure changes are committed and pushed
- Clear browser cache

**Python script failing?**
- Check you have Python 3.8+: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`
- Check for error messages in script output

**PDGA scraping not working?**
- PDGA website may have changed structure
- Update selectors in scraper code
- Test with `pdga_scraper_helper.py` first

## Next Steps

1. **Customize Styling:** Edit `styles.css`
2. **Adjust Scoring:** Modify multipliers in `update_league.py`
3. **Add Features:** 
   - Player stats page
   - Historical tournament archive
   - Trade deadline countdown
   - Weekly recap emails

## Need Help?

- Check the main README.md for detailed info
- Open an issue on GitHub
- Review the example data in `data/` folder

---

**Good luck with your fantasy league! 🥏**
