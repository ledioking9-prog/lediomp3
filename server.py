from flask import Flask, request, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Server running"

@app.route("/convert")
def convert():
    url = request.args.get("url")

    if not url:
        return "No URL provided", 400

    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": file_id,  # no extension here
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
        "noplaylist": True
    }

    try:
        # download + convert
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # check if file exists
        if not os.path.exists(filename):
            return "Conversion failed (file not created)", 500

        # send file
        return send_file(filename, as_attachment=True)

    except Exception as e:
        print("ERROR:", str(e))
        return str(e), 500

    finally:
        # clean up file after sending (optional)
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
