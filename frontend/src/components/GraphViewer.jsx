import { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { getGraph, getDecisions } from '../api';

const nodeColors = {
  message: '#e0e7ff',
  decision: '#dbeafe',
  action: '#fef3c7',
  tone: '#fed7aa',
  sender_type: '#d1fae5',
};

const GraphViewer = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState(null);
  const [decisions, setDecisions] = useState([]);

  useEffect(() => {
    loadGraph();
  }, []);

  const loadGraph = async () => {
    setLoading(true);
    try {
      const [graphData, decisionsData] = await Promise.all([
        getGraph(),
        getDecisions(),
      ]);
      
      setDecisions(decisionsData);

      // Convert to ReactFlow format
      const flowNodes = graphData.nodes.map((node, index) => ({
        id: node.id,
        type: 'default',
        data: { 
          label: node.label,
          nodeType: node.type,
        },
        position: calculatePosition(node, index, graphData.nodes.length),
        style: {
          background: nodeColors[node.type] || '#f3f4f6',
          border: '2px solid #6b7280',
          borderRadius: '8px',
          padding: '10px',
          fontSize: '12px',
          fontWeight: '500',
        },
      }));

      const flowEdges = graphData.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: edge.type === 'based_on_precedent' ? 'default' : 'smoothstep',
        animated: edge.type === 'based_on_precedent',
        style: {
          stroke: edge.type === 'based_on_precedent' ? '#ef4444' : '#6b7280',
          strokeWidth: edge.type === 'based_on_precedent' ? 2 : 1,
        },
        label: edge.type === 'based_on_precedent' ? 'precedent' : '',
        labelStyle: { fontSize: '10px', fill: '#ef4444' },
      }));

      setNodes(flowNodes);
      setEdges(flowEdges);
    } catch (error) {
      console.error('Error loading graph:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculatePosition = (node, index, total) => {
    // Simple circular layout
    const radius = 250;
    const angle = (index / total) * 2 * Math.PI;
    
    // Group by type for better layout
    const typeOffsets = {
      message: { x: 0, y: -100 },
      decision: { x: 0, y: 0 },
      action: { x: 200, y: 0 },
      tone: { x: 200, y: 100 },
      sender_type: { x: -200, y: 0 },
    };

    const offset = typeOffsets[node.type] || { x: 0, y: 0 };
    
    return {
      x: Math.cos(angle) * radius + 400 + offset.x,
      y: Math.sin(angle) * radius + 300 + offset.y,
    };
  };

  const onNodeClick = useCallback((event, node) => {
    if (node.data.nodeType === 'decision') {
      // Find the decision details
      const decisionId = node.id.replace('dec_', '');
      const decision = decisions.find(d => d.decision_id.startsWith(decisionId));
      setSelectedNode(decision);
    } else {
      setSelectedNode(null);
    }
  }, [decisions]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="text-sm text-gray-500 mt-2">Loading context graph...</p>
      </div>
    );
  }

  if (nodes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
        <div className="text-4xl mb-4">🕸️</div>
        <p className="text-lg font-medium">No decisions yet</p>
        <p className="text-sm mt-2">
          Make some decisions in the inbox to build your context graph
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Context Graph</h3>
            <p className="text-sm text-gray-500">
              {nodes.length} nodes • {edges.length} edges
            </p>
          </div>
          <div className="flex gap-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded" style={{ background: nodeColors.message }}></div>
              <span>Message</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded" style={{ background: nodeColors.decision }}></div>
              <span>Decision</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded" style={{ background: nodeColors.action }}></div>
              <span>Action</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded" style={{ background: nodeColors.tone }}></div>
              <span>Tone</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded" style={{ background: nodeColors.sender_type }}></div>
              <span>Sender Type</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow" style={{ height: '600px' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      {selectedNode && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Decision Details</h3>
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-gray-700">Agent Suggested:</span>
              <p className="text-sm text-gray-600">
                {selectedNode.agent_suggestion.action} • {selectedNode.agent_suggestion.tone}
              </p>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-700">Human Chose:</span>
              <p className="text-sm text-gray-600">
                {selectedNode.human_action.action} • {selectedNode.human_action.tone}
              </p>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-700">Reasoning:</span>
              <p className="text-sm text-gray-600">{selectedNode.why}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-700">Timestamp:</span>
              <p className="text-sm text-gray-600">
                {new Date(selectedNode.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GraphViewer;

