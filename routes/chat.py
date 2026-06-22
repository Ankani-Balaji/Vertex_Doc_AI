# chat.py
from flask import Blueprint, request, render_template, session
from services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    question = request.form.get("question")

    if question:
        # FIX: pass session_id as second argument
        answer = ChatService.ask_question(question, session["session_id"])

        history = session.get("history", [])
        history.append({"question": question, "answer": answer})
        session["history"] = history[-5:]

    return render_template(
        "index.html",
        uploaded_file=session.get("uploaded_file"),
        extracted_text=session.get("extracted_text"),
        summary=session.get("summary"),
        history=session.get("history", []),
        # FIX: added missing template variables
        word_count=session.get("word_count"),
        page_count=session.get("page_count"),
        chunk_count=session.get("chunk_count"),
        suggested_questions=session.get("suggested_questions", [])
    )