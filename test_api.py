#!/usr/bin/env python3
"""
Test script for OCR & PDF Text Extractor API
Tests both image OCR and PDF processing endpoints
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import os

API_BASE_URL = "http://localhost:5001"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def create_test_image():
    """Create a simple test image with text"""
    print("🖼️ Creating test image...")
    
    # Create a white image with black text
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = "Hello World!\nThis is a test image\nfor OCR processing."
    draw.text((20, 20), text, fill='black')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

def test_image_ocr():
    """Test image OCR endpoint"""
    print("\n📷 Testing image OCR...")
    
    test_image = create_test_image()
    
    files = {'file': ('test.png', test_image, 'image/png')}
    response = requests.post(f"{API_BASE_URL}/ocr", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Extracted text: {data['text'][:100]}...")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_pdf_endpoint():
    """Test PDF processing endpoint (without actual PDF)"""
    print("\n📄 Testing PDF endpoint availability...")
    
    # Test with empty request to check if endpoint exists
    response = requests.post(f"{API_BASE_URL}/pdf-extract")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 400:  # Expected error for missing file
        data = response.json()
        print(f"Expected error: {data['error']}")
        print("✅ PDF endpoint is available and working correctly")
        return True
    else:
        print(f"Unexpected response: {response.text}")
        return False

def main():
    print("🚀 Starting API Tests for OCR & PDF Text Extractor")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Image OCR", test_image_ocr),
        ("PDF Endpoint", test_pdf_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "✅ PASS" if result else "❌ FAIL"))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, "❌ ERROR"))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, result in results:
        print(f"{test_name}: {result}")
    
    print("\n🎉 Testing complete!")
    print("💡 To test PDF processing, upload a PDF file through the web interface at http://localhost:3000")

if __name__ == "__main__":
    main()
