"""
Configuration settings for the Multi-Agent Project Refiner AI System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Model Settings
    GPT_MODEL = "gpt-4-turbo-preview"  # GPT-4.1
    GEMINI_MODEL = "gemini-1.5-flash"
    
    # System Settings
    MAX_ITERATIONS = 3
    CHUNK_SIZE = 3000  # Characters per chunk for large inputs
    OVERLAP_SIZE = 200  # Overlap between chunks to maintain context
    
    # Temperature settings for different phases
    STRATEGIST_TEMPERATURE = 0.7
    REFINER_TEMPERATURE = 0.8
    
    @classmethod
    def validate_config(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        if not cls.OPENAI_API_KEY:
            missing_keys.append('OPENAI_API_KEY')
        if not cls.GEMINI_API_KEY:
            missing_keys.append('GEMINI_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True
