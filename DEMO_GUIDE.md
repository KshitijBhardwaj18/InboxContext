# Demo Guide: Inbox Context Graph

## Overview

This guide will walk you through demonstrating the key feature: **the agent learns from human decisions and improves its suggestions over time**.

## Setup

1. Make sure both backend and frontend are running
2. Visit http://localhost:5173
3. Click "Reset Demo" to start fresh

## Demo Script: Before vs After

### Phase 1: Before (No Precedent)

**Goal**: Show that the agent uses only basic heuristics without precedent.

1. **Click on an investor message** (e.g., "Sarah Chen" or "Jessica Wong")
   - Note the agent's suggestion
   - Note the reasoning: "No precedent found. Using default logic..."
   - The agent suggests based ONLY on sender type

2. **Accept or Override** - Choose your preference
   - Example: Agent suggests "reply_now + neutral"
   - You might override to "reply_now + warm" (investors deserve warmth!)
   - Click "Confirm Decision"

3. **Click on another investor message**
   - Still no precedent (need more data)
   - Agent still using basic logic

4. **Repeat for 2-3 more investor messages**
   - Each time, choose "warm" tone for investors
   - This builds your precedent

### Phase 2: After (With Precedent)

**Goal**: Show the agent has learned from your decisions.

5. **Click on a NEW investor message**
   - 🎉 Notice the change!
   - Agent now suggests: "reply_now + **warm**"
   - Reasoning: "Based on 3 prior investor message(s), you usually chose 'reply_now' with 'warm' tone."
   - Badge shows: "✨ Based on 3 similar decisions"

6. **Try with different sender types**
   - Build precedent for "support" messages → always warm
   - Build precedent for "sales" messages → usually ignore
   - Each sender type learns independently

### Phase 3: Graph Visualization

7. **Click "Context Graph" tab**
   - See the visual representation of decisions
   - Different node types (messages, decisions, actions, tones)
   - Red animated edges = precedent links
   - Click on a decision node to see details

8. **Click "Decision History" tab**
   - See all captured decisions
   - Green checkmark = accepted suggestion
   - Orange pencil = override
   - See how precedent count grows

## Key Talking Points

### 1. Learning from Decisions
"The agent doesn't just make suggestions—it learns from every human decision. When I consistently choose 'warm' tone for investors, the agent picks up on that pattern."

### 2. Hybrid Retrieval
"Behind the scenes, the system uses hybrid retrieval: semantic similarity to find related messages, plus structured filtering by sender type. This means it learns context-specific patterns."

### 3. The Graph
"Every decision becomes a node in the context graph. The graph captures not just what you decided, but WHY—the precedent that informed it. This creates an ever-growing knowledge base."

### 4. Precedent Awareness
"Notice how the reasoning changes. Early on: 'No precedent found.' After a few decisions: 'Based on 5 prior messages...' The agent explicitly tells you it's learning."

### 5. Overrides Are Features
"Overrides aren't failures—they're teaching moments. When I override the agent, I'm training it on my preferences. The system treats both acceptances and overrides as valuable learning data."

## Reset & Repeat

- Click "Reset Demo" to clear all decisions
- Messages remain, but learning resets
- Perfect for showing the before/after contrast again

## Advanced Demo: Multi-Type Learning

1. Build precedent: investors → warm, immediate
2. Build precedent: sales → ignore
3. Build precedent: support → warm, immediate
4. Show that the agent handles each type differently
5. Emphasize: "This is like having an assistant that learns your communication style across different relationship types."

## What This Demonstrates

✅ AI agent with base logic  
✅ Human-in-the-loop decision capture  
✅ Precedent-based learning  
✅ Hybrid retrieval (semantic + structured)  
✅ Context graph visualization  
✅ Visible behavior improvement  
✅ Decision trace as canonical object  
✅ Before/after demonstration  

This is a **real system** showing how context layers can make AI agents more personalized and effective over time.

