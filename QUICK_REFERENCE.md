# ⚡ Quick Reference: Fantasy Disc Golf Scoring

## 🎯 Core Rules (1 Minute Read)

### Roster Setup
- **7 players** per team (MPO only)
- **Player #7** = Must be outside top 50 in rankings
- **Player #7** = Scores **2x points** (the underdog bonus)

### Weekly Scoring
- Only your **BEST 3 PLAYERS** count each week
- Lower scores = better (it's like golf!)
- Scores carry over week to week (cumulative season total)

### Point Calculation
```
Points = Placement × Tier Multiplier × (2x if underdog)
```

**Tier Multipliers:**
- 🔴 Elite Series → **3.0x**
- 🟠 Major → **2.5x**
- 🔵 A-Tier → **2.0x**
- ⚫ B-Tier → **1.0x**

## 📊 Quick Examples

### Example 1: Elite Series Winner
- Placement: **1st**
- Tier: Elite (3x)
- Regular player: `1 × 3 = 3 points`
- Underdog player: `1 × 3 × 2 = 6 points`

### Example 2: A-Tier Top 10
- Placement: **7th**
- Tier: A-Tier (2x)
- Regular player: `7 × 2 = 14 points`
- Underdog player: `7 × 2 × 2 = 28 points`

### Example 3: Your Weekly Top 3
Your 7 players this week:
1. Player A: 3 pts ✅ Counted
2. Player B: 8 pts ✅ Counted
3. Player C: 15 pts
4. Player D: 12 pts ✅ Counted
5. Player E: 20 pts
6. Player F: 25 pts
7. Player G (underdog): 30 pts

**Your week score: 3 + 8 + 12 = 23 points**

## 🏆 Season Standings

Teams are ranked by **total season score** (lower is better).

Your season total = Sum of all weekly top-3 scores

## 📈 Player Stats Tracked

For each player, we track:
- **Season Total** - All points from weeks they were top-3
- **Times Counted** - How many weeks they made top-3
- **Tournaments Played** - How many events they competed in
- **Average When Counted** - Season Total ÷ Times Counted

## 🎲 Strategy Tips

**Consistency Pays**
- A player who's always in your top-3 is gold
- Better to have 7 solid players than 3 stars and 4 duds

**Underdog Value**
- The 2x multiplier can make your 7th pick a weekly star
- Good underdog = competitive advantage

**Depth Matters**
- Injuries happen, players skip tournaments
- Having 7 good options means you're always competitive

**Tournament Schedule**
- Players who compete more often have more chances
- But quality > quantity for top-3 selection

## 🔍 Where to Find Stats

**On the Website:**
- **Current Standings** → Team rankings
- **Player Performance Leaderboard** → Individual stats
- **Weekly Performance Breakdown** → See each week's top 3
- **Team Rosters** → Player-by-player breakdown

## ⏰ Update Schedule

- Updates run **every Monday at 6 AM UTC**
- Can also trigger manually from GitHub Actions
- Checks for tournaments from past 14 days

## 🆘 Quick Troubleshooting

**"Why didn't my best player count?"**
→ Only top 3 per week count. Check if 3 others scored better.

**"My player competed but scored 0?"**
→ They probably didn't play in any tournaments that week.

**"Underdog not getting 2x?"**
→ Make sure `is_underdog: true` in rosters.json

**"Standings not updating?"**
→ Check GitHub Actions tab for workflow status

## 📱 Mobile Friendly

The entire site works great on phones and tablets!

---

**Lower score wins. Best 3 count each week. Let's go! 🥏**
