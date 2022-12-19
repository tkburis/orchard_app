from flask import Blueprint, current_app, send_from_directory

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/display/<filename>')
def display_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
