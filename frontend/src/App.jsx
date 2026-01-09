import { useState, useEffect } from 'react';
import MessageList from './components/MessageList';
import MessageDetail from './components/MessageDetail';
import GraphViewer from './components/GraphViewer';
import DecisionHistory from './components/DecisionHistory';
import { getMessages, getDecisions, resetDemo } from './api';

function App() {
  const [messages, setMessages] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [activeTab, setActiveTab] = useState('inbox'); // inbox, graph, history
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    loadMessages();
    loadDecisions();
  }, [refreshKey]);

  const loadMessages = async () => {
    try {
      const data = await getMessages();
      setMessages(data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const loadDecisions = async () => {
    try {
      const data = await getDecisions();
      setDecisions(data);
    } catch (error) {
      console.error('Error loading decisions:', error);
    }
  };

  const handleMessageSelect = (message) => {
    setSelectedMessage(message);
  };

  const handleDecisionComplete = () => {
    setRefreshKey(prev => prev + 1);
    setSelectedMessage(null);
  };

  const handleReset = async () => {
    if (window.confirm('Reset all decisions and start fresh? (Messages will remain)')) {
      try {
        await resetDemo();
        setRefreshKey(prev => prev + 1);
        setSelectedMessage(null);
        alert('Demo reset complete! You can now start fresh.');
      } catch (error) {
        console.error('Error resetting demo:', error);
        alert('Error resetting demo');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Inbox Context Graph
              </h1>
              <p className="text-sm text-gray-500">
                AI agent learning from human decisions
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                {decisions.length} decision{decisions.length !== 1 ? 's' : ''} captured
              </div>
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition"
              >
                Reset Demo
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-8">
            <button
              onClick={() => setActiveTab('inbox')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition ${
                activeTab === 'inbox'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Inbox
            </button>
            <button
              onClick={() => setActiveTab('graph')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition ${
                activeTab === 'graph'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Context Graph
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition ${
                activeTab === 'history'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Decision History
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'inbox' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <MessageList
              messages={messages}
              selectedMessage={selectedMessage}
              onMessageSelect={handleMessageSelect}
            />
            <MessageDetail
              message={selectedMessage}
              onDecisionComplete={handleDecisionComplete}
            />
          </div>
        )}

        {activeTab === 'graph' && (
          <GraphViewer key={refreshKey} />
        )}

        {activeTab === 'history' && (
          <DecisionHistory decisions={decisions} messages={messages} />
        )}
      </main>
    </div>
  );
}

export default App;

