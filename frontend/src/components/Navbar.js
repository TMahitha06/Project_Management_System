import React from 'react';

function Navbar({ activeTab, setActiveTab, userName, userRole, onLogout }) {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="nav-brand">
                    <span className="brand-text">Project Management System</span>
                </div>
                
                <div className="nav-menu">
                    <button 
                        className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
                        onClick={() => setActiveTab('dashboard')}
                    >
                        Dashboard
                    </button>
                    <button 
                        className={`nav-item ${activeTab === 'projects' ? 'active' : ''}`}
                        onClick={() => setActiveTab('projects')}
                    >
                        Projects
                    </button>
                    <button 
                        className={`nav-item ${activeTab === 'tasks' ? 'active' : ''}`}
                        onClick={() => setActiveTab('tasks')}
                    >
                        Tasks
                    </button>
                    
                    <div className="nav-user">
                        <span className="user-name">{userName} ({userRole})</span>
                        <button className="logout-btn" onClick={onLogout}>
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;