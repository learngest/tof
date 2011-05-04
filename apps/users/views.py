# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from users.models import Inscrit, SessionExam, Section
from users.controllers import UserSection

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

@login_required
def dashboard(request):
    """
    Wrapper pour les tableaux de bords des différents types
    d'utilisateurs :
    - staff
    - user standard (étudiant)
    """
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    return dashboard_student(request)

@login_required
def dashboard_student(request):
    """
    Tableau de bord standard :
    - liste des sessions d'examen auxquelles le User est inscrit avec choix
    - ou accès direct à la session s'il n'y en a qu'une
    """
    sessions = [i.sessionexam
            for i in Inscrit.objects.filter(user=request.user)
            if not i.sessionexam.hidden]
    if len(sessions)==1:
        return HttpResponseRedirect(sessions[0].sessionexam.get_absolute_url)
    return render_to_response('users/liste_sessions.html',{
        'sessions': sessions,
        }, context_instance=RequestContext(request))

@login_required
def session(request, exam_id=None):
    """
    Renvoie l'état courant des sections d'une session d'examen
    """
    if not exam_id:
        request.user.message_set.create( message=_("Requested url is invalid."))
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)
    try:
        exam = SessionExam.exams.get(pk=exam_id)
    except SessionExam.DoesNotExist:
        request.user.message_set.create( message=_("This exam does not exist."))
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)
    try:
        inscrit = Inscrit.objects.get(user=request.user, sessionexam=exam)
    except Inscrit.DoesNotExist:
        request.user.message_set.create( message=_("You are not subscribed to this exam."))
        return HttpResponseRedirect(LOGIN_REDIRECT_URL)
    sections = [UserSection(request.user, section) for section in
            Section.objects.filter(sessionexam = exam)]
    return render_to_response('users/liste_sections.html',{
        'exam': exam,
        'sections': sections,
        }, context_instance=RequestContext(request))
