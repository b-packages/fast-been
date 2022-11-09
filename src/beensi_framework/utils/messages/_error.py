def error(message: str) -> dict:
    return {
        'status': 'error',
        'message': message,
    }
