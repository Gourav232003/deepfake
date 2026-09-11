"""
Shared error types and a consistent JSON error envelope, per TechSpec.md:
    { "success": false, "error": { "code": "...", "message": "..." } }

No stack traces or internal detail ever reach the client.
"""


class DeepGuardError(Exception):
    """Base class for all handled application errors."""

    status_code = 500
    code = "internal_error"

    def __init__(self, message, status_code=None, code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code


class InvalidFileError(DeepGuardError):
    status_code = 400
    code = "invalid_file"


class FileTooLargeError(DeepGuardError):
    status_code = 413
    code = "file_too_large"


class UnprocessableFileError(DeepGuardError):
    """File passed basic checks but couldn't actually be decoded/processed."""

    status_code = 422
    code = "unprocessable_file"


class InferenceError(DeepGuardError):
    status_code = 500
    code = "inference_failed"


def error_response(err: DeepGuardError):
    return {
        "success": False,
        "error": {"code": err.code, "message": err.message},
    }, err.status_code


def register_error_handlers(app):
    @app.errorhandler(DeepGuardError)
    def handle_deepguard_error(err):
        return error_response(err)

    @app.errorhandler(413)
    def handle_flask_413(_err):
        return error_response(FileTooLargeError("Uploaded file exceeds the maximum allowed size."))

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        # Log the real exception server-side in a real deployment.
        app.logger.exception("Unhandled exception")
        return error_response(DeepGuardError("Something went wrong while processing your request."))
