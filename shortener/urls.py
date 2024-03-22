from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ShortenerAPI, TopUrlAPI

urlpatterns = {
    path('', ShortenerAPI.as_view()),
    path('<slug:short_url>', ShortenerAPI.as_view()),
    path('top/', TopUrlAPI.as_view({'get': 'list'})),
}

urlpatterns = format_suffix_patterns(urlpatterns)
