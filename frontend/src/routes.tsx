/**
 * Main application routing configuration.
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

// Placeholder components - will be created in user story implementations
const HomePage: React.FC = () => <div>Home Page</div>;
const LoginPage: React.FC = () => <div>Login Page (To be implemented)</div>;
const RegisterPage: React.FC = () => <div>Register Page (To be implemented)</div>;
const DashboardPage: React.FC = () => <div>Dashboard (To be implemented)</div>;

const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes - will add ProtectedRoute wrapper in US1 */}
          <Route path="/dashboard" element={<DashboardPage />} />

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default AppRoutes;
