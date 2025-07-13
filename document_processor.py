
import PyPDF2
import nltk
#nltk.download('punkt')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
from typing import List, Dict, Tuple
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class DocumentProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def process_document(self, file_path: str) -> Dict:
        """Process uploaded document and extract structured information"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or TXT files.")
        
        # Clean and structure the text
        cleaned_text = self.clean_text(text)
        sentences = sent_tokenize(cleaned_text)
        paragraphs = self.extract_paragraphs(cleaned_text)
        
        return {
            'raw_text': text,
            'cleaned_text': cleaned_text,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'word_count': len(word_tokenize(cleaned_text)),
            'sentence_count': len(sentences)
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove page numbers and common artifacts
        text = re.sub(r'\n\d+\n', '\n', text)
        text = re.sub(r'\f', '', text)
        
        return text
    
    def extract_paragraphs(self, text: str) -> List[str]:
        """Extract paragraphs from text"""
        # Split by double newlines or significant breaks
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Clean and filter paragraphs
        clean_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50:  # Filter out very short paragraphs
                clean_paragraphs.append(para)
        
        return clean_paragraphs
    
    def find_relevant_context(self, text: str, query: str, max_chars: int = 500) -> List[str]:
        """Find relevant text segments for a query"""
        sentences = sent_tokenize(text)
        query_words = set(word_tokenize(query.lower()))
        
        # Score sentences based on query relevance
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            sentence_words = set(word_tokenize(sentence.lower()))
            common_words = query_words.intersection(sentence_words)
            score = len(common_words) / len(query_words) if query_words else 0
            scored_sentences.append((score, sentence, i))
        
        # Sort by relevance and return top contexts
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        relevant_contexts = []
        for score, sentence, idx in scored_sentences[:3]:
            if score > 0:
                # Get surrounding context
                start_idx = max(0, idx - 1)
                end_idx = min(len(sentences), idx + 2)
                context = " ".join(sentences[start_idx:end_idx])
                if len(context) <= max_chars:
                    relevant_contexts.append(context)
        
        return relevant_contexts

