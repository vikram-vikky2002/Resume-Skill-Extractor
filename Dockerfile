FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -c "import spacy.cli; spacy.cli.download('en_core_web_sm')"

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt')" && \
    python -c "import nltk; nltk.download('stopwords')"

# Copy application code
COPY . .

# Expose port 8501 (default Streamlit port)
EXPOSE 8501

# Run Streamlit app with event loop fix
CMD ["python", "-c", "import asyncio; import nest_asyncio; nest_asyncio.apply(); from streamlit.web import bootstrap; import streamlit; bootstrap.run('app.py', '', ['--server.port=8501', '--server.address=0.0.0.0'], None)"]
