from app.adapter.security.password import PasswordProvider


def test_verify_password():
    password_provider = PasswordProvider()

    secret = "password"
    secret_hash = password_provider.context.hash(secret)
    assert password_provider.verify_password(secret, secret_hash) is True
