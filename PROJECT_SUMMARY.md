# Fantasy Disc Golf League - Project Summary

## 🎯 What You've Got

A complete GitHub Pages website system for running your fantasy disc golf league with automatic updates!

## 📦 Package Contents

### Website Files
- **index.html** - Main league website with standings, rosters, and recent results
- **styles.css** - Professional styling with responsive design
- **app.js** - Frontend logic for loading and displaying data

### Data Files (in `data/` folder)
- **rosters.json** - Team rosters with PDGA player numbers
- **standings.json** - Current league standings
- **recent_tournaments.json** - Tournament history and results

### Python Scripts
- **update_league.py** - Main updater that calculates scores and updates standings
- **pdga_scraper_helper.py** - Example PDGA scraper implementation
- **requirements.txt** - Python dependencies

### Automation
- **.github/workflows/update-league.yml** - GitHub Actions for weekly auto-updates

### Documentation
- **README.md** - Comprehensive documentation
- **QUICKSTART.md** - Step-by-step setup guide
- **.gitignore** - Git ignore patterns

## 🏆 League Scoring System

**How It Works:**
1. Each player picks 7 MPO disc golfers
2. 7th pick must be outside top 50 (scores 2x points)
3. **Only best 3 players count each week** (this is KEY!)
4. Points = Placement × Tier Multiplier
5. **Lower score wins!**

**Tier Multipliers:**
- Elite Series: 3x
- Major: 2.5x
- A-Tier: 2x
- B-Tier: 1x

**Example Week:**
Your roster has 7 players, but only your 3 best performers count:
- Player A: 2nd at Elite = 2 × 3 = 6 pts ✅ (counted)
- Player B: 5th at A-Tier = 5 × 2 = 10 pts
- Player C: 1st at Major = 1 × 2.5 = 2.5 pts ✅ (counted)
- Player D: Did not play = 0 pts ✅ (counted - best score!)
- Player E: 8th at B-Tier = 8 × 1 = 8 pts
- Player F: 12th at A-Tier = 12 × 2 = 24 pts
- Player G (underdog): 10th at Elite = 10 × 3 × 2 = 60 pts

**Your weekly score: 0 + 2.5 + 6 = 8.5 points**

The other 4 players' scores don't count this week, but are still tracked in their individual stats!

### Why Weekly Top-3?

- **Rewards roster depth**: Not just about having the best single player
- **Strategic diversity**: Do you build 3 stars + 4 depth, or 7 solid performers?
- **Consistency matters**: Players who regularly make top-3 are valuable
- **Injury protection**: Off weeks or injuries don't kill your team
- **Underdog strategy**: The 2x multiplier can make your 7th pick a top-3 performer

## ⚙️ How Automatic Updates Work

1. **GitHub Actions** runs every Monday at 6 AM UTC
2. Runs `update_league.py` to fetch recent tournaments
3. Calculates fantasy points for all players with tier multipliers
4. For each team, selects the **best 3 players** for the week
5. Updates team standings (adds weekly top-3 score to season total)
6. Updates individual player statistics (season totals, times counted, etc.)
7. Updates JSON data files with weekly breakdown
8. Commits changes back to repository
9. GitHub Pages automatically deploys updates

**Key Files Updated:**
- `standings.json` - Team totals and weekly breakdown
- `rosters.json` - Player stats (season totals, times counted)
- `player_stats.json` - Leaderboard of all players
- `recent_tournaments.json` - Tournament history

## 🚀 Setup Steps

### 1. Create GitHub Repository
```bash
# Create new repo on GitHub
# Clone locally and add these files
git add .
git commit -m "Initial setup"
git push
```

### 2. Configure Teams
Edit `data/rosters.json` with your teams and players.

Find PDGA numbers at: https://www.pdga.com
(Number is in player profile URL)

### 3. Enable GitHub Pages
Settings → Pages → Deploy from main branch

### 4. Implement PDGA Scraping
The scraper needs to be customized for current PDGA website structure:

**Key Functions to Implement in `update_league.py`:**

```python
def get_recent_mpo_tournaments(self, days_back=14):
    # Scrape or fetch PDGA tournaments from last 14 days
    # Return list of tournament dicts with:
    # - name, date, location, tier
    # - results (list of player placements)
    pass

def get_player_tournament_results(self, pdga_number, tournament_id):
    # Get specific player's result from tournament
    # Return placement and score
    pass
```

**Resources:**
- Start with `pdga_scraper_helper.py` example
- Inspect https://www.pdga.com HTML structure
- Consider using PDGA API if available

### 5. Test Locally
```bash
python3 -m pip install -r requirements.txt
python3 update_league.py
python3 -m http.server 8000
# Visit http://localhost:8000
```

### 6. Deploy
Push to GitHub and visit your site!

## 🔧 Customization Options

### Change Update Frequency
Edit `.github/workflows/update-league.yml`:
```yaml
schedule:
  - cron: '0 6 * * 1'  # Monday 6 AM
  - cron: '0 6 * * 4'  # Thursday 6 AM (add this line)
```

### Modify Scoring Multipliers
Edit `update_league.py`:
```python
TIER_MULTIPLIERS = {
    'DGPT - Elite Series': 3.0,  # Change these values
    'Major': 2.5,
    'A-Tier': 2.0,
}
```

### Customize Appearance
Edit `styles.css` variables:
```css
:root {
    --primary-color: #2c5f8d;    /* Main color */
    --secondary-color: #4a9eff;  /* Accent */
    --accent-color: #ff6b35;     /* Highlights */
}
```

## 📊 Data Flow

```
PDGA Website
    ↓
update_league.py (scraper)
    ↓
data/*.json files
    ↓
GitHub Actions (commit & push)
    ↓
GitHub Pages (deploy)
    ↓
Website (app.js loads JSON)
```

## 🐛 Common Issues

### "PDGA scraping needs to be implemented"
Normal! You need to add actual scraping code based on current PDGA site structure.

### GitHub Actions failing
Check Actions tab for error logs. Common issues:
- Python script errors
- Missing dependencies
- PDGA website changes

### Site not updating after push
- Wait 1-2 minutes for GitHub Pages to deploy
- Check repository Settings → Pages for deploy status
- Hard refresh browser (Ctrl+Shift+R)

## 📝 Manual Testing

Before going live, test manually:

```bash
# 1. Edit rosters
nano data/rosters.json

# 2. Run update (won't fetch real data yet)
python3 update_league.py

# 3. Check updated files
cat data/standings.json

# 4. View website locally
python3 -m http.server 8000
```

## 🎨 Feature Ideas

Easy additions:
- Add team logos/avatars
- Weekly email summaries
- Player stats charts
- Trade deadline timer
- Draft history
- Head-to-head matchups
- Mobile app integration

## 📱 Mobile Friendly

The site is already responsive and works great on phones and tablets!

## 🔒 Security Notes

- No API keys needed for basic PDGA scraping
- If you add API features, use GitHub Secrets
- Don't commit sensitive data to repository

## 🆘 Getting Help

1. Check QUICKSTART.md for detailed setup
2. Read README.md for full documentation
3. Review example code in pdga_scraper_helper.py
4. Search PDGA website for their data API docs
5. Open GitHub issue for bugs

## ✅ Next Steps Checklist

- [ ] Create GitHub repository
- [ ] Add your teams to rosters.json
- [ ] Enable GitHub Pages
- [ ] Implement PDGA scraping
- [ ] Test locally
- [ ] Push to GitHub
- [ ] Verify site is live
- [ ] Run manual update test
- [ ] Share with league members!

## 🏁 You're Ready!

Everything is set up and ready to customize. The hardest part will be implementing the PDGA scraper, but the helper script gives you a great starting point.

Good luck with your fantasy league! 🥏

---

**Questions?** Review the documentation or inspect the code - it's well-commented!
