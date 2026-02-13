// Load and display league data
async function loadLeagueData() {
    try {
        // Load standings data
        const standingsResponse = await fetch('data/standings.json');
        const standingsData = await standingsResponse.json();
        
        // Load team rosters
        const rostersResponse = await fetch('data/rosters.json');
        const rostersData = await rostersResponse.json();
        
        // Load recent tournaments
        const tournamentsResponse = await fetch('data/recent_tournaments.json');
        const tournamentsData = await tournamentsResponse.json();
        
        // Load player stats
        const playerStatsResponse = await fetch('data/player_stats.json');
        const playerStatsData = await playerStatsResponse.json();
        
        displayStandings(standingsData);
        displayPlayerStats(playerStatsData);
        displayTeamRosters(rostersData);
        displayWeeklyBreakdown(standingsData);
        displayRecentTournaments(tournamentsData);
        displayLastUpdated(standingsData.last_updated);
    } catch (error) {
        console.error('Error loading league data:', error);
        displayError();
    }
}

let currentPlayerStats = [];
let currentStatsFilter = 'all';

function displayStandings(data) {
    const container = document.getElementById('standings-table');
    
    let html = '<table><thead><tr>';
    html += '<th>Rank</th>';
    html += '<th>Team</th>';
    html += '<th>Owner</th>';
    html += '<th>Total Score</th>';
    html += '<th>Weeks</th>';
    html += '<th>Avg/Week</th>';
    html += '</tr></thead><tbody>';
    
    data.standings.forEach((team, index) => {
        const rankClass = index === 0 ? 'rank-1' : '';
        const avgPerWeek = team.weeks_counted > 0 ? (team.total_score / team.weeks_counted).toFixed(1) : '0.0';
        html += `<tr class="${rankClass}">`;
        html += `<td>${index + 1}</td>`;
        html += `<td><strong>${team.team_name}</strong></td>`;
        html += `<td>${team.owner}</td>`;
        html += `<td><strong>${team.total_score.toFixed(1)}</strong></td>`;
        html += `<td>${team.weeks_counted}</td>`;
        html += `<td>${avgPerWeek}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    
    if (data.current_week > 0) {
        html = `<p style="margin-bottom: 15px; color: #666;">Week ${data.current_week} • Best 3 players count each week</p>` + html;
    }
    
    container.innerHTML = html;
}

function displayPlayerStats(data) {
    currentPlayerStats = data.player_stats || [];
    renderPlayerStats();
}

function renderPlayerStats() {
    const container = document.getElementById('player-stats-table');
    
    let filteredPlayers = currentPlayerStats;
    
    if (currentStatsFilter === 'counted') {
        filteredPlayers = currentPlayerStats.filter(p => p.times_counted > 0);
    } else if (currentStatsFilter === 'underdogs') {
        filteredPlayers = currentPlayerStats.filter(p => p.is_underdog);
    }
    
    if (filteredPlayers.length === 0) {
        container.innerHTML = '<p>No player data available yet.</p>';
        return;
    }
    
    let html = '<table><thead><tr>';
    html += '<th>Rank</th>';
    html += '<th>Player</th>';
    html += '<th>Team</th>';
    html += '<th>Season Total</th>';
    html += '<th>Times Counted</th>';
    html += '<th>Tournaments</th>';
    html += '<th>Avg When Counted</th>';
    html += '</tr></thead><tbody>';
    
    filteredPlayers.forEach((player, index) => {
        const underdogBadge = player.is_underdog ? ' <span class="underdog-badge">⭐</span>' : '';
        html += '<tr>';
        html += `<td>${index + 1}</td>`;
        html += `<td>${player.name}${underdogBadge}</td>`;
        html += `<td>${player.team}</td>`;
        html += `<td><strong>${player.season_total.toFixed(1)}</strong></td>`;
        html += `<td>${player.times_counted}</td>`;
        html += `<td>${player.tournaments_played}</td>`;
        html += `<td>${player.average_when_counted.toFixed(1)}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function showAllPlayers() {
    currentStatsFilter = 'all';
    updateStatsButtons('all');
    renderPlayerStats();
}

function showCountedOnly() {
    currentStatsFilter = 'counted';
    updateStatsButtons('counted');
    renderPlayerStats();
}

function showUnderdogs() {
    currentStatsFilter = 'underdogs';
    updateStatsButtons('underdogs');
    renderPlayerStats();
}

function updateStatsButtons(active) {
    document.querySelectorAll('.stats-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const buttons = document.querySelectorAll('.stats-btn');
    if (active === 'all') buttons[0].classList.add('active');
    else if (active === 'counted') buttons[1].classList.add('active');
    else if (active === 'underdogs') buttons[2].classList.add('active');
}

function displayTeamRosters(data) {
    const container = document.getElementById('team-rosters');
    let html = '';
    
    data.teams.forEach(team => {
        html += '<div class="team-card">';
        html += `<div class="team-name">${team.team_name} - ${team.owner}</div>`;
        html += '<ul class="player-list">';
        
        team.players.forEach((player, index) => {
            const underdogClass = index === 6 ? 'underdog' : '';
            const seasonTotal = player.season_total ? player.season_total.toFixed(1) : '0.0';
            const timesCounted = player.times_counted || 0;
            const tournamentsPlayed = player.tournaments_played || 0;
            
            html += `<li class="${underdogClass}">`;
            html += `<strong>${player.name}</strong> (PDGA #${player.pdga_number})`;
            html += `<div style="font-size: 0.9em; color: #666; margin-top: 3px;">`;
            html += `Season: ${seasonTotal} pts • Counted: ${timesCounted}x • Played: ${tournamentsPlayed}`;
            html += `</div>`;
            html += '</li>';
        });
        
        html += '</ul>';
        html += '</div>';
    });
    
    container.innerHTML = html;
}

function displayWeeklyBreakdown(data) {
    const container = document.getElementById('weekly-breakdown');
    
    if (!data.standings || data.standings.length === 0 || data.current_week === 0) {
        container.innerHTML = '<p>No weekly data available yet. Check back after tournaments begin!</p>';
        return;
    }
    
    let html = '';
    
    data.standings.forEach(team => {
        if (!team.weekly_breakdown || team.weekly_breakdown.length === 0) return;
        
        html += '<div class="team-card">';
        html += `<div class="team-name">${team.team_name} - ${team.owner}</div>`;
        html += '<div class="weekly-data">';
        
        team.weekly_breakdown.forEach(week => {
            html += `<div class="week-card">`;
            html += `<div style="font-weight: bold; margin-bottom: 8px;">Week ${week.week}: ${week.score.toFixed(1)} pts</div>`;
            
            if (week.top_3_players && week.top_3_players.length > 0) {
                html += '<div style="font-size: 0.9em; margin-left: 15px;">';
                week.top_3_players.forEach((p, idx) => {
                    html += `<div>${idx + 1}. ${p.name}: ${p.score.toFixed(1)} pts (${p.tournaments} event${p.tournaments > 1 ? 's' : ''})</div>`;
                });
                html += '</div>';
            }
            
            html += '</div>';
        });
        
        html += '</div>';
        html += '</div>';
    });
    
    container.innerHTML = html;
}

function displayRecentTournaments(data) {
    const container = document.getElementById('recent-tournaments');
    let html = '';
    
    if (data.tournaments.length === 0) {
        html = '<p>No recent tournaments found. Check back after the season starts!</p>';
    } else {
        data.tournaments.forEach(tournament => {
            const tierClass = getTierClass(tournament.tier);
            html += '<div class="tournament-card">';
            html += `<div class="tournament-name">`;
            html += `${tournament.name}`;
            html += `<span class="tournament-tier ${tierClass}">${tournament.tier}</span>`;
            html += `</div>`;
            html += `<div style="font-size: 0.9em; color: #666; margin-top: 5px;">`;
            html += `${tournament.date} • ${tournament.location}`;
            html += `</div>`;
            
            if (tournament.fantasy_results && tournament.fantasy_results.length > 0) {
                html += '<div style="margin-top: 10px; font-size: 0.9em;">';
                html += '<strong>Fantasy Points:</strong><ul style="margin-left: 20px; margin-top: 5px;">';
                tournament.fantasy_results.forEach(result => {
                    html += `<li>${result.player}: ${result.finish} (${result.points.toFixed(1)} pts)</li>`;
                });
                html += '</ul></div>';
            }
            
            html += '</div>';
        });
    }
    
    container.innerHTML = html;
}

function getTierClass(tier) {
    const tierMap = {
        'Elite': 'tier-elite',
        'Major': 'tier-major',
        'A-Tier': 'tier-a',
        'B-Tier': 'tier-b'
    };
    return tierMap[tier] || 'tier-b';
}

function displayLastUpdated(timestamp) {
    const container = document.getElementById('last-updated');
    if (timestamp) {
        const date = new Date(timestamp);
        container.textContent = `Last updated: ${date.toLocaleDateString()} at ${date.toLocaleTimeString()}`;
    }
}

function displayError() {
    const standingsContainer = document.getElementById('standings-table');
    standingsContainer.innerHTML = '<p style="color: red;">Error loading data. Please check back later.</p>';
}

function toggleRules() {
    const modal = document.getElementById('rules-modal');
    if (modal.style.display === 'block') {
        modal.style.display = 'none';
    } else {
        modal.style.display = 'block';
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('rules-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadLeagueData);
