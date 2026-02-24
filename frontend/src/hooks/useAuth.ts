/**
 * Authentication hook - re-exports useAuth from AuthContext
 * with added logout functionality.
 */
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';

// We need to duplicate the interface here since we export useAuth
// The actual context is in AuthContext.tsx
import { useAuth as useAuthContext } from '../contexts/AuthContext';

interface AuthContextType {
  user: any;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (accessToken: string, refreshToken: string, user: any) => void;
  logout: () => void;
  updateUser: (user: any) => void;
}

/**
 * Hook to access authentication context and logout functionality
 * @returns AuthContextType with login, logout, and user info
 */
export const useAuth = (): AuthContextType & { logout: () => Promise<void> } => {
  const auth = useAuthContext();
  const navigate = useNavigate();

  /**
   * Logout the current user
   * - Calls backend logout endpoint
   * - Clears auth context
   * - Redirects to login
   */
  const logoutWithApiCall = async () => {
    try {
      // Call backend logout endpoint
      await apiClient.post('/api/v1/auth/logout');
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear local auth state
      auth.logout();

      // Redirect to login
      navigate('/login');
    }
  };

  return {
    ...auth,
    logout: logoutWithApiCall,
  };
};
