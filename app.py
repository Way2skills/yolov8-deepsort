from flask import Flask, render_template, request, send_from_directory, session
import os
import uuid
import shutil
from src.marine_detect.predict import predict_on_images

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # Required for session handling

# Configuration
app.config['UPLOAD_FOLDER'] = 'input'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def cleanup_previous_uploads():
    """Delete previous upload/output directories if they exist"""
    if 'current_uuid' in session:
        uid = session['current_uuid']
        input_dir = os.path.join(app.config['UPLOAD_FOLDER'], uid)
        output_dir = os.path.join('output', uid)
        
        if os.path.exists(input_dir):
            shutil.rmtree(input_dir)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        session.pop('current_uuid', None)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Clean up previous uploads when accessing the main page
    if request.method == 'GET':
        cleanup_previous_uploads()
    
    if request.method == 'POST':
        cleanup_previous_uploads()  # Cleanup before new upload
        
        if 'file' not in request.files:
            return render_template('index.html', error='No file selected')
            
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No file selected')
            
        if file and allowed_file(file.filename):
            # Generate unique ID and paths
            uid = uuid.uuid4().hex
            session['current_uuid'] = uid
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            
            # Create directories
            input_dir = os.path.join(app.config['UPLOAD_FOLDER'], uid)
            output_dir = os.path.join('output', uid)
            os.makedirs(input_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
            
            # Save uploaded file
            input_filename = f'input.{file_ext}'
            file_path = os.path.join(input_dir, input_filename)
            file.save(file_path)
            
            # Process image
            try:
                predict_on_images(
                    model_paths=["FishInv.pt", "MegaFauna.pt"],
                    confs_threshold=[0.522, 0.6],
                    images_input_folder_path=input_dir,
                    images_output_folder_path=output_dir,
                )
                
                # Get result file path
                result_filename = f'input.{file_ext}'
                result_path = os.path.join(output_dir, result_filename)
                
                if not os.path.exists(result_path):
                    raise FileNotFoundError("Processing failed - no output file generated")
                
                return render_template('result.html', result_url=f'/output/{uid}/{result_filename}')
                                     
            except Exception as e:
                return render_template('index.html', error=f'Error processing file: {str(e)}')
                
        return render_template('index.html', error='Invalid file type')
        
    return render_template('index.html')

@app.route('/output/<uid>/<filename>')
def serve_output(uid, filename):
    return send_from_directory(os.path.join('output', uid), filename)

if __name__ == '__main__':
    app.run(debug=True)