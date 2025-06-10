# ⚙️ Setup & Running Instructions

This guide will help you get the AI Data Pipeline Auto-Documenter up and running on your local machine.

## Prerequisites ✅
* Python 3.8+ installed 🐍
* `pip` (Python package installer)

## Installation & Setup 셋업! 🛠️

### 1. **Get the Code**

First, ensure you have the `app.py` and `index.html` files in the same directory. If you're cloning from a repository:

```bash
git clone [https://github.com/YourGitHubUsername/ai-pipeline-auto-documenter.git](https://github.com/YourGitHubUsername/ai-pipeline-auto-documenter.git)
cd ai-pipeline-auto-documenter

2. Set Up Python Environment
Create and activate a new Python virtual environment:

Bash

python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
3. Install Dependencies
Install all required Python libraries. First, create a requirements.txt file in your project root with the following content:

Flask
google-generativeai
Flask-Cors
Markdown
Then, install them:

Bash

pip install -r requirements.txt
4. Configure Gemini API Key
Obtain your Google Gemini API key from Google AI Studio. Open app.py and replace the placeholder with your actual key:

Python

# app.py snippet
GOOGLE_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE" # <--- REPLACE THIS!
▶️ Running the Application
Start the Flask Backend:
In your terminal (with the virtual environment active), run:

Bash

python app.py
Access the Web Interface:
Open your web browser and navigate to http://127.0.0.1:5000/.

<!-- end list -->
