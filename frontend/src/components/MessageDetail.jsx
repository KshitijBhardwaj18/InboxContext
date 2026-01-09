import { useState, useEffect } from "react";
import { getAgentSuggestion, createDecision } from "../api";

const MessageDetail = ({ message, onDecisionComplete }) => {
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState(null);
  const [humanAction, setHumanAction] = useState("");
  const [humanTone, setHumanTone] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (message) {
      loadSuggestion();
    } else {
      setSuggestion(null);
      setHumanAction("");
      setHumanTone("");
    }
  }, [message]);

  const loadSuggestion = async () => {
    setLoading(true);
    try {
      const data = await getAgentSuggestion(message.id);
      setSuggestion(data);
      // Pre-populate with agent suggestion
      setHumanAction(data.action);
      setHumanTone(data.tone);
    } catch (error) {
      console.error("Error loading suggestion:", error);
      alert("Error getting AI suggestion");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!humanAction || !humanTone) {
      alert("Please select action and tone");
      return;
    }

    setSubmitting(true);
    try {
      const decisionData = {
        message_id: message.id,
        agent_suggestion: {
          action: suggestion.action,
          tone: suggestion.tone,
        },
        human_action: {
          action: humanAction,
          tone: humanTone,
        },
        context_used: {
          sender_type: message.sender_type,
          similar_decisions: suggestion.similar_decisions,
        },
        why: suggestion.reasoning,
      };

      await createDecision(decisionData);
      alert("Decision captured! The agent will learn from this.");
      onDecisionComplete();
    } catch (error) {
      console.error("Error creating decision:", error);
      alert("Error capturing decision");
    } finally {
      setSubmitting(false);
    }
  };

  if (!message) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
        <div className="text-4xl mb-4">👋</div>
        <p className="text-lg font-medium">Select a message to start</p>
        <p className="text-sm mt-2">
          Click any message in your inbox to see AI agent suggestions
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Message Content */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-start gap-3 mb-4">
          <div className="text-3xl">
            {message.channel === "email"
              ? "📧"
              : message.channel === "slack"
              ? "💬"
              : "🎮"}
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900">
              {message.sender_name}
            </h2>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-sm text-gray-500">
                {message.sender_type}
              </span>
              <span className="text-gray-300">•</span>
              <span className="text-sm text-gray-500">{message.channel}</span>
            </div>
          </div>
        </div>
        {message.subject && (
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            {message.subject}
          </h3>
        )}
        <div className="text-gray-700 whitespace-pre-wrap">
          {message.content}
        </div>
      </div>

      {/* AI Suggestion */}
      {loading ? (
        <div className="px-6 py-8 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="text-sm text-gray-500 mt-2">Getting AI suggestion...</p>
        </div>
      ) : suggestion ? (
        <div className="px-6 py-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-2 mb-2">
              <span className="text-xl">🤖</span>
              <div className="flex-1">
                <div className="font-semibold text-blue-900 mb-1">
                  AI Agent Suggests:
                </div>
                <div className="text-sm text-blue-800 mb-2">
                  <span className="font-medium">Action:</span>{" "}
                  {suggestion.action} •
                  <span className="font-medium"> Tone:</span> {suggestion.tone}
                </div>
                <div className="text-sm text-blue-700">
                  {suggestion.reasoning}
                </div>
                {suggestion.precedent_count > 0 && (
                  <div className="text-xs text-blue-600 mt-2 bg-blue-100 inline-block px-2 py-1 rounded">
                    ✨ Based on {suggestion.precedent_count} similar decision
                    {suggestion.precedent_count !== 1 ? "s" : ""}
                  </div>
                )}
                {suggestion.draft_response && (
                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <div className="text-xs font-medium text-blue-900 mb-1">
                      📝 AI Draft:
                    </div>
                    <div className="text-sm text-blue-800 bg-white p-2 rounded border border-blue-100 italic">
                      "{suggestion.draft_response}"
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Human Override */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Action
              </label>
              <div className="grid grid-cols-3 gap-2">
                {["reply_now", "reply_later", "ignore"].map((action) => (
                  <button
                    key={action}
                    onClick={() => setHumanAction(action)}
                    className={`px-4 py-2 rounded-lg border-2 text-sm font-medium transition ${
                      humanAction === action
                        ? "border-blue-500 bg-blue-50 text-blue-700"
                        : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    {action.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Tone
              </label>
              <div className="grid grid-cols-3 gap-2">
                {["neutral", "warm", "formal"].map((tone) => (
                  <button
                    key={tone}
                    onClick={() => setHumanTone(tone)}
                    className={`px-4 py-2 rounded-lg border-2 text-sm font-medium transition ${
                      humanTone === tone
                        ? "border-blue-500 bg-blue-50 text-blue-700"
                        : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    {tone}
                  </button>
                ))}
              </div>
            </div>

            {/* Decision Summary */}
            {humanAction && humanTone && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div className="text-sm text-gray-700">
                  {humanAction === suggestion.action &&
                  humanTone === suggestion.tone ? (
                    <div className="flex items-center gap-2 text-green-700">
                      <span>✅</span>
                      <span className="font-medium">
                        Accepting AI suggestion
                      </span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-orange-700">
                      <span>✏️</span>
                      <span className="font-medium">
                        Overriding AI suggestion
                      </span>
                    </div>
                  )}
                  <div className="mt-2 text-xs text-gray-600">
                    Agent learns from both acceptances and overrides to improve
                    future suggestions.
                  </div>
                </div>
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={submitting || !humanAction || !humanTone}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {submitting ? "Capturing..." : "Confirm Decision"}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default MessageDetail;
