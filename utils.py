import os
import re
from typing import List, Dict, Optional
from werkzeug.utils import secure_filename
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def sanitize_filename(filename: str) -> str:
    """Sanitize uploaded filename"""
    # Remove or replace potentially dangerous characters
    filename = secure_filename(filename)
    # Add timestamp to avoid conflicts
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    return f"{timestamp}_{name}{ext}"

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,;:()$%/]', '', text)
    return text.strip()

def extract_currency_amounts(text: str) -> List[str]:
    """Extract currency amounts from text"""
    patterns = [
        r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|billion|thousand|k|m|b))?',
        r'USD?\s*[\d,]+(?:\.\d{2})?',
        r'dollars?\s*[\d,]+(?:\.\d{2})?',
    ]
    
    amounts = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            amounts.append(match.group().strip())
    
    return list(set(amounts))  # Remove duplicates

def extract_dates(text: str) -> List[str]:
    """Extract dates from text"""
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY or MM/DD/YY
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # MM-DD-YYYY or MM-DD-YY
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b',
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            dates.append(match.group().strip())
    
    return list(set(dates))

def calculate_reading_time(text: str) -> int:
    """Calculate estimated reading time in minutes"""
    words = len(text.split())
    # Average reading speed: 200-250 words per minute
    reading_time = max(1, words // 225)
    return reading_time

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes"""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)
