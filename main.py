from flask import Flask, render_template, request
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        if "template" in request.form:
            img_path = "nyan_cat.png"
            doc = DocxTemplate('input.docx')
            visual = InlineImage(doc, img_path, width=Mm(150))
            context = {'first_name' : 'Lady', 
                    'last_name': 'Gaga',
                    'phone' : '123456789',
                    'visual':visual}
            doc.render(context)
            doc.save("output.docx")
        if 'transform' in request.form:
            convert("output.docx", 'output.pdf')
        return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
