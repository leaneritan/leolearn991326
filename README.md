# Interactive Grammar App

This application turns the "Basic English Grammar" PDF into an interactive learning experience.

## Features
- **Interactive Exercises**: Fill-in-the-blanks and word circling with instant feedback.
- **Table of Contents**: Easy navigation to chapters and sections.
- **Search**: Full-text search across all 159 pages.
- **Progress Tracking**: Marks pages as finished and saves your state using local storage.
- **Responsive Layout**: Preserves the original book layout using modern CSS techniques.

## How to Run
To run the app locally, serve the `app` directory using a web server.

### Using Python
```bash
python3 -m http.server 8080 --directory app
```

### Using Node.js (serve)
```bash
npx serve app
```

Then open `http://localhost:8080` in your browser.

## Data Extraction
The application data was generated using `extract_all.py`. If you need to regenerate the data, you will need the `pymupdf` (fitz) library:
```bash
pip install pymupdf
python3 extract_all.py
```
