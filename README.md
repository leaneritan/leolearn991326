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
- **Coach Leo Edition**: Soccer-themed branding and interactive quizzes for a fun learning experience.

## How to Run

### Option 1: One-Click Launcher (Windows)
1. Double-click `start.bat` in the root directory.
2. This will start a local server and open the app in your browser automatically.

### Option 2: Manual Start
1. Navigate to the root directory.
2. Run a local web server (required for loading data files):
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000/docs/index.html` in your browser.

## For Developers

The app content is extracted from the PDF using a custom extraction pipeline.

- `docs/book_data.json`: Contains the layout, text, and image references for all 159 pages.
- `docs/toc.json`: The Table of Contents structure.
- `docs/answers.json`: The answer key for fill-in-the-blank exercises.
- `docs/circles.json`: The list of correct words for circling exercises.
- `docs/quiz_questions.js`: Soccer-themed quiz data for Leo.
- `docs/images/`: Extracted images from the book.
- `extract_all.py`: The Python script used to extract text and images from the PDF (requires `PyMuPDF`).

### Re-extracting Data

If you need to re-extract the data:
1.  Install dependencies: `pip install pymupdf`
2.  Run the script: `python extract_all.py`
3.  The script will update the files in the `docs/` directory.
