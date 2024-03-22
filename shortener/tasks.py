
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.db import transaction
from celery import shared_task
from .models import Url


@shared_task
def crawl_url(url: str) -> str:
    """
    Retrieves the title of a webpage given its original URL.
    Args:
        url (str): The URL of the webpage to crawl.
    Returns:
        str: The retrieved title of the URLs webpage.
    """
    title = ''
    try:
        soup = BeautifulSoup(urlopen(url), 'lxml')
        title = soup.title.string
        with transaction.atomic():
            url = Url.objects.select_for_update().filter(original_url=url).first()
            if url:
                url.title = title
                url.save()

    except Exception as e:
        print(e)

    return title
