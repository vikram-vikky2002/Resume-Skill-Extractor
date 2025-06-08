import PyPDF2
import spacy
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# Common skill keywords
SKILL_KEYWORDS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'sql', 'html', 'css', 'node.js',
    'react', 'angular', 'vue.js', 'django', 'flask', 'spring', 'hibernate',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github', 'gitlab',
    'mysql', 'postgresql', 'mongodb', 'redis', 'tensorflow', 'pytorch',
    'machine learning', 'data science', 'cloud', 'devops', 'agile',
    'scrum', 'rest api', 'graphql', 'docker', 'kubernetes', 'k8s',
    'linux', 'windows', 'bash', 'powershell', 'api', 'restful',
    'docker-compose', 'jenkins', 'circleci', 'github actions',
    'terraform', 'ansible', 'kafka', 'rabbitmq', 'elasticsearch',
    'kibana', 'grafana', 'prometheus', 'nginx', 'apache', 'tomcat'
]

class ResumeSkillExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.skill_patterns = self._create_skill_patterns()

    def _create_skill_patterns(self):
        """Create regex patterns for skill extraction"""
        patterns = []
        for skill in SKILL_KEYWORDS:
            # Handle skills with spaces (e.g., "machine learning")
            patterns.append(re.escape(skill.replace(' ', r'\s*')))
        return '|'.join(patterns)

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
        return text

    def preprocess_text(self, text):
        """Preprocess text by removing stopwords and special characters"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)

    def extract_skills(self, text):
        """Extract skills from preprocessed text"""
        # Use regex to find skill patterns
        found_skills = set()
        matches = re.finditer(self.skill_patterns, text)
        for match in matches:
            skill = match.group(0)
            # Clean up any extra spaces
            skill = re.sub(r'\s+', ' ', skill)
            found_skills.add(skill)
        
        # Use spaCy for additional skill extraction
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'TECHNOLOGY']:
                found_skills.add(ent.text.lower())
        
        return sorted(list(found_skills))

    def process_resume(self, pdf_path):
        """Process a resume PDF and extract skills"""
        # Extract text from PDF
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text:
            return []
            
        # Preprocess text
        processed_text = self.preprocess_text(raw_text)
        
        # Extract skills
        skills = self.extract_skills(processed_text)
        return skills

def main():
    extractor = ResumeSkillExtractor()
    
    # Example usage
    resume_path = input("Enter the path to the resume PDF: ")
    if not os.path.exists(resume_path):
        print("File not found!")
        return
    
    skills = extractor.process_resume(resume_path)
    if skills:
        print("\nExtracted Skills:")
        for skill in skills:
            print(f"- {skill}")
    else:
        print("No skills found in the resume.")

if __name__ == "__main__":
    main()
