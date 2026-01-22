import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';
import './UploadZone.css';
import UploadHistory from './UploadHistory';

const UploadZone: React.FC = () => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const constant_api_base = "http://localhost:8000";

    const uploadFile = async (file: File) => {
        if (!file) return;

        setIsUploading(true);
        setUploadStatus('idle');

        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post(`${constant_api_base}/ingest/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setUploadStatus('success');
            setRefreshTrigger(prev => prev + 1);
        } catch (error) {
            console.error("Upload failed", error);
            setUploadStatus('error');
        } finally {
            setIsUploading(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            uploadFile(e.target.files[0]);
        }
    };

    return (
        <div className="upload-section">
            <h3>Ingest Operational Artifacts</h3>
            <div
                className={`drop-zone ${isDragging ? 'dragging' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                    accept=".pdf,.txt,.md"
                />

                {isUploading ? (
                    <div className="status-content">
                        <div className="spinner"></div>
                        <p>Analyzing decision nodes...</p>
                    </div>
                ) : uploadStatus === 'success' ? (
                    <div className="status-content success">
                        <CheckCircle className="icon-large" />
                        <p>Ingestion Complete. Memory Updated.</p>
                    </div>
                ) : uploadStatus === 'error' ? (
                    <div className="status-content error">
                        <AlertCircle className="icon-large" style={{ color: '#ef4444' }} />
                        <p>Upload Failed. Please try again.</p>
                    </div>
                ) : (
                    <div className="default-content">
                        <Upload className="icon-large" />
                        <p>Drag & drop project docs, meeting notes, or emails</p>
                        <span className="sub-text">Supports PDF, TXT</span>
                    </div>
                )}
            </div>

            <UploadHistory key={refreshTrigger} />
        </div>
    );
};

export default UploadZone;
