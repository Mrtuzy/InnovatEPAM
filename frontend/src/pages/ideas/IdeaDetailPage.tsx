/**
 * Idea Detail Page - View full idea details
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { getIdeaById, downloadAttachment, Idea } from '../../api/ideas';
import { useAuth } from '../../hooks/useAuth';
import EvaluationHistory from '../../components/ideas/EvaluationHistory';
import './IdeaDetailPage.css';

const IdeaDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const [idea, setIdea] = useState<Idea | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [downloading, setDownloading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string>('');

  useEffect(() => {
    // Check for success message from navigation state
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the state
      window.history.replaceState({}, document.title);
      
      // Auto-dismiss after 5 seconds
      setTimeout(() => setSuccessMessage(''), 5000);
    }
  }, [location]);

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

  const handleDownload = async () => {
    if (!idea?.attachment || !id) return;

    try {
      setDownloading(true);
      await downloadAttachment(id, idea.attachment.filename);
    } catch (err) {
      console.error('Error downloading attachment:', err);
      alert('Failed to download attachment. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  const getStatusBadgeClass = (status: string): string => {
    switch (status) {
      case 'submitted':
        return 'status-badge status-submitted';
      case 'under_review':
        return 'status-badge status-under-review';
      case 'accepted':
        return 'status-badge status-accepted';
      case 'rejected':
        return 'status-badge status-rejected';
      default:
        return 'status-badge';
    }
  };

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

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  if (loading) {
    return (
      <div className="idea-detail-page">
        <div className="idea-detail-container">
          <div className="loading-state">Loading idea details...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="idea-detail-page">
        <div className="idea-detail-container">
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h2>Error</h2>
            <p>{error}</p>
            <button 
              className="btn-back"
              onClick={() => navigate('/ideas')}
            >
              ← Back to My Ideas
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!idea) {
    return null;
  }

  return (
    <div className="idea-detail-page">
      <div className="idea-detail-container">
        <button 
          className="btn-back"
          onClick={() => navigate('/ideas')}
        >
          ← Back to My Ideas
        </button>

        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}

        <div className="idea-detail-card">
          <div className="idea-detail-header">
            <div className="idea-header-left">
              <h1 className="idea-detail-title">{idea.title}</h1>
              <span className={getStatusBadgeClass(idea.status)}>
                {idea.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            {user?.role === 'admin' && (
              <button 
                className="btn-evaluate"
                onClick={() => navigate(`/admin/ideas/${id}/evaluate`)}
              >
                ⚖️ Evaluate Idea
              </button>
            )}
          </div>

          <div className="idea-meta-row">
            <div className="meta-item">
              <span className="meta-label">Category:</span>
              <span className="meta-value">📁 {idea.category.name}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Submitted by:</span>
              <span className="meta-value">👤 {idea.submitter.full_name}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Created:</span>
              <span className="meta-value">📅 {formatDate(idea.created_at)}</span>
            </div>
            {idea.updated_at !== idea.created_at && (
              <div className="meta-item">
                <span className="meta-label">Updated:</span>
                <span className="meta-value">🔄 {formatDate(idea.updated_at)}</span>
              </div>
            )}
          </div>

          <div className="idea-section">
            <h2 className="section-title">Description</h2>
            <div className="idea-description">
              {idea.description.split('\n').map((paragraph, index) => (
                <p key={index}>{paragraph}</p>
              ))}
            </div>
          </div>

          {idea.category.description && (
            <div className="idea-section">
              <h2 className="section-title">About Category</h2>
              <div className="category-info">
                <p>{idea.category.description}</p>
              </div>
            </div>
          )}

          {idea.attachment && (
            <div className="idea-section">
              <h2 className="section-title">Attachment</h2>
              <div className="attachment-card">
                <div className="attachment-info">
                  <div className="attachment-icon">📎</div>
                  <div className="attachment-details">
                    <div className="attachment-filename">{idea.attachment.filename}</div>
                    <div className="attachment-meta">
                      {formatFileSize(idea.attachment.size)} • {idea.attachment.mimetype}
                    </div>
                  </div>
                </div>
                <button 
                  className="btn-download"
                  onClick={handleDownload}
                  disabled={downloading}
                >
                  {downloading ? 'Downloading...' : '⬇ Download'}
                </button>
              </div>
            </div>
          )}

          {/* Evaluation History */}
          <EvaluationHistory ideaId={id!} />
        </div>
      </div>
    </div>
  );
};

export default IdeaDetailPage;
