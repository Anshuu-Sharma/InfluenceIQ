document.addEventListener('DOMContentLoaded', () => {
    const sortSelect = document.getElementById('sort-select');
    const leaderboardBody = document.getElementById('leaderboard-body');

    //1 april ansh
    const categoryTabs = document.getElementById('category-tabs');
    let currentCategory = 'all';
    // Load categories
    fetch('/categories')
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const tab = document.createElement('a');
                tab.href = "#";
                tab.className = 'category-tab';
                tab.dataset.category = category.id;
                tab.textContent = category.name;
                tab.addEventListener('click', (e) => {
                    e.preventDefault();
                    selectCategory(category.id);
                });
                categoryTabs.appendChild(tab);
            });
        });

    function selectCategory(category) {
        currentCategory = category;
        document.querySelectorAll('.category-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`.category-tab[data-category="${category}"]`).classList.add('active');
        loadLeaderboard(sortSelect.value);
    }

    
    function loadLeaderboard(sortBy = 'influence_score') {
        // Show loading state
        leaderboardBody.innerHTML = '<tr><td colspan="6" class="loading-message">Loading leaderboard data...</td></tr>';
        
        let url = `/leaderboard?sort_by=${sortBy}&t=${Date.now()}`;
        if (currentCategory !== 'all') {
            url += `&category=${currentCategory}`;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Leaderboard data:", data);
                
                if (!data || data.length === 0) {
                    leaderboardBody.innerHTML = '<tr><td colspan="6" class="empty-message">No data available for this category.</td></tr>';
                    return;
                }
                
                
                leaderboardBody.innerHTML = '';
                
                data.forEach((entry, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td><a href="/?username=${entry.username}&autoanalyze=true" class="username-link">@${entry.username}</a></td>
                        <td>${typeof entry.influence_score === 'number' ? entry.influence_score.toFixed(2) : 'N/A'}</td>
                        <td>${typeof entry.engagement_rate === 'number' ? entry.engagement_rate.toFixed(2) : 'N/A'}%</td>
                        <td>${typeof entry.followers === 'number' ? entry.followers.toLocaleString() : 'N/A'}</td>
                        <td>${entry.timestamp ? new Date(entry.timestamp).toLocaleDateString() : 'N/A'}</td>
                    `;
                    leaderboardBody.appendChild(row);
                });
                
            })
            .catch(error => {
                console.error('Error loading leaderboard:', error);
                leaderboardBody.innerHTML = `<tr><td colspan="6" class="error-message">Error loading leaderboard data: ${error.message}</td></tr>`;
            });
    }
    
    sortSelect.addEventListener('change', () => {
        loadLeaderboard(sortSelect.value);
    });
    
    // Initial load
    loadLeaderboard();
});
