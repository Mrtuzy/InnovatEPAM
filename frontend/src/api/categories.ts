/**
 * API service for categories endpoints
 */
import apiClient from './client';

export interface Category {
  id: string;
  name: string;
  description: string | null;
  display_order: number;
  is_active: boolean;
}

/**
 * Get active categories
 */
export const getCategories = async (): Promise<Category[]> => {
  const response = await apiClient.get<Category[]>('/api/v1/categories');
  return response.data;
};

/**
 * Get all categories (including inactive) - admin only
 */
export const getAllCategories = async (includeInactive: boolean = false): Promise<Category[]> => {
  const response = await apiClient.get<Category[]>('/api/v1/categories', {
    params: { include_inactive: includeInactive }
  });
  return response.data;
};
