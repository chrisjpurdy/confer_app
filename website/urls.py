from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
	path('events/', views.AdminPageView.as_view(), name='admin'),
	path('events/<slug:event_id>/manage', views.ManageEventView.as_view(), name='manage'), #NEED TO ADD EVENT MANAGEMENT VIEW
	path('events/<slug:event_id>/presentation', views.PresentationPageView.as_view(), name='presentation'),
    path('events/<slug:event_id>/participate', views.ParticipateView.as_view(), name='participate'),
	path('events/new_event', views.CreateEventView.as_view(), name='create_event'),
	path('events/<slug:event_id>/question_manage', views.manage_event_questions, name='question_manage'),
	path('events/<slug:event_id>/presentation_questions', views.presentation_event_questions, name='presentation_questions'),
]
