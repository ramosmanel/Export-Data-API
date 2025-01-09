from flask import Flask
from flask_cors import CORS
from routes.export import export_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(export_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)