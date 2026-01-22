import { useState } from 'react'
import { BookOpen } from 'lucide-react'
import UploadZone from './components/UploadZone'
import SearchInterface from './components/SearchInterface'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState<'search' | 'upload'>('search');

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <BookOpen className="logo-icon" />
          <h1>Precedent</h1>
        </div>
        <p className="tagline">Institutional Decision Memory</p>
      </header>

      <main className="main-content">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            Search Memory
          </button>
          <button
            className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            Ingest Data
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'search' ? <SearchInterface /> : <UploadZone />}
        </div>
      </main>

      <footer className="app-footer">
        <p>Precedent v0.1 • Powered by Qdrant</p>
      </footer>
    </div>
  )
}

export default App
