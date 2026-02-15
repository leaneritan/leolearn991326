# Grammar 1 - Interactive Learning App

This application turns the "Basic English Grammar Book 1" PDF into a fully interactive web application.

## Features

- **Interactive Exercises**:
  - **Fill-in-the-blanks**: Type your answers directly into the spaces provided.
  - **Click-to-Circle**: Click on words to circle them (useful for exercises like "Circle the letters that should be CAPITALS").
- **Check Answers**: Toggle the "Check Answers" button to see immediate feedback (Green for correct, Red for incorrect).
- **Progress Tracking**: Your progress and answers are automatically saved to your browser's local storage.
- **Searchable Lessons**: Quickly find any topic or keyword using the search bar.
- **Responsive Design**: Kid-friendly UI with a clean sidebar Table of Contents.
- **Offline Ready**: Works directly by opening `index.html` in your browser (no web server required).

## How to Run

1.  Navigate to the `app/` directory.
2.  Double-click `index.html` to open it in your favorite web browser.
3.  Enjoy learning!

## For Developers

The app content is extracted from the PDF using a custom extraction pipeline.

- `app/data.js`: Contains the layout, text, and image references for all 159 pages.
- `app/toc.js`: The Table of Contents structure.
- `app/answers.js`: The answer key for fill-in-the-blank exercises.
- `app/circles.js`: The list of correct words for circling exercises.
- `app/images/`: Extracted images from the book.
- `extract_all.py`: The Python script used to extract text and images from the PDF (requires `PyMuPDF`).

### Re-extracting Data

If you need to re-extract the data:
1.  Install dependencies: `pip install pymupdf`
2.  Run the script: `python extract_all.py`
3.  The script will update the files in the `app/` directory.
