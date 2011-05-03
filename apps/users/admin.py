# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from users.models import Client, SessionExam, Section, Inscrit, ContenuStd, ContenuCas
from testing.models import Granule

class ClientAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
admin.site.register(Client, ClientAdmin)

class SectionInline(admin.TabularInline):
    model = Section

class SessionExamAdmin(admin.ModelAdmin):
    search_fields = ('titre',)
    list_display = ('id','client','titre','ouverture','fermeture')
    list_filter = ('client',)
    inlines = [SectionInline,]
admin.site.register(SessionExam, SessionExamAdmin)

class ContenuStdInline(admin.TabularInline):
    model = ContenuStd

class ContenuCasInline(admin.TabularInline):
    model = ContenuCas

class SectionAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_display = ('id','sessionexam','rang')
    list_filter = ('sessionexam',)
    inlines = [ContenuStdInline, ContenuCasInline]
admin.site.register(Section, SectionAdmin)

class InscritAdmin(admin.ModelAdmin):
    search_fields = ('sessionexam',)
    list_filter = ('sessionexam',)
    ordering = ['sessionexam',]
admin.site.register(Inscrit, InscritAdmin)   

class ContenuStdAdmin(admin.ModelAdmin):
    list_filter = ('section','granule',)
admin.site.register(ContenuStd, ContenuStdAdmin)

class ContenuCasAdmin(admin.ModelAdmin):
    search_fields = ('titre', 'libel',)
    list_filter = ('section',)
admin.site.register(ContenuCas, ContenuCasAdmin)
