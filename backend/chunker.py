"""Message chunking for better retrieval"""
from typing import List, Dict
import re


class MessageChunker:
    """Chunk messages into semantic units for vector storage"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """Initialize chunker
        
        Args:
            chunk_size: Maximum words per chunk
            overlap: Overlapping words between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_message(self, message: Dict) -> List[Dict]:
        """Chunk a single message into smaller pieces
        
        Args:
            message: Dict with id, content, sender_name, sender_type, etc.
            
        Returns:
            List of chunk dicts with text and metadata
        """
        # Combine subject and content
        subject = message.get("subject", "")
        content = message.get("content", "")
        
        full_text = f"From: {message['sender_name']} ({message['sender_type']})\n"
        if subject:
            full_text += f"Subject: {subject}\n"
        full_text += f"Message: {content}"
        
        # For short messages, return as single chunk
        words = full_text.split()
        if len(words) <= self.chunk_size:
            return [{
                "text": full_text,
                "chunk_id": f"{message['id']}_0",
                "metadata": {
                    "message_id": message["id"],
                    "sender_name": message["sender_name"],
                    "sender_type": message["sender_type"],
                    "channel": message.get("channel", "email"),
                    "timestamp": str(message.get("timestamp", "")),
                    "chunk_index": 0,
                    "total_chunks": 1
                }
            }]
        
        # Split into overlapping chunks
        chunks = []
        chunk_index = 0
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "chunk_id": f"{message['id']}_{chunk_index}",
                "metadata": {
                    "message_id": message["id"],
                    "sender_name": message["sender_name"],
                    "sender_type": message["sender_type"],
                    "channel": message.get("channel", "email"),
                    "timestamp": str(message.get("timestamp", "")),
                    "chunk_index": chunk_index,
                    "total_chunks": -1  # Updated below
                }
            })
            chunk_index += 1
        
        # Update total_chunks
        for chunk in chunks:
            chunk["metadata"]["total_chunks"] = len(chunks)
        
        return chunks
    
    def chunk_conversation(self, messages: List[Dict]) -> List[Dict]:
        """Chunk multiple messages
        
        Args:
            messages: List of message dicts
            
        Returns:
            List of all chunks from all messages
        """
        all_chunks = []
        for message in messages:
            chunks = self.chunk_message(message)
            all_chunks.extend(chunks)
        return all_chunks
    
    def chunk_by_sentences(self, text: str, max_sentences: int = 5) -> List[str]:
        """Alternative: chunk by sentences
        
        Args:
            text: Text to chunk
            max_sentences: Maximum sentences per chunk
            
        Returns:
            List of text chunks
        """
        # Split by sentence boundaries
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        for i in range(0, len(sentences), max_sentences):
            chunk_sentences = sentences[i:i + max_sentences]
            chunk = ". ".join(chunk_sentences) + "."
            chunks.append(chunk)
        
        return chunks


# Global instance
_chunker = None


def get_chunker() -> MessageChunker:
    """Get or create chunker singleton"""
    global _chunker
    if _chunker is None:
        _chunker = MessageChunker()
    return _chunker

