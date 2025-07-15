# Smart Research Assistant

An AI-powered document analysis tool that enables intelligent question-answering and reasoning challenges based on uploaded documents. Now powered by **Groq AI** for ultra-fast inference with Llama 3 models.

## Features

- **Document Upload**: Support for PDF and TXT files
- **Auto Summary**: Generate concise summaries (≤150 words)
- **Ask Anything Mode**: Free-form question answering with document-based justifications
- **Challenge Mode**: AI-generated logic questions with answer evaluation
- **Contextual Understanding**: All responses grounded in document content
- **Memory Handling**: Maintains context across interactions
- **Lightning Fast**: Powered by Groq AI for ultra-fast inference speeds

## Setup Instructions

### Prerequisites
- Python 3.8+
- Groq AI API key (free tier available)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd research_assistant
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up Groq AI API Key:**
   - Visit [Groq Console](https://console.groq.com/) and create a free account
   - Generate an API key from your dashboard
   - Update the API key in `ai_assistant.py`:
   ```python
   self.client = Groq(
       api_key="your_groq_api_key_here"  # Replace with your actual API key
   )
   ```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Access the application:**
Open your browser and go to `http://localhost:8501`

## Architecture

### Core Components

1. **DocumentProcessor**: Handles PDF/TXT file processing, text extraction, and context finding
2. **AIAssistant**: Manages AI interactions using Groq's Llama 3 model, question generation, and answer evaluation
3. **Streamlit App**: Provides the web interface and user interaction flow

### AI Model Details

- **Model**: Llama 3 8B (llama3-8b-8192) via Groq AI
- **Context Window**: 8,192 tokens
- **Inference Speed**: Ultra-fast with Groq's optimized hardware
- **Alternative Models**: llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it

### Data Flow

1. User uploads document → DocumentProcessor extracts and structures text
2. AI generates summary using Groq's Llama 3 model and stores document in memory
3. User selects interaction mode:
   - **Ask Anything**: Query → Context retrieval → AI answer with justification
   - **Challenge Me**: AI generates questions → User answers → AI evaluation with feedback

### Key Features Implementation

- **Contextual Understanding**: Uses sentence similarity and keyword matching to find relevant document sections
- **Justification**: Every answer includes specific document references
- **Challenge Generation**: AI creates comprehension-focused questions with expected answers
- **Answer Evaluation**: Compares user responses against expected answers with detailed feedback
- **Fast Processing**: Leverages Groq's optimized inference for near-instantaneous responses

## Usage

1. **Upload Document**: Click "Choose a PDF or TXT file" and select your document
2. **Process**: Click "Process Document" to analyze the content
3. **Review Summary**: Read the auto-generated summary (powered by Llama 3)
4. **Choose Mode**:
   - **Ask Anything**: Enter questions and get contextual answers
   - **Challenge Me**: Answer AI-generated questions and receive feedback

## Technical Details

- **Backend**: Python with Groq AI SDK
- **AI Model**: Llama 3 8B via Groq for ultra-fast inference
- **Frontend**: Streamlit web interface
- **Document Processing**: PyPDF2 for PDF extraction, NLTK for text processing
- **AI Integration**: Groq AI API for summarization, QA, and evaluation
- **Context Management**: Intelligent text segmentation and relevance scoring

## API Configuration

### Groq AI Setup
1. Create account at [Groq Console](https://console.groq.com/)
2. Generate API key from dashboard
3. Update `ai_assistant.py` with your key:
```python
self.client = Groq(
    api_key="your_groq_api_key_here"
)
```

### Available Models
- `llama3-8b-8192` - Fast, efficient (default)
- `llama3-70b-8192` - More capable, slower
- `mixtral-8x7b-32768` - Large context window
- `gemma-7b-it` - Google's Gemma model

## Performance Benefits

✅ **Ultra-fast inference** - Groq's optimized hardware delivers responses in milliseconds
✅ **Cost-effective** - Groq offers competitive pricing with generous free tier
✅ **High-quality outputs** - Llama 3 models provide excellent reasoning capabilities
✅ **Reliable API** - Stable and well-documented API interface

## File Structure

```
research_assistant/
├── app.py                 # Main Streamlit application
├── ai_assistant.py        # Groq AI integration and logic
├── document_processor.py  # Document parsing and context extraction
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Dependencies

Key dependencies include:
- `streamlit` - Web interface
- `groq` - Official Groq AI Python SDK
- `PyPDF2` - PDF text extraction
- `nltk` - Natural language processing
- `python-dotenv` - Environment variable management

## Evaluation Criteria Alignment

- **Response Quality**: Document-grounded answers with clear justifications
- **Reasoning Mode**: Logic-based question generation and evaluation
- **UI/UX**: Clean, intuitive Streamlit interface
- **Code Structure**: Modular design with clear documentation
- **Creativity**: Context highlighting and memory handling
- **Minimal Hallucination**: All responses anchored to document content
- **Performance**: Lightning-fast responses with Groq AI

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Groq API key is correctly set in `ai_assistant.py`
2. **Model Limits**: If you hit rate limits, try switching to a different model
3. **Document Processing**: Ensure PDF files are text-based (not scanned images)
4. **Dependencies**: Run `pip install -r requirements.txt` to install all required packages

### Getting Help

- Check [Groq Documentation](https://console.groq.com/docs)
- Review error logs in the Streamlit interface
- Ensure all dependencies are properly installed

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This application uses Groq AI's fast inference capabilities to provide near-instantaneous responses while maintaining high-quality document analysis and reasoning.
