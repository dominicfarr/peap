import os

from flask import Flask, request
from flask_cors import CORS
from main import AppConfig, Peap

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/uploadfile", methods=["POST"])
def upload_file():
    uploaded_file = request.files["myFile"]

    peap = Peap(
        AppConfig(
            config_path=None,
            inline={
                "rules": [
                    {
                        "pattern": "TD®Aeroplan®Visa Infinite",
                        "label": "TD Aeroplan Visa",
                        "class": "TD",
                    },
                    {"pattern": "PTK", "label": "Pass The Keys"},
                ],
                "output": "results.csv",
                "delimiter": "|",
            },
        )
    )

    peap._process_pdf(uploaded_file)

    return "Hello, World!"


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_RUN_PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
