/**
 * Evaluation Form Component
 * Form for admins to evaluate ideas
 */
import React, { useState } from 'react';
import { EvaluateRequest } from '../../api/ideas';
import './EvaluationForm.css';

interface EvaluationFormProps {
  currentStatus: string;
  onSubmit: (request: EvaluateRequest) => Promise<void>;
  onCancel: () => void;
}

const EvaluationForm: React.FC<EvaluationFormProps> = ({
  currentStatus,
  onSubmit,
  onCancel
}) => {
  const [newStatus, setNewStatus] = useState<'under_review' | 'accepted' | 'rejected'>('under_review');
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!comment || comment.trim().length < 10) {
      setError('Comment must be at least 10 characters');
      return;
    }

    if (newStatus === currentStatus) {
      setError(`Idea is already in "${newStatus}" status`);
      return;
    }

    try {
      setSubmitting(true);
      await onSubmit({ new_status: newStatus, comment: comment.trim() });
    } catch (err: any) {
      console.error('Error submitting evaluation:', err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to submit evaluation. Please try again.');
      }
      setSubmitting(false);
    }
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'under_review': return '#ED8936';
      case 'accepted': return '#48BB78';
      case 'rejected': return '#F56565';
      default: return '#4299E1';
    }
  };

  return (
    <form onSubmit={handleSubmit} className="evaluation-form">
      <div className="form-header">
        <h3>Evaluate Idea</h3>
        <p>Current status: <strong style={{ 
          color: getStatusColor(currentStatus),
          textTransform: 'capitalize'
        }}>{currentStatus.replace('_', ' ')}</strong></p>
      </div>

      {error && (
        <div className="form-error">
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="new_status">New Status *</label>
        <select
          id="new_status"
          value={newStatus}
          onChange={(e) => setNewStatus(e.target.value as any)}
          disabled={submitting}
          required
        >
          <option value="under_review">Under Review</option>
          <option value="accepted">Accepted</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="comment">Evaluation Comment *</label>
        <textarea
          id="comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          disabled={submitting}
          placeholder="Provide detailed feedback for the submitter (minimum 10 characters)..."
          rows={6}
          required
        />
        <div className="char-count">
          {comment.length} / 2000 characters
          {comment.length < 10 && ' (minimum 10)'}
        </div>
      </div>

      <div className="form-actions">
        <button 
          type="button" 
          className="btn-cancel"
          onClick={onCancel}
          disabled={submitting}
        >
          Cancel
        </button>
        <button 
          type="submit" 
          className="btn-submit"
          disabled={submitting || comment.trim().length < 10}
        >
          {submitting ? 'Submitting...' : 'Submit Evaluation'}
        </button>
      </div>
    </form>
  );
};

export default EvaluationForm;
