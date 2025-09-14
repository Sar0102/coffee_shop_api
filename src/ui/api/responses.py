from starlette import status

from src.ui.schemas.error import ErrorResponse

# Generic error responses you can reuse per router/endpoint
GENERIC_ERROR_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Bad Request"},
    status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Unauthorized"},
    status.HTTP_403_FORBIDDEN: {"model": ErrorResponse, "description": "Forbidden"},
    status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Conflict"},
}

# Focused sets for specific endpoints (can be extended)
AUTH_SIGNUP_RESPONSES = {
    **{status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Email already taken"}},
    **{status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Validation/Business error"}},
}

AUTH_LOGIN_RESPONSES = {
    **{status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Invalid credentials or unverified"}},
}

AUTH_VERIFY_RESPONSES = {
    **{status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid/expired code"}},
    **{status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "User not found"}},
}
