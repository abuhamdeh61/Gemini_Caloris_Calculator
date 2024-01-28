from flask import Flask, render_template, request, jsonify
import os
import marko
import google.generativeai
app = Flask(__name__)


google.generativeai.configure(api_key="AIzaSyDp9UIHKwUeghwSQRrhxrCy2OBN2Jk07bg")

def get_gemini_response(input, image, prompt):
    model = google.generativeai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return marko.convert(response.text)

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.content_type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
      
      
@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
        input_prompt = """
        You are an expert in nutritionist where you need to see the food items from the image
        and calculate the total calories, also provide the details of every food items with calories intake
        in the below format:

        1. Item 1 - no of calories
        2. Item 2 - no of calories
        ----
        ----
        """

        input_text = request.form['input_text']
        uploaded_file = request.files['file']

        if uploaded_file:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input_text)
            return render_template('index.html', response=response)
        else:
            return render_template('index.html', error="No file uploaded")
  return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True, port=5000)