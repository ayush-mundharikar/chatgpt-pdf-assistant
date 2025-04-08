import streamlit as st
import fitz  # PyMuPDF
import pyttsx3
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere client
co = cohere.Client(api_key)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.set_page_config(page_title="ChatGPT PDF Assistant", layout="wide")
st.title("📄 ChatGPT PDF Assistant")

uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
  
    pdf_text_translated = pdf_text
    st.subheader("📄 Extracted PDF Text:")
    st.text_area("Text from PDF:", pdf_text, height=300)

    search_query = st.text_input("🔍 Search in PDF content")
    if search_query:
     st.subheader("🔎 Search Results")
     matched_lines = [line for line in pdf_text.split('\n') if search_query.lower() in line.lower()]

     if matched_lines:
        for line in matched_lines:
            st.write(f"- {line}")
     else:
        st.info("❌ No matches found.")

    # Summarization
    if st.button("💡 Summarize PDF"):
        with st.spinner("Using AI to summarize your PDF..."):
            response = co.summarize(
                text=pdf_text_translated,
                length='medium',
                format='paragraph',
                model='command'
            )
            summary = response.summary

       
            st.subheader("🧠 AI Summary:")
            st.write(summary)

    # Q&A Section
    st.subheader("🤖 Ask Questions About the PDF")
    user_question = st.text_input("Ask a question based on the PDF content:")

    if user_question:
      with st.spinner("Thinking... 💭"):
        context = pdf_text[:3000]

        try:
            response = co.generate(
                model='command',
                prompt=f"""Answer the following question based only on the content of the PDF:

PDF Content:
{context}

Question: {user_question}
Answer:""",
                max_tokens=200
            )
            answer = response.generations[0].text.strip()

            # Store in history
            st.session_state.chat_history.append((user_question, answer))

            st.markdown(f"**Answer:** {answer}")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

            # 🔊 Speak Answer Button (Correctly indented inside try block)
            if st.button("🔊 Speak Answer"):
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
                engine.say(answer)
                engine.runAndWait()

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

    # Sidebar: Chat history + clear button
with st.sidebar:
    st.markdown("## 💬 Chat History")

    if st.session_state.chat_history:
        for i, (q, a) in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
    else:
        st.write("No questions asked yet.")

    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")

