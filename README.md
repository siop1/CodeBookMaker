# CodeBookMaker

Create beautiful, syntax-highlighted PDF notebooks from your source code.

This project is a web application that takes a ZIP archive of your source code and generates a clean, professional-looking PDF document. The PDF includes a table of contents, syntax-highlighted code blocks, and is optimized for both digital viewing and printing.

## ✨ Features

- **Instant PDF Generation**: Upload a ZIP file and get a PDF notebook in seconds.  
- **Beautiful Typography**: Clean, monospaced fonts and proper spacing for maximum readability.  
- **Syntax Highlighting**: Code blocks are automatically highlighted for various programming languages.  
- **Automatic Table of Contents**: A clickable table of contents is generated for easy navigation of your files and folders.  
- **Privacy-First**: Your code is processed temporarily and is not stored on our servers.

---

## 🚀 How to Use

1. **Visit the Website**: Go to [https://codebookmaker.onrender.com](https://codebookmaker.onrender.com).  
2. **Enter a Title**: Give your notebook a descriptive title.  
3. **Upload Your Code**: Drag and drop a `.zip` file of your project into the upload area or click "browse" to select a file.  
4. **Generate & Download**: Click the "Generate PDF" button. A PDF file will be automatically downloaded to your computer.

---

## 💻 Local Development

### Prerequisites

You'll need a backend server to handle the file upload and PDF generation. This project uses **Python** and **Flask**.

- **Python** 3.7+  
- **pip** (Python package installer)

### Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/siop1/CodeBookMaker.git
   cd CodeBookMaker
   ```

2. Install all the necessary backend dependencies from the `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt
   ```

### Project Structure

The project has a simple and organized structure:

```
CodeBookMaker/
├── app.py                  # The backend server logic (Flask)
├── templates/
│   └── index.html          # The frontend user interface
├── static/
│   └── sample.pdf          # Sample PDF for demonstration
├── uploads/                # Directory for handling temporary uploads
├── requirements.txt        # List of Python dependencies
└── README.md
```

### Running the Application

1. Start the backend server by running the main Flask application file:  
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`. The `index.html` file will be served, and you can begin using the application.

---

## 📄 Sample Output

To see what the final output looks like, check out this [sample PDF](https://github.com/siop1/CodeBookMaker/blob/master/static/sample.pdf).

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/siop1/CodeBookMaker/blob/master/LICENSE) file for details.
