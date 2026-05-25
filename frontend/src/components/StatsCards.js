import React from 'react';

function StatsCards({ stats }) {
    return (
        <div className="stats-grid">
            <div className="stat-card1">
                <div className="stat-info">
                    <h3>Total Projects</h3>
                    <p>{stats.total_projects}</p>
                </div>
            </div>
            <div className="stat-card2">
                <div className="stat-info">
                    <h3>Total Tasks</h3>
                    <p>{stats.total_tasks}</p>
                </div>
            </div>
            <div className="stat-card3 completed">
                <div className="stat-info">
                    <h3>Completed Tasks</h3>
                    <p>{stats.completed_tasks}</p>
                </div>
            </div>
            <div className="stat-card4 pending">
                <div className="stat-info">
                    <h3>Pending Tasks</h3>
                    <p>{stats.pending_tasks}</p>
                </div>
            </div>
        </div>
    );
}

export default StatsCards;