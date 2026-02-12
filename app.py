import os
import yt_dlp
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Map waar de video's tijdelijk worden opgeslagen
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return "Voer aub een geldige URL in.", 400

    try:
        # Alles hieronder moet ingesprongen zijn t.o.v. 'try'
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(id)s.%(ext)s',
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android'],
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.mp4"
            
        return render_template('index.html', filename=filename)
        
    except Exception as e:
        # Ook dit blok moet netjes onder 'except' staan
        return f"Er is iets misgegaan: {str(e)}", 500

@app.route('/files/<filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
