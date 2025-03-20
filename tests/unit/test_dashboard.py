import pytest
import os

@pytest.fixture
def test_dashboard_page_loads(client, sample_docx_file):
    # Simulate a POST request to the dashboard route with a file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert response.status_code == 200
    assert b"Transforming into PDFs" in response.data  # Check if the progress card is present

# def test_placeholder_form(client, sample_docx_file):
#     # Simulate a POST request to the dashboard route with a file
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<form id="placeholderForm"' in response.data  # Check if the placeholder form is present
    
# def test_placeholder_extraction(client, sample_docx_file):
#     # Test placeholder extraction from .docx file
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<input type="text" id="first_name"' in response.data
#     assert b'<input type="text" id="last_name"' in response.data

# def test_excel_data_population(client, sample_docx_file, sample_excel_file):
#     # Test Excel data population into placeholder fields
#     with open(sample_docx_file, 'rb') as docx_f, open(sample_excel_file, 'rb') as excel_f:
#         response = client.post('/dashboard', data={'wordFile': docx_f, 'excelFile': excel_f, 'radioButton': 'excel', 'batchQuantity': '1'})
#     assert b'<input type="text" id="first_name" value="John"' in response.data
#     assert b'<input type="text" id="last_name" value="Doe"' in response.data

# def test_batch_quantity_handling(client, sample_docx_file):
#     # Test batch quantity handling
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '3'})
#     assert b'<div id="form1"' in response.data
#     assert b'<div id="form2"' in response.data
#     assert b'<div id="form3"' in response.data

# def test_pdf_preview_generation(client, sample_docx_file):
#     # Test PDF preview generation
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<iframe id="pdfPreview"' in response.data

# def test_pdf_preview_reload(client, sample_docx_file):
#     # Test PDF preview reload on input change
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<input type="text" id="first_name"' in response.data
#     # Simulate input change and check if PDF preview reloads
#     response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': 'Jane'})
#     assert b'<iframe id="pdfPreview"' in response.data

# def test_form_navigation(client, sample_docx_file):
#     # Test form navigation with "Previous" and "Next" buttons
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '2'})
#     assert b'<button id="nextButton"' in response.data
#     assert b'<button id="previousButton"' in response.data
#     # Simulate clicking "Next" button
#     response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '2', 'formIndex': '1'})
#     assert b'<div id="form2"' in response.data
#     # Simulate clicking "Previous" button
#     response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '2', 'formIndex': '0'})
#     assert b'<div id="form1"' in response.data

# def test_file_name_pattern_selection(client, sample_docx_file):
#     # Test file name pattern selection
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<input type="checkbox" id="first_name_checkbox"' in response.data
#     assert b'<input type="checkbox" id="last_name_checkbox"' in response.data
#     # Simulate selecting checkboxes
#     response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name_checkbox': 'on', 'last_name_checkbox': 'on'})
#     assert b'<input type="text" id="fileNamePattern" value="first_name-last_name"' in response.data

# def test_form_submission_and_zip_generation(client, sample_docx_file):
#     # Test form submission and ZIP file generation
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': 'John', 'last_name': 'Doe', 'fileNamePattern': 'first_name-last_name'})
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/zip'
#     assert response.headers['Content-Disposition'] == 'attachment; filename=output.zip'

# def test_progress_card_display(client, sample_docx_file):
#     # Test progress card display during file processing
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert b'<div id="progressCard"' in response.data

# def test_error_handling_missing_placeholder_values(client, sample_docx_file):
#     # Test error handling for missing placeholder values
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': '', 'last_name': ''})
#     assert b'<button id="zipFilesButton" disabled>' in response.data

# def test_form_data_submission_to_backend(client, sample_docx_file):
#     # Test form data submission to backend
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': 'John', 'last_name': 'Doe'})
#     assert response.status_code == 200
#     assert b'"first_name": "John"' in response.data
#     assert b'"last_name": "Doe"' in response.data

# def test_invalid_file_format(client):
#     # Simulate a POST request with an invalid file format
#     with open('../static/wrong.txt', 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert response.status_code == 400
#     assert b"Invalid file format. Please upload a .docx file." in response.data