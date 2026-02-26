/**
 * Dashboard page.
 * Shows user profile and main portal features.
 */
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    // Check for message from navigation state
    if (location.state?.message) {
      setMessage(location.state.message);
      // Clear the state
      window.history.replaceState({}, document.title);
      
      // Auto-dismiss after 5 seconds
      setTimeout(() => setMessage(''), 5000);
    }
  }, [location]);

  const handleLogout = async () => {
    await logout();
    // logout hook handles navigation to /login
  };

  return (
    <div className="dashboard-page">
      <div className="page-container">
        <div className="dashboard-header fade-in">
          <div>
            <h1>Welcome back, {user?.full_name}</h1>
            <p className="link-muted">Keep the innovation momentum going.</p>
          </div>
          <button className="logout-button" onClick={handleLogout}>Logout</button>
        </div>

        {message && (
          <div className="alert alert-warning" style={{ marginBottom: '1.5rem' }}>
            {message}
          </div>
        )}

        <div className="dashboard-grid stagger">
          <div className="panel-card">
            <h3>Profile Snapshot</h3>
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Role:</strong> <span className="badge">{user?.role}</span></p>
          </div>

          <div className="panel-card">
            <h3>Quick Actions</h3>
            <div className="quick-actions-container">
              {user?.role === 'admin' ? (
                <>
                  <button 
                    className="action-button action-primary" 
                    onClick={() => navigate('/ideas')}
                  >
                    <span className="action-icon">📋</span>
                    <div className="action-content">
                      <span className="action-title">Review All Ideas</span>
                      <span className="action-subtitle">Evaluate submissions</span>
                    </div>
                  </button>
                </>
              ) : (
                <>
                  <button 
                    className="action-button action-primary" 
                    onClick={() => navigate('/ideas/submit')}
                  >
                    <span className="action-icon">💡</span>
                    <div className="action-content">
                      <span className="action-title">Submit New Idea</span>
                      <span className="action-subtitle">Share your innovation</span>
                    </div>
                  </button>
                  <button 
                    className="action-button action-secondary" 
                    onClick={() => navigate('/ideas')}
                  >
                    <span className="action-icon">📋</span>
                    <div className="action-content">
                      <span className="action-title">View My Ideas</span>
                      <span className="action-subtitle">Track your submissions</span>
                    </div>
                  </button>
                </>
              )}
            </div>
          </div>

          <div className="panel-card">
            <h3>What you can do</h3>
            {user?.role === 'admin' ? (
              <ul>
                <li>Evaluate incoming ideas</li>
                <li>Share feedback with submitters</li>
                <li>Track portfolio status</li>
              </ul>
            ) : (
              <ul>
                <li>Submit new ideas</li>
                <li>Check current status</li>
                <li>Respond to feedback</li>
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
