# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from users.models import Client, SessionExam, Section, Inscrit, ContenuStd, ContenuCas

admin.site.register(User)

class ClientAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
admin.site.register(Client, ClientAdmin)

class SessionExamAdmin(admin.ModelAdmin):
    search_fields = ('titre',)
    list_display = ('id','client','titre','ouverture','fermeture')
    list_filter = ('client',)
admin.site.register(SessionExam, SessionExamAdmin)

class SectionAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_display = ('id','sessionexam','rang')
    list_filter = ('sessionexam',)
admin.site.register(Section, SectionAdmin)

class InscritAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_filter = ('sessionexam',)
admin.site.register(Inscrit, InscritAdmin)   

class ContenuStdAdmin(admin.ModelAdmin):
    list_filter = ('section','granule',)
admin.site.register(ContenuStd, ContenuStdAdmin)

class ContenuCasAdmin(admin.ModelAdmin):
    search_fields = ('titre', 'libel',)
    list_filter = ('section',)
admin.site.register(ContenuCas, ContenuCasAdmin)
