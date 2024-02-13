import os

from flask import Flask, request
from flask_cors import CORS
from main import Peap
from config import AppConfig
from data_store import FileSystemDataStore
import itertools


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/uploadfile", methods=["POST"])
def upload_file():
    config = AppConfig()
    ds = FileSystemDataStore(config)
    
    peap = Peap(ds)
    files = request.files.getlist('files')

    for file in files:
        peap.process_pdf(file) 
       
    return ds.read()


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_RUN_PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
