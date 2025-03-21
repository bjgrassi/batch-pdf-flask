import pytest
from app import create_app
import os

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def sample_docx_file():
    # Get the directory of the current file (conftest.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to sample.docx in the static directory
    sample_file_path = os.path.join(current_dir, "static", "sample.docx")
    return sample_file_path

@pytest.fixture
def sample_excel_file():
    # Get the directory of the current file (conftest.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to sample.docx in the static directory
    sample_file_path = os.path.join(current_dir, "static", "sample.xlsx")
    return sample_file_path

@pytest.fixture
def sample_wrong_file_type():
    # Get the directory of the current file (conftest.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to sample.docx in the static directory
    sample_file_path = os.path.join(current_dir, "static", "wrong.txt")
    return sample_file_path