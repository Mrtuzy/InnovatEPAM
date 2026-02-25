/**
 * Registration page.
 * Displays the registration form.
 */
import React from 'react';
import RegistrationForm from '../../components/auth/RegistrationForm';

const RegisterPage: React.FC = () => {
  return (
    <div className="auth-page register-page">
      <div className="auth-shell fade-in">
        <div className="auth-brand">
          <h1>InnovatEPAM Portal</h1>
          <p>
            Launch your next idea with a workspace built for clarity, feedback,
            and momentum. Submitters and admins stay aligned from day one.
          </p>
          <div className="auth-highlight stagger">
            <div>Structured submissions with smart validation</div>
            <div>Role-aware access for submitters and admins</div>
            <div>Fast feedback loop with built-in review flow</div>
          </div>
        </div>
        <div className="auth-card">
          <RegistrationForm />
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
