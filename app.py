from flask import Flask, render_template, request, send_file
import csv, os, io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    files = request.files.getlist("files")

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV header (industry standard)
    writer.writerow(["filename", "title", "keywords", "category"])

    for file in files:
        name = os.path.splitext(file.filename)[0]

        title = f"Minimal outline vector icon of {name.replace('-', ' ')}"
        keywords = (
            f"{name}, vector icon, outline icon, minimal icon, line icon, "
            "eco icon, sustainability, environment, green energy, climate, "
            "recycling, nature, ecology, clean design, editable stroke, "
            "isolated icon, web icon, app icon, ui ux, infographic, "
            "flat design, symbol, pictogram, illustration, eps, svg"
        )
        category = "Nature"

        writer.writerow([file.filename, title, keywords, category])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="metadata.csv"
    )

if __name__ == "__main__":
    app.run()
