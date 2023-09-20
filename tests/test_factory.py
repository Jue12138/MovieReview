from flask_app import create_app


def test_config():
    """
    Tests whether `testing` attribute is not set by
    default and is enabled with a custom configuration
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
