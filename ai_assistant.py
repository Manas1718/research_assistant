from groq import Groq
import os
import random
from typing import List, Dict, Tuple
import re
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self):
        self.conversation_history = []
        # Initialize Groq client
        self.client = Groq(
            api_key="YOUR_GROQAI_API_KEY" #PASTE YOUR GROQ API KEY
        )

    def generate_summary(self, document_content: str) -> str:
        """Generate a concise summary of the document (≤300 words)"""
        prompt = f"""
        Please provide a concise summary of the following document in no more than 150 words. 
        Focus on the main points, key findings, and overall purpose of the document.
        
        Document:
        {document_content[:3000]}  # Limit input to avoid token limits
        
        Summary (≤300 words):
        """

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using Llama 3 8B model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def answer_question(self, question: str, document_content: str, relevant_contexts: List[str]) -> Dict:
        """Answer a question based on the document with justification"""
        context_text = "\n\n".join(relevant_contexts) if relevant_contexts else document_content[:2000]

        prompt = f"""
        Based on the following document content, please answer the question. 
        Your answer must be grounded in the provided text and include a clear justification 
        referencing specific parts of the document.
        
        Document Content:
        {context_text}
        
        Question: {question}
        
        Please provide:
        1. A clear, direct answer
        2. A justification explaining which part of the document supports your answer
        3. If the answer cannot be found in the document, clearly state that
        
        Format your response as:
        Answer: [Your answer here]
        Justification: [Reference to specific document section/paragraph]
        """

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using Llama 3 8B model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.2
            )

            full_response = response.choices[0].message.content.strip()

            # Parse the response to extract answer and justification
            answer_match = re.search(r'Answer:\s*(.*?)(?=\nJustification:|$)', full_response, re.DOTALL)
            justification_match = re.search(r'Justification:\s*(.*)', full_response, re.DOTALL)

            answer = answer_match.group(1).strip() if answer_match else full_response
            justification = justification_match.group(1).strip() if justification_match else "Based on document analysis"

            return {
                'answer': answer,
                'justification': justification,
                'contexts_used': relevant_contexts
            }

        except Exception as e:
            return {
                'answer': f"Error processing question: {str(e)}",
                'justification': "Error in AI processing",
                'contexts_used': []
            }

    def generate_challenge_questions(self, document_content: str) -> List[Dict]:
        """Generate 3 logic-based questions from the document"""
        prompt = f"""
        Based on the following document, generate exactly 3 challenging questions that test 
        comprehension and logical reasoning. Each question should:
        1. Require understanding of the document's content
        2. Test logical reasoning or inference
        3. Have a clear answer that can be found in or derived from the document
        
        Document:
        {document_content[:2500]}
        
        Please format each question as:
        Question 1: [Question text]
        Expected Answer: [Brief expected answer]
        
        Question 2: [Question text]  
        Expected Answer: [Brief expected answer]
        
        Question 3: [Question text]
        Expected Answer: [Brief expected answer]
        """

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using Llama 3 8B model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.4
            )

            questions_text = response.choices[0].message.content.strip()
            questions = self.parse_challenge_questions(questions_text)

            return questions

        except Exception as e:
            return [
                {
                    'question': f"Error generating questions: {str(e)}",
                    'expected_answer': "Error in processing"
                }
            ]

    def parse_challenge_questions(self, questions_text: str) -> List[Dict]:
        """Parse generated questions into structured format"""
        questions = []

        # Split by question numbers
        question_blocks = re.split(r'Question \d+:', questions_text)[1:]  # Skip empty first element

        for block in question_blocks:
            # Extract question and expected answer
            parts = block.split('Expected Answer:')
            if len(parts) >= 2:
                question = parts[0].strip()
                expected_answer = parts[1].strip()

                questions.append({
                    'question': question,
                    'expected_answer': expected_answer
                })

        return questions[:3]  # Ensure we return exactly 3 questions

    def evaluate_answer(self, user_answer: str, question: str, expected_answer: str, document_content: str) -> Dict:
        """Evaluate user's answer to a challenge question"""
        prompt = f"""
        A user was asked a question about a document and provided an answer. 
        Please evaluate their answer and provide feedback.
        
        Document Context:
        {document_content[:2000]}
        
        Question: {question}
        Expected Answer: {expected_answer}
        User's Answer: {user_answer}
        
        Please provide:
        1. A score (Excellent/Good/Fair/Poor)
        2. Specific feedback on what was correct/incorrect
        3. The correct answer with document reference
        
        Format:
        Score: [Score]
        Feedback: [Detailed feedback]
        Correct Answer: [Correct answer with document reference]
        """

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using Llama 3 8B model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )

            evaluation = response.choices[0].message.content.strip()

            # Parse evaluation
            score_match = re.search(r'Score:\s*(.*?)(?=\nFeedback:|$)', evaluation, re.DOTALL)
            feedback_match = re.search(r'Feedback:\s*(.*?)(?=\nCorrect Answer:|$)', evaluation, re.DOTALL)
            correct_answer_match = re.search(r'Correct Answer:\s*(.*)', evaluation, re.DOTALL)

            return {
                'score': score_match.group(1).strip() if score_match else "Good",
                'feedback': feedback_match.group(1).strip() if feedback_match else evaluation,
                'correct_answer': correct_answer_match.group(1).strip() if correct_answer_match else expected_answer
            }

        except Exception as e:
            return {
                'score': "Error",
                'feedback': f"Error evaluating answer: {str(e)}",
                'correct_answer': expected_answer
            }
