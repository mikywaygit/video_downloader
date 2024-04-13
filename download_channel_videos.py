from flask import Flask, request, render_template_string, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# Set a default download directory inside the server's file system
DEFAULT_DOWNLOAD_DIR = "downloads"

HTML = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        input[type=text], input[type=submit] {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            box-sizing: border-box;
        }
        input[type=submit] {
            background-color: #5cb85c;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        input[type=submit]:hover {
            background-color: #4cae4c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Video/Channel Downloader</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter YouTube Video/Channel URL" required>
            <!-- The output_path is now a hidden input, so users do not need to fill it out -->
            <input type="hidden" name="output_path" value="downloads">
            <input type="submit" value="Download">
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output_path = request.form.get('output_path', DEFAULT_DOWNLOAD_DIR)

        # Make sure the default download directory exists
        os.makedirs(output_path, exist_ok=True)

        # Perform the download
        download(url, output_path)
        # Since we're using a server directory, provide feedback to the user
        return "Download started. Check the 'downloads' directory on the server."
    return render_template_string(HTML)

def download(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    # Ensure the default download directory exists
    os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)
    # Run the Flask app
    app.run(debug=True)
