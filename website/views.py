from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic.base import TemplateView

from .models import Event


class HomePageView(TemplateView):
    
    template_name = "website/index.html"


class ParticipateView(TemplateView):
    
    template_name = "website/participant.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['event'] = Event.objects.get(event_id=self.kwargs['event_id'])
        except Event.DoesNotExist:
            raise Http404("Event does not exist :(")
        return context
