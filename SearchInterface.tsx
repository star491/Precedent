import React, { useState } from 'react';
import { Search } from 'lucide-react';
import axios from 'axios';
import DecisionCard from './DecisionCard';
import './SearchInterface.css';

interface SearchResult {
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

const SearchInterface: React.FC = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [teamFilter, setTeamFilter] = useState('');
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // Use relative path so Vite proxy handles it (works on Ngrok/Mobile)
    const constant_api_base = "";

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setErrorMsg(null);
        try {
            const response = await axios.post(`${constant_api_base}/search/`, {
                query: query,
                filter_team: teamFilter || null,
                limit: 10
            });
            setResults(response.data);
            if (response.data.length === 0) {
                setErrorMsg("No results found in memory.");
            }
        } catch (error) {
            console.error("Search failed", error);
            setErrorMsg("Failed to connect to Brain (Backend). Is it running?");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-container">
            <form onSubmit={handleSearch} className="search-box">
                <Search className="search-icon" size={20} />
                <input
                    type="text"
                    placeholder="Ask Precedent about past decisions (e.g., 'Why did we choose Postgres?')"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />

                <select
                    value={teamFilter}
                    onChange={(e) => setTeamFilter(e.target.value)}
                    className="filter-select"
                >
                    <option value="">All Teams</option>
                    <option value="Engineering">Engineering</option>
                    <option value="Product">Product</option>
                    <option value="Design">Design</option>
                </select>

                <button type="submit" disabled={loading}>
                    {loading ? 'Thinking...' : 'Search Memory'}
                </button>
            </form>

            {errorMsg && (
                <div style={{
                    padding: '1rem',
                    marginBottom: '1rem',
                    background: '#fee2e2',
                    color: '#dc2626',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    {errorMsg}
                </div>
            )}

            <div className="results-list">
                {results.map((result, idx) => (
                    <DecisionCard key={idx} {...result} />
                ))}
            </div>
        </div>
    );
};

export default SearchInterface;
