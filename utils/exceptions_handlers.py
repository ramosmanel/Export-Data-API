from flask import jsonify
from utils.exceptions import ExportError, ProcessingError

class ErrorHandler:
    @staticmethod
    def register_error_handlers(app):

        @app.errorhandler(ExportError)
        def handle_export_error(error):
            return jsonify({"error": error.message}), 400

        @app.errorhandler(ProcessingError)
        def handle_processing_error(error):
            return jsonify({"error": error.message}), 422

        @app.errorhandler(500)
        def handle_internal_server_error(error):
            return jsonify({"error": "Erro interno do servidor"}), 500