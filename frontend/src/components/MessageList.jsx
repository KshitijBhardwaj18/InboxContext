import { formatDistanceToNow } from '../utils';

const MessageList = ({ messages, selectedMessage, onMessageSelect }) => {
  const getSenderTypeBadge = (type) => {
    const badges = {
      investor: 'bg-purple-100 text-purple-800',
      sales: 'bg-blue-100 text-blue-800',
      support: 'bg-green-100 text-green-800',
    };
    return badges[type] || 'bg-gray-100 text-gray-800';
  };

  const getChannelIcon = (channel) => {
    const icons = {
      email: '📧',
      slack: '💬',
      discord: '🎮',
    };
    return icons[channel] || '📬';
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Inbox</h2>
        <p className="text-sm text-gray-500 mt-1">
          {messages.length} messages • Click to get AI suggestion
        </p>
      </div>
      <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
        {messages.length === 0 ? (
          <div className="px-6 py-12 text-center text-gray-500">
            No messages in inbox
          </div>
        ) : (
          messages.map((message) => (
            <button
              key={message.id}
              onClick={() => onMessageSelect(message)}
              className={`w-full text-left px-6 py-4 hover:bg-gray-50 transition ${
                selectedMessage?.id === message.id ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="text-2xl mt-1">{getChannelIcon(message.channel)}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-gray-900">
                      {message.sender_name}
                    </span>
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getSenderTypeBadge(
                        message.sender_type
                      )}`}
                    >
                      {message.sender_type}
                    </span>
                  </div>
                  {message.subject && (
                    <div className="text-sm font-medium text-gray-900 mb-1">
                      {message.subject}
                    </div>
                  )}
                  <div className="text-sm text-gray-600 line-clamp-2">
                    {message.content}
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    {formatDistanceToNow(message.timestamp)}
                  </div>
                </div>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
};

export default MessageList;

