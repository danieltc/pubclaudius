import os.path
import random
import unicodedata

from collections import OrderedDict as od
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.db.models import F

from rol.models import Membro, Relatorio, Rol, Pessoa, TipoGrupo, TurmaFrequencia, Frequencia
from rol.forms import TurmaForm, FreqCultoForm, FreqEbdForm, FreqTurmaForm, TalentoForm

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def talentos(request):
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii').exclude(talentos=None)
    return render(request, 'talentos.html',{'pessoas': pessoas})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def add_talentos(request):
    if request.method == 'POST':
        form = TalentoForm(request.POST)
        if form.is_valid():
            pessoa = form.cleaned_data['pessoa']
            talentos = form.cleaned_data['talentos']
            pessoa.talentos.clear()
            for t in talentos.all():
                pessoa.talentos.add(t)
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                object_id=pessoa.id,
                object_repr=str(pessoa.nome)+' - talentos: '+str(talentos.all()),
                action_flag=CHANGE)
        else:
            return HttpResponse(str(form.errors))
        return redirect('talentos')
    else:
        form = TalentoForm()
    return render(request, 'add_talentos.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def carros(request):
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii')
    pessoas_com_carro = []
    for p in pessoas:
        try:
            p.carros = p.contato_set.filter(tipo=26)[0].conteudo
            pessoas_com_carro.append(p)
        except:
            pass

    return render(request, 'carros.html',{'pessoas': pessoas_com_carro,})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def grupos(request):
    grupos = TipoGrupo.objects.all()
    return render(request, 'grupos.html',{'grupos': grupos,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def grupo(request,pk):
    grupo = TipoGrupo.objects.get(pk=pk)
    turmas = TurmaFrequencia.objects.filter(tipo_grupo_id = pk)
    return render(request, 'grupo.html',{'turmas': turmas, 'grupo': grupo,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def new_turma(request,pk): #esse 'pk' é do grupo ao qual a turma vai pertencer
    grupo = TipoGrupo.objects.get(pk=pk)
    if grupo.id is 9:
        return redirect('grupo', 9) #nao pode criar novo subgrupo em 'oficiais'
    formdata = {}
    if request.method == 'POST':
        form = TurmaForm(request.POST, {'grupo':grupo})
        if form.is_valid():
            turma = form.save(commit=False)
            turma.tipo_grupo = grupo
            turma.save()
            # turma.save_m2m()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(TurmaFrequencia).pk,
                object_id=turma.id,
                object_repr=str(turma.titulo),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))
        return redirect('turma', pk = turma.id)
    else:
        form = TurmaForm()
    return render(request, 'new_turma.html', {'form': form, 'grupo':grupo})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def turma(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    participantes = turma.participantes.all()
    lideranca = turma.lideranca.all()
    return render(request, 'turma.html',{'turma': turma,'participantes':participantes, 'lideranca':lideranca})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def edit_turma(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    formdata = {}
    if request.method == 'POST':
        form = TurmaForm(request.POST,instance=turma)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.user_update = request.user
            turma.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(TurmaFrequencia).pk,
                object_id=turma.id,
                object_repr=str(turma.titulo),
                action_flag=CHANGE)
        else:
            return HttpResponse(str(form.errors))
        return redirect('turma', pk = turma.id)
    else:
        form = TurmaForm(initial=formdata,instance=turma)
    return render(request, 'edit_turma.html', {'form': form, 'turma': turma, 'proibido_remover':[9,5,2,3,11]})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def del_turma(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    grupo = turma.tipo_grupo
    if grupo.id in (2,3,5,9,11):
        return redirect('grupo', pk = grupo.id)
    participantes = turma.participantes.all()
    for p in participantes:
        turma.participantes.remove(p)
    lideranca = turma.lideranca.all()
    for l in lideranca:
        turma.lideranca.remove(l)
    turma.delete()
    return redirect('grupo', pk = grupo.id)


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def del_pessoa_turma(request,pk,pessoa):
    turma = TurmaFrequencia.objects.get(pk=pk)
    p = Pessoa.objects.get(pk=pessoa)
    turma.participantes.remove(p)
    turma.save()
    return redirect('turma',pk=pk)

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def del_lider_turma(request,pk,lider):
    turma = TurmaFrequencia.objects.get(pk=pk)
    p = Pessoa.objects.get(pk=lider)
    turma.lideranca.remove(p)
    turma.save()
    return redirect('turma',pk=pk)


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def add_pessoa_turma_tipo(request,pessoa,turma,tipo):
    t = TurmaFrequencia.objects.get(pk=turma)
    p = Pessoa.objects.get(pk=pessoa)
    if int(tipo) is 0: # = lideranca
        t.lideranca.add(p)
    else:
        t.participantes.add(p)
    t.save()
    return redirect('pessoa',pk=pessoa)

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def del_pessoa_turma_tipo(request,pessoa,turma,tipo):
    p = Pessoa.objects.get(pk=pessoa)
    t = TurmaFrequencia.objects.get(pk=turma)
    if int(tipo) is 0: # = lideranca
        t.lideranca.remove(p)
    else:
        t.participantes.remove(p)
    t.save()
    return redirect('pessoa',pk=pessoa)


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def select_turma_pessoa_tipo(request,pessoa,tipo):
    p = Pessoa.objects.get(pk=pessoa)
    turmas = TurmaFrequencia.objects.all().order_by('tipo_grupo__nome')
    return render(request, 'selecionar_turma.html',{'pessoa':p,'turmas':turmas,'tipo':int(tipo)})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def select_relatorio_turma (request,pk):
    relatorio = Relatorio.objects.get(pk=pk)
    turmas = TurmaFrequencia.objects.all().order_by('tipo_grupo__nome')
    return render(request, 'selecionar_turma_exportar.html',{'relatorio':relatorio,'turmas':turmas})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def add_relatorio_turma (request,pk,turma):
    today = date.today()
    relatorio = Relatorio.objects.get(pk = pk)
    filtros = {}
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
    t = TurmaFrequencia.objects.get(pk=turma)
    if t.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    for p in pessoas:
        t.participantes.add(p)
        t.save()
    return redirect('turma',pk=turma)

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def add_pessoa_turma(request,pk,pessoa):
    turma = TurmaFrequencia.objects.get(pk=pk)
    if turma.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    p = Pessoa.objects.get(pk=pessoa)
    turma.participantes.add(p)
    turma.save()
    return redirect('turma',pk=pk)

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def add_lider_turma(request,pk,lider):
    turma = TurmaFrequencia.objects.get(pk=pk)
    if turma.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    p = Pessoa.objects.get(pk=lider)
    turma.lideranca.add(p)
    turma.save()
    return redirect('turma',pk=pk)

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def selecionar_participante(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    if turma.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii')
    return render(request, 'selecionar_participante.html',{'pessoas':pessoas,'turma':turma})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def selecionar_lider(request,pk):
    turma = TurmaFrequencia.objects.get(pk=pk)
    if turma.restrito and not request.user.has_perm('rol.add_ata'):
        return HttpResponse('TURMA RESTRITA AO CONSELHO')
    pessoas = Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii')
    return render(request, 'selecionar_lider.html',{'pessoas':pessoas,'turma':turma})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def frequencia(request):
    return render(request, 'frequencias.html')

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def freq_culto(request, turno):
    if turno == 'matutino':
        turma_culto = TurmaFrequencia.objects.get(pk = 1)#matutino
        turma_bercario = TurmaFrequencia.objects.get(pk = 2)#matutino
    elif turno == 'noturno': #noturno
        turma_culto = TurmaFrequencia.objects.get(pk = 3)#noturno
        turma_bercario = TurmaFrequencia.objects.get(pk = 4)#noturno


    if request.method == 'POST':
        form = FreqCultoForm(request.POST)
        if form.is_valid():
            culto = form.cleaned_data['culto']
            bercario = form.cleaned_data['bercario']
            data = form.cleaned_data['data']

            contado = Frequencia.objects.filter(data=data,turma=turma_culto).count()
            if(contado):
                the_action_flag = CHANGE
                f_culto = Frequencia.objects.get(data=data,turma=turma_culto)
                f_bercario = Frequencia.objects.get(data=data,turma=turma_bercario)
                if(culto == 0 and bercario == 0):
                    the_action_flag = DELETION
                    f_culto.delete()
                    f_bercario.delete()
                else:
                    f_culto.quantidade = culto
                    f_bercario.quantidade = bercario
                    f_culto.save()
                    f_bercario.save()
            else:
                the_action_flag = ADDITION
                f_culto = Frequencia.objects.create(turma=turma_culto,data=data,quantidade=culto)
                f_bercario = Frequencia.objects.create(turma=turma_bercario,data=data,quantidade=bercario)

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                object_id=f_culto.id,
                object_repr=str(f_culto),
                action_flag=the_action_flag)

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                object_id=f_bercario.id,
                object_repr=str(f_bercario),
                action_flag=the_action_flag)
        else:
            return HttpResponse(str(form.errors))
        return redirect('freq_culto',turno=turno)
    else:
        formdata = {'data':date.today,'culto':0,'bercario':0}
        form = FreqCultoForm(initial=formdata)
        seis_meses = datetime.now() - relativedelta(months=6)
        freq_culto = Frequencia.objects.filter(turma=turma_culto,data__gte=seis_meses).order_by('-data')
        freq = []
        for f in freq_culto:
            f.culto = f.quantidade
            f.bercario = 0
            try:
                freq_ber = Frequencia.objects.get(turma=turma_bercario,data=f.data)
                f.bercario = freq_ber.quantidade
            except:
                pass
            freq.append(f)
    return render(request, 'freq_culto.html', {'form': form, 'freq': freq, 'turno':turno})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def freq_ebd(request):
    if request.method == 'POST':
        form = FreqEbdForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data['data']
            contado = Frequencia.objects.filter(data=data,turma_id=5).count()
            if(contado): 
                the_action_flag = CHANGE
                flag_para_deletar_todas = True
                for f in form.fields:
                    if f != 'data':
                        turma = TurmaFrequencia.objects.get(pk = int(f[5:]))
                        quantidade = form.cleaned_data[f]
                        if(quantidade > 0):
                            flag_para_deletar_todas = False

                if(flag_para_deletar_todas):#testa se todas as frequencias sao ZERO, nesse caso deleta todas
                    the_action_flag = DELETION
                    for f in form.fields:
                        if f != 'data':
                            turma = TurmaFrequencia.objects.get(pk = int(f[5:]))
                            try:
                                frequencia = Frequencia.objects.get(turma=turma,data=data)
                                frequencia.delete()
                                LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                                object_id=frequencia.pk,
                                object_repr=str(frequencia),
                                action_flag=the_action_flag)
                            except:
                                pass
                else:#editando frequencias existentes
                    for f in form.fields:
                        if f != 'data':
                            turma = TurmaFrequencia.objects.get(pk = int(f[5:]))
                            quantidade = form.cleaned_data[f]
                            frequencia = Frequencia.objects.get(turma=turma,data=data)
                            frequencia.quantidade = quantidade
                            frequencia.save()

                            LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                                object_id=frequencia.pk,
                                object_repr=str(frequencia),
                                action_flag=the_action_flag)

            else: #criando nova frequencia
                the_action_flag = ADDITION
                for f in form.fields:
                    if f != 'data':
                        turma = TurmaFrequencia.objects.get(pk = int(f[5:]))
                        quantidade = form.cleaned_data[f]
                        frequencia = Frequencia.objects.create(turma=turma,data=data,quantidade=quantidade)

                        LogEntry.objects.log_action(
                            user_id=request.user.id,
                            content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                            object_id=frequencia.pk,
                            object_repr=str(frequencia),
                            action_flag=the_action_flag)
        else:
            return HttpResponse(str(form.errors))
        return redirect('freq_ebd')
    else:
        form = FreqEbdForm()
        turmas = TurmaFrequencia.objects.filter(tipo = 'ebd').filter( dt_inicio__lte=date.today()).exclude(dt_fim__lte=date.today()).order_by('-id')
        domingos = Frequencia.objects.distinct().filter(turma_id = 5).order_by('-data')
        for d in domingos:
            frequencias = []
            for t in turmas:
                try:
                    frequencias.append(Frequencia.objects.get(data = d.data, turma = t))
                except:
                    frequencias.append([]);
            d.frequencias = frequencias
        return render(request, 'freq_ebd.html', {'form': form, 'domingos': domingos, 'turmas':turmas,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def freq_turma(request,pk):
    turma = TurmaFrequencia.objects.get(pk = pk)
    if request.method == 'POST':
        form = FreqTurmaForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            data = form.cleaned_data['data']
            contado = Frequencia.objects.filter(data=data,turma=turma).count()
            if(contado):
                frequencia = Frequencia.objects.get(turma=turma,data=data)
                if(quantidade == 0):
                    the_action_flag = DELETION
                    frequencia.delete()
                else:
                    the_action_flag = CHANGE
                    frequencia.quantidade = quantidade
                    frequencia.save()
            else:
                the_action_flag = ADDITION
                frequencia = Frequencia.objects.create(turma=turma,data=data,quantidade=quantidade)
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Frequencia).pk,
                object_id=frequencia.id,
                object_repr=str(frequencia),
                action_flag=the_action_flag)
        else:
            return HttpResponse(str(form.errors))
        return redirect('freq_turma',pk=pk)
    else:
        form = FreqTurmaForm()
        seis_meses = datetime.now() - relativedelta(months=6)
        freq = Frequencia.objects.filter(turma=turma,data__gte=seis_meses).order_by('-data')
    return render(request, 'freq_turma.html', {'form': form, 'freq': freq, 'turma':turma})
