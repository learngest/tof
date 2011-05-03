# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from users.models import Inscrit

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
    sessions = [i.sessionexam for i in Inscrit.objects.filter(user=request.user)]
    if len(sessions)==1:
        return HttpResponseRedirect(sessions[0].sessionexam.get_absolute_url)
    return render_to_response('users/liste_sessions.html',{
        'sessions': sessions,
        }, context_instance=RequestContext(request))
