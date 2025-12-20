import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.services.auth import create_access_token
from app.config import get_settings

settings = get_settings()


def test_create_access_token_success():
    """Test that create_access_token generates a valid JWT."""
    test_subject = "testuser@example.com"
    data = {"sub": test_subject}

    token = create_access_token(data)

    assert isinstance(token, str)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload.get("sub") == test_subject
        assert "exp" in payload
        # Check if expiry is roughly correct (within a small delta)
        expected_expiry = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        actual_expiry = datetime.utcfromtimestamp(payload["exp"])
        assert abs((expected_expiry - actual_expiry).total_seconds()) < 5  # 5 seconds tolerance
    except JWTError as e:
        pytest.fail(f"JWT decoding failed: {e}")


def test_create_access_token_different_data():
    """Test token creation with different subject and additional data."""
    test_subject = "anotheruser@example.com"
    additional_data = {"user_id": 123, "role": "admin"}
    data = {"sub": test_subject, **additional_data}

    token = create_access_token(data)
    assert isinstance(token, str)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload.get("sub") == test_subject
        assert payload.get("user_id") == 123
        assert payload.get("role") == "admin"
        assert "exp" in payload
    except JWTError:
        pytest.fail("JWT decoding failed for token with additional data.")


# Example of how you might test for expected failures if the function had validation
# (currently, create_access_token doesn't have input validation that would cause it to fail before encoding)
# def test_create_access_token_missing_sub():
#     """Test token creation fails if 'sub' is missing (if validation was added)."""
#     data = {"foo": "bar"} # Missing 'sub'
#     with pytest.raises(ValueError): # Or whatever appropriate error
#         create_access_token(data)
