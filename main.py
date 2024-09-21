from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/download', methods=['POST'])
def download():
    search_term = request.form['search']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{search_term}", download=True)
        video_title = result['entries'][0]['title']
        video_filename = f"{video_title}.webm"

    return render_template('index.html', filename=video_filename)
@app.route('/play/<filename>')
def play(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=True)
