import numpy
from django.db import transaction
from .models import Counter


def create_url(number: int) -> str:
    """
    Convert a number to a base36 string 0-9a-z
    Parameters:
        number (int): The number to convert.
    Returns:
        str: The base32 string.
    Examples:
        >>> create_url(0)
        '0'
        >>> create_url(11)
        'b'
    """

    return numpy.base_repr(number, base=36).lower()


def get_next_counter() -> int:
    """
    Get the next counter value and increment it.
    Record locking for update so the operation is atomic and thread-safe.
    Returns:
        int: The next counter value.
    """

    with transaction.atomic():
        counter = Counter.objects.select_for_update().filter(name='url_counter').first()
        result = counter.value + 1
        counter.value = result
        counter.save()
        return result


def generate_short_url() -> str:
    """
    Generate a short URL.
    Returns:
        str: The short URL.
    """

    counter = get_next_counter()
    return create_url(counter)
