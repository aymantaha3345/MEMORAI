import re
from typing import List, Dict, Any

def count_tokens(text: str) -> int:
    """Simple token counting - roughly estimate using word splitting"""
    # This is a very rough estimation
    # In a real implementation, use tiktoken or similar
    return len(re.findall(r'\b\w+\b', text))

def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords from text"""
    # Simple keyword extraction - in reality, would use NLP techniques
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count frequency and return top keywords
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:num_keywords]]

def sanitize_input(text: str) -> str:
    """Sanitize input text"""
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>\[\]{}]', '', text)
    return sanitized.strip()