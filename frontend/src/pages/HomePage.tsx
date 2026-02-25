/**
 * Public landing page.
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const HomePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="hero">
      <div className="page-container hero-grid">
        <div className="fade-in">
          <h1>Innovation deserves a clear runway.</h1>
          <p>
            InnovatEPAM Portal brings structure, visibility, and momentum to your
            idea submissions. Submitters and admins stay in sync with a shared
            workflow built for quick decisions.
          </p>
          <div className="cta-row">
            {isAuthenticated ? (
              <Link to="/dashboard" className="primary-button">
                Go to Dashboard
              </Link>
            ) : (
              <Link to="/register" className="primary-button">
                Start a Submission
              </Link>
            )}
            {isAuthenticated ? (
              <span className="ghost-button">Signed in as {user?.full_name}</span>
            ) : (
              <Link to="/login" className="ghost-button">
                Sign In
              </Link>
            )}
          </div>
        </div>

        <div className="hero-card stagger">
          <h3>Why teams choose this portal</h3>
          <ul>
            <li>Role-based access to keep reviews secure.</li>
            <li>Fast onboarding with guided registration.</li>
            <li>Clear visibility into every idea stage.</li>
            <li>Built-in feedback loop to keep momentum.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
