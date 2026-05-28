import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Function to check if a link is active
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/dashboard" className="logo">Project Management System</Link>
        
        <div className="nav-links">
          <Link 
            to="/dashboard" 
            className={isActive('/dashboard') ? 'nav-link active' : 'nav-link'}
          >
            Dashboard
          </Link>
          
          <Link 
            to="/projects" 
            className={isActive('/projects') ? 'nav-link active' : 'nav-link'}
          >
            Projects
          </Link>
          
          <Link 
            to="/tasks" 
            className={isActive('/tasks') ? 'nav-link active' : 'nav-link'}
          >
            Tasks
          </Link>
          
          {/* {user?.role !== 'member' && (
            <Link 
              to="/pending-verification" 
              className={isActive('/pending-verification') ? 'nav-link active' : 'nav-link'}
            >
              Pending Review
            </Link>
          )} */}
          
          {user?.role === 'admin' && (
            <Link 
              to="/users" 
              className={isActive('/users') ? 'nav-link active' : 'nav-link'}
            >
              Users
            </Link>
          )}
          
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
