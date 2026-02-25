/**
 * API service for ideas endpoints
 */
import apiClient from './client';

export interface IdeaSubmitter {
  id: string;
  full_name: string;
  email: string;
}

export interface IdeaCategory {
  id: string;
  name: string;
  description: string | null;
  display_order: number;
  is_active: boolean;
}

export interface IdeaAttachment {
  filename: string;
  size: number;
  mimetype: string;
}

export interface Idea {
  id: string;
  title: string;
  description: string;
  status: 'submitted' | 'under_review' | 'accepted' | 'rejected';
  category: IdeaCategory;
  submitter: IdeaSubmitter;
  attachment: IdeaAttachment | null;
  created_at: string;
  updated_at: string;
}

export interface PaginationInfo {
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface IdeaListResponse {
  items: Idea[];
  pagination: PaginationInfo;
}

export interface Evaluation {
  id: string;
  idea_id: string;
  evaluator: IdeaSubmitter;
  previous_status: string;
  new_status: string;
  comment: string;
  created_at: string;
}

export interface EvaluationListResponse {
  evaluations: Evaluation[];
  total: number;
}

export interface EvaluateRequest {
  new_status: 'under_review' | 'accepted' | 'rejected';
  comment: string;
}

export interface CreateIdeaRequest {
  title: string;
  description: string;
  category_id: string;
  attachment?: File;
}

/**
 * Create a new idea with optional file attachment
 */
export const createIdea = async (data: CreateIdeaRequest): Promise<Idea> => {
  const formData = new FormData();
  formData.append('title', data.title);
  formData.append('description', data.description);
  formData.append('category_id', data.category_id);
  
  if (data.attachment) {
    formData.append('attachment', data.attachment);
  }

  const response = await apiClient.post<Idea>('/api/v1/ideas', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get user's own ideas with pagination and filtering
 */
export const getMyIdeas = async (
  status?: string,
  categoryId?: string,
  page: number = 1,
  limit: number = 20,
  sort: string = 'created_at_desc'
): Promise<IdeaListResponse> => {
  const response = await apiClient.get<IdeaListResponse>('/api/v1/ideas/my-ideas', {
    params: {
      status,
      category_id: categoryId,
      page,
      limit,
      sort
    }
  });
  return response.data;
};

/**
 * Get all ideas (admin/evaluator view)
 */
export const getAllIdeas = async (
  status?: string,
  categoryId?: string,
  page: number = 1,
  limit: number = 20,
  sort: string = 'created_at_desc'
): Promise<IdeaListResponse> => {
  const response = await apiClient.get<IdeaListResponse>('/api/v1/ideas', {
    params: {
      status,
      category_id: categoryId,
      page,
      limit,
      sort
    }
  });
  return response.data;
};

/**
 * Get idea by ID
 */
export const getIdeaById = async (id: string): Promise<Idea> => {
  const response = await apiClient.get<Idea>(`/api/v1/ideas/${id}`);
  return response.data;
};

/**
 * Download idea attachment
 */
export const downloadAttachment = async (ideaId: string, filename: string): Promise<void> => {
  const response = await apiClient.get(`/api/v1/ideas/${ideaId}/attachment`, {
    responseType: 'blob'
  });
  
  // Create a download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

/**
 * Evaluate an idea (admin only)
 */
export const evaluateIdea = async (ideaId: string, request: EvaluateRequest): Promise<Evaluation> => {
  const response = await apiClient.post<Evaluation>(`/api/v1/ideas/${ideaId}/evaluate`, request);
  return response.data;
};

/**
 * Get evaluation history for an idea
 */
export const getIdeaEvaluations = async (ideaId: string): Promise<EvaluationListResponse> => {
  const response = await apiClient.get<EvaluationListResponse>(`/api/v1/ideas/${ideaId}/evaluations`);
  return response.data;
};
