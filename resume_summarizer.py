import spacy
from spacy.lang.en import English
from collections import Counter
import re
import google.generativeai as genai

class ResumeSummarizer:
    def __init__(self):
        """Initialize the summarizer with spaCy and Google's Gemini API."""
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = set(self.nlp.Defaults.stop_words)
        # Get your Google API key from https://makersuite.google.com/app/apikey
        self.api_key = "AIzaSyAqxr2uJPiU6C7dagYN2Yv79mawuwP8_eI"  # Replace with your actual Google API key
        genai.configure(api_key=self.api_key)

    def extract_key_sentences(self, text, num_sentences=3):
        """
        Extract key sentences from resume text.
        
        Args:
            text (str): Resume text
            num_sentences (int): Number of sentences to extract
            
        Returns:
            str: Summary of key sentences
        """
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        # Calculate sentence scores based on word frequency
        word_frequencies = Counter()
        for word in doc:
            if word.text.lower() not in self.stop_words and word.text.isalpha():
                word_frequencies[word.text.lower()] += 1
        
        max_freq = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_freq
        
        # Score sentences
        sentence_scores = {}
        for i, sent in enumerate(sentences):
            sent_doc = self.nlp(sent.lower())
            for token in sent_doc:
                if token.text in word_frequencies.keys():
                    if i not in sentence_scores.keys():
                        sentence_scores[i] = word_frequencies[token.text]
                    else:
                        sentence_scores[i] += word_frequencies[token.text]
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        # Create summary
        summary = "\n".join([sentences[idx] for idx, _ in top_sentences])
        return summary

    def generate_summary(self, resume_data):
        """
        Generate a comprehensive summary of the resume using OpenAI's free model.
        
        Args:
            resume_data (dict): Parsed resume data
            
        Returns:
            str: Summary paragraph
        """
        try:
            # Extract key information
            name = resume_data.get('name', "")
            skills = resume_data.get('skills', [])
            experience = resume_data.get('raw_text', "")
            
            # Create a concise prompt
            skill_str = ", ".join(skills[:5]) if skills else ""
            prompt = f"""
            Write a professional summary for {name}:
            
            Skills: {skill_str}
            Experience: {experience[:500]}  # Limit to 500 chars to stay within free tier
            
            Summary (in 3-4 sentences):
            """
            
            # Call Gemini API
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.8,
                        "top_k": 40
                    },
                    stream=False
                )
                
                # Handle the response correctly
                if isinstance(response, str):
                    return f"Professional Summary:\n- {response.strip()}"
                elif hasattr(response, 'text'):
                    if isinstance(response.text, list) and len(response.text) > 0:
                        return f"Professional Summary:\n- {response.text[0].strip()}"
                    else:
                        return f"Professional Summary:\n- {response.text.strip()}"
                else:
                    print("Invalid response format from Gemini API")
                    return self._generate_basic_summary(name, skills, experience)
            except Exception as e:
                print(f"Error generating summary with Gemini: {str(e)}")
                return self._generate_basic_summary(name, skills, experience)
            
            if response.choices:
                summary = response.choices[0].message.content.strip()
                return f"Professional Summary:\n- {summary}"
            else:
                print("No response from OpenAI API")
                return self._generate_basic_summary(name, skills, experience)
            
        except Exception as e:
            print(f"Error generating summary with OpenAI: {str(e)}")
            # Fallback to basic summary if API fails
            return self._generate_basic_summary(name, skills, experience)
    
    def _generate_basic_summary(self, name, skills, experience):
        """Fallback method to generate a basic summary."""
        summary = []
        
        if name:
            summary.append(f"{name} is a professional with experience in")
        
        if skills:
            skill_str = ", ".join(skills[:5])  # Top 5 skills
            summary.append(f"key skills including {skill_str}")
        
        if experience:
            # Extract key sentences
            key_sentences = self.extract_key_sentences(experience, 3)
            if key_sentences:
                # Clean up sentences
                sentences = key_sentences.split('\n')
                for sent in sentences:
                    sent = sent.strip().replace('•', '').strip()
                    if sent:
                        summary.append(sent)
        
        return ' '.join(summary).strip()
