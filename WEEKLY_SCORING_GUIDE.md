# Weekly Top-3 Scoring System Explained

## How It Works

### Basic Concept
Instead of counting all 7 players on your roster every week, **only your best 3 players count toward your team score each week**. This creates strategic depth and keeps teams competitive even when some players have off weeks.

### Weekly Cycle

Each week, the system:
1. Collects all tournaments from the past 7-14 days
2. Calculates scores for every player who competed
3. For each team, ranks all 7 players by their weekly score
4. Takes the **3 lowest scores** (remember: lower is better!)
5. Adds those 3 scores to the team's season total

### Example Week

**Your Roster:**
- Paul McBeth: 5th at Elite Series = 5 × 3 = **15 pts**
- Eagle McMahon: 2nd at Major = 2 × 2.5 = **5 pts** ✅ Counted
- Calvin Heimburg: 10th at A-Tier = 10 × 2 = **20 pts**
- Ricky Wysocki: 1st at Elite Series = 1 × 3 = **3 pts** ✅ Counted
- Gannon Buhr: 8th at A-Tier = 8 × 2 = **16 pts**
- Chris Dickerson: Did not play = **0 pts** ✅ Counted (best score!)
- Thomas Gilbert (underdog): 15th at B-Tier = 15 × 1 × 2 = **30 pts**

**Your Week Score:** 0 + 3 + 5 = **8 points**

The other 4 players' scores don't count this week, but they're still tracked!

## Player Statistics Tracking

### Individual Player Stats

Every player accumulates statistics throughout the season:

- **Season Total**: Sum of ALL their weekly scores when they were in the top 3
- **Tournaments Played**: How many events they competed in
- **Times Counted**: How many weeks they were in the top 3
- **Average When Counted**: Season Total ÷ Times Counted

### Why This Matters

You can see:
- Which players are consistently making your top 3
- Which players are underperforming and might need to be watched
- Whether your underdog pick is paying off with the 2x multiplier
- How each player contributes to your overall strategy

## Strategic Implications

### Roster Construction
- **Consistency vs. Ceiling**: Do you want 7 solid performers or 3 stars and 4 wildcards?
- **Underdog Value**: A 2x multiplier can turn a mediocre finish into a top-3 score
- **Tournament Schedule**: Players who compete more often have more chances to score

### Weekly Management
- You don't need all 7 players to perform every week
- Having depth means you're protected from injuries/off-weeks
- Players who don't compete get a score of 0 (which counts if they're top 3!)

### Season-Long Strategy
- Track which players are consistently in your top 3
- Monitor players who are on the bubble
- Watch for emerging talent from your underdog pick

## Data Tracking

### Team Weekly Breakdown
Each team's page shows:
- Week-by-week scores
- Which 3 players counted each week
- How many tournaments those players competed in

### Player Leaderboard
Sort and filter by:
- **All Players**: See everyone in the league
- **Counted Players Only**: Players who've made a top 3
- **Underdogs**: See how the 2x picks are performing

## Viewing Your Data

### On the Website

**Current Standings**: See overall team rankings and weekly totals

**Player Performance Leaderboard**: Sort by:
- Season total (who's scoring most points)
- Times counted (who's most consistent)
- Average when counted (who's most efficient)

**Weekly Performance Breakdown**: See each week's top 3 players for every team

**Team Rosters**: See each player's:
- Season total points
- Times counted in top 3
- Total tournaments played

## Example Season Scenario

### Week 1
- You pick up 12 points from your top 3
- Your underdog was in the top 3 with a great performance

### Week 2
- One of your stars doesn't play
- Your depth players step up
- You still only get 15 points (not as good as week 1)

### Week 3
- Your top 3 all have excellent weeks
- You score only 8 points (your best week!)

**Season Total After 3 Weeks: 35 points**

## Frequently Asked Questions

**Q: What if only 2 of my players compete in a week?**
A: Those 2 scores count, plus a 0 for the third spot (if no one else played).

**Q: Does my underdog's 2x multiplier apply before selecting top 3?**
A: Yes! The multiplier is applied to their tournament score first, then top 3 selection happens.

**Q: Can the same 3 players count every week?**
A: Absolutely! If they're consistently your best performers, they'll keep making your top 3.

**Q: What if there are no tournaments in a week?**
A: No problem! The week is skipped and your season total stays the same.

**Q: How do I know which players were counted each week?**
A: Check the "Weekly Performance Breakdown" section on the website!

## Advanced Analytics Ideas

Want to dig deeper? You can track:
- **Counting Percentage**: Times Counted ÷ Tournaments Played
- **Efficiency Rating**: Season Total ÷ Tournaments Played
- **Roster Diversity**: How many different players have made your top 3
- **Underdog ROI**: How much better is your underdog vs. their draft position

## Technical Implementation

The `update_league.py` script:
1. Groups tournaments by week
2. Calculates all player scores with tier multipliers
3. Sorts each team's players by weekly score
4. Selects the best 3 (lowest scores)
5. Updates the standings and player stats
6. Saves weekly breakdown for historical tracking

All data is preserved in JSON files for complete season transparency.

---

**This system rewards both consistency and depth, making every roster spot meaningful!**
