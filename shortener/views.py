from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView,Response
from django.db import transaction
from .models import Url
from .serializers import UrlSerializer
from .tasks import crawl_url
from .helpers import generate_short_url


MAX_URL_IN_RESPONCE = 100


class ShortenerAPI(APIView):

    def get(self, request, **kwargs):
        short_url = kwargs.get('short_url')
        with transaction.atomic():
            record = Url.objects.select_for_update().filter(short_url=short_url).first()
            if not record:
                response = {
                    'msg': 'URL not found',
                }
                return Response(response, status=HTTP_404_NOT_FOUND)

            record.count += 1
            record.save()

        response = {
            'original_url': record.original_url,
        }
        return Response(response, status=HTTP_200_OK)

    def post(self, request, **kwargs):
        original_url = request.data.get('url')
        if not original_url:
            response = {
                'msg': 'URL not found',
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        record = Url.objects.filter(original_url=original_url).first()
        if not record:
            short_url = generate_short_url()
            record = Url.objects.create(original_url=original_url, short_url=short_url)
            record.save()

            crawl_url.delay(original_url)

        response = {
            'short_url': request.build_absolute_uri('/') + 'shortener/' + record.short_url,
        }
        return Response(response, status=HTTP_201_CREATED)


class TopUrlAPI(ModelViewSet):
    queryset = Url.objects.all().order_by('-count')[:MAX_URL_IN_RESPONCE]
    serializer_class = UrlSerializer
