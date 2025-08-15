from flask import Flask, render_template, request, send_from_directory, url_for
import os
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# --- Model Loading (on startup) ---
print("Loading YOLOv8 model...")
# Load the trained YOLOv8 model
model = YOLO('best.pt') # Path to your trained model file
print("Model loaded successfully!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get the uploaded image file
        if 'image' not in request.files:
            return render_template('result.html', error="No image file provided.")
        
        image_file = request.files['image']
        if image_file.filename == '':
             return render_template('result.html', error="No image selected.")
        
        # 2. Save the uploaded image temporarily
        input_filename = image_file.filename
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        image_file.save(input_path)

        # 3. Perform inference using the YOLO model
        results = model(input_path) # This returns a list of Results objects
        result = results[0] # Get the first (and likely only) result

        # 4. Plot the results (image with bounding boxes)
        # result.plot() returns the image as a NumPy array (BGR format)
        annotated_image_bgr = result.plot()

        # 5. Save the annotated image
        output_filename = f"output_{input_filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        # cv2.imwrite expects BGR format, which result.plot() provides
        success = cv2.imwrite(output_path, annotated_image_bgr)

        if not success:
            return render_template('result.html', error="Failed to save the output image.")

        # 6. Render the result page with paths to the images
        # url_for generates the correct URL for static files
        input_image_url = url_for('static', filename=f'uploads/{input_filename}')
        output_image_url = url_for('static', filename=f'outputs/{output_filename}')

        return render_template(
            'result.html',
            input_image_url=input_image_url,
            output_image_url=output_image_url
        )

    except Exception as e:
        error_message = f"An error occurred during processing: {str(e)}"
        app.logger.error(error_message) # Log the error for debugging
        return render_template('result.html', error=error_message)

# Optional: Serve uploaded/processed files directly (useful for debugging)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    # Run the app
    # host='0.0.0.0' makes it accessible from outside the container (important for Docker/Render)
    # port=5000 is the standard Flask port
    # debug=False for production (more secure than debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
