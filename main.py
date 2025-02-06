from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import re
import os
from docxtpl import DocxTemplate
from docx2pdf import convert
import pythoncom
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

file_path = ''

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
            batch_quantity = int(request.form.get('batchQuantity', 1))
            print(batch_quantity)
            global file_path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            placeholders = extract_placeholders_from_docx(file_path)
            html_content = docx_to_html(file_path) 
            return render_template(
                'dashboard.html', placeholders=placeholders, file_name=file.filename,
                batch_quantity=batch_quantity, html_content=html_content
            )
        else:
            return "Invalid file format. Please upload a .docx file.", 400
    return render_template('index.html')
    
@app.route("/post-doc-form", methods=['POST'])
def transform_file():
    try:
        # Initialize the COM library
        pythoncom.CoInitialize()

        data = request.get_json()
        form_data_array = data['formDataArray']
        file_name = data['fileName']
        print(file_name)

        pdf_files = []

        for index, form_data in enumerate(form_data_array):
            # Fill the placeholders
            doc = DocxTemplate(file_path)
            doc.render(form_data)

            # Save the rendered document temporarily
            temp_docx = os.path.join(app.config['UPLOAD_FOLDER'], f"{index}_{file_name}.docx")
            doc.save(temp_docx)

            # Convert the temporary .docx to PDF
            output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{index}_{file_name}.pdf")
            convert(temp_docx, output_pdf)
            pdf_files.append(output_pdf)

        # Create a ZIP file and add all PDFs to it
        zipfile_name = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_name}.zip")
        with zipfile.ZipFile(zipfile_name, "w") as myzip:
            for pdf_file in pdf_files:
                # Add each PDF file to the ZIP archive
                myzip.write(pdf_file, os.path.basename(pdf_file))

        # Send the ZIP file as a response
        return send_file(zipfile_name, mimetype='application/zip', as_attachment=True, download_name=f"{file_name}.zip")

    except Exception as e:
        print(f"Error in transform_file: {e}")
        return f"An error occurred: {str(e)}", 500
    finally:
        # Uninitialize the COM library
        pythoncom.CoUninitialize()

        # Clean up temporary files
        for index in range(len(form_data_array)):
            temp_docx = os.path.join(app.config['UPLOAD_FOLDER'], f"{index}_{file_name}.docx")
            if os.path.exists(temp_docx):
                os.remove(temp_docx)  # Delete the .docx

            temp_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{index}_{file_name}.pdf")
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)  # Delete the .pdf

        # # Delete the ZIP file after sending it (optional)
        # if os.path.exists(zipfile_name):
        #     os.remove(zipfile_name)

if __name__ == "__main__":
    app.run(debug=True)