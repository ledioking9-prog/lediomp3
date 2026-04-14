from flask import Flask, request, send_file, send_from_directory
import yt_dlp
import uuid
import os

app = Flask(__name__)

# ---------------- UI (your website) ----------------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/script.js")
def js():
    return send_from_directory(".", "script.js")

@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")


# ---------------- CONVERTER ----------------
@app.route("/convert")
def convert():
    url = request.args.get("url")

    if not url:
        return "No URL provided", 400

    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": file_id,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(filename):
            return "Conversion failed", 500

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e), 500


# ---------------- RENDER PORT FIX ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
