from app.users.utils import send_messages


def test_send_messages():
    numbers = ["+17134306973"]

    send_messages("testing testing 123", numbers, testing=True)


def test_create_chart():
    """
    GIVEN a set of preferencs by user
    WHEN a verified user accesses the home page
    THEN a chart must be created for displaying current information regarding who's out when.
    """
    pass
