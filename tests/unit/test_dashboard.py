import pytest
import os

@pytest.fixture
def sample_docx_file():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'sample.docx')

    if not os.path.exists(file_path):
        pytest.skip("Sample .docx file not found. Please add it")
    
    return file_path

def test_dashboard_page_loads(client, sample_docx_file):
    # Simulate a POST request to the dashboard route with a file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert response.status_code == 200
    assert b"Transforming into PDFs" in response.data  # Check if the progress card is present

def test_placeholder_form(client, sample_docx_file):
    # Simulate a POST request to the dashboard route with a file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert b'<form id="placeholderForm"' in response.data  # Check if the placeholder form is present

def test_pdf_embed(client, sample_docx_file):
    # Simulate a POST request to the dashboard route with a file
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
    assert b'<embed src="/uploads/temp/output.pdf"' in response.data  # Check if the PDF embed is present

def test_missing_form_data(client, sample_docx_file):
    # Simulate a POST request without required form data
    with open(sample_docx_file, 'rb') as f:
        response = client.post('/dashboard', data={'wordFile': f})
    assert response.status_code == 400
    assert b"Missing required form data" in response.data

# def test_invalid_file_format(client):
#     # Simulate a POST request with an invalid file format
#     with open('app/uploads/sample.txt', 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert response.status_code == 400
#     assert b"Invalid file format. Please upload a .docx file." in response.data