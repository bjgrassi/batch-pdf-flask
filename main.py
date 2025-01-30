from flask import Flask, render_template, request, redirect, url_for
import re
import os
from docxtpl import DocxTemplate
from docx2pdf import convert

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Extract placeholders like {{first_name}} from a .docx file.
def extract_placeholders_from_docx(doc_path):
    try:
        doc = DocxTemplate(doc_path)
        docx_obj = doc.get_docx()
        placeholders = set()
        
        # Scan document for placeholders
        for para in docx_obj.paragraphs:
            matches = re.findall(r"{{(.*?)}}", para.text)
            placeholders.update(matches)
    
    except Exception as e:
        print(f"Error loading document: {e}")
    
    return list(placeholders)

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.docx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            placeholders = extract_placeholders_from_docx(file_path)
            return render_template('index.html', placeholders=placeholders, file_path=file_path, file_name=file.filename)
        else:
            return "Invalid file format. Please upload a .docx file.", 400
    return render_template('index.html')

@app.route("/transform", methods=['POST'])
def transform_file():
    file_path = request.form['file_path']
    doc = DocxTemplate(file_path)
    context = {key: request.form[key] for key in request.form if key != 'file_path' and key != 'fileName'}
    doc.render(context)

    # Save the rendered document temporarily
    temp_docx = os.path.join(app.config['UPLOAD_FOLDER'], "temp_output.docx")
    doc.save(temp_docx)

    # Convert the temporary .docx to PDF
    output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{request.form['fileName']}.pdf")
    convert(temp_docx, output_pdf)

    # Delete the temporary .docx file
    os.remove(temp_docx)

    return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run(debug=True)