import os
import tempfile
import shutil
import zipfile
from flask import Flask, request, send_file, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
import weasyprint

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for flashing messages

ALLOWED_EXTENSIONS = {'zip'}
OUTPUT_DIR = tempfile.mkdtemp()
DESCRIPTION_FILES = ["README.md", "README.txt", "description.txt"]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_notebook(base_dir, notebook_title):
    formatter = HtmlFormatter(style="tango", full=False)

    html_content = [
        "<html><head><meta charset='utf-8'>",
        f"<style>{formatter.get_style_defs('.highlight')}</style>",
        "<style>",
        "body { font-family: 'DejaVu Sans Mono', monospace; font-size: 12px; padding: 2rem; }",
        "h1 { text-align: center; margin-bottom: 3rem; font-weight: 700; }",
        "h2 { color: #2e86c1; border-bottom: 3px solid #a3c1da; padding-bottom: .3rem; margin-top: 3rem; font-weight: 600; }",
        "h3 { border-bottom: 1px solid #ddd; padding-bottom: .2rem; margin-top: 2rem; font-weight: 600; }",
        "p.description { font-style: italic; color: #555; margin-bottom: 1.5rem; font-size: 0.95rem; }",
        "a { text-decoration: none; color: #2e86c1; }",
        ".highlight pre { white-space: pre-wrap; word-wrap: break-word; overflow-wrap: anywhere; font-family: monospace; margin: 0; padding: 1em; background: #f8f8f8; border-radius: 5px; font-size: 12px; line-height: 1.4; }",
        "</style></head><body>",
        f"<h1>{notebook_title}</h1>",
    ]

    folder_map = {}
    folder_descriptions = {}

    all_files = []
    for root, _, files in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        chapter_name = "Root" if rel_root == "." else rel_root.replace("\\", "/")
        folder_map.setdefault(chapter_name, [])

        for desc_file in DESCRIPTION_FILES:
            desc_path = os.path.join(root, desc_file)
            if os.path.exists(desc_path):
                with open(desc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    folder_descriptions[chapter_name] = f.read().strip()
                break

        for filename in sorted(files):
            if filename not in DESCRIPTION_FILES:
                folder_map[chapter_name].append(os.path.join(root, filename))
                all_files.append((chapter_name, os.path.join(root, filename)))

    # Table of contents
    html_content.append("<h2>Table of Contents</h2><ol>")
    chapter_index = 0
    for chapter, files in sorted(folder_map.items()):
        html_content.append(f'<li><strong>{chapter}</strong><ol>')
        for file_path in files:
            file_name = os.path.basename(file_path)
            file_id = f"{chapter_index}-{file_name}"
            html_content.append(f'<li><a href="#file{file_id}">{file_name}</a></li>')
        html_content.append("</ol></li>")
        chapter_index += 1
    html_content.append("</ol>")

    # Content
    chapter_index = 0
    for chapter, files in sorted(folder_map.items()):
        chapter_index += 1
        html_content.append(f'<h2 id="chapter{chapter_index}">{chapter}</h2>')
        if chapter in folder_descriptions:
            html_content.append(f'<p class="description">{folder_descriptions[chapter]}</p>')
        for file_path in files:
            file_name = os.path.basename(file_path)
            file_id = f"{chapter_index}-{file_name}"
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                lexer = guess_lexer_for_filename(file_name, code)
                highlighted = highlight(code, lexer, formatter)
                html_content.append(f'<h3 id="file{file_id}">{file_name}</h3>')
                html_content.append(highlighted)
            except Exception as e:
                print(f"Skipping {file_name}: {e}")

    html_content.append("</body></html>")

    html_file = os.path.join(base_dir, "all_codes.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

    output_pdf_path = os.path.join(OUTPUT_DIR, "notebook.pdf")
    weasyprint.HTML(html_file).write_pdf(output_pdf_path)

    return output_pdf_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, filename)
        file.save(zip_path)

        extract_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Get the notebook title from the form, fallback to default
            notebook_title = request.form.get('title', '').strip()
            if not notebook_title:
                notebook_title = "My Notebook"

            pdf_path = generate_notebook(extract_dir, notebook_title)

            # Secure filename for download
            download_name = secure_filename(notebook_title) + ".pdf"

            return send_file(pdf_path, as_attachment=True, download_name=download_name)
        finally:
            shutil.rmtree(temp_dir)
            shutil.rmtree(extract_dir)
    else:
        flash('Allowed file type is .zip')
        return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
