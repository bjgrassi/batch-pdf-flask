import pytest
import os

# @pytest.fixture
# def sample_docx_file():
#     file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'sample.docx')
#     if not os.path.exists(file_path):
#         pytest.skip("Sample .docx file not found. Please add it")
#     return file_path

# @pytest.fixture
# def sample_excel_file():
#     file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'sample.xlsx')
#     if not os.path.exists(file_path):
#         pytest.skip("Sample .xlsx file not found. Please add it")
#     return file_path

# def test_radio_button_selection(client, sample_docx_file):
#     # Test "Manually" radio button
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post(
#             '/dashboard',
#             data={
#                 'radioButton': 'manually',
#                 'batchQuantity': '1',
#                 'wordFile': f  # Include the file in the data dictionary
#             },
#             content_type='multipart/form-data',  # Ensure the content type is set correctly
#             follow_redirects=True
#         )
#     assert b'<div id="manuallyView"' in response.data
#     assert b'<div id="excelView"' not in response.data

#     # Test "Excel" radio button
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post(
#             '/dashboard',
#             data={
#                 'radioButton': 'excel',
#                 'batchQuantity': '',
#                 'wordFile': f  # Include the file in the data dictionary
#             },
#             content_type='multipart/form-data',  # Ensure the content type is set correctly
#             follow_redirects=True
#         )
#     assert b'<div id="excelView"' in response.data
#     assert b'<div id="manuallyView"' not in response.data

# def test_batch_quantity_input(client):
#     # Test valid numeric input
#     response = client.post('/dashboard', data={'radioButton': 'manually', 'batchQuantity': '5'})
#     assert response.status_code == 200
#     assert b"Batch quantity set to 5" in response.data

#     # Test non-numeric input
#     response = client.post('/dashboard', data={'radioButton': 'manually', 'batchQuantity': 'abc'})
#     assert response.status_code == 400
#     assert b"Invalid batch quantity. Please enter a numeric value." in response.data

# def test_excel_file_upload(client, sample_excel_file):
#     # Test valid .xlsx file upload
#     with open(sample_excel_file, 'rb') as f:
#         response = client.post('/dashboard', data={'excelFile': f, 'radioButton': 'excel', 'batchQuantity': '1'}, content_type='multipart/form-data')
#     assert response.status_code == 200
#     assert b"File example.xlsx uploaded successfully!" in response.data

#     # Test invalid file upload
#     with open('../static/wrong.txt', 'rb') as f:
#         response = client.post('/dashboard', data={'excelFile': f, 'radioButton': 'excel', 'batchQuantity': '1'}, content_type='multipart/form-data')
#     assert response.status_code == 400
#     assert b"Invalid file type. Please upload a valid Excel (.xlsx or .csv) file." in response.data

# def test_upload_button_state(client, sample_docx_file):
#     # Test upload button state during form submission
#     with open(sample_docx_file, 'rb') as f:
#         response = client.post('/dashboard', data={'radioButton': 'manually', 'batchQuantity': '1'}, files={'wordFile': f}, follow_redirects=True)
#     assert b'<button id="uploadDocument" disabled>' not in response.data  # Button should be enabled
#     assert b'<button id="uploadDocument" disabled>' in response.data  # Button should be disabled during processing

# def test_invalid_file_format(client):
#     # Simulate a POST request with an invalid file format
#     with open('../static/wrong.txt', 'rb') as f:
#         response = client.post('/dashboard', data={'wordFile': f, 'radioButton': 'manually', 'batchQuantity': '1'})
#     assert response.status_code == 400
#     assert b"Invalid file format. Please upload a .docx file." in response.data