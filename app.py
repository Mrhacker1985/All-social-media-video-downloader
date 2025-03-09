from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import yt_dlp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'

# Ensure the downloads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def download_video(url):
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best',  # Download the best quality available
        'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),  # Save file with title as name
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    
    return file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            file_path = download_video(video_url)
            return redirect(url_for('download', filename=os.path.basename(file_path)))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)