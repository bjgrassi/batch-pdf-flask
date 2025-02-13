from flask import Flask, render_template, request, send_file
import re
import os
from docxtpl import DocxTemplate
from docx2pdf import convert
import pythoncom
import zipfile
import pandas as pd
import glob

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
        wordFile = request.files['wordFile']
        if wordFile and wordFile.filename.endswith('.docx'):
            global file_path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], wordFile.filename)
            wordFile.save(file_path)
            placeholders = extract_placeholders_from_docx(file_path)
            html_content = docx_to_html(file_path)

            if request.form['radioButton'] == 'manually':
                batch_quantity = int(request.form.get('batchQuantity', 1))
                return render_template(
                    'dashboard.html', placeholders=placeholders, file_name=wordFile.filename,
                    batch_quantity=batch_quantity, html_content=html_content
                )
            else:
                excelFile = request.files['excelFile']
                if excelFile and (excelFile.filename.endswith('.xlsx') or excelFile.filename.endswith('.csv')):
                    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excelFile.filename)
                    excelFile.save(excel_path)
                    df = pd.read_excel(excel_path) if excelFile.filename.endswith('.xlsx') else pd.read_csv(excel_path)
                    excel_array = df.to_dict(orient='records')
                    return render_template(
                        'dashboard.html', placeholders=placeholders, file_name=wordFile.filename,
                        batch_quantity=len(df), html_content=html_content, excel_array=excel_array
                    )
                else:
                    return "Invalid Excel file format. Please upload a .xlsx or .csv file.", 400
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
        file_name_pattern = data['fileName']  # e.g., "first_name-phone"
        print(file_name_pattern)

        pdf_files = []

        for index, form_data in enumerate(form_data_array):
            # Fill the placeholders
            doc = DocxTemplate(file_path)
            doc.render(form_data)

            # Generate the file name based on the pattern and form data
            file_name_parts = file_name_pattern.split('-')  # Split the pattern into parts
            file_name_values = []

            for part in file_name_parts:
                if part in form_data:  # Check if the placeholder exists in the form data
                    file_name_values.append(form_data[part])  # Add the corresponding value
                else:
                    file_name_values.append(part)  # Fallback to the placeholder name if value is missing

            # Join the values with hyphens to create the final file name
            dynamic_file_name = '-'.join(file_name_values)

            # Save the rendered document temporarily
            temp_docx = os.path.join(app.config['UPLOAD_FOLDER'], f"{dynamic_file_name}.docx")
            doc.save(temp_docx)

            # Convert the temporary .docx to PDF
            output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{dynamic_file_name}.pdf")
            convert(temp_docx, output_pdf)
            pdf_files.append(output_pdf)

        # Create a ZIP file and add all PDFs to it
        zipfile_name = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_name_pattern}.zip")
        with zipfile.ZipFile(zipfile_name, "w") as myzip:
            for pdf_file in pdf_files:
                # Add each PDF file to the ZIP archive
                myzip.write(pdf_file, os.path.basename(pdf_file))

        # Send the ZIP file as a response
        return send_file(zipfile_name, mimetype='application/zip', as_attachment=True, download_name=f"{file_name_pattern}.zip")

    except Exception as e:
        print(f"Error in transform_file: {e}")
        return f"An error occurred: {str(e)}", 500
    finally:
        # Uninitialize the COM library
        pythoncom.CoUninitialize()

        # Construct the path pattern for .docx and .pdf files
        docx_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.docx'))
        pdf_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.pdf'))

        # Delete all .docx files
        for docx_file in docx_files:
            try:
                os.remove(docx_file)
                print(f"Deleted: {docx_file}")
            except Exception as e:
                print(f"Error deleting {docx_file}: {e}")

        # Delete all .pdf files
        for pdf_file in pdf_files:
            try:
                os.remove(pdf_file)
                print(f"Deleted: {pdf_file}")
            except Exception as e:
                print(f"Error deleting {pdf_file}: {e}")

        # Delete the XLSX or CSV file after sending it (optional)
        # Delete the ZIP file after sending it (optional)

if __name__ == "__main__":
    app.run(debug=True)