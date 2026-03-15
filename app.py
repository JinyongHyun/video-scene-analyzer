import os
import sys
import uuid
import subprocess
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def get_ytdlp():
    """yt-dlp를 python -m yt_dlp 방식으로 실행"""
    return [sys.executable, "-m", "yt_dlp"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL이 필요합니다"}), 400

    video_id = str(uuid.uuid4())[:8]
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    cmd = get_ytdlp() + [
        url,
        "-f", "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best[height<=720]",
        "--merge-output-format", "mp4",
        "-o", output_path,
        "--no-playlist",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            # 간단한 fallback
            cmd2 = get_ytdlp() + [url, "-f", "best[height<=480]/best", "-o", output_path, "--no-playlist"]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
            if result2.returncode != 0:
                return jsonify({"error": result2.stderr[-500:]}), 500

        if not os.path.exists(output_path):
            # 확장자가 다를 수 있음
            for f in os.listdir(DOWNLOAD_DIR):
                if f.startswith(video_id):
                    output_path = os.path.join(DOWNLOAD_DIR, f)
                    video_id = f.rsplit(".", 1)[0]
                    break

        filename = os.path.basename(output_path)
        return jsonify({"filename": filename, "video_id": video_id})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "다운로드 시간 초과"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
