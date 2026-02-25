/**
 * Ideas List Page - View user's ideas or all ideas (admin)
 */
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getMyIdeas, Idea } from '../../api/ideas';
import './IdeasListPage.css';

const IdeasListPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
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
    const fetchIdeas = async () => {
      try {
        setLoading(true);
        const response = await getMyIdeas();
        setIdeas(response.items);
        setError('');
      } catch (err) {
        console.error('Error fetching ideas:', err);
        setError('Failed to load ideas. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchIdeas();
  }, []);

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
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="ideas-list-page">
        <div className="ideas-container">
          <div className="loading-state">Loading ideas...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="ideas-list-page">
      <div className="ideas-container">
        <div className="ideas-header">
          <div>
            <button 
              className="btn-back"
              onClick={() => navigate('/dashboard')}
            >
              ← Back to Dashboard
            </button>
            <h1 className="ideas-title">My Ideas</h1>
            <p className="ideas-subtitle">View and manage your submitted innovation ideas</p>
          </div>
          <button 
            className="btn-submit-idea"
            onClick={() => navigate('/ideas/submit')}
          >
            + Submit New Idea
          </button>
        </div>

        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {ideas.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">💡</div>
            <h2>No ideas yet</h2>
            <p>Start contributing by submitting your first innovation idea!</p>
            <button 
              className="btn-submit-idea"
              onClick={() => navigate('/ideas/submit')}
            >
              Submit Your First Idea
            </button>
          </div>
        ) : (
          <div className="ideas-grid">
            {ideas.map((idea) => (
              <div 
                key={idea.id} 
                className="idea-card"
                onClick={() => navigate(`/ideas/${idea.id}`)}
              >
                <div className="idea-card-header">
                  <span className={getStatusBadgeClass(idea.status)}>
                    {idea.status.replace('_', ' ')}
                  </span>
                  <span className="idea-date">{formatDate(idea.created_at)}</span>
                </div>
                
                <h3 className="idea-card-title">{idea.title}</h3>
                
                <p className="idea-card-description">
                  {idea.description.length > 150 
                    ? `${idea.description.substring(0, 150)}...` 
                    : idea.description}
                </p>
                
                <div className="idea-card-footer">
                  <span className="idea-category">
                    📁 {idea.category.name}
                  </span>
                  {idea.attachment && (
                    <span className="idea-attachment">
                      📎 Attachment
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IdeasListPage;
