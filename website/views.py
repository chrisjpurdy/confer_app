from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Event, Question
from .forms import NewEventForm, JoinEventForm, NewQuestionForm
from django.utils import timezone

import threading
lock = threading.Lock()

class HomePageView(FormView):

	template_name = "index.html"
	form_class = JoinEventForm

	def form_valid(self, form):
		self.success_url = "/events/"+form['event_id'].value()+"/participate"
		return super(HomePageView, self).form_valid(form)
	

class AdminPageView(LoginRequiredMixin, TemplateView):

	login_url = "login"
	template_name = "admin.html"
	
	def get_context_data(self, **kwargs):
		context = super(AdminPageView, self).get_context_data(**kwargs)
		context['events'] = Event.objects.filter(username=self.request.user).order_by('date_opened')
		return context
	

class ManageEventView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	
	login_url = "login"
	template_name = "manage_event.html"
	
	def test_func(self):
		return self.request.user == Event.objects.get(event_id=self.kwargs['event_id']).username
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['event'] = Event.objects.get(event_id=self.kwargs['event_id'])
		except Event.DoesNotExist:
			raise Http404("Event does not exist :(")
		return context
	
	
def manage_event_questions(request, event_id):
	
	# THE QUESTION ACCEPTING SYSTEM IS INSECURE
	# need to check:
	# 	- questions being changed are in the event given
	# 	- flag is a correct value
	#	- event is owned by the logged in user
	
	event = Event.objects.get(event_id=event_id)
	question_id = request.GET.get('qid', False)
	new_flag = request.GET.get('flag', False)
	
	if event.username != request.user:
		print("Another hacker oops") #event isnt owned by this user
		qs = {} #show them no data 
	else:
		if question_id and new_flag:
			if Question.objects.get(pk=question_id).event != event:
				print("O dear its a hacker")
			else:
				Question.objects.filter(pk=question_id).update(flag=new_flag)
	
		qs = Question.objects.filter(event=event).order_by('time_asked')
	
	return render_to_response('manage_questions.html', { 'questions': qs })


def presentation_event_questions(request, event_id):
	
	# THE QUESTION ACCEPTING SYSTEM IS INSECURE
	# need to check:
	# 	- questions being changed are in the event given
	# 	- flag is a correct value
	#	- event is owned by the logged in user
	
	event = Event.objects.get(event_id=event_id)
	
	if event.username != request.user:
		print("Another hacker oops") #event isnt owned by this user
		qs = {} #show them no data 
	else:
		qs = Question.objects.filter(event=event, flag='Y').order_by('time_asked')
	
	return render_to_response('presentation_questions.html', { 'questions': qs })


class PresentationPageView(LoginRequiredMixin, TemplateView):

	login_url = "login"
	template_name = "presentation.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['event'] = Event.objects.get(event_id=self.kwargs['event_id'])
		except Event.DoesNotExist:
			raise Http404("Event does not exist :(")
		return context


class ParticipateView(FormView):
	
	template_name = "participant.html"
	form_class = NewQuestionForm
	success_url = "/"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['event'] = Event.objects.get(event_id=self.kwargs['event_id'])
		except Event.DoesNotExist:
			raise Http404("Event does not exist :(")
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.event = Event.objects.get(event_id=self.kwargs['event_id'])
		self.object.time_asked = timezone.now()
		self.object.save()
		return super(ParticipateView, self).form_valid(form)


class CreateEventView(LoginRequiredMixin, generic.CreateView):
	login_url = "login"
	form_class = NewEventForm
	template_name = 'event_create.html'
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.event_id = self.generate_event_uid()
		self.object.username = self.request.user
		self.object.date_opened = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.object.event_id+'/manage')
	
	def chartoint(self, c):
		asciival = ord(c)
		if asciival in range(97,123):
			return asciival - 97
		elif asciival in range(65,91):
			return (asciival - 65) + 26
	
	def inttochar(self, n):
		if n in range(0,26):
			return chr(n+97)
		if n >= 26:
			return chr((n-26)+65)

	#using 5 bits per char
	def generate_event_uid(self):
		with open("uid.val",'r') as f:
			lock.acquire()
			textuid = f.read()
			if len(list(filter(lambda c: c=='F',textuid))) == len(textuid):
				for c in textuid:
					c = 'a'
			numuid = 0
			for i in range(0,len(textuid)):
				numuid += self.chartoint(textuid[i]) << (5*((len(textuid)-i)-1))
			numuid = (numuid + 1) % pow(2,5*len(textuid))
			newtextuid = ""
			for i in range(len(textuid)-1,-1,-1):
				newtextuid = newtextuid + self.inttochar(numuid >> (5*i))
				numuid = numuid%(pow(2,5*i))
		with open("uid.val",'w') as f:
			f.write(str(newtextuid))
			lock.release()
			return newtextuid