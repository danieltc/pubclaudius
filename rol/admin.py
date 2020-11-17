from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import *

UserAdmin.list_display = ('__str__', 'last_login')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class LogEntryAdmin (admin.ModelAdmin):
        date_hierarchy = 'action_time'
        list_display = ('__str__','user','action_time',)
        list_filter = ['user']
        search_fields = ['change_message']

class IgrejaAdmin(admin.ModelAdmin):
        list_display =  ('nome','ipb','id')
        list_filter = ['classe']
        search_fields = ['nome']

class PessoaAdmin(admin.ModelAdmin):
        list_display =  ('nome','categoria','id')
        list_filter = ['categoria']
        search_fields = ['nome']

class CategoriaAdmin(admin.ModelAdmin):
        list_display =  ('agregador','descricao','id')
        list_filter = ['agregador']
        search_fields = ['descricao']

class AtoOficialAdmin(admin.ModelAdmin):
        list_display = ('pessoa','tipo_ato','data','id')
        list_filter = ['ata_ato']
        search_fields = ['pessoa__nome']

class OficialatoAdmin(admin.ModelAdmin):
        list_display = ('pessoa','cargo_atual','data_inicio_mandato','data_fim_mandato','ativo')
        list_filter = ['ativo','cargo_atual','pessoa__categoria__agregador']
        search_fields = ['pessoa__nome']


class ContatoAdmin(admin.ModelAdmin):
        list_display =  ('pessoa','tipo','conteudo')
        list_filter = ['tipo']
        search_fields = ['pessoa__nome']

class AtaAdmin(admin.ModelAdmin):
        list_display = ('identificacao','numero','data')

class MembroAdmin(admin.ModelAdmin):
        list_display = ('pessoa', 'matricula', 'ata_admissao', 'ata_demissao','id')
        search_fields = ['pessoa__nome']

admin.site.register(Igreja, IgrejaAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(AgregadorCategoria)
admin.site.register(Oficialato, OficialatoAdmin)
admin.site.register(AtoOficial, AtoOficialAdmin)
admin.site.register(Contato, ContatoAdmin)
admin.site.register(Ata, AtaAdmin)
admin.site.register(Membro, MembroAdmin)
admin.site.register(TipoContato)
admin.site.register(TipoEstadoCivilComplemento)
admin.site.register(TipoEstadoCivil)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(TurmaFrequencia)
admin.site.register(Frequencia)
admin.site.register(TipoGrupo)
admin.site.register(Rol)
admin.site.register(Relatorio)
admin.site.register(Talento)
admin.site.register(CategoriaTalento)


admin.site.site_header = 'Rol de Membros'