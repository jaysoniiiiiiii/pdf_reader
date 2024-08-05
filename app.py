from flask import Flask, render_template, request, send_file, jsonify
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename} with ID: {upload.id}'
    return render_template('index.html')

@app.route('/pdf/<int:pdf_id>', methods=['GET'])
def get_pdf(pdf_id):
    upload = Upload.query.get(pdf_id)
    if upload is None:
        return jsonify({"error": "PDF not found"}), 404

    # Read PDF content
    pdf_data = upload.data
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

    pdf_content = []
    image_texts = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_content.append(page.get_text("text"))

        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert image bytes to PIL Image
            image = Image.open(BytesIO(image_bytes))

            # Use pytesseract to extract text from image
            image_text = pytesseract.image_to_string(image)
            image_texts.append({
                "page": page_num,
                "img_index": img_index,
                "text": image_text
            })
    total_pages = pdf_document.page_count

    filename = upload.filename
    total_pages = total_pages 
        metadata = [{"page_num":image_texts[page_num], "data":[pdf_content[page_num]]}]
        # "image_texts": image_texts,
        # "content": pdf_content,

    for data in pdf_json (0, total_pages):
        pdf_json = {
        "filename": upload.filename,
        "total_pages": total_pages, 
        "metadata" : [{"page_num":image_texts[page_num], "data":[pdf_content[page_num]]}]
        # "image_texts": image_texts,
        # "content": pdf_content,

    }
    return jsonify(pdf_json)

if __name__ == '__main__':
    app.run(debug=True)

# {file_name: "abc.pdf", total_pages: 10, metadata: [{page_num: 1, data: [text: "", image_text: ""]}]}
