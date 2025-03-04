import pytest

# def test_upload_word_file(client):
#     # Simulate uploading a Word file and check if the dashboard loads
#     with open('tests/sample.docx', 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert response.status_code == 200
#     assert b"Transforming into PDFs" in response.data  # Check if the dashboard loads after upload

# def test_upload_excel_file(client):
#     # Simulate uploading an Excel file and check if the dashboard loads
#     with open('tests/sample.docx', 'rb') as f, open('tests/sample.xlsx', 'rb') as excel_f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'excel', 'excelFile': excel_f})
#     assert response.status_code == 200
#     assert b"Transforming into PDFs" in response.data  # Check if the dashboard loads after upload

# def test_save_file(client):
#     # Simulate filling the form and saving the file
#     with open('tests/sample.docx', 'rb') as f:
#         client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     response = client.post('/post-doc-form', json={
#         'formDataArray': [{'placeholder1': 'value1', 'placeholder2': 'value2'}],
#         'fileName': 'test_file'
#     })
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/zip'  # Check if the response is a ZIP file