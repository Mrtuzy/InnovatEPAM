/**
 * Main application routing configuration.
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/routing/ProtectedRoute';

// Auth Pages
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import LogoutPage from './pages/auth/LogoutPage';
import DashboardPage from './pages/DashboardPage';
import HomePage from './pages/HomePage';

// Ideas Pages
import IdeasListPage from './pages/ideas/IdeasListPage';
import SubmitIdeaPage from './pages/ideas/SubmitIdeaPage';
import IdeaDetailPage from './pages/ideas/IdeaDetailPage';

// Admin Pages
import EvaluateIdeaPage from './pages/admin/EvaluateIdeaPage';

const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/logout"
            element={
              <ProtectedRoute>
                <LogoutPage />
              </ProtectedRoute>
            }
          />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          {/* Ideas routes */}
          <Route
            path="/ideas"
            element={
              <ProtectedRoute>
                <IdeasListPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/ideas/submit"
            element={
              <ProtectedRoute>
                <SubmitIdeaPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/ideas/:id"
            element={
              <ProtectedRoute>
                <IdeaDetailPage />
              </ProtectedRoute>
            }
          />

          {/* Admin routes */}
          <Route
            path="/admin/ideas/:id/evaluate"
            element={
              <ProtectedRoute>
                <EvaluateIdeaPage />
              </ProtectedRoute>
            }
          />

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default AppRoutes;
