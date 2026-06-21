from reportlab.pdfgen import canvas


class ExportService:

    @staticmethod
    def build_conversation(history):

        content = "VertexDoc AI Conversation History\n"
        content += "=" * 50 + "\n\n"

        for index, chat in enumerate(history, start=1):

            content += f"Question {index}:\n"
            content += f"{chat['question']}\n\n"

            content += f"Answer {index}:\n"
            content += f"{chat['answer']}\n\n"

            content += "-" * 50 + "\n\n"

        return content

    @staticmethod
    def export_txt(content, filename="conversation.txt"):

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        return filename

    @staticmethod
    def export_pdf(content, filename="conversation.pdf"):

        pdf = canvas.Canvas(filename)

        y = 800

        for line in content.split("\n"):

            pdf.drawString(40, y, line)

            y -= 20

            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()

        return filename