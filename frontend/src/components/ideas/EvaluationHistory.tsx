/**
 * Evaluation History Component
 * Displays evaluation timeline for an idea
 */
import React, { useEffect, useState } from 'react';
import { getIdeaEvaluations, Evaluation } from '../../api/ideas';
import './EvaluationHistory.css';

interface EvaluationHistoryProps {
  ideaId: string;
}

const EvaluationHistory: React.FC<EvaluationHistoryProps> = ({ ideaId }) => {
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchEvaluations = async () => {
      try {
        setLoading(true);
        const response = await getIdeaEvaluations(ideaId);
        setEvaluations(response.evaluations);
        setError('');
      } catch (err: any) {
        console.error('Error fetching evaluations:', err);
        setError('Failed to load evaluation history');
      } finally {
        setLoading(false);
      }
    };

    fetchEvaluations();
  }, [ideaId]);

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusClass = (status: string): string => {
    switch (status) {
      case 'submitted':
        return 'status-submitted';
      case 'under_review':
        return 'status-under-review';
      case 'accepted':
        return 'status-accepted';
      case 'rejected':
        return 'status-rejected';
      default:
        return '';
    }
  };

  if (loading) {
    return (
      <div className="evaluation-history">
        <h3 className="evaluation-history-title">Evaluation History</h3>
        <div className="evaluation-loading">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="evaluation-history">
        <h3 className="evaluation-history-title">Evaluation History</h3>
        <div className="evaluation-error">{error}</div>
      </div>
    );
  }

  if (evaluations.length === 0) {
    return (
      <div className="evaluation-history">
        <h3 className="evaluation-history-title">Evaluation History</h3>
        <div className="evaluation-empty">No evaluations yet</div>
      </div>
    );
  }

  return (
    <div className="evaluation-history">
      <h3 className="evaluation-history-title">Evaluation History</h3>
      <div className="evaluation-timeline">
        {evaluations.map((evaluation, index) => (
          <div key={evaluation.id} className="evaluation-item">
            <div className="evaluation-marker"></div>
            {index < evaluations.length - 1 && <div className="evaluation-line"></div>}
            
            <div className="evaluation-content">
              <div className="evaluation-header">
                <div className="evaluation-status-change">
                  <span className={`status-badge ${getStatusClass(evaluation.previous_status)}`}>
                    {evaluation.previous_status.replace('_', ' ')}
                  </span>
                  <span className="status-arrow">→</span>
                  <span className={`status-badge ${getStatusClass(evaluation.new_status)}`}>
                    {evaluation.new_status.replace('_', ' ')}
                  </span>
                </div>
                <div className="evaluation-meta">
                  <span className="evaluation-evaluator">
                    By {evaluation.evaluator.full_name}
                  </span>
                  <span className="evaluation-date">
                    {formatDate(evaluation.created_at)}
                  </span>
                </div>
              </div>
              
              <div className="evaluation-comment">
                <p>{evaluation.comment}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EvaluationHistory;
