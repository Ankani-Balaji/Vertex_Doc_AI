from flask import Blueprint, request, render_template, session

from services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    question = request.form.get("question")

    if question:

        answer = ChatService.ask_question(question)

        history = session.get("history", [])

        history.append({
            "question": question,
            "answer": answer
        })

        session["history"] = history[-5:]

    return render_template(
        "index.html",
        uploaded_file=session.get("uploaded_file"),
        extracted_text=session.get("extracted_text"),
        summary=session.get("summary"),
        history=session.get("history", [])
    )