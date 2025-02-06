from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import re
import os
from docxtpl import DocxTemplate
from docx2pdf import convert
import pythoncom

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

def docx_to_html(file_path):
    doc = DocxTemplate(file_path)
    docx_obj = doc.get_docx()
    html_content = ""
    for para in docx_obj.paragraphs:
        html_content += f"<p>{para.text}</p>"

    return html_content


@app.route("/", methods=['GET', 'POST'])
def home_page():
    success_message = request.args.get('success', None)
    return render_template('index.html', success_message=success_message)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.docx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            placeholders = extract_placeholders_from_docx(file_path)
            html_content = docx_to_html(file_path) 
            return render_template('dashboard.html', placeholders=placeholders, file_path=file_path, file_name=file.filename, html_content=html_content)
        else:
            return "Invalid file format. Please upload a .docx file.", 400
    return render_template('index.html')
    
@app.route("/post-doc-form", methods=['POST'])
def transform_file():
    try:
        # Initialize the COM library
        pythoncom.CoInitialize()

        file_path = request.form['file_path']
        print(f"File path: {file_path}")  # Debugging: Log the file path

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Fill the placeholders
        doc = DocxTemplate(file_path)
        context = {key: request.form[key] for key in request.form if key != 'file_path' and key != 'fileName'}
        print(f"Context: {context}")  # Debugging: Log the context data
        doc.render(context)

        # Save the rendered document temporarily
        temp_docx = os.path.join(app.config['UPLOAD_FOLDER'], "temp_output.docx")
        doc.save(temp_docx)
        print(f"Temporary DOCX saved: {temp_docx}")  # Debugging: Log the temp DOCX path

        # Convert the temporary .docx to PDF
        output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{request.form['fileName']}.pdf")
        convert(temp_docx, output_pdf)
        print(f"PDF saved: {output_pdf}")  # Debugging: Log the PDF path

        response = make_response(send_file(output_pdf, mimetype='application/pdf'))
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # Cache for 1 year
        response.headers['Expires'] = '31536000'  # Expires in 1 year

        # Return the PDF file as a response
        return response

    except Exception as e:
        print(f"Error in transform_file: {e}")
        return f"An error occurred: {str(e)}", 500
    finally:
        # Uninitialize the COM library
        pythoncom.CoUninitialize()
        os.remove(temp_docx)  # Delete the .docx

if __name__ == "__main__":
    app.run(debug=True)