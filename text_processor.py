"""
Text processing utilities for handling large inputs
"""
import tiktoken
from typing import List, Dict

class TextProcessor:
    def __init__(self, chunk_size: int = 3000, overlap_size: int = 200):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split large text into overlapping chunks to maintain context
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at a sentence or paragraph
            if end < len(text):
                # Look for sentence endings within the last 200 characters
                search_start = max(end - 200, start)
                sentence_breaks = ['.', '!', '?', '\n\n']
                
                best_break = -1
                for i in range(end, search_start, -1):
                    if text[i] in sentence_breaks:
                        best_break = i + 1
                        break
                
                if best_break != -1:
                    end = best_break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.overlap_size
            if start >= len(text):
                break
        
        return chunks
    
    def summarize_chunks(self, chunks: List[str]) -> str:
        """
        Create a summary of chunked content for context preservation
        """
        if len(chunks) <= 1:
            return chunks[0] if chunks else ""
        
        summary_parts = []
        for i, chunk in enumerate(chunks):
            # Extract key points from each chunk
            lines = chunk.split('\n')
            key_lines = []
            
            for line in lines:
                line = line.strip()
                if line and (
                    line.startswith('- ') or 
                    line.startswith('* ') or
                    line.startswith('1.') or
                    line.startswith('2.') or
                    line.startswith('3.') or
                    len(line) < 100  # Short lines are likely key points
                ):
                    key_lines.append(line)
            
            if key_lines:
                summary_parts.append(f"Section {i+1}:\n" + '\n'.join(key_lines[:5]))  # Top 5 key points
            else:
                # Fallback: take first few sentences
                sentences = chunk.split('. ')
                summary_parts.append(f"Section {i+1}:\n" + '. '.join(sentences[:3]) + '.')
        
        return '\n\n'.join(summary_parts)
    
    def prepare_input(self, user_input: str) -> Dict[str, any]:
        """
        Prepare user input for processing by the multi-agent system
        """
        token_count = self.count_tokens(user_input)
        
        if token_count <= 2000:  # Small input, process directly
            return {
                'type': 'direct',
                'content': user_input,
                'token_count': token_count
            }
        else:  # Large input, chunk and summarize
            chunks = self.chunk_text(user_input)
            summary = self.summarize_chunks(chunks)
            
            return {
                'type': 'chunked',
                'original_content': user_input,
                'chunks': chunks,
                'summary': summary,
                'token_count': token_count,
                'chunk_count': len(chunks)
            }
    
    def process_input(self, user_input: str) -> Dict[str, any]:
        """
        Process user input for the multi-agent system (alias for prepare_input)
        """
        result = self.prepare_input(user_input)
        
        # Convert to expected format for orchestrator
        if result['type'] == 'direct':
            return {
                'processing_type': 'direct',
                'content': result['content'],
                'token_count': result['token_count']
            }
        else:
            return {
                'processing_type': 'chunked',
                'content': result['summary'],
                'chunks': result['chunks'],
                'token_count': result['token_count'],
                'chunk_count': result['chunk_count']
            }
