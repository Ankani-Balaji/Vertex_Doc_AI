import os
import uuid
from services.pdf_service import PDFService
from services.summary_service import SummaryService
from services.rag_service import RAGService
from services.chat_service import ChatService
from services.export_service import ExportService
from services.question_service import QuestionService
from flask import send_file

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    current_app,
    session,
)

from werkzeug.utils import secure_filename


upload_bp = Blueprint("upload", __name__)


ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@upload_bp.route("/")
def home():

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    if "history" not in session:
        session["history"] = []

    return render_template(
        "index.html",
        uploaded_file=session.get("uploaded_file"),
        extracted_text=session.get("extracted_text"),
        summary=session.get("summary"),
        history=session.get("history", []),
        word_count=session.get("word_count"),
        page_count=session.get("page_count"),
        chunk_count=session.get("chunk_count"),
        suggested_questions=session.get("suggested_questions", [])
    )

@upload_bp.route("/upload", methods=["POST"])
def upload_pdf():

    if "pdf_file" not in request.files:

        flash("No file selected.", "danger")
        return redirect("/")

    file = request.files["pdf_file"]

    if file.filename == "":

        flash("Please choose a PDF.", "warning")
        return redirect("/")

    if not allowed_file(file.filename):

        flash("Only PDF files are allowed.", "danger")
        return redirect("/")

    filename = secure_filename(file.filename)

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    raw_text = PDFService.extract_text(filepath)
    word_count = len(raw_text.split())
    page_count = raw_text.count("\f") + 1

    if not raw_text.strip():

        flash(
            "Unable to extract text from this PDF. Please upload a searchable PDF.",
            "danger"
        )

        return redirect("/")

    try:

        summary = SummaryService.generate_summary(raw_text)

    except Exception:

        summary = (
            "AI Summary is temporarily unavailable. "
            "Document upload completed successfully."
        )

    try:

        suggested_questions = QuestionService.generate_questions(raw_text)

    except Exception:

        suggested_questions = [
            "What is this document about?",
            "Summarize this document.",
            "What are the important points?"
        ]

    chunk_count = RAGService.create_vector_store(
        raw_text,
        session["session_id"]
    )
    session["word_count"] = word_count
    session["page_count"] = page_count
    session["chunk_count"] = chunk_count

    if chunk_count == 0:

        flash(
            "No readable text found in this PDF. It may be a scanned document.",
            "warning"
        )

        return redirect("/")

    session["uploaded_file"] = filename
    session["extracted_text"] = raw_text
    session["summary"] = summary
    session["suggested_questions"] = suggested_questions

    flash(
        f"PDF processed successfully ({chunk_count} chunks created).",
        "success"
    )

    return redirect("/")

@upload_bp.route("/ask", methods=["POST"])
def ask_question():

    question = request.form.get("question")

    if not question:

        flash("Please enter a question.", "warning")

        return redirect("/")

    answer = ChatService.ask_question(

        question,

        session["session_id"]

    )

    history = session.get("history", [])

    history.append({

        "question": question,

        "answer": answer

    })

    session["history"] = history[-5:]

    return redirect("/")

@upload_bp.route("/export/txt")
def export_txt():

    history = session.get("history", [])

    if not history:

        flash("No conversation available.", "warning")

        return redirect("/")

    content = ExportService.build_conversation(history)

    filename = ExportService.export_txt(content)

    return send_file(
        filename,
        as_attachment=True
    )

@upload_bp.route("/export/pdf")
def export_pdf():

    history = session.get("history", [])

    if not history:

        flash("No conversation available.", "warning")

        return redirect("/")

    content = ExportService.build_conversation(history)

    filename = ExportService.export_pdf(content)

    return send_file(
        filename,
        as_attachment=True
    )

@upload_bp.route("/clear")
def clear_chat():

    session["history"] = []

    flash(

        "Conversation cleared successfully.",

        "success"

    )

    return redirect("/")

@upload_bp.route("/reset")
def reset_document():

    session.pop("uploaded_file", None)
    session.pop("summary", None)
    session.pop("extracted_text", None)
    session["history"] = []

    flash(

        "Document removed successfully.",

        "success"

    )

    return redirect("/")
