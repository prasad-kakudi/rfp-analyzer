import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict

class AnalysisDatabase:
    """Simple SQLite database for storing analysis results"""
    
    def __init__(self, db_path: str = 'rfp_analysis.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    title TEXT,
                    organization TEXT,
                    analysis_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_analysis(self, filename: str, title: str, organization: str, analysis_data: Dict) -> int:
        """Save analysis results to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO analyses (filename, title, organization, analysis_data)
                VALUES (?, ?, ?, ?)
            ''', (filename, title, organization, json.dumps(analysis_data)))
            conn.commit()
            return cursor.lastrowid
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict]:
        """Retrieve analysis by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT * FROM analyses WHERE id = ?
            ''', (analysis_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'filename': row[1],
                    'title': row[2],
                    'organization': row[3],
                    'analysis_data': json.loads(row[4]),
                    'created_at': row[5]
                }
        return None
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get recent analyses"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, filename, title, organization, created_at 
                FROM analyses 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            return [
                {
                    'id': row[0],
                    'filename': row[1],
                    'title': row[2],
                    'organization': row[3],
                    'created_at': row[4]
                }
                for row in cursor.fetchall()
            ]

