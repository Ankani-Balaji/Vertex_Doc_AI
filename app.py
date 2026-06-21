from flask import Flask, flash, redirect
from config import Config
from routes.upload import upload_bp
from routes.chat import chat_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)

    return app


app = create_app()


# Global 500 Error Handler
@app.errorhandler(500)
def internal_error(error):

    flash(
        "Something went wrong. Please try again.",
        "danger"
    )

    return redirect("/")


if __name__ == "__main__":
    app.run()