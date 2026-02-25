/**
 * Logout page.
 * Triggers logout and redirects to login.
 */
import React, { useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';

const LogoutPage: React.FC = () => {
  const { logout } = useAuth();

  useEffect(() => {
    const runLogout = async () => {
      await logout();
    };

    runLogout();
  }, [logout]);

  return (
    <div className="auth-page">
      <div className="auth-card fade-in">
        <h1>Signing you out</h1>
        <p>Please wait a moment while we close your session.</p>
      </div>
    </div>
  );
};

export default LogoutPage;
