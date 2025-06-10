import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import markdown # Required for converting Markdown output to HTML

app = Flask(__name__)
CORS(app)

# --- Gemini API Configuration ---
# Replace "YOUR_ACTUAL_GEMINI_API_KEY_HERE" with your actual Google Gemini API key.
# WARNING: Hardcoding API keys is NOT recommended for production or public repositories.
# For secure projects, use environment variables (e.g., with python-dotenv).
GOOGLE_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
    raise ValueError("Please replace 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' with your actual Google Gemini API key in app.py")

genai.configure(api_key=GOOGLE_API_KEY)

model = None

def get_available_text_model():
    """
    Lists available Gemini models and returns the first one suitable for
    generating text content (supporting 'generateContent' method).
    Prioritizes 'gemini-1.5-flash' and then 'gemini-1.0-pro'.
    """
    print("Checking for available Gemini models...")
    
    for m in genai.list_models():
        if m.name == 'models/gemini-1.5-flash' and 'generateContent' in m.supported_generation_methods:
            print(f"Prioritizing recommended model: {m.name}")
            return genai.GenerativeModel(m.name)
            
    for m in genai.list_models():
        if m.name == 'models/gemini-1.0-pro' and 'generateContent' in m.supported_generation_methods:
            print(f"Falling back to suitable text model: {m.name}")
            return genai.GenerativeModel(m.name)
            
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Using general suitable model: {m.name}")
            return genai.GenerativeModel(m.name)
            
    raise Exception("No Gemini model found that supports 'generateContent'. Please ensure your API key is correct and valid.")

with app.app_context():
    try:
        model = get_available_text_model()
    except Exception as e:
        print(f"FATAL ERROR: Could not initialize Gemini model: {e}")
        print("Exiting application. Please check your API key and network connection.")
        exit()

# --- AI Logic for Documentation ---
def auto_document_pipeline_llm(pipeline_code_or_description):
    """
    Sends pipeline code or a description to the selected Gemini model for documentation generation.
    Returns the generated documentation as HTML.
    """
    if not pipeline_code_or_description.strip():
        return "Please enter pipeline code or a description to document."

    prompt = f"""
    You are an expert Data Engineer and Technical Writer. Your task is to generate clear, concise, and professional documentation for the given data pipeline code or description.
    Focus on:
    - **Purpose:** What does the pipeline achieve?
    - **Inputs & Outputs:** What data does it consume and produce?
    - **Key Steps/Logic:** How does it transform data?
    - **Technologies Used:** Identify any obvious technologies.
    - **Dependencies:** If any are implied.

    Present the documentation using Markdown formatting (headings, bullet points, bold text, code blocks) for readability.

    Data Pipeline Code/Description:
    ```
    {pipeline_code_or_description}
    ```
    Generated Documentation:
    """
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Convert markdown response to HTML for rendering in the browser
        html_documentation = markdown.markdown(raw_text)
        return html_documentation
    except Exception as e:
        return f"An error occurred during documentation generation: {e}. The model might have encountered an issue or you hit a rate limit."

# --- Flask Routes ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/document_pipeline', methods=['POST'])
def document_pipeline():
    data = request.get_json()
    pipeline_input = data.get('pipeline_input', '') 

    if not pipeline_input:
        return jsonify({'error': 'No pipeline code or description provided'}), 400

    documentation = auto_document_pipeline_llm(pipeline_input)
    
    if documentation.startswith("An error occurred during documentation generation:"):
        return jsonify({'error': documentation}), 500
    
    return jsonify({'documentation': documentation}) 

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000/")
    app.run(debug=True)