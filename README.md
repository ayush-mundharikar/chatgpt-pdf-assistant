🧠 ChatGPT PDF Assistant
An AI-powered intelligent assistant that understands your PDF documents.
Upload, summarize, chat, listen — all inside a sleek Streamlit web app.

🚀 Features
Clearly tell what the app does:

📄 Upload any PDF file

✨ Get AI-generated summary (via OpenAI GPT-4)

💬 Ask natural-language questions based on PDF content

🔊 Hear answers using Text-to-Speech

🧾 View & delete chat history inside the app

🧼 Clean & modern UI with Streamlit

🛠️ Tech Stack
Tool	Purpose
Python	Core programming language
Streamlit	Interactive web UI
OpenAI API	Language model for Q&A & summary
PyMuPDF	Extracting PDF text
gTTS	Convert text to voice
dotenv	Manage API keys securely
📁 Project Structure
bash
Copy
Edit
chatgpt-pdf-assistant/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── .env                # Stores your OpenAI API key
├── README.md           # Project documentation