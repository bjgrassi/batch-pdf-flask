from docxtpl import DocxTemplate
from docx import Document
import xml.etree.ElementTree as ET

def docx_to_html(file_path):
    # Load the .docx file using both python-docx and docxtpl
    doc = Document(file_path)  # Using python-docx for header and body
    docx_obj = DocxTemplate(file_path)  # Using docxtpl for rendering placeholders

    # Initialize HTML content
    html_content = ""

    # 1. Extract Header Content
    for section in doc.sections:
        header = section.header
        for paragraph in header.paragraphs:
            html_content += "<div class='header'><p>"
            for run in paragraph.runs:
                text = run.text
                if run.bold:
                    text = f"<b>{text}</b>"
                if run.italic:
                    text = f"<i>{text}</i>"
                if run.underline:
                    text = f"<u>{text}</u>"
                html_content += text
            html_content += "</p></div>"

    # 2. Convert Document Paragraphs to HTML
    for para in docx_obj.get_docx().paragraphs:
        para_html = "<p>"
        for run in para.runs:
            text = run.text
            # Text formatting (bold, italic, underline)
            if run.bold:
                text = f"<b>{text}</b>"
            if run.italic:
                text = f"<i>{text}</i>"
            if run.underline:
                text = f"<u>{text}</u>"
            # Font size
            if run.font.size:
                font_size = run.font.size.pt if run.font.size else 12
                text = f'<span style="font-size:{font_size}px;">{text}</span>'
            para_html += text
        para_html += "</p>"
        html_content += para_html

    # 3. Convert Tables to HTML (including headers)
    for table in docx_obj.get_docx().tables:
        html_content += "<table border='1' style='border-collapse:collapse;'>"
        for row_idx, row in enumerate(table.rows):
            html_content += "<tr>"
            for cell_idx, cell in enumerate(row.cells):
                if row_idx == 0:  # First row as header
                    html_content += f"<th style='font-weight: bold;'>{cell.text}</th>"
                else:
                    html_content += f"<td>{cell.text}</td>"
            html_content += "</tr>"
        html_content += "</table>"

    # 4. Handle Hyperlinks by parsing the XML
    # This part works by directly extracting hyperlinks from the XML of the document
    docx_xml = docx_obj.get_docx().element
    for rel in docx_xml.findall('.//w:hyperlink', namespaces=docx_xml.nsmap):
        # Extract the hyperlink URL
        url = rel.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}target')
        text = ""
        for text_elem in rel.findall('.//w:t', namespaces=docx_xml.nsmap):
            text += text_elem.text

        # Wrap the hyperlink in an <a> tag
        html_content += f'<a href="{url}">{text}</a>'

    # 5. Handle Images (optional, if needed)
    # You can add logic here to extract and handle images if required

    return html_content
