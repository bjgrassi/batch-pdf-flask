from flask import Blueprint, send_from_directory, render_template, request, send_file, jsonify, current_app
import re
import os
from docxtpl import DocxTemplate
from docx2pdf import convert
import pythoncom
import zipfile
import pandas as pd
import glob

# Create a Blueprint instead of a Flask app
main = Blueprint('main', __name__)

# Global variable
file_path = ''

# Define routes using the Blueprint
@main.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory('uploads', filename)

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

        for table in docx_obj.tables:
            for row in table.rows:
                for cell in row.cells:
                    matches = re.findall(r"{{(.*?)}}", cell.text)
                    placeholders.update(matches)

    except Exception as e:
        print(f"Error loading document: {e}")
    
    return list(placeholders)

# Generate PDF preview
def generate_pdf_preview(doc_path, json_data):
    try:
        # Initialize COM library
        pythoncom.CoInitialize()

        # Load the .docx template
        doc = DocxTemplate(doc_path)

        # Render the document with JSON data
        if len(json_data) > 0:
            doc.render(json_data)

        # Save to a temporary .docx file
        temp_docx = os.path.join(current_app.config['UPLOAD_FOLDER'], "transformed.docx")
        doc.save(temp_docx)

        doc = None

        # Convert the temporary .docx file to PDF
        temp_pdf = os.path.join(current_app.config['UPLOAD_FOLDER'], "output.pdf")
        convert(temp_docx, temp_pdf, keep_active=True)

        # Clean up the temporary .docx file
        if os.path.exists(temp_docx):
            os.remove(temp_docx)

        # Return the path to the generated PDF file
        return temp_pdf

    except Exception as e:
        # If there's an error, return an error message
        return f"Error generating PDF preview: {str(e)}"

    finally:
        # Uninitialize COM library
        pythoncom.CoUninitialize()

# Route to generate PDF preview
@main.route("/generate-pdf-preview", methods=['POST'])
def generate_pdf_for_current_index():
    try:
        data = request.get_json()  # Get data from the frontend
        index = data.get("index")
        form_data = data.get("formData")

        if not form_data:
            return jsonify({"error": "No form data provided"}), 400

        cleaned_data = {}
        for key, value in form_data.items():
            # Remove the numeric prefix (e.g., "2_rate3" → "rate3")
            new_key = "_".join(key.split("_")[1:])  # Remove first part (index)
            cleaned_data[new_key] = value

        generate_pdf_preview(file_path, cleaned_data)

        return jsonify({"message": "PDF generated successfully", "pdf_path": f"/uploads/preview_{index}.pdf"})

    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

# Home page route
@main.route("/", methods=['GET', 'POST'])
def home_page():
    success_message = request.args.get('success', None)
    return render_template('index.html', success_message=success_message)

# Dashboard route
@main.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        wordFile = request.files['wordFile']
        if wordFile and wordFile.filename.endswith('.docx'):
            global file_path
            file_path = os.path.join(current_app.config['STATIC_FOLDER'], wordFile.filename)
            wordFile.save(file_path)
            
            placeholders = extract_placeholders_from_docx(file_path)
            if request.form['radioButton'] == 'manually':
                batch_quantity = int(request.form.get('batchQuantity', 1))
                generate_pdf_preview(file_path, {})
                return render_template(
                    'dashboard.html', placeholders=placeholders, file_name=wordFile.filename,
                    batch_quantity=batch_quantity
                )
            else:
                excelFile = request.files['excelFile']
                if excelFile and (excelFile.filename.endswith('.xlsx') or excelFile.filename.endswith('.csv')):
                    excel_path = os.path.join(current_app.config['STATIC_FOLDER'], excelFile.filename)
                    excelFile.save(excel_path)
                    df = pd.read_excel(excel_path) if excelFile.filename.endswith('.xlsx') else pd.read_csv(excel_path)
                    excel_array = df.to_dict(orient='records')
                    pdf_content_pre = generate_pdf_preview(file_path, excel_array[0])
                    return render_template(
                        'dashboard.html', placeholders=placeholders, file_name=wordFile.filename,
                        batch_quantity=len(df), excel_array=excel_array
                    )
                else:
                    return "Invalid Excel file format. Please upload a .xlsx or .csv file.", 400
        else:
            return "Invalid file format. Please upload a .docx file.", 400
    return render_template('index.html')

# Route to handle form submission
@main.route("/post-doc-form", methods=['POST'])
def transform_file():
    try:
        # Initialize the COM library
        pythoncom.CoInitialize()
        data = request.get_json()

        form_data_array = data['formDataArray']
        file_name_pattern = data['fileName']  # e.g., "first_name-phone"

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
            temp_docx = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{dynamic_file_name}.docx")
            doc.save(temp_docx)

            # Convert the temporary .docx to PDF
            output_pdf = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{dynamic_file_name}.pdf")
            convert(temp_docx, output_pdf)

            pdf_files.append(output_pdf)

        # Create a ZIP file and add all PDFs to it
        zipfile_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{file_name_pattern}.zip")
        with zipfile.ZipFile(zipfile_path, "w") as myzip:
            for pdf_file in pdf_files:
                # Add each PDF file to the ZIP archive
                myzip.write(pdf_file, os.path.basename(pdf_file))

        # Send the ZIP file as a response
        return send_file(zipfile_path, mimetype='application/zip', as_attachment=True, download_name=f"{file_name_pattern}.zip")

    except Exception as e:
        print(f"Error in transform_file: {e}")
        return f"An error occurred: {str(e)}", 500
    finally:
        # Uninitialize the COM library
        pythoncom.CoUninitialize()

        # Construct the path pattern for .docx and .pdf files
        docx_files = glob.glob(os.path.join(current_app.config['UPLOAD_FOLDER'], '*.docx'))
        pdf_files = glob.glob(os.path.join(current_app.config['UPLOAD_FOLDER'], '*.pdf'))

        # Delete all .docx files
        for docx_file in docx_files:
            try:
                os.remove(docx_file)
            except Exception as e:
                print(f"Error deleting {docx_file}: {e}")

        # Delete all .pdf files
        for pdf_file in pdf_files:
            try:
                os.remove(pdf_file)
            except Exception as e:
                print(f"Error deleting {pdf_file}: {e}")

        # Delete the XLSX or CSV file after sending it (optional)
        # Delete the ZIP file after sending it (optional)