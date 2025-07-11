from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Create downloads folder if it doesn't exist
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    # Load HTML page
    return open('index.html').read()

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']

    try:
        # Set yt_dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send file back to user as download
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"❌ Error downloading video: {str(e)}"

# Dynamic port binding for deployment (Render, Railway, etc.)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
