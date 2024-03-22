from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from shortener.helpers import create_url
from shortener.models import Url, Counter


URL_INIT_VALUES = [
        {'original_url': 'http://www.site1.com', 'short_url': '1', 'title': 'Site 1', 'count': 3},
        {'original_url': 'http://www.site2.com', 'short_url': '2', 'title': 'Site 2', 'count': 2},
        {'original_url': 'http://www.site3.com', 'short_url': '3', 'title': 'Site 3', 'count': 1},
        {'original_url': 'http://www.site4.com', 'short_url': '4', 'title': 'Site 4', 'count': 8},
        {'original_url': 'http://www.site5.com', 'short_url': '5', 'title': 'Site 5', 'count': 10},
    ]


class ShortenerApiTest(APITestCase):
    def setUp(self):
        for value in URL_INIT_VALUES:
            Url.objects.create(**value)

        counter = Counter.objects.get(name='url_counter')
        counter.value = 5
        counter.save()

    def test_get_shortener(self):
        for url in URL_INIT_VALUES:
            response = self.client.get(f'/shortener/{url["short_url"]}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('original_url'), url['original_url'])


    def test_post_shortener(self):
        url = '/shortener/'

        # Retrieve the current counter value
        current_counter = Counter.objects.get(name='url_counter').value + 1

        # Create 10 new short URLs
        for site_number in range(current_counter, current_counter + 10):
            response = self.client.post(url, {'url': f'http://www.site{site_number}.com'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            computed_url = response.data.get('short_url')
            expected_url = 'http://testserver/shortener/' + create_url(site_number)
            self.assertEqual(computed_url, expected_url)

    def test_get_shortner_top(self):
        url = '/shortener/top/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['original_url'], 'http://www.site5.com')
        self.assertEqual(response.data[1]['original_url'], 'http://www.site4.com')
        self.assertEqual(response.data[2]['original_url'], 'http://www.site1.com')
        self.assertEqual(response.data[3]['original_url'], 'http://www.site2.com')
        self.assertEqual(response.data[4]['original_url'], 'http://www.site3.com')


class UrlEncoderTest(SimpleTestCase):
    def test_encoder(self):
        cases = [(0, '0'), (1, '1'), (11, 'b'), (1001, 'rt'), (1000000, 'lfls')]
        for case in cases:
            calculated, expected = case
            self.assertEqual(create_url(calculated), expected)
