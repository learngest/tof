# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

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
        self.is_open = self.section.is_open()
        self._state = -1
        if self.section.ouverture:
            self.ouverture = self.section.ouverture
        else:
            self.ouverture = self.section.sessionexam.ouverture
        self.retard_permis = self.section.retard_permis
        self.fermeture = self.section.fermeture
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
