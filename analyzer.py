from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
import PyPDF2
import docx
from datetime import datetime
import re
from werkzeug.utils import secure_filename
#import openai
from typing import Dict, List, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class RFPAnalyzer:
    def __init__(self):
        self.requirements_template = {
            'eligibility': [],
            'geographic': [],
            'impact': [],
            'financial': [],
            'timeline': [],
            'documents': []
        }
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from uploaded file based on extension"""
        text = ""
        file_extension = file_path.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            
            elif file_extension == 'docx':
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            
            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            
        return text
    
    def parse_financial_requirements(self, text: str) -> List[str]:
        """Extract financial requirements from RFP text"""
        financial_requirements = []
        
        # Common patterns for financial requirements
        patterns = [
            r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?',  # Dollar amounts
            r'(?:minimum|maximum|range).*?(?:\$[\d,]+|\d+%)',
            r'budget.*?(?:\$[\d,]+|\d+%)',
            r'matching.*?funds?',
            r'(?:cannot exceed|must not exceed).*?(?:\$[\d,]+|\d+%)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 50)
                context = text[context_start:context_end].strip()
                if context and context not in financial_requirements:
                    financial_requirements.append(context)
        
        return financial_requirements[:5]  # Limit to top 5 matches
    
    def parse_timeline(self, text: str) -> List[str]:
        """Extract timeline and deadline information"""
        timeline_items = []
        
        # Patterns for dates and deadlines
        date_patterns = [
            r'(?:deadline|due|submit|application).*?(?:by|on|before).*?(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\w+ \d{1,2}, \d{4})',
            r'(?:award|announcement|notification).*?(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\w+ \d{1,2}, \d{4})',
            r'(?:program period|grant period|project period).*?(?:\d{4}.*?\d{4})',
            r'(?:reporting|report).*?(?:due|deadline).*?(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\w+ \d{1,2}, \d{4})',
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                timeline_items.append(match.group().strip())
        
        return list(set(timeline_items))[:10]  # Remove duplicates and limit
    
    def parse_eligibility(self, text: str) -> List[str]:
        """Extract eligibility requirements"""
        eligibility_items = []
        
        # Common eligibility patterns
        patterns = [
            r'(?:must be|required to be|eligible).*?(?:501\(c\)\(3\)|nonprofit|tax-exempt)',
            r'(?:serve|target|focus on).*?(?:youth|students|ages? \d+-\d+)',
            r'(?:located in|serve|operate in).*?(?:county|counties|state|region)',
            r'(?:minimum|maximum).*?(?:budget|revenue|staff|experience)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 20)
                context_end = min(len(text), match.end() + 80)
                context = text[context_start:context_end].strip()
                if len(context) < 200:  # Avoid overly long matches
                    eligibility_items.append(context)
        
        return list(set(eligibility_items))[:8]  # Remove duplicates and limit
    
    def analyze_rfp(self, text: str) -> Dict:
        """Main analysis function that processes RFP text"""
        analysis = {
            'title': self.extract_title(text),
            'organization': self.extract_organization(text),
            'funding_amount': self.extract_funding_amount(text),
            'requirements': {
                'eligibility': self.parse_eligibility(text),
                'financial': self.parse_financial_requirements(text),
                'timeline': self.parse_timeline(text),
                'geographic': self.extract_geographic_requirements(text),
                'focus_areas': self.extract_focus_areas(text),
                'documents': self.extract_document_requirements(text)
            },
            'application_sections': self.extract_application_sections(text),
            'success_tips': self.extract_success_tips(text)
        }
        
        return analysis
    
    def extract_title(self, text: str) -> str:
        """Extract RFP title"""
        lines = text.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            if 'rfp' in line.lower() or 'request for proposal' in line.lower():
                return line.strip()
        return "RFP Document"
    
    def extract_organization(self, text: str) -> str:
        """Extract organization name"""
        # Look for common organization patterns
        patterns = [
            r'(?:from|by|issued by)\s+([A-Z][A-Za-z\s&]+(?:Foundation|Institute|University|Corporation|Union|Agency|Department))',
            r'^([A-Z][A-Za-z\s&]+(?:Foundation|Institute|University|Corporation|Union|Agency|Department))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Organization"
    
    def extract_funding_amount(self, text: str) -> str:
        """Extract funding amount information"""
        patterns = [
            r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?\s*(?:total|available|per\s+grant)',
            r'up to \$[\d,]+',
            r'maximum.*?\$[\d,]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return "Amount not specified"
    
    def extract_geographic_requirements(self, text: str) -> List[str]:
        """Extract geographic/location requirements"""
        geo_items = []
        patterns = [
            r'(?:serve|located in|operate in).*?(?:county|counties|state|region|area)',
            r'(?:California|New York|Texas|Florida).*?(?:county|counties)',
            r'(?:urban|rural|suburban).*?(?:areas|communities)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                geo_items.append(match.group().strip())
        
        return list(set(geo_items))[:5]
    
    def extract_focus_areas(self, text: str) -> List[str]:
        """Extract program focus areas or priorities"""
        focus_areas = []
        
        # Look for common focus area indicators
        patterns = [
            r'(?:focus|priority|pillar|area).*?(?:education|health|environment|community|youth)',
            r'(?:support|funding for).*?(?:programs|initiatives|projects)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 30)
                context_end = min(len(text), match.end() + 70)
                context = text[context_start:context_end].strip()
                focus_areas.append(context)
        
        return list(set(focus_areas))[:6]
    
    def extract_document_requirements(self, text: str) -> List[str]:
        """Extract required documents"""
        doc_patterns = [
            r'(?:submit|provide|include|upload).*?(?:budget|financial|audit|form 990)',
            r'(?:letter of|certificate|license|permit)',
            r'(?:tax-exempt|501\(c\)\(3\)).*?(?:letter|determination|status)',
        ]
        
        documents = []
        for pattern in doc_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                documents.append(match.group().strip())
        
        return list(set(documents))[:8]
    
    def extract_application_sections(self, text: str) -> List[Dict]:
        """Extract application structure/sections"""
        sections = []
        
        # Look for section headers or numbered items
        section_patterns = [
            r'Section \d+[:\.]?\s*([A-Za-z\s]+)',
            r'Part [A-Z\d]+[:\.]?\s*([A-Za-z\s]+)',
            r'\d+\.\s*([A-Za-z\s]{10,50})',
        ]
        
        for pattern in section_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                section_name = match.group(1).strip()
                if len(section_name) > 5:  # Filter out short matches
                    sections.append({
                        'title': section_name,
                        'description': f"Section focusing on {section_name.lower()}"
                    })
        
        # Default sections if none found
        if not sections:
            sections = [
                {'title': 'Organization Information', 'description': 'Basic organizational details'},
                {'title': 'Project Description', 'description': 'Detailed project narrative'},
                {'title': 'Budget', 'description': 'Financial information and budget'},
                {'title': 'Evaluation', 'description': 'Success metrics and evaluation plan'},
            ]
        
        return sections[:8]  # Limit to reasonable number
    
    def extract_success_tips(self, text: str) -> List[str]:
        """Extract tips for successful applications"""
        tips = []
        
        # Look for tip indicators
        tip_patterns = [
            r'(?:successful|competitive|strong).*?(?:applications|proposals)',
            r'(?:tips?|recommendations?|suggestions?).*?(?:for|include)',
            r'(?:review.*?will|we look for|consider)',
        ]
        
        for pattern in tip_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end].strip()
                if len(context) < 300:
                    tips.append(context)
        
        return list(set(tips))[:6]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze the RFP
        analyzer = RFPAnalyzer()
        text = analyzer.extract_text_from_file(file_path)
        analysis = analyzer.analyze_rfp(text)
        
        # Store analysis in session or database (for demo, we'll pass it directly)
        return render_template('analysis.html', analysis=analysis, filename=filename)
    
    flash('Invalid file type. Please upload PDF, DOCX, or TXT files.')
    return redirect(url_for('index'))

@app.route('/generate_prompt')
def generate_prompt():
    # This route can be used to generate LLM prompts
    return render_template('prompt_generator.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    analyzer = RFPAnalyzer()
    text = analyzer.extract_text_from_file(file_path)
    analysis = analyzer.analyze_rfp(text)
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)

# requirements.txt contents (create this file):
"""
Flask==2.3.3
PyPDF2==3.0.1
python-docx==0.8.11
Werkzeug==2.3.7
"""
