from flask import Flask, request, jsonify, render_template, session
import PyPDF2
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# ✅ Configure Gemini API
genai.configure(api_key="-------")

# ✅ Load textbook content globally (Not in session)
TEXTBOOK_PATH = "-------"
textbook_content = ""

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""  
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

if os.path.exists(TEXTBOOK_PATH):
    textbook_content = extract_text_from_pdf(TEXTBOOK_PATH)
    print("✅ Textbook loaded successfully.")
else:
    print("❌ Error: Textbook file not found!")

# ✅ Chatbot Route (Proper Session Handling)
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # ✅ Handle invalid or ambiguous input
    if not user_message or len(set(user_message)) == 1:  # Checks if input is repeated characters like "??"
        return jsonify({"response": "Please ask a clear question."})

    # ✅ Retrieve previous chat history
    chat_history = session.get("chat_history", [])

    # ✅ Check if the user asks for more information
    if "more" in user_message.lower() or "explain more" in user_message.lower() or "tell me more" in user_message.lower():
        # If the user asks for more info, repeat the last response and provide additional content from the textbook
        last_question = chat_history[-1]["user"] if chat_history else ""
        last_answer = chat_history[-1]["bot"] if chat_history else ""

        # Update the prompt to provide more detailed content
        prompt = f"""
        You are a helpful study assistant. 
        Please continue the previous explanation with additional details.
        **Previous Question**: {last_question}
        **Previous Answer**: {last_answer}
        
        **Relevant Textbook Content (Use only as reference, don’t copy directly)**:
        {textbook_content[:5000]}  # You can adjust this length if needed.

        **Answer:**
        """
    else:
        # Regular user question, proceed with initial prompt
        prompt = f"""
        You are a helpful and interactive study assistant. Your responses should be:
        - Concise and directly answer the user's question using the textbook content.
        - Avoid unnecessary elaboration and provide clear, relevant information.
        - If the user asks for more information, provide more from the textbook without repeating.
        
        **User Question**: {user_message}
        
        **Relevant Textbook Content (Use only as reference, don’t copy directly)**:
        {textbook_content[:5000]}  

        **Answer:**
        """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt).text.strip()
    except Exception as e:
        return jsonify({"error": f"Error with Gemini API: {str(e)}"}), 500

    # ✅ Store only the last 5 messages in session
    chat_history.append({"user": user_message, "bot": response})
    session["chat_history"] = chat_history[-5:]

    # ✅ Make the bot interactive by asking for more questions or explaining more
    interactive_response = f"{response} \n\nWould you like to ask more about this topic or need further explanation?"

    return jsonify({"response": interactive_response})

# ✅ Clear Chat Route
@app.route("/clear", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    return jsonify({"message": "Chat history cleared!"})

@app.route("/session", methods=["GET"])
def view_session():
    return jsonify(session)

# ✅ Serve Frontend
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
