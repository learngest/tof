# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from users.models import Client, SessionExam, Section, Inscrit
from testing.models import Granule

class ClientAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
admin.site.register(Client, ClientAdmin)

class SectionInline(admin.StackedInline):
    model = Section
    exclude = ('libel','duree',)

class SessionExamAdmin(admin.ModelAdmin):
    search_fields = ('titre',)
    list_display = ('id','client','titre','ouverture','fermeture')
    list_filter = ('client',)
    inlines = [SectionInline,]
admin.site.register(SessionExam, SessionExamAdmin)

class SectionAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_display = ('id','sessionexam','titre','rang')
    list_filter = ('sessionexam',)
    ordering = ['sessionexam','rang']
admin.site.register(Section, SectionAdmin)

class InscritAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_filter = ('sessionexam',)
    ordering = ['sessionexam',]
admin.site.register(Inscrit, InscritAdmin)   

