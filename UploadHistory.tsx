import React, { useEffect, useState } from 'react';
import { Clock, File, User } from 'lucide-react';
import axios from 'axios';
import './UploadHistory.css';

interface UploadedFile {
    filename: string;
    upload_time: string;
    uploaded_by: string;
}

const UploadHistory: React.FC = () => {
    const [files, setFiles] = useState<UploadedFile[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchHistory = async () => {
        try {
            const response = await axios.get('http://localhost:8000/uploads/');
            setFiles(response.data);
        } catch (error) {
            console.error("Failed to load history", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    if (loading) return null;
    if (files.length === 0) return null;

    return (
        <div className="history-container">
            <h4>Upload History</h4>
            <div className="history-list">
                {files.map((file, idx) => (
                    <div key={idx} className="history-item">
                        <div className="file-info">
                            <File size={16} className="icon" />
                            <span className="filename">{file.filename}</span>
                        </div>
                        <div className="meta-info">
                            <span className="meta-tag">
                                <Clock size={12} /> {file.upload_time}
                            </span>
                            <span className="meta-tag">
                                <User size={12} /> {file.uploaded_by}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UploadHistory;
