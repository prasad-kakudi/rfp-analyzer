from setuptools import setup, find_packages

setup(
    name="rfp-analyzer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "PyPDF2==3.0.1",
        "python-docx==0.8.11",
        "Werkzeug==2.3.7",
        "python-dotenv==1.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered RFP document analyzer and response generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rfp-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

