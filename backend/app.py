from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pytesseract
import base64
import tempfile
import os
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF
from pdf2image import convert_from_path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure Tesseract path (will be set in Docker)
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def handle_image_ocr(image_path):
    """Handle OCR for regular images"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image).strip()
    return text

def handle_pdf_ocr(pdf_path):
    """Handle OCR for scanned PDFs by converting to images"""
    text = ""
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        for i, image in enumerate(images):
            # Perform OCR on each page
            page_text = pytesseract.image_to_string(image).strip()
            if page_text:
                text += f"\n--- Page {i+1} ---\n{page_text}\n"
    except Exception as e:
        text = f"Error processing PDF with OCR: {str(e)}"
    
    return text

def analyze_pdf_type(pdf_path):
    """Analyze whether PDF contains extractable text or needs OCR"""
    try:
        doc = fitz.open(pdf_path)
        total_text_length = 0
        
        # Check first few pages
        pages_to_check = min(3, doc.page_count)
        
        for page_num in range(pages_to_check):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            total_text_length += len(page_text.strip())
        
        doc.close()
        
        # If very little text found, it's likely a scanned PDF
        return "text" if total_text_length > 50 else "scanned"
    except:
        return "scanned"

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "OCR API is running!", "version": "1.0"})

@app.route('/ocr', methods=['POST'])
def extract_text():
    try:
        # Check if file is provided
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        text = ""
        filename_lower = filename.lower()

        if filename_lower.endswith('.pdf'):
            # Handle as PDF
            doc = fitz.open(temp_path)
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                text += page.get_text()
            if not text.strip():  # If direct extraction fails, use OCR
                text = handle_pdf_ocr(temp_path)
            doc.close()
        else:
            # Handle as image
            text = handle_image_ocr(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        # Split text into lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Return results
        return jsonify({
            "success": True,
            "text": text,
            "lines": lines
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pdf-extract', methods=['POST'])
def extract_pdf_text():
    """Advanced PDF text extraction with analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        file = request.files['file']
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Please provide a valid PDF file"}), 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        # Analyze PDF type
        pdf_type = analyze_pdf_type(temp_path)
        
        # Open PDF
        doc = fitz.open(temp_path)
        total_pages = doc.page_count
        
        pages_data = []
        full_text = ""
        
        # Extract text from each page
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            
            page_info = {
                "page_number": page_num + 1,
                "text": page_text.strip(),
                "char_count": len(page_text.strip()),
                "has_text": len(page_text.strip()) > 10
            }
            
            pages_data.append(page_info)
            full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
        
        doc.close()
        
        # If no text found, try OCR
        if pdf_type == "scanned" or not full_text.strip():
            ocr_text = handle_pdf_ocr(temp_path)
            if ocr_text:
                full_text = ocr_text
                # Update pages data for OCR
                for page_info in pages_data:
                    if not page_info["has_text"]:
                        page_info["processing_method"] = "OCR"
        
        # Clean up
        os.remove(temp_path)
        
        # Statistics
        total_chars = len(full_text)
        word_count = len(full_text.split())
        
        return jsonify({
            "success": True,
            "text": full_text.strip(),
            "pdf_info": {
                "total_pages": total_pages,
                "pdf_type": pdf_type,
                "total_characters": total_chars,
                "word_count": word_count,
                "processing_method": "Direct extraction" if pdf_type == "text" else "OCR"
            },
            "pages": pages_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ocr-base64', methods=['POST'])
def extract_text_base64():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "No base64 image provided"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        
        # Convert to OpenCV format
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save temporarily
        temp_path = tempfile.mktemp(suffix='.jpg')
        cv2.imwrite(temp_path, img)
        
        # Open image with PIL
        image = Image.open(temp_path)
        
        # Perform OCR with confidence data
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(image).strip()
        
        # Extract confidence scores for words
        confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Split text into lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "text": text,
            "lines": lines,
            "confidence_scores": confidences,
            "average_confidence": average_confidence / 100.0  # Convert to 0-1 scale
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
