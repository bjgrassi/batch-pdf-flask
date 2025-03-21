import pytest

def test_dashboard_manual_upload(client, sample_docx_file):
    # Open the sample .docx file
    with open(sample_docx_file, 'rb') as word_file:
        # Simulate the form submission with manual input
        response = client.post('/dashboard', data={
            'wordFile': word_file,
            'radioButton': 'manually',
            'batchQuantity': '2'
        }, content_type='multipart/form-data')
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the success message and the uploaded file name are in the response
    assert b"Uploaded file:" in response.data
    assert b"PDF 1:" in response.data

def test_dashboard_excel_upload(client, sample_docx_file, sample_excel_file):
    # Open the sample .docx and .xlsx files
    with open(sample_docx_file, 'rb') as word_file, open(sample_excel_file, 'rb') as excel_file:
        # Simulate the form submission with Excel input
        response = client.post('/dashboard', data={
            'wordFile': word_file,
            'radioButton': 'excel',
            'excelFile': excel_file
        }, content_type='multipart/form-data')
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the success messages and the uploaded file names are in the response
    assert b"Uploaded file:" in response.data
    assert b"PDF 1:" in response.data

def test_generate_pdf_preview(client, sample_docx_file):    
    with open(sample_docx_file, 'rb') as word_file:
        client.post('/dashboard', data={
            'wordFile': word_file,
            'radioButton': 'manually',
            'batchQuantity': '1'
        }, content_type='multipart/form-data')
    
    response = client.post('/generate-pdf-preview', json={
        "index": 0,
        "formData": {
            "0_name": ""
        }
    })
    
    assert response.status_code == 200
    assert response.json['message'] == "PDF generated successfully"

def test_transform_file(client, sample_docx_file):    
    with open(sample_docx_file, 'rb') as word_file:
        client.post('/dashboard', data={
            'wordFile': word_file,
            'radioButton': 'manually',
            'batchQuantity': '1'
        }, content_type='multipart/form-data')
    
    response = client.post('/post-doc-form', json={
        "formDataArray": [{"first_name": "Alice"}],
        "fileName": "first_name"
    })
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'

def test_invalid_word_file_upload(client):
    response = client.post('/dashboard', data={
        'wordFile': (b'fake content', 'test.txt'),
        'radioButton': 'manually',
        'batchQuantity': '1'
    }, content_type='multipart/form-data')
    
    assert response.status_code == 400

def test_invalid_excel_file_upload(client, sample_docx_file, sample_wrong_file_type):
    with open(sample_docx_file, 'rb') as word_file, open(sample_wrong_file_type, 'rb') as wrong_f:
        response = client.post('/dashboard', data={
            'wordFile': word_file,
            'radioButton': 'excel',
            'excelFile': wrong_f
        }, content_type='multipart/form-data')
    
    assert response.status_code == 400