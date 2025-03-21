import pytest

@pytest.fixture
def test_dashboard_page_loads(client, sample_docx_file):
    # Simulate a POST request to the dashboard route with a file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert response.status_code == 200
    assert b"Transforming into PDFs" in response.data  # Check if the progress card is present
    
def test_placeholder_extraction(client, sample_docx_file):
    # Test placeholder extraction from .docx file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert b'<input class="input is-small" type="text" name="0_first_name"' in response.data
    assert b'<input class="input is-small" type="text" name="0_last_name"' in response.data
    assert b'<input class="input is-small" type="text" name="0_phone"' in response.data

def test_excel_data_population(client, sample_docx_file, sample_excel_file):
    # Test Excel data population into placeholder fields
    with open(sample_docx_file, 'rb') as docx_f, open(sample_excel_file, 'rb') as excel_f:
        response = client.post('/dashboard', data={'wordFile': docx_f, 'excelFile': excel_f, 'radioButton': 'excel', 'batchQuantity': '1'})
    assert b'<input class="input is-small" type="text" name="0_first_name"' in response.data
    assert b'<input class="input is-small" type="text" name="0_last_name"' in response.data
    assert b'<input class="input is-small" type="text" name="0_phone"' in response.data

def test_batch_quantity_handling(client, sample_docx_file):
    # Test batch quantity handling
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '3'})
    assert b'<div id="0_form"' in response.data
    assert b'<div id="1_form"' in response.data
    assert b'<div id="2_form"' in response.data

def test_pdf_preview_generation(client, sample_docx_file):
    # Test PDF preview generation
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert b'<embed\n      src="/uploads/output.pdf"' in response.data

def test_pdf_preview_reload(client, sample_docx_file):
    # Step 1: Upload a .docx file to the dashboard
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    
    # Ensure the dashboard page loads successfully
    assert response.status_code == 200
    assert b'<input class="input is-small" type="text" name="0_first_name"' in response.data  # Ensure the input field is present

    # Step 2: Simulate an input change (e.g., change the value of 'first_name')
    response = client.post(
        '/generate-pdf-preview',
        json={
            "index": 0,
            "formData": {
                "0_first_name": "John",  # Change the value of 'first_name'
                "0_last_name": "Doe",   # Other fields can remain unchanged
                "0_phone": "1234567890"
            }
        }
    )

    # Step 3: Verify that the PDF preview reloads
    assert response.status_code == 200

def test_form_navigation(client, sample_docx_file):
    # Test form navigation with "Previous" and "Next" buttons
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '2'})
    assert b'<button\n                type="button"\n                id="nextButton"' in response.data
    assert b'<button\n                type="button"\n                id="previousButton"' in response.data

    # Simulate clicking "Next" button
    response = client.post(
        '/generate-pdf-preview',
        json={
            "index": 1,
            "formData": {
                "1_first_name": "",
                "1_last_name": "",
                "1_phone": ""
            }
        }
    )
    assert b'{"message":"PDF generated successfully","pdf_path":"/uploads/preview_1.pdf"}' in response.data
    # Simulate clicking "Previous" button
    response = client.post(
        '/generate-pdf-preview',
        json={
            "index": 0,
            "formData": {
                "first_name": "Jane",
                "last_name": "Silva",
                "phone": "1234567"
            }
        }
    )
    assert b'{"message":"PDF generated successfully","pdf_path":"/uploads/preview_0.pdf"}' in response.data

def test_file_name_pattern_selection(client, sample_docx_file):
    # Step 1: Upload a .docx file to the dashboard
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    
    # Ensure the dashboard page loads successfully
    assert response.status_code == 200
    assert b'<input type="checkbox" name="checkbox" value="first_name"' in response.data  # Ensure checkboxes are present
    assert b'<input type="checkbox" name="checkbox" value="last_name"' in response.data

    # Step 2: Simulate selecting the checkboxes for first_name and last_name
    with open(sample_docx_file, 'rb') as f:  # Reopen the file
        response = client.post(
            '/dashboard',
            data={
                'wordFile': f,
                'radioButton': 'manually',
                'batchQuantity': '1',
                'checkbox': ['first_name', 'last_name']  # Simulate selecting both checkboxes
            }
        )

    # Step 3: Verify that the file name pattern input field is updated correctly
    assert response.status_code == 200
    assert b'<input class="input is-small" type="text" name="fileName"' in response.data  # Check the pattern

def test_form_submission_and_zip_generation(client, sample_docx_file):
    # Test form submission and ZIP file generation
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': 'John', 'last_name': 'Doe', 'fileNamePattern': 'first_name-last_name'})
    assert response.status_code == 200

def test_progress_card_display(client, sample_docx_file):
    # Test progress card display during file processing
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert b'<div id="progressCard"' in response.data

def test_error_handling_missing_placeholder_values(client, sample_docx_file):
    # Test error handling for missing placeholder values
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1', 'first_name': '', 'last_name': ''})
    assert b'<button type="button" id="submitButton"' in response.data

def test_form_data_submission_to_backend(client, sample_docx_file):
    # Step 1: Upload a .docx file to the dashboard
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    
    # Ensure the dashboard page loads successfully
    assert response.status_code == 200
    assert b'<input class="input is-small" type="text" name="0_first_name"' in response.data  # Ensure input fields are present

    # Step 2: Simulate form data submission
    form_data = {
        "formDataArray": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890"
            }
        ],
        "fileName": "first_name-last_name"
    }

    response = client.post(
        '/post-doc-form',
        json=form_data,  # Send JSON data
        headers={'Content-Type': 'application/json'}
    )

    # Step 3: Verify the response from the backend
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'  # Ensure the response is a ZIP file
    assert response.headers['Content-Disposition'] == 'attachment; filename=first_name-last_name.zip'  # Check the filename