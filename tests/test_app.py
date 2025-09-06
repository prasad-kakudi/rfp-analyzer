import unittest
import tempfile
import os
from app import app, RFPAnalyzer

class RFPAnalyzerTestCase(unittest.TestCase):
    """Test cases for RFP Analyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        
    def test_home_page(self):
        """Test home page loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'RFP Document Analyzer', rv.data)
    
    def test_file_upload_no_file(self):
        """Test file upload with no file"""
        rv = self.app.post('/upload', data={})
        self.assertEqual(rv.status_code, 302)  # Redirect
    
    def test_analyzer_text_extraction(self):
        """Test text extraction functionality"""
        analyzer = RFPAnalyzer()
        
        # Test with sample text
        sample_text = "This is a test RFP document with $50,000 funding available."
        amounts = analyzer.parse_financial_requirements(sample_text)
        self.assertTrue(any('50,000' in str(amount) for amount in amounts))
    
    def test_currency_extraction(self):
        """Test currency amount extraction"""
        from utils import extract_currency_amounts
        
        text = "Funding available: $25,000 to $100,000 per grant"
        amounts = extract_currency_amounts(text)
        self.assertTrue(len(amounts) >= 2)
    
    def test_date_extraction(self):
        """Test date extraction"""
        from utils import extract_dates
        
        text = "Application deadline: December 15, 2024"
        dates = extract_dates(text)
        self.assertTrue(len(dates) >= 1)
    
    def test_prompt_generator_page(self):
        """Test prompt generator page"""
        rv = self.app.get('/generate_prompt')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Prompt Generator', rv.data)

if __name__ == '__main__':
    unittest.main()

