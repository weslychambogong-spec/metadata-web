from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    saved_files = []

    for file in files:
        if file.filename != "":
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            saved_files.append(file.filename)

    return f"Uploaded successfully: {', '.join(saved_files)}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
