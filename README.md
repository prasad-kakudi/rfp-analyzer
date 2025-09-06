"""
# RFP Analyzer - AI-Powered Grant Proposal Assistant

A Flask web application that automatically analyzes Request for Proposal (RFP) documents and generates AI prompts for creating compelling grant proposal responses.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Intelligent Analysis**: Automatically extracts key requirements, deadlines, and criteria
- **AI Prompt Generation**: Creates optimized prompts for LLMs to generate responses
- **Interactive Interface**: User-friendly web interface with tabbed navigation
- **Export Capabilities**: Download analysis results and prompts

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/rfp-analyzer.git
   cd rfp-analyzer
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:5000`

## Usage

### Upload RFP Document
1. Go to the main page
2. Upload your RFP document (PDF, DOCX, or TXT)
3. Click "Analyze RFP Document"

### View Analysis Results
The analysis provides:
- **Eligibility Requirements**: Who can apply and basic criteria
- **Financial Requirements**: Funding amounts, budget constraints
- **Timeline**: Important dates and deadlines  
- **Geographic Focus**: Location requirements and service areas
- **Focus Areas**: Program priorities and impact areas
- **Required Documents**: What you need to submit

### Generate AI Prompts
1. Switch to the "AI Prompt Generator" tab
2. Use the generated prompt template
3. Copy or download for use with ChatGPT, Claude, or other AI tools

### Standalone Prompt Generator
- Visit `/generate_prompt` for a custom prompt builder
- Fill in your organization and project details
- Generate tailored prompts for your specific needs

## API Usage

The application also provides a REST API endpoint:

```bash
curl -X POST -F "file=@your_rfp.pdf" http://localhost:5000/api/analyze
```

Returns JSON with analysis results.

## File Support

- **PDF**: Uses PyPDF2 for text extraction
- **DOCX**: Uses python-docx for Microsoft Word documents  
- **TXT**: Direct text file processing
- **Size Limit**: 16MB maximum file size

## Configuration

Key configuration options in `app.py`:

```python
app.config['UPLOAD_FOLDER'] = 'uploads'           # Upload directory
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}       # Supported formats
```

## Analysis Components

The RFP analyzer extracts:

1. **Title & Organization**: RFP title and issuing organization
2. **Funding Information**: Available amounts and restrictions
3. **Requirements Analysis**:
   - Eligibility criteria
   - Financial requirements  
   - Geographic restrictions
   - Timeline and deadlines
   - Required documents
   - Focus areas and priorities
4. **Application Structure**: Sections and components
5. **Success Tips**: Best practices from the RFP

## AI Integration

Generated prompts work with:
- OpenAI GPT (ChatGPT, GPT-4)
- Anthropic Claude
- Google Bard
- Other large language models

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New File Types
1. Install appropriate library
2. Add to `ALLOWED_EXTENSIONS`
3. Update `extract_text_from_file()` method

### Customizing Analysis
Modify the `RFPAnalyzer` class methods:
- `parse_financial_requirements()`
- `parse_timeline()`
- `parse_eligibility()`
- etc.

## Deployment

### Local Production
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker (optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Cloud Deployment
Compatible with:
- Heroku
- AWS Elastic Beanstalk  
- Google Cloud Platform
- DigitalOcean App Platform

## Security Considerations

- File upload validation
- Secure filename handling
- Size limitations
- Input sanitization
- No persistent file storage (files deleted after processing)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review the code comments

## Roadmap

- [ ] Support for more file formats (RTF, HTML)
- [ ] Integration with popular LLM APIs
- [ ] Template library for different grant types
- [ ] Collaborative features for teams
- [ ] Advanced text analytics and scoring
- [ ] Mobile-responsive improvements
"""
