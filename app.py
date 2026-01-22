from flask import Flask, render_template, request
import os, csv, re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

BASE_KEYWORDS = [
    "eco","ecology","environment","environmental","green","sustainability","sustainable",
    "nature","natural","renewable","recycle","recycling","energy","clean energy",
    "climate","climate change","earth","planet","conservation","environmental protection",
    "green technology","eco friendly","zero waste","bio","organic","green living",
    "environmental care","nature protection","clean environment","environmental awareness",
    "outline icon","line icon","minimal icon","vector","symbol","pictogram","infographic","ui icon"
]

def detect_category(text):
    t = text.lower()
    if any(w in t for w in ["eco","tree","solar","water","climate","recycle","green"]):
        return "Nature"
    if any(w in t for w in ["business","finance","growth","money","startup"]):
        return "Business"
    if any(w in t for w in ["technology","tech","ai","digital","data"]):
        return "Technology"
    return "Nature"

def clean_title(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r"(minimal|outline|vector|icon|of)", "", name, flags=re.I)
    name = re.sub(r"[_\-]+"," ",name).strip()
    words = name.title().split()
    if len(words) < 5:
        words += ["Environmental","Sustainability","Concept"]
    return " ".join(words[:8]) + " Vector Icon"

def unique_keywords(filename):
    base = set(BASE_KEYWORDS)
    words = re.findall(r"[a-zA-Z]+", filename.lower())
    extra = set(words[:8])
    all_kw = list(base.union(extra))
    return ", ".join(all_kw[:50])

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("files")
        if not files or files[0].filename == "":
            return render_template("index.html", message="No file selected")

        sites = ["shutterstock","adobe","dreamstime","123rf","vecteezy","istock"]
        writers, handles = {}, {}

        for s in sites:
            f = open(os.path.join(OUTPUT_FOLDER,f"{s}.csv"),"w",newline="",encoding="utf-8")
            w = csv.writer(f)
            w.writerow(["filename","title","keywords","category"])
            writers[s]=w
            handles[s]=f

        for file in files:
            title = clean_title(file.filename)
            keywords = unique_keywords(file.filename)
            category = detect_category(file.filename)

            for w in writers.values():
                w.writerow([file.filename,title,keywords,category])

        for f in handles.values():
            f.close()

        return render_template("index.html",message="✅ Unique metadata CSV generated")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
