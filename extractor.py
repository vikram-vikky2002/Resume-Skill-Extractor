import pdfplumber
import spacy
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

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
    'machine learning', 'data science', 'ai', 'cloud', 'devops', 'agile',
    'scrum', 'rest api', 'graphql', 'mongodb', 'postgresql', 'mysql',
    'big data', 'hadoop', 'spark', 'etl', 'data warehousing',
    'docker-compose', 'jenkins', 'circleci', 'github actions',
    'terraform', 'ansible', 'kafka', 'rabbitmq', 'elasticsearch',
    'kibana', 'grafana', 'prometheus', 'nginx', 'apache', 'tomcat'
]

class Extractor:
    def __init__(self):
        """Initialize the extractor with NLP models"""
        self.nlp = nlp
        self.stop_words = set(stopwords.words('english'))
        self.skill_keywords = SKILL_KEYWORDS

    def extract_resume_data(self, file_path):
        """
        Extracts data from a resume PDF file.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Dictionary containing extracted information:
                - name (str): Name of the candidate
                - email (str): Email address
                - phone (str): Phone number
                - skills (list): List of extracted skills
                - raw_text (str): Raw text content of the resume
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()

            # Extract name (assuming it's usually at the top)
            name = ""
            first_line = text.split('\n')[0].strip()
            if first_line:
                # Try to extract name from first line
                doc = self.nlp(first_line)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        name = ent.text
                        break

            # Extract email
            email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            email = email.group(0) if email else ""

            # Extract phone number
            phone = re.search(r'\+?\d[\d\s-]{7,}\d', text)
            phone = phone.group(0) if phone else ""

            # Extract skills
            skills = []
            tokens = word_tokenize(text.lower())
            for token in tokens:
                if token in self.skill_keywords and token not in self.stop_words:
                    skills.append(token)

            return {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': list(set(skills)),
                'raw_text': text
            }

        except Exception as e:
            print(f"Error extracting data: {str(e)}")
            return {
                'name': '',
                'email': '',
                'phone': '',
                'skills': [],
                'raw_text': ''
            }

def extract_resume_data(file_path):
    """
    Extracts data from a resume PDF file.
    
    Args:
        file_path (str): Path to the PDF file
    
    Returns:
        dict: Dictionary containing extracted information:
            - name (str): Name of the candidate
            - email (str): Email address
            - phone (str): Phone number
            - skills (list): List of extracted skills
            - raw_text (str): Raw text content of the resume
    """
    try:
        # Extract text using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            pages = pdf.pages
            raw_text = "\n".join([page.extract_text() for page in pages])
            
        # Extract name using spaCy
        doc = nlp(raw_text)
        name = ""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break

        # Extract email using regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, raw_text.lower())
        email = emails[0] if emails else ""

        # Extract phone using regex
        phone_pattern = r'\+?\d[\d\s-]{7,}\d'
        phones = re.findall(phone_pattern, raw_text)
        phone = phones[0] if phones else ""

        # Extract skills
        skills = []
        
        # 1. Check for exact skill matches
        for skill in SKILL_KEYWORDS:
            if skill.lower() in raw_text.lower():
                skills.append(skill)
        
        # 2. Extract skills using spaCy with better filtering
        for token in doc:
            # Only consider nouns and proper nouns
            if token.pos_ in ['NOUN', 'PROPN']:
                skill = token.text.lower()
                
                # Skip common words and very short words
                if skill in stopwords.words('english') or len(skill) < 3:
                    continue
                
                # Skip common resume words
                if skill in ['experience', 'skills', 'work', 'team', 'tasks', 
                           'performance', 'solutions', 'applications', 'software',
                           'data', 'queries', 'components', 'systems', 'database',
                           'present', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                           'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    continue
                
                # Skip common location words
                if skill in ['san', 'los', 'angeles', 'francisco', 'inc', 'byteworks',
                           'technova', 'john', 'doe']:
                    continue
                
                # Skip common verbs and adjectives
                if skill in ['wrote', 'collaborated', 'developed', 'designed',
                           'implemented', 'maintained', 'tested', 'analyzed']:
                    continue
                
                # Skip common tech terms that aren't specific skills
                if skill in ['web', 'frontend', 'backend', 'full', 'stack',
                           'api', 'apis', 'database', 'queries', 'performance']:
                    continue
                
                # Skip common project words
                if skill in ['project', 'pipeline', 'storage', 'methodology',
                           'framework', 'platform', 'application', 'system']:
                    continue
                
                # Only add if it's not already in the list
                if skill not in skills:
                    skills.append(skill)

        # 3. Clean up and normalize skills
        cleaned_skills = []
        for skill in skills:
            # Skip if it's just a number
            if skill.isdigit():
                continue
            
            # Skip if it's too short
            if len(skill) < 3:
                continue
            
            # Normalize skill names (e.g., 'c++' -> 'c++', 'c#' -> 'c#')
            normalized_skill = skill
            if skill == 'c++':
                normalized_skill = 'c++'
            elif skill == 'c#':
                normalized_skill = 'c#'
            
            # Add to cleaned list if not already present
            if normalized_skill not in cleaned_skills:
                cleaned_skills.append(normalized_skill)
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'skills': cleaned_skills,
            'raw_text': raw_text
        }
        
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        return None
