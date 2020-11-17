
from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions, filters
from rol.serializers import PessoaSerializer, MembroSerializer, PessoaListSerializer, MembroListSerializer
from rol.models import Pessoa, Membro

class MembroViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action != 'list' and self.request.user.has_perm('rol.add_pessoa'):
            return MembroSerializer
        else:
            return MembroListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['pessoa__nome']
    queryset = Membro.objects.filter(data_demissao__isnull = True)
    

class PessoaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action != 'list' and self.request.user.has_perm('rol.add_pessoa'):
            return PessoaSerializer
        else:
            return PessoaListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    queryset = Pessoa.objects.all().order_by('categoria','nome')
