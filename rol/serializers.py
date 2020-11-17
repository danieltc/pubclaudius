from rest_framework import serializers
from rol.models import Pessoa, Membro

class MembroListSerializer(serializers.ModelSerializer):
    pessoa = serializers.StringRelatedField()
    detalhes = serializers.HyperlinkedIdentityField(view_name='membro-detail')
    class Meta:
        model = Membro
        fields = ['id','matricula','pessoa','detalhes']

class MembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membro
        depth = 1
        fields = '__all__'

class PessoaListSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    detalhes = serializers.HyperlinkedIdentityField(view_name='pessoa-detail')
    class Meta:
        model = Pessoa
        fields = ['id','nome','categoria','foto','detalhes']

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        depth = 1
        fields = '__all__'
