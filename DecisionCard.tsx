import React from 'react';
import { Calendar, Users, FileText } from 'lucide-react';
import './DecisionCard.css';

interface DecisionProps {
    score: number;
    decision: {
        decision_title: string;
        decision_date: string;
        team: string;
        rationale: string[];
        alternatives: string[];
        outcome?: string;
        source_file: string;
    };
    context: string;
}

const DecisionCard: React.FC<DecisionProps> = ({ score, decision }) => {
    return (
        <div className="decision-card">
            <div className="card-header">
                <div className="meta-row">
                    <span className="team-badge">
                        <Users size={14} /> {decision.team}
                    </span>
                    <span className="date-badge">
                        <Calendar size={14} /> {decision.decision_date}
                    </span>
                    <span className="similarity-score" title="Relevance Score">
                        {Math.round(score * 100)}% Match
                    </span>
                </div>
                <h4>{decision.decision_title}</h4>
            </div>

            <div className="card-body">
                <div className="section">
                    <h5>Rationale</h5>
                    <ul className="rationale-list">
                        {Array.isArray(decision.rationale) ? (
                            decision.rationale.map((point, idx) => (
                                <li key={idx}>{point}</li>
                            ))
                        ) : (
                            <li>{decision.rationale}</li> // Fallback for old data
                        )}
                    </ul>
                </div>

                {decision.alternatives && decision.alternatives.length > 0 && (
                    <div className="section">
                        <h5>Alternatives Considered</h5>
                        <ul className="alt-list">
                            {decision.alternatives.map((alt, idx) => (
                                <li key={idx}>{alt}</li>
                            ))}
                        </ul>
                    </div>
                )}

                <div className="source-link">
                    <FileText size={14} />
                    <span style={{ marginRight: '4px' }}>Source:</span>
                    <a
                        href={`http://localhost:8000/documents/${decision.source_file}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#3b82f6', textDecoration: 'underline' }}
                    >
                        {decision.source_file}
                    </a>
                </div>
            </div>
        </div>
    );
};

export default DecisionCard;
