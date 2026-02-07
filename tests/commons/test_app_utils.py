from commons.utils.app_settings import get_settings
from commons.utils.app_utils import hash_email, encrypt_email, decrypt_email, generate_password_hash,verify_password


def test_email_hash(get_test_email_data):
    actual_email = get_test_email_data['actual_email']
    actual_hashed_email = get_test_email_data['hashed_email']

    expected_hashed_email = hash_email(actual_email)

    assert actual_hashed_email == expected_hashed_email



def test_email_encrypt(get_test_email_data):
    # Given
    actual_email = get_test_email_data['actual_email']
    key = get_settings().aes_key

    # When
    encrypted_email = encrypt_email(actual_email, key)

    # Then
    assert encrypted_email is not None
    assert encrypted_email != actual_email
    assert isinstance(encrypted_email, str)



def test_email_decrypt(get_test_email_data):
    # Given
    actual_email = get_test_email_data['actual_email']
    encrypted_email = get_test_email_data['encrypted_email']
    key = get_settings().aes_key

    # When
    decrypted_email = decrypt_email(encrypted_email, key)

    # Then
    assert decrypted_email == actual_email
    assert isinstance(decrypted_email, str)


def test_hash_password():
    # GIVEN
    actual_password = "samplepassword"

    # WHEN
    hashed_password = generate_password_hash(actual_password)

    # Then
    assert hashed_password is not None
    assert hashed_password != actual_password
    assert isinstance(hashed_password, str)


def test_verify_password_positive():
    # GIVEN
    actual_password = "samplepassword"
    hashed_password = generate_password_hash(actual_password)

    # WHEN
    result = verify_password(actual_password, hashed_password)

    # THEN
    assert result is True


def test_verify_password_negative():
    # GIVEN
    actual_password = "samplepassword"
    hashed_password = generate_password_hash("samplepassword")
    entered_password = "wrongpassword"

    # WHEN
    result = verify_password(entered_password, hashed_password)

    # THEN
    assert result is False
    assert entered_password != actual_password

