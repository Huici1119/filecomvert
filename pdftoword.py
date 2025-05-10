from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf
from pdf2image import convert_from_path
import uuid
import pythoncom  # ← 加入 COM 初始化用

app = Flask(__name__)
app.secret_key = 'secretkey'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'Missing file', 400

    files = request.files.getlist('file')
    mode = request.form.get('mode')

    if not files or any(f.filename == '' for f in files):
        return 'No file selected', 400

    converted_files = []
    errors = []

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        try:
            if mode == 'pdf2docx' and ext == '.pdf':
                out_path = os.path.join(OUTPUT_FOLDER, name + '.docx')
                cv = Converter(file_path)
                cv.convert(out_path, start=0, end=None)
                cv.close()
                converted_files.append(os.path.basename(out_path))

            elif mode == 'docx2pdf' and ext == '.docx':
                try:
                    pythoncom.CoInitialize()  # 🟢 初始化 COM

                    temp_uuid = str(uuid.uuid4())
                    temp_docx = os.path.join(UPLOAD_FOLDER, f"{temp_uuid}.docx")
                    temp_pdf = os.path.join(UPLOAD_FOLDER, f"{temp_uuid}.pdf")

                    os.rename(file_path, temp_docx)
                    docx_to_pdf(temp_docx, temp_pdf)

                    final_pdf_path = os.path.join(OUTPUT_FOLDER, name + '.pdf')
                    os.rename(temp_pdf, final_pdf_path)
                    os.remove(temp_docx)
                    converted_files.append(os.path.basename(final_pdf_path))

                    pythoncom.CoUninitialize()  # 🟢 釋放 COM
                except Exception as e:
                    errors.append(f"{filename} 轉換失敗：{str(e)}")

            else:
                errors.append(f"{filename} 的副檔名不支援此模式")

        except Exception as e:
            errors.append(f"{filename} 轉換失敗：{str(e)}")

    return render_template('result_list.html', filenames=converted_files, errors=errors)

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        return "檔案不存在", 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5560, threaded=True)
