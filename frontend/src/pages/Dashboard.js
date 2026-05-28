import React, { useState, useEffect } from 'react';
import { getDashboardStats } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  if (!stats) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="welcome-banner">
        <h2>Welcome back, {user?.first_name || user?.username}! </h2>
      </div>

      <div className="stats-container">
        <div className="stat-card1">
          <h3>Total Projects</h3>
          <p className="stat-number">{stats.total_projects}</p>
        </div>
        <div className="stat-card2">
          <h3>Total Tasks</h3>
          <p className="stat-number">{stats.total_tasks}</p>
        </div>
        <div className="stat-card3">
          <h3>Completed Tasks</h3>
          <p className="stat-number">{stats.completed_tasks}</p>
        </div>
        <div className="stat-card4">
          <h3>Pending Tasks</h3>
          <p className="stat-number">{stats.pending_tasks}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;