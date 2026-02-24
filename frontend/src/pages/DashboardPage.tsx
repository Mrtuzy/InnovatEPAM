/**
 * Dashboard page.
 * Shows user profile and main portal features.
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    // logout hook handles navigation to /login
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Welcome to InnovatEPAM Portal</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="dashboard-content">
        <div className="user-profile">
          <h2>User Profile</h2>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Name:</strong> {user?.full_name}</p>
          <p><strong>Role:</strong> {user?.role}</p>
        </div>

        <div className="dashboard-features">
          <h2>Portal Features</h2>
          {user?.role === 'admin' && (
            <div className="feature-section">
              <h3>Admin Features</h3>
              <ul>
                <li>Manage ideas</li>
                <li>Review submissions</li>
                <li>Manage users</li>
              </ul>
            </div>
          )}
          {user?.role === 'submitter' && (
            <div className="feature-section">
              <h3>Submitter Features</h3>
              <ul>
                <li>Submit ideas</li>
                <li>View submitted ideas</li>
                <li>Track ideas status</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
