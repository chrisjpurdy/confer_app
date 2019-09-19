from django.urls import path
from django.views.generic.base import RedirectView
from . import views

favicon_view = RedirectView.as_view(url = '/static/favicon.ico', permanent = True)

urlpatterns = [
    path('favicon.ico', favicon_view),
    path('', views.HomePageView.as_view(), name='index'),
    path('<slug:event_id>/participate', views.ParticipateView.as_view(), name='participate'),
]
