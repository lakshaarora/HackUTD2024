# from flask import Flask, request, jsonify, render_template
# import google.generativeai as genai

# app = Flask(__name__)

# genai.configure(api_key = "AIzaSyC_o4HHVxQiNukuyMTCeRqEOtZ7eJnNfFY")
# model = genai.GenerativeModel('gemini-1.5-flash')

# @app.route('/')
# def run_app_logic():
#     return render_template('chatbot.html')  # This looks for chatbot.html in the templates/ directory


# @app.route('/run-python-script', methods=['POST'])
# def run_python_script():
#     try:
#         # Call the internal Python function instead of using subprocess
#         result = run_app_logic()
        
#         # Return the result as a response
#         return jsonify({'message': 'Python script executed successfully', 'output': result}), 200
#     except Exception as e:
#         return jsonify({'message': 'Error', 'error': str(e)}), 500
    
    

# @app.route('/process_input', methods=['POST'])
# def process_input():
#     try:
#         # Log the raw request data and parsed JSON
#         print("Raw request data:", request.data)
#         print("Parsed JSON:", request.json)

#         prompt = request.json.get('input')  # Extract 'input' from JSON
        
#         if not prompt:
#             return jsonify({'error': 'No input provided'}), 400

#         # Generate response from the model
#         response = model.generate_content(prompt)

#         # Assuming response has a 'text' or 'content' attribute to get the generated response
#         generated_text = response.text  # Replace this with the correct attribute from the response

#         # Return the generated response as JSON
#         return jsonify({'response': generated_text})

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
