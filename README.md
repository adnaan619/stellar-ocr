# OCR & PDF Text Extractor 🔍📄

A professional web application that extracts text from images and PDFs using advanced OCR technology, featuring intelligent PDF analysis, multi-format support, and a beautiful React frontend.

## Features ✨

### 🖼️ **Image Processing**
- **Drag & Drop Interface**: Easy file upload with visual feedback
- **Real-time OCR**: Extract text from images using Tesseract OCR
- **Confidence Scoring**: See how confident the OCR engine is about the results
- **Multiple Formats**: Supports PNG, JPG, GIF, BMP, and other image formats

### 📄 **PDF Processing**
- **Intelligent PDF Analysis**: Automatically detects text-based vs scanned PDFs
- **Direct Text Extraction**: Fast extraction from searchable PDFs
- **OCR for Scanned PDFs**: Converts PDF pages to images and performs OCR
- **Page-by-page Processing**: Handles multi-page documents efficiently
- **PDF Statistics**: Shows page count, processing method, word count

### 🎨 **User Experience**
- **Copy to Clipboard**: One-click copying of extracted text
- **File Type Detection**: Automatically handles images and PDFs appropriately
- **Processing Progress**: Visual feedback during text extraction
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Professional UI**: Clean, modern interface with detailed file information

## Tech Stack 🛠️

### Backend
- **Flask**: Python web framework
- **Tesseract OCR**: Open-source OCR engine
- **OpenCV**: Image processing
- **Docker**: Containerization

### Frontend
- **React**: User interface library
- **Tailwind CSS**: Styling
- **Font Awesome**: Icons

## Quick Start 🚀

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd ocr-app
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

### Manual Setup

#### Backend
```bash
cd backend
docker build -t ocr-backend .
docker run -d -p 5001:5000 --name ocr-backend ocr-backend
```

#### Frontend
```bash
cd frontend
python -m http.server 3000
```

## API Endpoints 📡

### Health Check
```
GET /
```
Returns API status and version.

### Universal OCR (Images & PDFs)
```
POST /ocr
Content-Type: multipart/form-data
Body: file (image or PDF)
```

Response (Image):
```json
{
  "success": true,
  "text": "Extracted text here...",
  "lines": ["Line 1", "Line 2", "..."]
}
```

### Advanced PDF Processing
```
POST /pdf-extract
Content-Type: multipart/form-data
Body: PDF file
```

Response (PDF):
```json
{
  "success": true,
  "text": "Full extracted text...",
  "pdf_info": {
    "total_pages": 5,
    "pdf_type": "text",
    "total_characters": 2400,
    "word_count": 450,
    "processing_method": "Direct extraction"
  },
  "pages": [
    {
      "page_number": 1,
      "text": "Page 1 content...",
      "char_count": 480,
      "has_text": true
    }
  ]
}
```

### Base64 OCR (Alternative)
```
POST /ocr-base64
Content-Type: application/json
Body: {"image": "data:image/jpeg;base64,/9j/4AAQ..."}
```

## Free Deployment Options 🌐

### Backend Deployment
1. **Railway** (Recommended)
   - Connect your GitHub repo
   - Railway auto-detects Dockerfile
   - Free tier: 500 hours/month

2. **Render**
   - Connect GitHub repo
   - Choose "Web Service"
   - Free tier with sleep mode

3. **Fly.io**
   - `flyctl launch` in backend directory
   - Free allowance included

### Frontend Deployment
1. **Vercel** (Recommended)
   - Connect GitHub repo
   - Auto-deploys on commits
   - Free tier for personal projects

2. **Netlify**
   - Drag & drop deployment
   - Continuous deployment from Git

3. **GitHub Pages**
   - Push to `gh-pages` branch
   - Free for public repositories

## Deployment Configuration 🔧

### Environment Variables
- `FLASK_ENV`: Set to `production` for deployment
- `PORT`: Port for the backend (default: 5000)

### CORS Configuration
The backend is configured to accept requests from any origin. For production, update the CORS settings in `app.py`:

```python
CORS(app, origins=['https://yourdomain.com'])
```

## Usage Tips 💡

### 🖼️ **Image Processing Tips**
1. **Best Results**: Use high-contrast images with clear text
2. **Supported Formats**: PNG, JPG, JPEG, GIF, BMP
3. **File Size**: Keep images under 10MB for best performance
4. **Text Orientation**: The OCR handles rotated text automatically

### 📄 **PDF Processing Tips**
1. **Text-based PDFs**: Instantly extract text without OCR processing
2. **Scanned PDFs**: Automatically converts to images and applies OCR
3. **Large PDFs**: Processing time scales with page count and complexity
4. **Mixed PDFs**: Handles documents with both text and scanned pages
5. **Security**: Password-protected PDFs are not currently supported

### ⚡ **Performance Optimization**
- **Small files process faster**: Compress large PDFs when possible
- **Text PDFs >> Scanned PDFs**: Direct extraction is 100x faster than OCR
- **Page limits**: Consider splitting very large PDFs (>50 pages)

## Sample Images to Test 📸

Try the OCR with:
- Screenshots of documents
- Photos of signs or text
- Scanned documents
- Book pages
- Business cards
- Handwritten text (results may vary)

## Development 👨‍💻

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Development
The frontend is a single HTML file with embedded React. Simply edit `frontend/index.html` and refresh the browser.

## Troubleshooting 🔧

### Common Issues

1. **CORS Errors**: Make sure the backend is running and accessible
2. **Poor OCR Results**: Try preprocessing images (increase contrast, resize)
3. **Container Issues**: Check Docker logs with `docker logs ocr-backend`

### Performance Tips

1. **Image Preprocessing**: Resize very large images before OCR
2. **Text Enhancement**: Increase contrast for better results
3. **Memory**: OCR can be memory-intensive for large images

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open-source and available under the MIT License.

---

**Happy OCR-ing! 🎉**
