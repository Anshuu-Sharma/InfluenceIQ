document.addEventListener('DOMContentLoaded', () => {
    // const exploreBtn = document.querySelector('.explore-btn');
    // const searchInput = document.getElementById('search');
    // const resultsDiv = document.getElementById('results');
    // const graphContainer = document.getElementById('graph-container');

    // // Handle Analyze Button Click
    // exploreBtn.addEventListener('click', async () => {
    //     const username = searchInput.value.trim();

    //     if (!username) {
    //         resultsDiv.innerHTML = '<p>Please enter a username.</p>';
    //         return;
    //     }

    //     // Change button to loading state
    //     exploreBtn.innerHTML = '<div class="loading-spinner"></div>';
    //     exploreBtn.style.cursor = 'not-allowed';
    //     exploreBtn.disabled = true;

    //     resultsDiv.innerHTML = '<p>Analyzing...</p>';
    //     graphContainer.innerHTML = ''; // Clear previous graph

    //     try {
    //         const response = await fetch('/analyze', {
    //             method: 'POST',
    //             headers: { 'Content-Type': 'application/json' },
    //             body: JSON.stringify({ username })
    //         });

    //         if (!response.ok) {
    //             throw new Error(`Server error: ${response.status}`);
    //         }

    //         const data = await response.json();

    //         if (data.error) {
    //             resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
    //             return;
    //         }

            // Display metrics dynamically
            // resultsDiv.innerHTML = `
            //     <div class="feature-card"><h3>Username</h3><p>@${data.username}</p></div>
            //     <div class="feature-card"><h3>Full Name</h3><p>${data.full_name}</p></div>
            //     <div class="feature-card"><h3>Bio</h3><p>${data.biography || 'No bio available'}</p></div>
            //     <div class="feature-card"><h3>Verified</h3><p>${data.verified ? '✅ Yes' : '❌ No'}</p></div>
            //     <div class="feature-card"><h3>Followers</h3><p>${data.followers.toLocaleString()}</p></div>
            //     <div class="feature-card"><h3>Following</h3><p>${data.following.toLocaleString()}</p></div>
            //     <div class="feature-card"><h3>Total Posts</h3><p>${data.posts_count.toLocaleString()}</p></div>
            //     <div class="feature-card"><h3>Profile URL</h3><a href="${data.profile_url}" target="_blank">${data.profile_url}</a></div>
            //     <div class="feature-card"><h3>Business Address</h3><p>${data.business_address || 'N/A'}</p></div>
            //     <div class="feature-card"><h3>Category</h3><p>${data.categories?.join(', ') || 'No category detected'}</p></div>
            //     <div class="feature-card"><h3>Standard Engagement Rate</h3><p>${data.engagement_rate?.toFixed(2)}%</p></div>
            //     <div class="feature-card"><h3>Adjusted Engagement Rate</h3><p>${data.engagement_rate_adjusted?.toFixed(2)}%</p></div>
            //     <div class="feature-card"><h3>Weighted Engagement Rate</h3><p>${data.engagement_rate_weighted?.toFixed(2)}%</p></div>
            //     <div class="feature-card"><h3>Average Likes</h3><p>${data.avg_likes?.toLocaleString()}</p></div>
            //     <div class="feature-card"><h3>Average Comments</h3><p>${data.avg_comments?.toLocaleString()}</p></div>
            //     <div class="feature-card"><h3>Fake Followers Percentage</h3><p>${data.fake_follower_percentage?.toFixed(2)}%</p></div>
            //     <div class="feature-card"><h3>Influence Score</h3><p>${data.influence_score?.toFixed(2)}</p></div>`;

            // Display network graph if available
    //         if (data.network_graph) {
    //             graphContainer.innerHTML = `
    //                 <div class="graph-card">
    //                     <img src="${data.network_graph}" alt="Network graph for ${data.username}" />
    //                 </div>`;
    //         } else {
    //             graphContainer.innerHTML = '<p>No network graph available.</p>';
    //         }
    //     } catch (error) {
    //         resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    //         console.error(error);
    //     } finally {
    //         // Reset button state
    //         exploreBtn.innerHTML = 'Analyze →';
    //         exploreBtn.style.cursor = 'pointer';
    //         exploreBtn.disabled = false;
    //     }
    // });

    const exploreBtn = document.querySelector('.explore-btn');
    const searchInput = document.getElementById('search');
    const resultsDiv = document.getElementById('results'); // Placeholder for dynamic content
    const graphContainer = document.getElementById('graph-container'); // Placeholder for network graph

    // Format large numbers to compact format (e.g., 1.2m, 450k)
    function formatNumber(num) {
        if (!num) return '0';
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'm';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'k';
        }
        return num.toString();
    }

    // Handle Analyze Button Click
    exploreBtn.addEventListener('click', async () => {
        const username = searchInput.value.trim();

        if (!username) {
            alert('Please enter a username.');
            return;
        }

        // Change button to loading state
        exploreBtn.innerHTML = '<div class="loading-spinner"></div>';
        exploreBtn.style.cursor = 'not-allowed';
        exploreBtn.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            // Dynamically create the profile card
            resultsDiv.innerHTML = `
            <div class= "data-card">
                <div class="profile-card">
                    <!-- Profile Header -->
                    <div class="profile-header">
                        <img src="/proxy-image?url=${encodeURIComponent(data.profile_pic_url) || `https://ui-avatars.com/api/?name=${data.username}&background=random`}" alt="Profile Picture" class="profile-picture" >
                        <div class="profile-info">
                            <h2 class="username">${data.username}</h2>
                            <p class="rank">🎤 ${data.categories?.[0] || 'GENERAL'} </p>
                        </div>
                    </div>

                
                    <!-- Performance Metrics -->
                    <div class="performance-metrics">
                        <div class="metric followers">
                            <p>Followers</p>
                            <h3>${formatNumber(data.followers)}</h3>
                        </div>
                        <div class="metric posts">
                            <p>Posts</p>
                            <h3>${formatNumber(data.posts_count)}</h3>
                        </div>
                        <div class="metric avg-likes">
                            <p>Avg. Likes</p>
                            <h3>${formatNumber(data.avg_likes)}</h3>
                        </div>
                        <div class="metric engagement">
                            <p>Engagement</p>
                            <h3>${data.engagement_rate?.toFixed(2)}%</h3>
                        </div>
                    </div>

                    <!-- Additional Insights -->
                    <div class="additional-insights">
                        <h4>Additional Insights</h4>
                        <div class="insights-grid">
                            <div class="insight total-likes">
                                <p>Total Likes</p>
                                <h4>${formatNumber(data.avg_likes * data.posts_count)}</h4>
                            </div>
                            <div class="insight avg-comments">
                                <p>Avg. Comments</p>
                                <h4>${formatNumber(data.avg_comments)}</h4>
                            </div>
                        </div>
                    </div>


                    <!-- Extended Metrics -->
<div class="extended-metrics">
    <h4>Extended Metrics</h4>
    <div class="metrics-grid">
        <div class="metric-card">
            <p class="metric-title">Full Name</p>
            <p class="metric-value">${data.full_name || 'N/A'}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Bio</p>
            <p class="metric-value">${data.biography || 'No bio available'}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Verified</p>
            <p class="metric-value">${data.verified ? '✅ Yes' : '❌ No'}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Following</p>
            <p class="metric-value">${data.following.toLocaleString()}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Business Address</p>
            <p class="metric-value">${data.business_address || 'N/A'}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Category</p>
            <p class="metric-value">${data.categories?.join(', ') || 'No category detected'}</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Adjusted Engagement Rate</p>
            <p class="metric-value">${data.engagement_rate_adjusted?.toFixed(2)}%</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Weighted Engagement Rate</p>
            <p class="metric-value">${data.engagement_rate_weighted?.toFixed(2)}%</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Fake Followers Percentage</p>
            <p class="metric-value">${data.fake_follower_percentage?.toFixed(2)}%</p>
        </div>
        <div class="metric-card">
            <p class="metric-title">Influence Score</p>
            <p class="metric-value">${data.influence_score?.toFixed(2)}</p>
        </div>
    </div>
</div>


                   
                </div>`;
            
            // Display network graph in a separate container if available
            if (data.network_graph && graphContainer) {
                graphContainer.innerHTML = `
                    <div class="graph-card">
                        <img src="${data.network_graph}" alt="Network graph for ${data.username}" />
                    </div>`;
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error(error);
        } finally {
            // Reset button state
            exploreBtn.innerHTML = 'Analyze →';
            exploreBtn.style.cursor = 'pointer';
            exploreBtn.disabled = false;
        }
    });
    const influencerGrid = document.getElementById('precomputed-influencers');


    // Fetch precomputed influencers
    fetch('/precomputed-influencers')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched Data:', data); // Debugging log
        influencerGrid.innerHTML = ''; // Clear existing content

        data.forEach((influencer, index) => {
            const card = document.createElement('div');
            card.className = 'influencer-card';
            card.innerHTML = `
                <div class="card-header">
                    <img src="${influencer.imageUrl || '/static/images/default.jpg'}" alt="${influencer.username}">
                    <span class="rank-badge">#${index + 1}</span>
                </div>
                <div class="card-body">
                    <h3>${influencer.name} (@${influencer.username})</h3>
                    <p>${influencer.category} Influencer</p>
                    <p><strong>Followers:</strong> ${influencer.followers.toLocaleString()}</p>
                    <p><strong>Influence Score:</strong> ${influencer.influence_score}/100</p>
                    <p><strong>Average Likes:</strong> ${influencer.avg_likes.toLocaleString()}</p>
                    <p><strong>Average Comments:</strong> ${influencer.avg_comments.toLocaleString()}</p>
                    <p><strong>Engagement Rate:</strong> ${influencer.engagement_rate}%</p>
                    <p><strong>Fake Followers:</strong> ${influencer.fake_follower_percentage}%</p>
                    <div class="badges">
                        ${influencer.verified ? '<span class="badge verified">Verified</span>' : ''}
                        <span class="badge global-reach">Global Reach</span>
                    </div>
                </div>
            `;
            influencerGrid.appendChild(card);
        });
    })
    .catch(error => {
        console.error('Error fetching top influencers:', error);
        influencerGrid.innerHTML = '<p>Error loading data.</p>';
    });


});
