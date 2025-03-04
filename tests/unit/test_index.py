import pytest

def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Batch PDF" in response.data  # Check if the page title is present

def test_file_upload_form(client):
    response = client.get('/')
    assert b'<form class="doc-form control"' in response.data  # Check if the form is present
    assert b'<input type="file" id="wordFile"' in response.data  # Check if the file input is present

def test_radio_buttons(client):
    response = client.get('/')
    assert b'<input type="radio" name="radioButton" value="manually"' in response.data  # Check if the "Manually" radio button is present
    assert b'<input type="radio" name="radioButton" value="excel"' in response.data  # Check if the "Excel" radio button is present

def test_manual_input_view_display(client):
    # Simulate selecting the "Manually" radio button
    response = client.get('/')
    assert b'<div id="manuallyView"' in response.data

def test_excel_input_view_display(client):
    # Simulate selecting the "Excel" radio button
    response = client.get('/')
    assert b'<div id="excelView"' in response.data