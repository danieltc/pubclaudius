import os.path
import random
import unicodedata

from collections import OrderedDict as od
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.db.models import F

from rol.models import Rol, Categoria, Pessoa, Contato, TipoContato, Ata, AtoOficial, Membro, TipoAto, TurmaFrequencia, Frequencia

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def debug_foto(request):
    membros = Membro.objects.exclude(invalido=True).exclude(ata_demissao__isnull=False).exclude(data_demissao__isnull=False).order_by('pessoa__nome_ascii')
    membros_sem_foto = []
    for m in membros:
        try:
            if m.pessoa.foto:
                pass
            else:
                membros_sem_foto.append(m)
        except:
            membros_sem_foto.append(m)

    contagem_membros_sem_foto = len(membros_sem_foto)
    contagem_membros = len(membros)
    return render(request, 'debug_foto.html', {
                'membros_sem_foto': membros_sem_foto,
                'contagem_membros': contagem_membros,
                'contagem_membros_sem_foto': contagem_membros_sem_foto,
                })


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def debug_basicos(request):

    # arr_contatos_basicos = ['email','celular','endereco','cidade_estado','cep']
    arr_contatos_basicos = ['endereco','cidade_estado','cep']
    contatos_basicos = TipoContato.objects.filter(desc_sistema__in=arr_contatos_basicos)
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('categoria','nome')
    membros = Membro.objects.exclude(invalido=True).exclude(ata_demissao__isnull=False).exclude(data_demissao__isnull=False)
    sem_dados_basicos = []
    for m in membros:
        dados_faltantes = ""
        if not m.pessoa.nome:
            dados_faltantes += "Nome Completo, "
        if not m.pessoa.data_nascimento:
            dados_faltantes += "Data de Nascimento, "
        if not m.pessoa.naturalidade:
            pass
            #dados_faltantes += "Naturalidade, "
        if not m.pessoa.pai:
            dados_faltantes += "Filiação (PAI), "
        if not m.pessoa.mae:
            dados_faltantes += "Filiação (MÃE), "
        if not m.pessoa.sexo:
            dados_faltantes += "Sexo, "
        if not m.pessoa.estado_civil:
            dados_faltantes += "Estado Civil, "

        for c in contatos_basicos:
            try:
                m_contato = Contato.objects.get(tipo=c.id, pessoa_id=m.pessoa.id)
                if not m_contato.conteudo:
                    dados_faltantes += c.descricao + ", "
            except:
                dados_faltantes += c.descricao + ", "

        if dados_faltantes:
            m.pessoa.dados_faltantes = dados_faltantes
            sem_dados_basicos.append(m)


    contagem_membros_sem_dados = len(sem_dados_basicos)
    contagem_membros = len(membros)

    return render(request, 'debug_basicos.html', {
        'sem_dados_basicos': sem_dados_basicos,
        'contagem_membros': contagem_membros,
        'contagem_membros_sem_dados': contagem_membros_sem_dados,
        })



@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def debug_geral(request):
    maior_matricula = Membro.objects.latest('matricula')
    mats = [] #disponiveis
    for i in range(1,maior_matricula.matricula):
        try:
            m = Membro.objects.get(matricula=i)
        except:
            mats.append(i)

    membros = Membro.objects.exclude(invalido=True).exclude(ata_demissao__isnull=False).exclude(data_demissao__isnull=False).order_by('pessoa__nome_ascii')
    contagem_membros = len(membros)
    membros_sem_ato = []
    membros_sem_data = []
    membros_sem_categoria = []
    membros_admissao_duplicado = []
    id_pessoa_membro = []
    for m in membros:
        id_pessoa_membro.append(m.pessoa.id)

        if m.data_admissao == None:
            membros_sem_data.append(m.pessoa)
        try:
            admissao = AtoOficial.objects.get(pessoa_id=m.pessoa_id,tipo_ato_id__in=[1,2])
        except AtoOficial.MultipleObjectsReturned:
            admissoes = AtoOficial.objects.filter(pessoa_id=m.pessoa_id,tipo_ato_id__in=[1,2])
            m.pessoa.admissoes = admissoes
            membros_admissao_duplicado.append(m.pessoa)
        except AtoOficial.DoesNotExist:
            membros_sem_ato.append(m.pessoa)
        if m.pessoa.categoria_id not in [1,51,37,39,24,63,70,59,64,69,65,62]:
            membros_sem_categoria.append(m.pessoa)

    atos_admissao = AtoOficial.objects.filter(tipo_ato_id__in=[1,2])
    pessoas_duplicadas_no_rol = []
    admissao_sem_membro = []
    for a in atos_admissao:
        try:
            membro = Membro.objects.get(pessoa = a.pessoa)
        except Membro.MultipleObjectsReturned:
            if a.pessoa not in pessoas_duplicadas_no_rol:
                pessoas_duplicadas_no_rol.append(a.pessoa)
        except:
            admissao_sem_membro.append(a)

    exmembros = Membro.objects.exclude(invalido=True).exclude(ata_demissao__isnull=True).exclude(data_demissao__isnull=True)
    exmembros_demissao_duplicado = []
    exmembros_sem_categoria = []
    exmembros_sem_ato = []

    for m in exmembros:
        try:
            demissao = AtoOficial.objects.get(pessoa_id=m.pessoa_id,tipo_ato_id__in=[5,27])
        except AtoOficial.MultipleObjectsReturned:
            demissoes = AtoOficial.objects.filter(pessoa_id=m.pessoa_id,tipo_ato_id__in=[5,27])
            m.pessoa.demissoes = demissoes
            exmembros_demissao_duplicado.append(m.pessoa)
        except AtoOficial.DoesNotExist:
            exmembros_sem_ato.append(m.pessoa)
        if m.pessoa.categoria_id  not in [9,52,12,50,48]:
            # categorias permitidas pra ex-membros:
            # 9 Pastores da Igreja
            # 52 Ex-membro
            # 12 Visitante frequente
            # 50 Visitante frequente, mas sem intenção de compromisso
            # 48 Visitante ocasional periódico
            exmembros_sem_categoria.append(m.pessoa)

    pessoas_categoria_membro = []
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('categoria','nome')
    pessoas_nao_membros = pessoas.exclude(id__in=id_pessoa_membro)
    pessoas = Pessoa.objects.filter(categoria_id__in = [1,51,37,39,24,63,70,59,64,69,65,62])

    for p in pessoas:
        try:
            membro = Membro.objects.get(pessoa_id = p.id)
        except Membro.MultipleObjectsReturned:
            if p not in pessoas_duplicadas_no_rol:
                pessoas_duplicadas_no_rol.append(p)
        except Membro.DoesNotExist:
            pessoas_categoria_membro.append(p)

    duplo_valido = []

    for p in pessoas_duplicadas_no_rol:
        if Membro.objects.filter(pessoa_id = p.id).filter(invalido=True).count() == 0:
            duplo_valido.append(p)


    return render(request, 'debug_geral.html', {
                'maior_matricula': maior_matricula.matricula,
                'matriculas_disponiveis': mats,
                'membros_sem_ato': membros_sem_ato,
                'membros_sem_data': membros_sem_data,
                'membros_sem_categoria': membros_sem_categoria,
                'membros_admissao_duplicado': membros_admissao_duplicado,
                'admissao_sem_membro': admissao_sem_membro,
                'duplo_valido': duplo_valido,
                'pessoas_duplicadas_no_rol': pessoas_duplicadas_no_rol,
                'pessoas_categoria_membro': pessoas_categoria_membro,
                'exmembros_demissao_duplicado': exmembros_demissao_duplicado,
                'exmembros_sem_ato': exmembros_sem_ato,
                'exmembros_sem_categoria': exmembros_sem_categoria,
                'contagem_membros': contagem_membros,
                'pessoas_nao_membros': pessoas_nao_membros,
                })

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def debug(request):
    return render(request, 'debug.html')