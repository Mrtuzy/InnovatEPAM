/**
 * Login page.
 * Displays the login form.
 */
import React from 'react';
import LoginForm from '../../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <div className="auth-page login-page">
      <div className="auth-shell fade-in">
        <div className="auth-brand">
          <h1>Return to the Idea Hub</h1>
          <p>
            Access submissions, review notes, and the full history of your
            innovation pipeline in one secure workspace.
          </p>
          <div className="auth-highlight stagger">
            <div>One login, unified idea tracking</div>
            <div>Secure session with token refresh</div>
            <div>Review feedback and next steps instantly</div>
          </div>
        </div>
        <div className="auth-card">
          <LoginForm />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
