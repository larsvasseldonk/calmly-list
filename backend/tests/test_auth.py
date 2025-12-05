import pytest
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from datetime import timedelta
import jwt
from jwt.exceptions import InvalidTokenError


def test_password_hashing():
    """Test that password hashing and verification works correctly"""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    # Hash should be different from original
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) is True
    
    # Wrong password should fail
    assert verify_password("wrong_password", hashed) is False


def test_password_hash_uniqueness():
    """Test that same password produces different hashes (due to salt)"""
    password = "same_password"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Token should have JWT structure (3 parts separated by dots)
    assert len(token.split('.')) == 3


def test_token_contains_correct_data():
    """Test that token contains the expected data"""
    from app.auth import SECRET_KEY, ALGORITHM
    
    email = "user@example.com"
    data = {"sub": email}
    token = create_access_token(data)
    
    # Decode token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Check data
    assert payload["sub"] == email
    assert "exp" in payload


def test_token_expiration():
    """Test that token expiration is set correctly"""
    from app.auth import SECRET_KEY, ALGORITHM
    from datetime import datetime
    
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Check expiration exists and is in the future
    assert "exp" in payload
    exp_time = datetime.fromtimestamp(payload["exp"])
    assert exp_time > datetime.utcnow()


def test_invalid_token_decode():
    """Test that invalid tokens raise errors"""
    from app.auth import SECRET_KEY, ALGORITHM
    
    invalid_token = "invalid.token.here"
    
    with pytest.raises(InvalidTokenError):
        jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])


def test_token_with_wrong_secret():
    """Test that tokens signed with wrong secret fail"""
    from app.auth import ALGORITHM
    
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    wrong_secret = "wrong_secret_key"
    
    with pytest.raises(InvalidTokenError):
        jwt.decode(token, wrong_secret, algorithms=[ALGORITHM])


def test_empty_password():
    """Test handling of empty password"""
    empty_password = ""
    hashed = get_password_hash(empty_password)
    
    # Even empty password should be hashed
    assert hashed != empty_password
    assert verify_password(empty_password, hashed) is True
