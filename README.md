# 🤖 AI Study Buddy

Your personal AI-powered learning assistant powered by Google Gemini. Quickly generate explanations, summaries, and quizzes for any topic. Upload PDF notes for intelligent content analysis.

## Features

- 📚 **Explain Topics** - Get detailed explanations at different difficulty levels (Beginner, Intermediate, Exam-Ready)
- 📝 **Summarize Content** - Generate concise 5-point summaries of any topic
- ❓ **Create Quizzes** - Auto-generate 5 multiple-choice questions with answers
- 📄 **PDF Analysis** - Upload and analyze PDF notes for explanations, summaries, or quizzes
- 🔄 **Automatic Retries** - Smart retry logic with exponential backoff for high-demand scenarios
- ⚠️ **Error Handling** - User-friendly error messages and graceful degradation

## Prerequisites

- Python 3.8 or higher
- Google Genai API key (set as an environment variable)
- Internet connection

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-study-buddy2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   The application reads `GOOGLE_API_KEY` directly from your environment. You can export it in your shell before running the app:
   
   ```bash
   # Windows (PowerShell)
   $env:GOOGLE_API_KEY="your_api_key_here"
   
   # macOS/Linux
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   
   Optionally, you may use a `.env` file with a library like `python-dotenv` if you prefer, but this project doesn't require it.

## Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **In the web interface:**
   - Enter a topic in the text input
   - Select mode: Explain, Summarize, or Quiz
   - Select explanation level (only for Explain mode)
   - Optionally upload a PDF file
   - Click "Generate" button

## Project Structure

```
ai-study-buddy2/
├── app.py              # Main Streamlit application
├── ai_engine.py        # AI response generation with error handling
├── prompts.py          # Prompt templates for different modes
├── pdf_utils.py        # PDF text extraction utilities
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Error Handling

The application includes robust error handling for high-demand scenarios:

- **TooManyRequests (429)** - Automatically retries up to 3 times with exponential backoff
- **ResourceExhausted** - Handles quota exceeded errors with retry logic
- **DeadlineExceeded** - Retries when requests timeout
- **ServiceUnavailable** - Retries when the service is temporarily down

Retry delays: 1s → 2s → 4s between attempts.

## Configuration

### Models & APIs
- **Model**: `gemini-2.5-flash` (Google Genai)
- **API Provider**: Google Generative AI

### Customization
Edit `prompts.py` to customize the prompt templates for different modes.

## Dependencies

- `streamlit==1.54.0` - Web application framework
- `google-genai==1.62.0` - Google Generative AI API client

## Future Enhancements

- [ ] Support for more output formats (PDF export, markdown)
- [ ] Chat history and conversation memory
- [ ] Multiple language support
- [ ] User authentication and storage
- [ ] Analytics dashboard

## Troubleshooting

**"Could not extract text from PDF"**
- Ensure the PDF file is not corrupted
- Try with a different PDF file

**"High demand" error after retries**
- Wait a few minutes and try again
- The service may be experiencing temporary overload


 
