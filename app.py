import streamlit as st
import os
import tempfile
from document_processor import DocumentProcessor
from ai_assistant import AIAssistant

# Configure Streamlit page
st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False
if 'document_data' not in st.session_state:
    st.session_state.document_data = None
if 'assistant' not in st.session_state:
    st.session_state.assistant = AIAssistant()
if 'processor' not in st.session_state:
    st.session_state.processor = DocumentProcessor()
if 'challenge_questions' not in st.session_state:
    st.session_state.challenge_questions = []
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0

def main():
    st.title("🔍 Smart Research Assistant")
    st.markdown("**Upload a document and interact with it through AI-powered question answering and reasoning challenges**")
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Upload")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=['pdf', 'txt'],
            help="Upload a structured document like a research paper, report, or manual"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document", type="primary"):
                process_document(uploaded_file)
        
        # Document info
        if st.session_state.document_processed:
            st.success("✅ Document processed successfully!")
            doc_data = st.session_state.document_data
            st.write(f"**Word Count:** {doc_data['word_count']}")
            st.write(f"**Sentences:** {doc_data['sentence_count']}")
            st.write(f"**Paragraphs:** {len(doc_data['paragraphs'])}")
    
    # Main content area
    if not st.session_state.document_processed:
        st.info("👆 Please upload a document to get started")
        
        # Display sample interface
        st.subheader("Features Preview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💬 Ask Anything Mode")
            st.write("Ask free-form questions about your document and get contextual answers with justifications.")
            
        with col2:
            st.markdown("### 🧠 Challenge Me Mode")
            st.write("Test your understanding with AI-generated questions and get detailed feedback.")
    
    else:
        # Display document summary
        st.subheader("📋 Document Summary")
        if 'summary' not in st.session_state:
            with st.spinner("Generating summary..."):
                summary = st.session_state.assistant.generate_summary(
                    st.session_state.document_data['cleaned_text']
                )
                st.session_state.summary = summary
        
        st.write(st.session_state.summary)
        
        # Interaction modes
        st.subheader("🎯 Choose Your Interaction Mode")
        
        mode = st.radio(
            "Select mode:",
            ["Ask Anything", "Challenge Me"],
            horizontal=True
        )
        
        if mode == "Ask Anything":
            ask_anything_mode()
        else:
            challenge_mode()

def process_document(uploaded_file):
    """Process uploaded document"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Process document
        with st.spinner("Processing document..."):
            document_data = st.session_state.processor.process_document(tmp_file_path)
            st.session_state.document_data = document_data
            st.session_state.document_processed = True
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        st.success("Document processed successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")

def ask_anything_mode():
    """Ask Anything interaction mode"""
    st.markdown("### 💬 Ask Anything Mode")
    st.write("Ask any question about your document and get contextual answers with justifications.")
    
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What are the main findings of this research?"
    )
    
    if st.button("Get Answer") and question:
        with st.spinner("Analyzing document and generating answer..."):
            # Find relevant context
            relevant_contexts = st.session_state.processor.find_relevant_context(
                st.session_state.document_data['cleaned_text'],
                question
            )
            
            # Get answer from AI
            result = st.session_state.assistant.answer_question(
                question,
                st.session_state.document_data['cleaned_text'],
                relevant_contexts
            )
            
            # Display answer
            st.markdown("#### 🎯 Answer")
            st.write(result['answer'])
            
            st.markdown("#### 📚 Justification")
            st.write(result['justification'])
            
            # Show relevant contexts if available
            if result['contexts_used']:
                with st.expander("📄 Source Context"):
                    for i, context in enumerate(result['contexts_used']):
                        st.markdown(f"**Context {i+1}:**")
                        st.write(context)
                        st.markdown("---")

def challenge_mode():
    """Challenge Me interaction mode"""
    st.markdown("### 🧠 Challenge Me Mode")
    st.write("Test your understanding with AI-generated questions based on your document.")
    
    # Generate questions if not already generated
    if not st.session_state.challenge_questions:
        if st.button("Generate Challenge Questions", type="primary"):
            with st.spinner("Generating challenge questions..."):
                questions = st.session_state.assistant.generate_challenge_questions(
                    st.session_state.document_data['cleaned_text']
                )
                st.session_state.challenge_questions = questions
                st.rerun()
    
    # Display questions if available
    if st.session_state.challenge_questions:
        st.markdown("#### 📝 Challenge Questions")
        
        # Question navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Previous") and st.session_state.current_question_idx > 0:
                st.session_state.current_question_idx -= 1
                st.rerun()
        
        with col2:
            st.write(f"Question {st.session_state.current_question_idx + 1} of {len(st.session_state.challenge_questions)}")
        
        with col3:
            if st.button("Next →") and st.session_state.current_question_idx < len(st.session_state.challenge_questions) - 1:
                st.session_state.current_question_idx += 1
                st.rerun()
        
        # Current question
        current_q = st.session_state.challenge_questions[st.session_state.current_question_idx]
        st.markdown(f"**Question:** {current_q['question']}")
        
        # User answer input
        user_answer = st.text_area(
            "Your answer:",
            height=100,
            placeholder="Type your answer here..."
        )
        
        if st.button("Submit Answer") and user_answer:
            with st.spinner("Evaluating your answer..."):
                evaluation = st.session_state.assistant.evaluate_answer(
                    user_answer,
                    current_q['question'],
                    current_q['expected_answer'],
                    st.session_state.document_data['cleaned_text']
                )
                
                # Display evaluation
                st.markdown("#### 📊 Evaluation")
                
                # Score with color coding
                score = evaluation['score']
                if score.lower() in ['excellent', 'good']:
                    st.success(f"Score: {score}")
                elif score.lower() == 'fair':
                    st.warning(f"Score: {score}")
                else:
                    st.error(f"Score: {score}")
                
                st.markdown("#### 💬 Feedback")
                st.write(evaluation['feedback'])
                
                st.markdown("#### ✅ Correct Answer")
                st.write(evaluation['correct_answer'])
        
        # Reset questions button
        if st.button("🔄 Generate New Questions"):
            st.session_state.challenge_questions = []
            st.session_state.current_question_idx = 0
            st.rerun()

if __name__ == "__main__":
    main()