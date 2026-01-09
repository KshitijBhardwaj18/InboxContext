const DecisionHistory = ({ decisions, messages }) => {
  const getMessageForDecision = (messageId) => {
    return messages.find((m) => m.id === messageId);
  };

  const wasOverride = (decision) => {
    return (
      decision.agent_suggestion.action !== decision.human_action.action ||
      decision.agent_suggestion.tone !== decision.human_action.tone
    );
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">
          Decision History
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          {decisions.length} decision{decisions.length !== 1 ? "s" : ""}{" "}
          captured
        </p>
      </div>

      {decisions.length === 0 ? (
        <div className="px-6 py-12 text-center text-gray-500">
          <div className="text-4xl mb-4">📊</div>
          <p className="text-lg font-medium">No decisions yet</p>
          <p className="text-sm mt-2">
            Start making decisions in the inbox to see them here
          </p>
        </div>
      ) : (
        <div className="divide-y divide-gray-200">
          {decisions.map((decision) => {
            const message = getMessageForDecision(decision.message_id);
            const override = wasOverride(decision);

            return (
              <div key={decision.decision_id} className="px-6 py-4">
                <div className="flex items-start gap-4">
                  <div className="text-2xl">{override ? "✏️" : "✅"}</div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-semibold text-gray-900">
                        {message?.sender_name || "Unknown"}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(decision.timestamp).toLocaleString()}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-3">
                      <div className="bg-blue-50 rounded-lg p-3">
                        <div className="text-xs font-medium text-blue-900 mb-1">
                          🤖 Agent Suggested
                        </div>
                        <div className="text-sm text-blue-800">
                          {decision.agent_suggestion.action} •{" "}
                          {decision.agent_suggestion.tone}
                        </div>
                      </div>
                      <div
                        className={`rounded-lg p-3 ${
                          override ? "bg-orange-50" : "bg-green-50"
                        }`}
                      >
                        <div
                          className={`text-xs font-medium mb-1 ${
                            override ? "text-orange-900" : "text-green-900"
                          }`}
                        >
                          👤 Human Chose
                        </div>
                        <div
                          className={`text-sm ${
                            override ? "text-orange-800" : "text-green-800"
                          }`}
                        >
                          {decision.human_action.action} •{" "}
                          {decision.human_action.tone}
                        </div>
                      </div>
                    </div>

                    <div className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
                      <span className="font-medium">Reasoning: </span>
                      {decision.why}
                    </div>

                    {decision.context_used.similar_decisions.length > 0 && (
                      <div className="mt-2 text-xs text-purple-600 bg-purple-50 inline-block px-2 py-1 rounded">
                        ✨ Used {decision.context_used.similar_decisions.length}{" "}
                        precedent
                        {decision.context_used.similar_decisions.length !== 1
                          ? "s"
                          : ""}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DecisionHistory;
