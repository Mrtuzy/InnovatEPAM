/**
 * Submit Idea Page - Protected route for submitters and admins
 */
import React from 'react';
import IdeaSubmissionForm from '../../components/ideas/IdeaSubmissionForm';
import './SubmitIdeaPage.css';

const SubmitIdeaPage: React.FC = () => {
  return (
    <div className="submit-idea-page">
      <div className="submit-idea-container">
        <div className="submit-idea-header">
          <h1 className="submit-idea-title">Submit Your Idea</h1>
          <p className="submit-idea-description">
            Share your innovative ideas with the team. Provide detailed information about your proposal,
            select the appropriate category, and optionally attach supporting documents.
          </p>
        </div>

        <div className="submit-idea-guidelines">
          <h2 className="guidelines-title">Guidelines</h2>
          <ul className="guidelines-list">
            <li>
              <strong>Be Specific:</strong> Clearly describe the problem and your proposed solution
            </li>
            <li>
              <strong>Be Detailed:</strong> Include expected benefits, implementation steps, and potential challenges
            </li>
            <li>
              <strong>Be Original:</strong> Ensure your idea hasn't been submitted before
            </li>
            <li>
              <strong>Be Professional:</strong> Use clear, professional language
            </li>
            <li>
              <strong>Attach Documentation:</strong> Include mockups, diagrams, or research to support your idea
            </li>
          </ul>
        </div>

        <IdeaSubmissionForm />
      </div>
    </div>
  );
};

export default SubmitIdeaPage;
