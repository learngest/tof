# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from users.models import UserCas
from testing.models import EnonceCas

import datetime

class UserExam(object):
    """
    Controller d'un exam pour un utilisateur
    """
    def __init__(self, user, exam):
        self.user = user
        self.exam = exam

class UserSection(object):
    """
    Controller d'une section d'exam pour un utilisateur
    """
    def __init__(self, user, section):
        self.user = user
        self.section = section
        self.titre = self.section.titre
        self.libel = self.section.libel
        self.granule = self.section.granule
        self.langue = self.section.sessionexam.langue
        self.nbq = self.section.nbq
        self.is_open = self.section.is_open()
        self._state = -1
        if self.section.ouverture:
            self.ouverture = self.section.ouverture
        else:
            self.ouverture = self.section.sessionexam.ouverture
        self.fermeture = self.section.fermeture
        self.retard_permis = self.section.retard_permis
        self.duree = self.section.duree

    def state(self):
        """
        Renvoie l'état de la session
        0 disponible
        1 en cours
        2 en retard
        3 fermée
        4 ouverture le
        Seul l'état 1 dépend de l'utilisateur
        """
        if self._state == -1:
            self._state = self.section.state()
            if self._state == 0:
                # tester si en cours
                self._state = 0
        return self._state

    def str_state(self):
        """
        Renvoie l'état de la session en clair
        """
        states =(
                _("Available"),
                _("Pending"),
                _("Late"),
                _("Closed"),
                )
        if self.state() == 4:
            return _("Opening on %s") % self.ouverture
        return states[self.state()]

    def cas(self):
        """
        Renvoie le lien vers un cas si disponible, False sinon
        Le cas est celui que le User a dld précédemment si déjà fait,
        tiré au hasard dans la granule sinon
        """
        if self.granule.typg == 'C':
            try:
                ucas = UserCas.objects.get(user=self.user, section=self.section)
            except UserCas.DoesNotExist:
                cas = EnonceCas.objects.filter(
                        granule=self.granule, langue=self.langue).order_by('?')[0]
                ucas = UserCas(user = self.user,
                        section = self.section,
                        cas = cas)
                ucas.save()
            return ucas.cas
        else:
            return None
