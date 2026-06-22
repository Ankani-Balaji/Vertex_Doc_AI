import os
import tempfile
from reportlab.pdfgen import canvas

class ExportService:

    @staticmethod
    def build_conversation(history):
        content = "VertexDoc AI Conversation History\n"
        content += "=" * 50 + "\n\n"
        for index, chat in enumerate(history, start=1):
            content += f"Question {index}:\n{chat['question']}\n\n"
            content += f"Answer {index}:\n{chat['answer']}\n\n"
            content += "-" * 50 + "\n\n"
        return content

    @staticmethod
    def export_txt(content, filename="conversation.txt"):
        # FIX: write to system temp dir so it works on any deployment
        path = os.path.join(tempfile.gettempdir(), filename)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path

    @staticmethod
    def export_pdf(content, filename="conversation.pdf"):
        path = os.path.join(tempfile.gettempdir(), filename)
        pdf = canvas.Canvas(path)
        y = 800
        # FIX: basic word-wrap to prevent long lines overflowing
        for raw_line in content.split("\n"):
            words = raw_line.split(" ")
            line = ""
            for word in words:
                if pdf.stringWidth(line + " " + word, "Helvetica", 11) < 520:
                    line += (" " if line else "") + word
                else:
                    pdf.drawString(40, y, line)
                    y -= 18
                    line = word
                    if y < 50:
                        pdf.showPage()
                        y = 800
            if line:
                pdf.drawString(40, y, line)
                y -= 18
                if y < 50:
                    pdf.showPage()
                    y = 800
        pdf.save()
        return path