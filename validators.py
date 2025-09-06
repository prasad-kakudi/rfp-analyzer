import re
from typing import Dict, List, Tuple

class RFPValidator:
    """Validation class for RFP analysis inputs"""
    
    @staticmethod
    def validate_file_upload(file) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if not file:
            return False, "No file provided"
        
        if file.filename == '':
            return False, "No file selected"
        
        # Check file extension
        allowed_extensions = {'pdf', 'docx', 'txt'}
        if not allowed_file(file.filename, allowed_extensions):
            return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        
        return True, "File is valid"
    
    @staticmethod
    def validate_text_content(text: str) -> Tuple[bool, str]:
        """Validate extracted text content"""
        if not text or len(text.strip()) < 100:
            return False, "Document appears to be empty or too short for analysis"
        
        if len(text) > 500000:  # 500KB text limit
            return False, "Document is too large for processing"
        
        return True, "Text content is valid"
    
    @staticmethod
    def validate_form_data(form_data: Dict) -> Dict[str, List[str]]:
        """Validate form data and return errors"""
        errors = {}
        
        # Organization name validation
        if not form_data.get('orgName', '').strip():
            errors.setdefault('orgName', []).append("Organization name is required")
        
        # Mission statement validation
        mission = form_data.get('mission', '').strip()
        if mission and len(mission) < 20:
            errors.setdefault('mission', []).append("Mission statement should be at least 20 characters")
        
        # Funding amount validation
        funding = form_data.get('fundingAmount', '').strip()
        if funding and not re.match(r'^\$?[\d,]+(?:\.\d{2})?, funding):
            errors.setdefault('fundingAmount', []).append("Invalid funding amount format")
        
        return errors

