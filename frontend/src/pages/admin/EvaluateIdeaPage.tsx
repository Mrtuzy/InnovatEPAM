/**
 * Evaluate Idea Page - Admin page for evaluating ideas
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIdeaById, evaluateIdea, Idea, EvaluateRequest } from '../../api/ideas';
import { useAuth } from '../../hooks/useAuth';
import EvaluationForm from '../../components/admin/EvaluationForm';
import EvaluationHistory from '../../components/ideas/EvaluationHistory';
import './EvaluateIdeaPage.css';

const EvaluateIdeaPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [idea, setIdea] = useState<Idea | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  // Redirect if not admin
  useEffect(() => {
    if (user && user.role !== 'admin') {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  useEffect(() => {
    if (!id) {
      setError('Idea ID is required');
      setLoading(false);
      return;
    }

    const fetchIdea = async () => {
      try {
        setLoading(true);
        const data = await getIdeaById(id);
        setIdea(data);
        setError('');
      } catch (err: any) {
        console.error('Error fetching idea:', err);
        if (err.response?.status === 404) {
          setError('Idea not found');
        } else if (err.response?.status === 403) {
          setError('You do not have permission to view this idea');
        } else {
          setError('Failed to load idea details. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchIdea();
  }, [id]);

  const handleEvaluate = async (request: EvaluateRequest) => {
    if (!id) return;

    try {
      await evaluateIdea(id, request);
      // Navigate back to idea detail page with success message
      navigate(`/ideas/${id}`, {
        state: { message: 'Evaluation submitted successfully!' }
      });
    } catch (err) {
      // Error is handled in the form component
      throw err;
    }
  };

  const handleCancel = () => {
    navigate(`/ideas/${id}`);
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="evaluate-idea-page">
        <div className="evaluate-container">
          <div className="loading-state">Loading idea details...</div>
        </div>
      </div>
    );
  }

  if (error || !idea) {
    return (
      <div className="evaluate-idea-page">
        <div className="evaluate-container">
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h2>Error</h2>
            <p>{error || 'Idea not found'}</p>
            <button 
              className="btn-back"
              onClick={() => navigate('/ideas')}
            >
              ← Back to Ideas
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="evaluate-idea-page">
      <div className="evaluate-container">
        <button 
          className="btn-back"
          onClick={() => navigate(`/ideas/${id}`)}
        >
          ← Back to Idea Details
        </button>

        <h1 className="page-title">Evaluate Idea</h1>

        <div className="evaluate-grid">
          {/* Left column: Idea details */}
          <div className="idea-summary-card">
            <h2 className="idea-title">{idea.title}</h2>
            
            <div className="idea-meta">
              <div className="meta-item">
                <span className="meta-label">Submitted by:</span>
                <span className="meta-value">{idea.submitter.full_name}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Category:</span>
                <span className="meta-value">{idea.category.name}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Submitted on:</span>
                <span className="meta-value">{formatDate(idea.created_at)}</span>
              </div>
            </div>

            <div className="idea-description-section">
              <h3>Description</h3>
              <div className="idea-description">
                {idea.description.split('\n').map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
            </div>

            {idea.attachment && (
              <div className="attachment-info">
                <strong>📎 Attachment:</strong> {idea.attachment.filename}
              </div>
            )}

            {/* Previous Evaluations */}
            <EvaluationHistory ideaId={id!} />
          </div>

          {/* Right column: Evaluation form */}
          <div className="evaluation-form-card">
            <EvaluationForm
              currentStatus={idea.status}
              onSubmit={handleEvaluate}
              onCancel={handleCancel}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default EvaluateIdeaPage;
