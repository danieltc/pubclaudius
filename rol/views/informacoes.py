import csv
import os.path
import random
import unicodedata

from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q

from collections import OrderedDict as od
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO

from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.db.models import F
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

from rol.models import Relatorio, Rol, TipoGrupo, Categoria, Pessoa, Contato, TipoContato, Ata, AtoOficial, Membro, TipoAto, TurmaFrequencia, Frequencia, Oficialato
from rol.forms import  RelatorioForm, PessoaForm, PresbPessoaForm, AtaForm, AtoOficialForm, AdmitirForm, DemitirForm, FreqCultoForm

from pprint import pprint

@login_required
def home(request):
    pastores = Oficialato.objects.filter(ativo=True).filter(cargo_atual__in=['pastor_aux', 'pastor_evang', 'pastor_titular'])
    presbiteros = Oficialato.objects.filter(ativo=True).filter(cargo_atual='presbitero')
    diaconos = Oficialato.objects.filter(ativo=True).filter(cargo_atual='diacono')
    # CULTOS
    tempo = datetime.now() - relativedelta(weeks=6)
    matutino = TurmaFrequencia.objects.get(pk = 1)#matutino
    noturno = TurmaFrequencia.objects.get(pk = 3)#noturno

    f_matutino = Frequencia.objects.filter(turma=matutino,data__gte=tempo).order_by('data')
    freq = []
    for f in f_matutino:
        f.matutino = f.quantidade
        f.dia = f.data.strftime("%d/%m")
        try:
            f_n = Frequencia.objects.get(turma=noturno,data=f.data)
            f.noturno = f_n.quantidade
        except:
            f.noturno = 0
        freq.append(f)

    tempo_anual = datetime.now() - relativedelta(years=1)
    
    f_matutino_anual = Frequencia.objects.filter(turma=matutino,data__gte=tempo_anual).order_by('data')
    turmas_ebd = TurmaFrequencia.objects.filter(Q(tipo = 'ebd')|Q(tipo = 'ebdi'))
    freq_anual = []
    for f in f_matutino_anual:
        f.matutino = f.quantidade
        f.dia = f.data.strftime("%d/%m")
        try:
            f_n = Frequencia.objects.get(turma=noturno,data=f.data)
            f.noturno = f_n.quantidade
        except:
            f.noturno = 0
        try:
            fs_ebds = Frequencia.objects.filter(turma__in=turmas_ebd,data=f.data)
            f.ebds = 0
            for x in fs_ebds:
                try:
                    f.ebds = f.ebds+x.quantidade
                except:
                    pass
        except:
            f.ebds = 0
        freq_anual.append(f)

    # EBD
    tempo_ebd = datetime.now() - relativedelta(weeks=4)
    turmas = TurmaFrequencia.objects.filter(tipo = 'ebd').filter( dt_inicio__lte=date.today()).exclude(dt_fim__lte=date.today()).order_by('-id')
    domingos = Frequencia.objects.distinct().filter(turma_id = 5,data__gte=tempo_ebd).order_by('data')
    for d in domingos:
        frequencias = []
        for t in turmas:
            try:
                frequencias.append(Frequencia.objects.get(data = d.data, turma = t))
            except:
                frequencias.append(0)
        d.frequencias = frequencias


     # EBDI
    turmas_i = TurmaFrequencia.objects.filter(tipo = 'ebdi').filter( dt_inicio__lte=date.today()).exclude(dt_fim__lte=date.today()).order_by('-id')
    domingos_i = Frequencia.objects.distinct().filter(turma_id = 6,data__gte=tempo_ebd).order_by('data')
    for d in domingos_i:
        frequencias_i = []
        for t in turmas_i:
            try:
                frequencias_i.append(Frequencia.objects.get(data = d.data, turma = t))
            except:
                frequencias_i.append(0)
        d.frequencias = frequencias_i


    atas = Ata.objects.all().order_by('data');
    progresso_membresia = []
    datas_membresia = []
    membresia_total = 0
    for ata in atas:
        try:
            admissoes = ata.admitidos.count()
            demissoes = ata.demitidos.count()
            if(1):
                membresia_total = membresia_total + admissoes - demissoes
                ata.data_formatada = ata.data.strftime("%d/%m/%y")
                ata.membresia_total=membresia_total
                progresso_membresia.append(ata)
        except:
            pass




    return render(request, 'home.html', {'progresso_membresia':progresso_membresia,'freq_anual': freq_anual,'freq': freq,'turmas':turmas,'domingos':domingos,'turmas_i':turmas_i,'domingos_i':domingos_i, 'pastores':pastores, 'presbiteros':presbiteros,'diaconos':diaconos})


@login_required
def aniversarios(request):
    today = date.today()
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,7,9,12,20,24,25,37,38,39,40,42,44,45,46,47,49,50,51,54,58,60,61,62,63,64,65,68,69,70])

    pessoas_marajo = pessoas.filter(rol=2)
    pessoas = pessoas.filter(rol=1)

    casados = [4,8] #magic numbers!
    aniversarios = {}
    random.Random()
    for p in pessoas:
        info = ""
        try:
            meta = p.data_nascimento.strftime('%m%d')+p.nome+str(p.id)
            info = p.data_nascimento.strftime('%d/%m: ')+p.nome
            aniversarios.update({meta:info})
        except:
            meta = '9'+p.nome
            info = p.nome + ' - sem aniversário cadastrado'
            aniversarios.update({meta:info})
        try:
            if p.estado_civil_id in casados :
                meta = p.data_inicio_relacionamento.strftime('%m%d')+p.nome+str(p.id)+'casamento'
                meta_conjuge = p.data_inicio_relacionamento.strftime('%m%d')+p.conjuge.nome+str(p.conjuge.id)+'casamento'
                if(p.sexo == 'M'):
                    info = p.data_inicio_relacionamento.strftime('%d/%m ')+"- Casamento: "+ p.nome +' e '+ p.conjuge.nome
                else:
                    info = p.data_inicio_relacionamento.strftime('%d/%m ')+"- Casamento: "+ p.conjuge.nome +' e '+ p.nome
                if meta_conjuge not in aniversarios:
                    aniversarios.update({meta:info})
        except:
            pass
    aniversarios.update({'8':'---------- Pessoas sem aniversário cadastrado ----------'})
    anivs = od(sorted(aniversarios.items(), key=lambda t: t[0]))
    return render(request, 'aniversarios.html',{'today':today,'aniversarios':anivs})

@login_required
def relatorios(request):
    relatorios_personalizados = Relatorio.objects.all()
    quatro_anos = datetime.now() - relativedelta(years=4)
    sete_anos = datetime.now() - relativedelta(years=7)
    treze_anos = datetime.now() - relativedelta(years=13)
    trinta_anos = datetime.now() - relativedelta(years=30)
    sessenta_anos = datetime.now() - relativedelta(years=60)
    dezoito_anos = datetime.now() - relativedelta(years=18)

    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('categoria','nome')

    pessoas_marajo = pessoas.filter(rol=2)
    pessoas = pessoas.filter(rol=1)

    total = pessoas
    homens = pessoas.filter(sexo = 'M')
    pais = pessoas.filter(tem_filhos = True).filter(sexo = 'M')
    mulheres = pessoas.filter( sexo = 'F')
    maes = pessoas.filter( tem_filhos = True ).filter( sexo = 'F')
    bebes = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__gt=quatro_anos)
    criancas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=quatro_anos).filter(data_nascimento__gt=sete_anos)
    upj = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sete_anos).filter(data_nascimento__gt=treze_anos)
    adolescentes = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=treze_anos).filter(data_nascimento__gt=dezoito_anos)
    jovens_ate_30 = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=dezoito_anos).filter(data_nascimento__gt=trinta_anos)
    adultos = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=trinta_anos).filter(data_nascimento__gt=sessenta_anos)
    idosos = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sessenta_anos)
    casados = pessoas.filter(estado_civil_id__in=[4,14]).filter(conjuge__isnull=False)
    viuvas = pessoas.filter(estado_civil_id__in=[11,8,5],sexo='F')
    casas = pessoas.filter(chefe_familia_id = F('pk'))
    sem_foto = pessoas.filter(foto = "")
    membros = pessoas.exclude(categoria_id=9)
    membros_nao_comungantes = pessoas.filter(categoria_id__in=[24,59,62,63,64,65,69,70])
    membros_comungantes = pessoas.exclude(categoria_id__in=[9,24,59,62,63,64,65,69,70])
    congregacao_marajo = pessoas_marajo

    relatorio_ump = pessoas.exclude(tem_filhos = True).exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=(datetime.now() - relativedelta(years=15))).filter(data_nascimento__gt=(datetime.now() - relativedelta(years=35)))

    participantes = pessoas.distinct().filter(turmas_membro__isnull = False).filter(turmas_membro__tipo_grupo_id__in=[8,9,10])
    lideres = pessoas.distinct().filter(turmas_lider__isnull = False)
    disponiveis = pessoas.exclude(id__in=participantes.values_list('id', flat=True)).exclude(id__in=lideres.values_list('id', flat=True))

    return render(request, 'relatorios.html', {
        'relatorios_personalizados':relatorios_personalizados,
        'total':total.count(),
        'homens':homens.count(),
        'pais':pais.count(),
        'mulheres':mulheres.count(),
        'maes':maes.count(),
        'bebes':bebes.count(),
        'criancas':criancas.count(),
        'upj':upj.count(),
        'adolescentes':adolescentes.count(),
        'jovens':jovens_ate_30.count(),
        'adultos':adultos.count(),
        'idosos':idosos.count(),
        'casados':casados.count(),
        'viuvas':viuvas.count(),
        'casas':casas.count(),
        'sem_foto':sem_foto.count(),
        'membros':membros.count(),
        'membros_nao_comungantes':membros_nao_comungantes.count(),
        'membros_comungantes':membros_comungantes.count(),
        'congregacao_marajo':congregacao_marajo.count(),
        'participantes':participantes.count(),
        'lideres':lideres.count(),
        'disponiveis':disponiveis.count(),
        'relatorio_ump':relatorio_ump.count(),

        })


@login_required
def rol_publico(request,tipo='todos'):

    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii')

    pessoas_marajo = pessoas.filter(rol=2)
    pessoas = pessoas.filter(rol=1)

    participantes = pessoas.distinct().filter(turmas_membro__isnull = False).filter(turmas_membro__tipo_grupo_id__in=[8,9,10])
    lideres = pessoas.distinct().filter(turmas_lider__isnull = False)

    today = date.today()
    quatro_anos = datetime.now() - relativedelta(years=4)
    sete_anos = datetime.now() - relativedelta(years=7)
    treze_anos = datetime.now() - relativedelta(years=13)
    trinta_anos = datetime.now() - relativedelta(years=30)
    sessenta_anos = datetime.now() - relativedelta(years=60)
    cinquenta_anos = datetime.now() - relativedelta(years=50)
    dezoito_anos = datetime.now() - relativedelta(years=18)

    total = pessoas.count()
    if(tipo == 'homens'):
        pessoas = pessoas.filter(sexo = 'M')
    elif(tipo == 'pais'):
        pessoas = pessoas.filter(tem_filhos = True).filter(sexo = 'M')
    elif(tipo == 'mulheres'):
        pessoas = pessoas.filter( sexo = 'F')
    elif(tipo == 'maes'):
        pessoas = pessoas.filter( tem_filhos = True ).filter( sexo = 'F')
    elif(tipo == 'bebes'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__gt=quatro_anos)
    elif(tipo == 'criancas'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=quatro_anos).filter(data_nascimento__gt=sete_anos)
    elif(tipo == 'upj'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sete_anos).filter(data_nascimento__gt=treze_anos)
    elif(tipo == 'adolescentes'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=treze_anos).filter(data_nascimento__gt=dezoito_anos)
    elif(tipo == 'jovens'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=dezoito_anos).filter(data_nascimento__gt=trinta_anos)
    elif(tipo == 'adultos'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=trinta_anos).filter(data_nascimento__gt=sessenta_anos)
    elif(tipo == 'idosos'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sessenta_anos)
    elif(tipo == 'casados'):
        pessoas = pessoas.filter(estado_civil_id__in=[4,14])
    elif(tipo == 'viuvas'):
        pessoas = pessoas.filter(estado_civil_id__in=[11,8,5],sexo='F')
    elif(tipo == 'casas'):
        pessoas = pessoas.filter(chefe_familia_id = F('pk'))
    elif(tipo == 'solteiros'):
        pessoas = pessoas.filter(estado_civil_complemento__isnull = True).exclude(estado_civil_id__in=[4,14]).filter(data_nascimento__lte=dezoito_anos).filter(sexo = 'M').filter(data_nascimento__gt=cinquenta_anos)
    elif(tipo == 'solteiras'):
        pessoas = pessoas.filter(estado_civil_complemento__isnull = True).exclude(estado_civil_id__in=[4,14]).filter(data_nascimento__lte=dezoito_anos).filter(sexo = 'F').filter(data_nascimento__gt=cinquenta_anos)
    elif(tipo == 'sem_foto'):
        pessoas = pessoas.filter(foto = "")
    elif(tipo == 'membros'):
        pessoas = pessoas.exclude(categoria_id=9)
    elif(tipo == 'membros_nao_comungantes'):
        pessoas = pessoas.filter(categoria_id__in=[24,59,62,63,64,65,69,70])
    elif(tipo == 'membros_comungantes'):
        pessoas = pessoas.exclude(categoria_id__in=[9,24,59,62,63,64,65,69,70])
    elif(tipo == 'congregacao_marajo'):
        pessoas = pessoas_marajo
    elif(tipo == 'participantes'):
        pessoas = participantes
    elif(tipo == 'lideres'):
        pessoas = lideres
    elif(tipo == 'disponiveis'):
        pessoas = pessoas.exclude(id__in=participantes.values_list('id', flat=True)).exclude(id__in=lideres.values_list('id', flat=True))
    elif(tipo == 'relatorio_ump'):
        pessoas = pessoas.exclude(tem_filhos = True).exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=(datetime.now() - relativedelta(years=15))).filter(data_nascimento__gt=(datetime.now() - relativedelta(years=35))).order_by('sexo').order_by('-data_nascimento')

    else:
        tipo = 'todos'

    if(tipo in ['bebes','criancas','upj','adolescentes','jovens','relatorio_ump']):
        pessoas = pessoas.order_by("-data_nascimento")

    for p in pessoas:
        try:
            p.idade = today.year - p.data_nascimento.year - ((today.month, today.day) < (p.data_nascimento.month, p.data_nascimento.day))
        except:
            pass
    return render(request, 'rol_publico.html', {'pessoas': pessoas, 'tipo': tipo.capitalize(), 'tipotxt': tipo.replace('_', ' ').capitalize(), 'quantidade':pessoas.count()})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def relatorio_padrao_turma(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    if turma.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    else:
        participantes = turma.participantes.all()
        for p in participantes:
            try:
                p.celular = p.contato_set.filter(tipo=3)[0].conteudo
            except:
                p.celular = "sem celular"
            try:
                p.email = p.contato_set.filter(tipo=1)[0].conteudo
            except:
                p.email = "sem email"

        lideranca = turma.lideranca.all()
        for p in lideranca:
            try:
                p.celular = p.contato_set.filter(tipo=3)[0].conteudo
            except:
                p.celular = "sem celular"
            try:
                p.email = p.contato_set.filter(tipo=1)[0].conteudo
            except:
                p.email = "sem email"

        tipo = "turma"+str(pk)

        html_string = render_to_string('../templates/relatorio_padrao_turma.html', {'lideranca':lideranca,'participantes':participantes,'titulo':turma.titulo})

        html = HTML(string=html_string)
        html.write_pdf(target=tipo+'.pdf')
        fs = FileSystemStorage('./')
        with fs.open(tipo+'.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+tipo+'.pdf"'
            return response
        return response

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def relatorio_padrao_grupo(request,pk):
    if pk is 12 and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('GRUPO RESTRITO AO CONSELHO')
    else:
        grupo = TipoGrupo.objects.get(pk=pk)
        if request.user.has_perm('rol.add_ata'):
            turmas = TurmaFrequencia.objects.filter(tipo_grupo_id=pk)
        else:
            turmas = TurmaFrequencia.objects.filter(tipo_grupo_id=pk).filter(restrito=False)
        turmas_grupo = []
        for turma in turmas:
            turma.lista_participantes = turma.participantes.all()
            turma.lista_lideranca = turma.lideranca.all()
            turmas_grupo.append(turma)

        tipo = "grupo"+str(pk)

        html_string = render_to_string('../templates/relatorio_padrao_grupo.html', {'turmas':turmas_grupo,'titulo':grupo.nome})

        html = HTML(string=html_string)
        html.write_pdf(target=tipo+'.pdf');
        fs = FileSystemStorage('./')
        with fs.open(tipo+'.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+tipo+'.pdf"'
            return response
        return response


@login_required
def relatorio_padrao(request,tipo='todos',titulo=""):

    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii')

    pessoas_marajo = pessoas.filter(rol=2)
    pessoas = pessoas.filter(rol=1)

    participantes = pessoas.distinct().filter(turmas_membro__isnull = False).filter(turmas_membro__tipo_grupo_id__in=[8,9,10])
    lideres = pessoas.distinct().filter(turmas_lider__isnull = False)

    today = date.today()
    quatro_anos = datetime.now() - relativedelta(years=4)
    sete_anos = datetime.now() - relativedelta(years=7)
    treze_anos = datetime.now() - relativedelta(years=13)
    trinta_anos = datetime.now() - relativedelta(years=30)
    sessenta_anos = datetime.now() - relativedelta(years=60)
    cinquenta_anos = datetime.now() - relativedelta(years=50)
    dezoito_anos = datetime.now() - relativedelta(years=18)

    total = pessoas.count()
    if(tipo == 'homens'):
        pessoas = pessoas.filter(sexo = 'M')
    elif(tipo == 'pais'):
        pessoas = pessoas.filter(tem_filhos = True).filter(sexo = 'M')
    elif(tipo == 'mulheres'):
        pessoas = pessoas.filter( sexo = 'F')
    elif(tipo == 'maes'):
        pessoas = pessoas.filter( tem_filhos = True ).filter( sexo = 'F')
    elif(tipo == 'bebes'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__gt=quatro_anos)
    elif(tipo == 'criancas'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=quatro_anos).filter(data_nascimento__gt=sete_anos)
    elif(tipo == 'upj'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sete_anos).filter(data_nascimento__gt=treze_anos)
    elif(tipo == 'adolescentes'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=treze_anos).filter(data_nascimento__gt=dezoito_anos)
    elif(tipo == 'jovens'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=dezoito_anos).filter(data_nascimento__gt=trinta_anos)
    elif(tipo == 'adultos'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=trinta_anos).filter(data_nascimento__gt=sessenta_anos)
    elif(tipo == 'idosos'):
        pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=sessenta_anos)
    elif(tipo == 'casados'):
        pessoas = pessoas.filter(estado_civil_id__in=[4,14])
    elif(tipo == 'viuvas'):
        pessoas = pessoas.filter(estado_civil_id__in=[11,8,5],sexo='F')
    elif(tipo == 'casas'):
        pessoas = pessoas.filter(chefe_familia_id = F('pk'))
    elif(tipo == 'solteiros'):
        pessoas = pessoas.filter(estado_civil_complemento__isnull = True).exclude(estado_civil_id__in=[4,14]).filter(data_nascimento__lte=dezoito_anos).filter(sexo = 'M').filter(data_nascimento__gt=cinquenta_anos)
    elif(tipo == 'solteiras'):
        pessoas = pessoas.filter(estado_civil_complemento__isnull = True).exclude(estado_civil_id__in=[4,14]).filter(data_nascimento__lte=dezoito_anos).filter(sexo = 'F').filter(data_nascimento__gt=cinquenta_anos)
    elif(tipo == 'sem_foto'):
        pessoas = pessoas.filter(foto = "")
    elif(tipo == 'membros'):
        pessoas = pessoas.exclude(categoria_id=9)
    elif(tipo == 'membros_nao_comungantes'):
        pessoas = pessoas.filter(categoria_id__in=[24,59,62,63,64,65,69,70])
    elif(tipo == 'membros_comungantes'):
        pessoas = pessoas.exclude(categoria_id__in=[9,24,59,62,63,64,65,69,70])
    elif(tipo == 'congregacao_marajo'):
        pessoas = pessoas_marajo
    elif(tipo == 'participantes'):
        pessoas = participantes
    elif(tipo == 'lideres'):
        pessoas = lideres
    elif(tipo == 'disponiveis'):
        pessoas = pessoas.exclude(id__in=participantes.values_list('id', flat=True)).exclude(id__in=lideres.values_list('id', flat=True))
    elif(tipo == 'relatorio_ump'):
        pessoas = pessoas.exclude(tem_filhos = True).exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=(datetime.now() - relativedelta(years=15))).filter(data_nascimento__gt=(datetime.now() - relativedelta(years=35)))
    else:
        tipo = 'todos'

    if titulo == "AG":
        titulo = "Igreja Presbiteriana Semear - Assembléia Geral Extraordinária - 06/10/2019"
    else:
        titulo = tipo

    if(tipo in ['bebes','criancas','upj','adolescentes','jovens','relatorio_ump']):
        pessoas = pessoas.order_by("-data_nascimento")
    for p in pessoas:
        try:
            p.idade = today.year - p.data_nascimento.year - ((today.month, today.day) < (p.data_nascimento.month, p.data_nascimento.day))
        except:
            pass


    html_string = render_to_string('../templates/relatorio_padrao.html', {'pessoas':enumerate(pessoas,1),'tipo':titulo})

    html = HTML(string=html_string)
    html.write_pdf(target=tipo+'.pdf')
    fs = FileSystemStorage('./')
    with fs.open(tipo+'.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+tipo+'.pdf"'
        return response
    return response


@login_required
def relatorio_personalizado(request, pk, pdf=False):
    generate_pdf = False
    generate_csv = False
    if str(pdf) == 'pdf':
        generate_pdf = True
    if str(pdf) == 'csv':
        generate_csv = True
    today = date.today()
    relatorio = Relatorio.objects.get(pk = pk)
    filtros = {}
    if relatorio.turma_grupo is not None:
        turma = TurmaFrequencia.objects.get(pk=relatorio.turma_grupo.pk)
        filtros['Turma/Grupo'] = turma
        pessoas = turma.participantes.all()

    else:
        if relatorio.formas_admissao.count() or \
        relatorio.data_admissao_inicial is not None or \
        relatorio.data_admissao_final is not None or \
        relatorio.formas_demissao.count() or \
        relatorio.data_demissao_inicial is not None or \
        relatorio.data_demissao_final is not None or \
        relatorio.rol_separado is not None or \
        relatorio.invalido is not None:
            pessoas = Pessoa.objects.filter( id__in = Membro.objects.values_list('pessoa_id', flat=True))
        else:
            pessoas = Pessoa.objects.all()
        if relatorio.formas_admissao.count(): 
            filtros['Formas Admissão'] = ", ".join(str(o) for o in relatorio.formas_admissao.all())
            pessoas = pessoas.filter( id__in = Membro.objects.filter(forma_admissao__in = relatorio.formas_admissao.all()).values_list('pessoa_id', flat=True))
        if relatorio.data_admissao_inicial is not None:
            filtros['Data de Admissão Inicial'] = relatorio.data_admissao_inicial
            pessoas = pessoas.filter( id__in = Membro.objects.filter(data_admissao__gte = relatorio.data_admissao_inicial).values_list('pessoa_id', flat=True))
        if relatorio.data_admissao_final is not None:
            filtros['Data de Admissão Final'] = relatorio.data_admissao_final
            pessoas = pessoas.filter( id__in = Membro.objects.filter(data_admissao__lte = relatorio.data_admissao_final).values_list('pessoa_id', flat=True))
        if relatorio.formas_demissao.count():
            filtros['Formas Demissão'] = ", ".join(str(o) for o in relatorio.formas_demissao.all())
            pessoas = pessoas.filter( id__in = Membro.objects.filter(forma_demissao__in = relatorio.formas_demissao.all()).values_list('pessoa_id', flat=True))
        if relatorio.data_demissao_inicial is not None:
            filtros['Data de Demissão Inicial'] = relatorio.data_demissao_inicial
            pessoas = pessoas.filter( id__in = Membro.objects.filter(data_admissao__gte = relatorio.data_admissao_inicial).values_list('pessoa_id', flat=True))
        if relatorio.data_demissao_final is not None:
            filtros['Data de Demissão Final'] = relatorio.data_demissao_final
            pessoas = pessoas.filter( id__in = Membro.objects.filter(data_admissao__lte = relatorio.data_admissao_final).values_list('pessoa_id', flat=True))
        if relatorio.rol_separado is not None:
            filtros['Rol Separado'] = 'Sim' if relatorio.rol_separado else 'Não'
            pessoas = pessoas.filter( id__in = Membro.objects.filter(rol_separado = relatorio.rol_separado).values_list('pessoa_id', flat=True))
        if relatorio.invalido is not None:
            filtros['Registro Inválido'] = 'Sim' if relatorio.invalido else 'Não'
            pessoas = pessoas.filter( id__in = Membro.objects.filter(invalido = relatorio.invalido).values_list('pessoa_id', flat=True))
        if relatorio.sexo is not None:
            filtros['Sexo'] = 'Masculino' if relatorio.sexo == 'M' else 'Feminino'
            pessoas = pessoas.filter(sexo=relatorio.sexo)
        if relatorio.comungante is not None:
            filtros['Comungante'] = 'Sim' if relatorio.comungante else 'Não'
            pessoas = pessoas.filter(comungante=relatorio.comungante)
        if relatorio.chefe_familia is not None:
            filtros['Chefe de Família'] = 'Sim' if relatorio.chefe_familia else 'Não'
            pessoas = pessoas.filter(chefe_familia_id = F('pk'))
        if relatorio.categorias.count():
            filtros['Categorias'] = ", ".join(str(o) for o in relatorio.categorias.all())
            pessoas = pessoas.filter(categoria__in = relatorio.categorias.all())
        if relatorio.idade_minima is not None:
            filtros['Idade Mínima'] = relatorio.idade_minima
            data_idade_minima = datetime.now() - relativedelta(years=relatorio.idade_minima)
            pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__lte=data_idade_minima)
        if relatorio.idade_maxima is not None:
            filtros['Idade Máxima'] = relatorio.idade_maxima
            data_idade_maxima = datetime.now() - relativedelta(years=relatorio.idade_maxima + 1 )#tricky one
            pessoas = pessoas.exclude(data_nascimento__isnull=True).filter(data_nascimento__gte=data_idade_maxima)
        if relatorio.data_falecimento_inicial is not None:
            filtros['Data de Falecimento Inicial'] = relatorio.data_falecimento_inicial
            pessoas = pessoas.exclude(data_falecimento__isnull=True).filter(data_falecimento__gte=relatorio.data_falecimento_inicial)
        if relatorio.data_falecimento_final is not None:
            filtros['Data de Falecimento Final'] = relatorio.data_falecimento_final
            pessoas = pessoas.exclude(data_falecimento__isnull=True).filter(data_falecimento__lte=relatorio.data_falecimento_final)
        if relatorio.formas_admissao_pretendida.count():
            filtros['Formas de Admissão Pretendidas'] = ", ".join(str(o) for o in relatorio.formas_admissao_pretendida.all())
            pessoas = pessoas.filter(forma_admissao_pretendida__in = relatorio.formas_admissao_pretendida.all())
        if relatorio.entrevista_admissao_realizada is not None:
            filtros['Entrevista de Admissão Realizada'] = 'Sim' if relatorio.entrevista_admissao_realizada else 'Não'
            pessoas = pessoas.filter(entrevista_admissao_realizada = relatorio.entrevista_admissao_realizada)
        if relatorio.carta_transferencia_requisitada is not None:
            filtros['Carta de Transferência Realizada'] = 'Sim' if relatorio.entrevista_admissao_realizada else 'Não'
            pessoas = pessoas.filter(carta_transferencia_requisitada = relatorio.carta_transferencia_requisitada)
        if relatorio.estados_civis.count():
            filtros['Estados Civis'] = ", ".join(str(o) for o in relatorio.estados_civis.all())
            pessoas = pessoas.filter(estado_civil__in = relatorio.estados_civis.all())
        if relatorio.estados_civis_complementos.count():
            filtros['Namoro e Noivado'] = ", ".join(str(o) for o in relatorio.estados_civis_complementos.all())
            pessoas = pessoas.filter(estado_civil_complemento__in = relatorio.estados_civis_complementos.all())
        if relatorio.data_inicio_relacionamento_inicial is not None:
            filtros['Data de Início de Relacionamento - Inicial'] = relatorio.data_inicio_relacionamento_inicial
            pessoas = pessoas.exclude(data_inicio_relacionamento__isnull=True).filter(data_inicio_relacionamento__gte=relatorio.data_inicio_relacionamento_inicial)
        if relatorio.data_inicio_relacionamento_final is not None:
            filtros['Data de Início de Relacionamento - Final'] = relatorio.data_inicio_relacionamento_final
            pessoas = pessoas.exclude(data_inicio_relacionamento__isnull=True).filter(data_inicio_relacionamento__lte=relatorio.data_inicio_relacionamento_final)
        if relatorio.data_pedido_admissao_inicial is not None:
            filtros['Data de Pedido de Admissão - Inicial'] = relatorio.data_pedido_admissao_inicial
            pessoas = pessoas.exclude(data_pedido_admissao__isnull=True).filter(data_pedido_admissao__gte=relatorio.data_pedido_admissao_inicial)
        if relatorio.data_pedido_admissao_final is not None:
            filtros['Data de Pedido de Admissão - Final'] = relatorio.data_pedido_admissao_final
            pessoas = pessoas.exclude(data_pedido_admissao__isnull=True).filter(data_pedido_admissao__lte=relatorio.data_pedido_admissao_final)
        if relatorio.tem_filhos is not None:
            filtros['Pessoa Tem Filhos'] = 'Sim' if relatorio.tem_filhos else 'Não'
            pessoas = pessoas.filter(tem_filhos = relatorio.tem_filhos)
        if relatorio.rols.count():
            filtros['Róis'] = ", ".join(str(o) for o in relatorio.rols.all())
            pessoas = pessoas.filter(rol__in = relatorio.rols.all())
    total = pessoas.count()
    relatorio.total = total
    relatorio.save()
    for p in pessoas:
        try:
            try:
                p.endereco = p.contato_set.filter(tipo=6)[0].conteudo
            except:
                p.endereco = "endereço não informado"
            try:
                p.celular = p.contato_set.filter(tipo=3)[0].conteudo
            except:
                p.celular = "sem celular"
            try:
                p.foto = "<img src='"+p.foto.url+"' style='max-height: 50px;max-width: 50px;'></img>"
            except:
                p.foto = "sem foto"
            try:
                p.email = p.contato_set.filter(tipo=1)[0].conteudo
            except:
                p.email = "sem email"
            try:
                p.forma_admissao = p.membro.get().forma_admissao
            except:
                p.forma_admissao = "sem registro"
            try:
                p.data_admissao = p.membro.get().data_admissao
            except:
                p.data_admissao = "sem registro"
            try:
                p.forma_demissao = p.membro.get().forma_demissao
            except:
                p.forma_demissao = "sem registro"
            try:
                p.data_demissao = p.membro.get().data_demissao
            except:
                p.data_demissao = "sem registro"
            try:
                p.idade = today.year - p.data_nascimento.year - ((today.month, today.day) < (p.data_nascimento.month, p.data_nascimento.day))
            except:
                p.idade = 'sem registro'
            try:
                p.sexo = p.get_sexo_display()
            except:
                p.sexo =  'sem registro'
            try:
                p.comungante = 'S,i,m' if p.comungante else 'Não'
            except:
                p.comungante = 'sem registro'
            setattr(p,'None','-')
        except:
            pass
        
    if generate_pdf:
        html_string = render_to_string('../templates/relatorio_personalizado.html', {
            'campo1':relatorio.campo1,
            'campo2':relatorio.campo2,
            'campo3':relatorio.campo3,
            'campo4':relatorio.campo4,
            'campo1display':relatorio.get_campo1_display(),
            'campo2display':relatorio.get_campo2_display(),
            'campo3display':relatorio.get_campo3_display(),
            'campo4display':relatorio.get_campo4_display(),
            'pessoas':enumerate(pessoas,1),
            'titulo':relatorio.titulo
        })

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        filename = slugify(relatorio.titulo)+'.pdf'
        html.write_pdf(target=filename, presentational_hints = True)
        fs = FileSystemStorage('./')
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
            return response
        return response
    elif generate_csv:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        writer = csv.writer(response)
        writer.writerow([relatorio.get_campo1_display(),relatorio.get_campo2_display(),relatorio.get_campo3_display(),relatorio.get_campo4_display()])
        for pessoa in pessoas:
            writer.writerow([str(getattr(pessoa, str(relatorio.campo1))),str(getattr(pessoa, str(relatorio.campo2))),str(getattr(pessoa, str(relatorio.campo3))),str(getattr(pessoa, str(relatorio.campo4)))])
        return response
    else:
        return render(request, 'rol_personalizado.html', {
            'relatorio':relatorio,
            'filtros':filtros,
            'pessoas': pessoas,
            'titulo': relatorio.titulo,
            'quantidade':pessoas.count(),
            'campo1':relatorio.campo1,
            'campo2':relatorio.campo2,
            'campo3':relatorio.campo3,
            'campo4':relatorio.campo4,
            'campo1display':relatorio.get_campo1_display(),
            'campo2display':relatorio.get_campo2_display(),
            'campo3display':relatorio.get_campo3_display(),
            'campo4display':relatorio.get_campo4_display(),
        })


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def new_relatorio(request):
    formdata = {}
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.user_update = request.user
            relatorio.save()
            form.save_m2m()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Relatorio).pk,
                object_id=relatorio.id,
                object_repr=str(relatorio.titulo),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))
        return redirect('relatorio_personalizado', pk = relatorio.id)
    else:
        form = RelatorioForm()
    return render(request, 'new_relatorio.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def edit_relatorio(request,pk):
    relatorio = Relatorio.objects.get(id=pk)
    formdata = {}
    if request.method == 'POST':
        form = RelatorioForm(request.POST,instance=relatorio)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.user_update = request.user
            relatorio.save()
            form.save_m2m()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Relatorio).pk,
                object_id=relatorio.id,
                object_repr=str(relatorio.titulo),
                action_flag=CHANGE)
        else:
            return HttpResponse(str(form.errors))
        return redirect('relatorio_personalizado', pk = relatorio.id)
    else:
        form = RelatorioForm(initial=formdata,instance=relatorio)
    return render(request, 'edit_relatorio.html', {'form': form, 'relatorio': relatorio,'proibido_remover':[],})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def del_relatorio(request,pk):
    relatorio = Relatorio.objects.get(pk=pk)
    if pk not in []: #se tiver alguem proibido de deletar, bota aqui.
        relatorio.delete()
    return redirect('relatorios')
