# -*- encoding: utf-8 -*-
"""
Models de l'application tofusers
"""

import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from email_auth.views import user_logged_in
from testing.models import Granule, Question, Reponse, EnonceCas

from listes import *

class Client(models.Model):
    """
    Le modèle de base Client.
    
    Définit la référence aux feuilles de style (CSS)
    et un champ libre pour les contacts etc.
    """
    
    nom = models.CharField(max_length=60, unique=True,
        help_text=_("Customer name, required."))
    style = models.CharField(_(u"Custom CSS"),
        max_length=20, null=True, blank=True,
        help_text=_("CSS to use with this customer."))
    contacts = models.TextField(null=True, blank=True,
        help_text=_("Free field (contacts, tel. numbers, ...)."))
    
    class Meta:
        ordering = ['nom']

    def __unicode__(self):
        return self.nom

class ExamManager(models.Manager):
    def get_query_set(self):
        return super(ExamManager, self).get_query_set().filter(hidden=False)

class SessionExam(models.Model):
    """
    Une session d'examen
    """
    titre = models.CharField(max_length=60, unique=True,
        help_text=_("Session title, required."))
    libel = models.TextField(null=True, blank=True,
        help_text=_("Free field for exam presentation, instructions, ...)."))
    client = models.ForeignKey(Client, 
        help_text=_("Session customer, required."))
    ouverture = models.DateTimeField(_("Opening date and time."),
        blank=True, null=True,
        help_text=_("Starting the session will not be possible before this date and time."))
    fermeture = models.DateTimeField(_("Closing date and time."),
        blank=True, null=True,
        help_text=_("Starting the session will be possible no later than this date and time."))
    langue = models.CharField(max_length=5, choices=LANGUAGES, 
        default='fr',
        help_text=_(
        "Session language, required."))
    hidden = models.BooleanField(
        help_text=_("If checked, the exam will be hidden in all views."))
    
    objects = models.Manager()
    exams = ExamManager()

    class Meta:
        ordering = ['client','ouverture']

    def __unicode__(self):
        return self.titre

    @models.permalink
    def get_absolute_url(self):
        return('users.views.session', [str(self.id)])

    def is_open(self):
        now = datetime.datetime.now()
        return((now >= self.ouverture) and (now <= self.fermeture))

class Section(models.Model):
    """
    Une section dans une session de test
    """
    sessionexam = models.ForeignKey(SessionExam,
            help_text=_('Session to which this section belongs, required.'))
    titre = models.CharField("Title", max_length=60, unique=True,
        help_text=_("Section title, required."))
    libel = models.TextField(_("Directions"), blank=True, null=True)
    rang = models.IntegerField(_("Rank"),
            help_text=_("Required."))
    granule = models.ForeignKey(Granule, help_text=_('Granule, required.'))
    nbq = models.IntegerField(_("# questions"), blank=True, null=True,
            help_text=_("Number of questions, default 5, for tests only."))
    duree = models.IntegerField(_("Duration"), null=True, blank=True,
            help_text=_("Maximum duration, minutes."))
    ouverture = models.DateTimeField(_("Opening date and time."),
        blank=True, null=True,
        help_text=_("Will use exam opening date if empty."))
    fermeture = models.DateTimeField(_("Closing date and time"),
            null=True, blank=True,
            help_text=_("Will use exam closing date if empty."))
    retard_permis = models.BooleanField(_("Late validation allowed"),
            help_text=_("Passing deadline allowed ?"))
    
    class Meta:
        ordering = ['sessionexam','rang']

    def __unicode__(self):
        return u'%s - %s' % (self.sessionexam,self.titre)

    def state(self):
        """
        Etat de la section indépendamment de l'utilisateur
        0 disponible
        3 fermée
        4 pas encore ouverte
        TODO voir comment utiliser duree vs fermeture
        """
        now = datetime.datetime.now()
        if not (self.duree or self.fermeture):
            self.fermeture = self.sessionexam.fermeture
        if not self.ouverture:
            self.ouverture = self.sessionexam.ouverture
        if now < self.ouverture:
            return 4
        if self.fermeture:
            if now > self.fermeture and not self.retard_permis:
                return 3
        return 0

    def is_open(self):
        """
        Vrai si la section est ouverte : self.state = 0
        """
        if self.state() == 0:
            return True
        return False

class Inscrit(models.Model):
    """
    Un user inscrit dans une session d'examen
    """
    sessionexam = models.ForeignKey(SessionExam,
            help_text=_('Session, required.'))
    user = models.ForeignKey(User,
            help_text=_('User, required.'))
    
    class Meta:
        ordering = ['sessionexam','user']

    def __unicode__(self):
        return u'%s - %s' % (self.sessionexam,self.user)

class UserCas(models.Model):
    """
    Un cas téléchargé par un user dans une section
    """
    user = models.ForeignKey(User,)
    section = models.ForeignKey(Section,)
    cas = models.ForeignKey(EnonceCas,)

    class Meta:
        ordering = ['user',]

    def __unicode__(self):
        return u'%s - %s' % (self.user.get_full_name(), self.cas.titre)

class ReponseStd(models.Model):
    """
    Réponse à une question standard
    """
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    question = models.ForeignKey(Question)
    reponse = models.ForeignKey(Reponse, blank=True, null=True)
    texte = models.TextField(blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        pass

    def __unicode__(self):
        return u'%s - %s - %s' % (self.user, self.contenu, self.question)

class ReponseCas(models.Model):
    """
    Devoir rendu par un utilisateur
    """
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    date = models.DateTimeField()
    fichier = models.FileField(upload_to=settings.WORKDONE_DIR)
    signature = models.CharField(max_length=54)

    class Meta:
        pass

    def __unicode__(self):
        return u'%s - %s - %s' % (self.utilisateur.email, 
                self.cas.titre, self.date)

