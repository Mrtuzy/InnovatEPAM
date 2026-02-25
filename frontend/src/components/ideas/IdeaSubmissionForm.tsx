/**
 * Idea submission form component
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createIdea } from '../../api/ideas';
import CategorySelector from './CategorySelector';
import FileUpload from './FileUpload';
import './IdeaSubmissionForm.css';

interface FormData {
  title: string;
  description: string;
  category_id: string;
  attachment: File | null;
}

interface FormErrors {
  title?: string;
  description?: string;
  category_id?: string;
  attachment?: string;
}

const IdeaSubmissionForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    title: '',
    description: '',
    category_id: '',
    attachment: null
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string>('');

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Title validation
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.trim().length < 10) {
      newErrors.title = 'Title must be at least 10 characters';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must not exceed 200 characters';
    }

    // Description validation
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    } else if (formData.description.trim().length < 50) {
      newErrors.description = 'Description must be at least 50 characters';
    } else if (formData.description.length > 5000) {
      newErrors.description = 'Description must not exceed 5000 characters';
    }

    // Category validation
    if (!formData.category_id) {
      newErrors.category_id = 'Please select a category';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    try {
      setIsSubmitting(true);

      await createIdea({
        title: formData.title.trim(),
        description: formData.description.trim(),
        category_id: formData.category_id,
        attachment: formData.attachment || undefined
      });

      // Success - redirect to ideas list
      navigate('/ideas', { state: { message: 'Idea submitted successfully!' } });
    } catch (err: any) {
      console.error('Error submitting idea:', err);
      
      if (err.response?.data?.detail) {
        setSubmitError(err.response.data.detail);
      } else if (err.response?.status === 413) {
        setSubmitError('File too large. Maximum size is 10MB.');
      } else if (err.response?.status === 415) {
        setSubmitError('Unsupported file type. Please upload PDF, DOC, DOCX, XLS, XLSX, JPG, PNG, or GIF.');
      } else if (err.response?.status === 400) {
        setSubmitError('Invalid input. Please check your form and try again.');
      } else {
        setSubmitError('Failed to submit idea. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, title: e.target.value }));
    if (errors.title) {
      setErrors(prev => ({ ...prev, title: undefined }));
    }
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, description: e.target.value }));
    if (errors.description) {
      setErrors(prev => ({ ...prev, description: undefined }));
    }
  };

  const handleCategoryChange = (categoryId: string) => {
    setFormData(prev => ({ ...prev, category_id: categoryId }));
    if (errors.category_id) {
      setErrors(prev => ({ ...prev, category_id: undefined }));
    }
  };

  const handleFileSelect = (file: File | null) => {
    setFormData(prev => ({ ...prev, attachment: file }));
    if (errors.attachment) {
      setErrors(prev => ({ ...prev, attachment: undefined }));
    }
  };

  const characterCount = {
    title: formData.title.length,
    description: formData.description.length
  };

  return (
    <form onSubmit={handleSubmit} className="idea-submission-form" noValidate>
      {submitError && (
        <div className="idea-form-alert idea-form-alert-error">
          {submitError}
        </div>
      )}

      <div className="idea-form-group">
        <label htmlFor="title" className="idea-form-label">
          Title <span className="required">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={formData.title}
          onChange={handleTitleChange}
          disabled={isSubmitting}
          className={`idea-form-input ${errors.title ? 'error' : ''}`}
          placeholder="Enter a descriptive title for your idea"
          maxLength={200}
          required
        />
        <div className="idea-form-meta">
          <span className={`character-count ${characterCount.title < 10 ? 'warning' : ''}`}>
            {characterCount.title}/200 characters {characterCount.title < 10 && '(minimum 10)'}
          </span>
        </div>
        {errors.title && <p className="idea-form-error">{errors.title}</p>}
      </div>

      <div className="idea-form-group">
        <label htmlFor="description" className="idea-form-label">
          Description <span className="required">*</span>
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={handleDescriptionChange}
          disabled={isSubmitting}
          className={`idea-form-textarea ${errors.description ? 'error' : ''}`}
          placeholder="Describe your idea in detail. Include the problem, your solution, and expected benefits."
          maxLength={5000}
          rows={8}
          required
        />
        <div className="idea-form-meta">
          <span className={`character-count ${characterCount.description < 50 ? 'warning' : ''}`}>
            {characterCount.description}/5000 characters {characterCount.description < 50 && '(minimum 50)'}
          </span>
        </div>
        {errors.description && <p className="idea-form-error">{errors.description}</p>}
      </div>

      <CategorySelector
        value={formData.category_id}
        onChange={handleCategoryChange}
        disabled={isSubmitting}
        error={errors.category_id}
      />

      <div className="idea-form-group">
        <label className="idea-form-label">
          Attachment <span className="optional">(optional)</span>
        </label>
        <FileUpload
          onFileSelect={handleFileSelect}
          disabled={isSubmitting}
        />
        <p className="idea-form-hint">
          Upload supporting documents, diagrams, or mockups (PDF, DOC, DOCX, XLS, XLSX, JPG, PNG, GIF - max 10MB)
        </p>
      </div>

      <div className="idea-form-actions">
        <button
          type="button"
          onClick={() => navigate('/ideas')}
          disabled={isSubmitting}
          className="idea-form-btn idea-form-btn-secondary"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="idea-form-btn idea-form-btn-primary"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Idea'}
        </button>
      </div>
    </form>
  );
};

export default IdeaSubmissionForm;
