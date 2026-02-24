/**
 * Registration page.
 * Displays the registration form.
 */
import React from 'react';
import RegistrationForm from '../../components/auth/RegistrationForm';

const RegisterPage: React.FC = () => {
  return (
    <div className="auth-page register-page">
      <div className="auth-container">
        <RegistrationForm />
      </div>
    </div>
  );
};

export default RegisterPage;
