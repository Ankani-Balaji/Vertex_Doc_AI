import os
from services.pdf_service import PDFService

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    current_app,
)

from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)


ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        if "pdf_file" not in request.files:

            flash("No file selected.", "danger")
            return redirect(request.url)

        file = request.files["pdf_file"]

        if file.filename == "":
            flash("Please choose a PDF file.", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            upload_folder = current_app.config["UPLOAD_FOLDER"]

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)
            raw_text = PDFService.extract_text(filepath)

            flash("PDF uploaded successfully!", "success")

            return render_template(
                "index.html",
                uploaded_file=filename,
                extracted_text=raw_text,
            )

        flash("Only PDF files are allowed.", "danger")

    return render_template("index.html")