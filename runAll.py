from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import time
import webbrowser
import os
import threading
from flask import send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

genai.configure(api_key = "AIzaSyC_o4HHVxQiNukuyMTCeRqEOtZ7eJnNfFY")
model = genai.GenerativeModel('gemini-1.5-flash')

# Global variable to hold chat history
chat_history = []

# # Function to log chat history to the file
# def log_to_history():
#     while True:
#         if chat_history:
#             # Open the history file and append the new chat history
#             with open("history.txt", "a", encoding="utf-8") as history_file:
#                 for message in chat_history:
#                     history_file.write(f"{message}\n")
#             # Clear the chat history after saving
#             chat_history.clear()
#         time.sleep(2)  # Delay between checks (2 seconds)

# # Start the background logging task in a separate thread
# thread = threading.Thread(target=log_to_history, daemon=True)
# thread.start()


@app.route('/download_history', methods=['POST'])
def download_history():
    try:
        # Get chat history from the request
        chat_history = request.json.get('chat_history', [])

        # Write to history.txt file
        with open("history.txt", "w", encoding="utf-8") as history_file:
            for message in chat_history:
                history_file.write(f"{message}\n")

        # Return the file for download
        history_file_path = os.path.join(os.getcwd(), 'history.txt')
        return send_file(history_file_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/run-python-script', methods=['POST'])
def run_python_script():
    try:
        # Call the internal Python function instead of using subprocess
        return render_template('chatbot.html')
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500
    
    
@app.route('/process_input', methods=['POST'])
def process_input():
    # Log the raw request data and parsed JSON
    print("Raw request data:", request.data)
    print("Parsed JSON:", request.json)

    prompt = request.json.get('input')  # Extract 'input' from JSON
    
    if prompt == 'Hey! How are you?' or prompt == 'Hello!' or prompt == 'Hello' or prompt == 'hello' or prompt == 'Good afternoon.' or prompt == 'Good afternoon!' or prompt == 'Howdy' or prompt == 'Good Afternoon.':
        # Generate response from the model
        response = model.generate_content("Hello! I am a young adult. Please ask me if I have any finanical questions today.")
        generated_text = response.text  # Replace this with the correct attribute from the response
        return jsonify({'response': generated_text})
    
    else:
        txtOptions = ['bankrate_credit_cards.txt', 
                      'credit_karma_credit_cards.txt',
                      'nerdwallet_credit_cards.txt',
                      'the_points_guy.txt']
        
        txtListContents = []
        for txtFile in txtOptions:
            # Open and read the file
            with open(txtFile, 'r', encoding='utf-8') as file:
                txtListContents.append(file.read())  # Read file and append its content
        
        # Construct the prompt
        csv_functionality_prompt = f'I am a young adult and would like to know more about finance in order to help my financial future. I have a good amount of txt files containing information that NextGen Money collected for me. Here are their contents in that order: {txtListContents[0]}, {txtListContents[1]}, {txtListContents[2]}, and {txtListContents[3]}. With this information and other public information about young adult finance, answer this question:'

        # Append the user prompt to the csv functionality prompt
        csv_functionality_prompt += prompt

        # Generate response from the model
        response = model.generate_content(csv_functionality_prompt)

        # Assuming response has a 'text' or 'content' attribute to get the generated response
        generated_text = response.text  # Replace this with the correct attribute from the response

        return jsonify({'response': generated_text})
    

if __name__ == '__main__':
    # Prevent the browser from opening twice in debug mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True)