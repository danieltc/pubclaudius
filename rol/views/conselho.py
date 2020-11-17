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

from rol.models import Igreja, Rol, Categoria, Pessoa, Contato, TipoContato, Ata, AtoOficial, Membro, TipoAto, TurmaFrequencia, Frequencia
from rol.forms import IgrejaForm, PessoaForm, PresbPessoaForm, AtaForm, AtoOficialForm, AdmitirForm, DemitirForm, FreqCultoForm, PresbiterioForm

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def new_igreja(request):
    if request.method == 'POST':
        form = IgrejaForm(request.POST)
        if form.is_valid():

            igreja = form.save(commit=False)
            igreja.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Igreja).pk,
                object_id=igreja.id,
                object_repr=str(igreja.nome),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))

        return redirect('igrejas')
    else:
        form = IgrejaForm()
    return render(request, 'new_igreja.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def edit_igreja(request,pk):
    igreja = Igreja.objects.get(id=pk)
    formdata = {}
    if request.method == 'POST':
        form = IgrejaForm(request.POST,instance=igreja)
        if form.is_valid():
            igreja = form.save(commit=False)
            igreja.save()
            
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Igreja).pk,
                object_id=igreja.id,
                object_repr=str(igreja.nome),
                action_flag=CHANGE)
        else:
            return HttpResponse(str(form.errors))
        return redirect('igrejas')
    else:
        form = IgrejaForm(instance=igreja)
    return render(request, 'edit_igreja.html', {'form': form, 'igreja': igreja,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def igrejas(request):
    igrejas = Igreja.objects.all()
    return render(request, 'igrejas.html', {'igrejas': igrejas})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def new_ata(request):
    if request.method == 'POST':
        form = AtaForm(request.POST)
        if form.is_valid():

            ata = form.save(commit=False)
            ata.identificacao = "Conselho"+str(ata.numero).zfill(3)
            ata.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Ata).pk,
                object_id=ata.id,
                object_repr=str(ata.identificacao),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))

        return redirect('ata', pk = ata.id)
    else:
        formdata = {'numero':(Ata.objects.latest('numero').numero+1), 'data':date.today()}
        form = AtaForm(initial=formdata)
    return render(request, 'new_ata.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def ata(request, pk):
    ata = Ata.objects.get(pk=pk)
    atos = AtoOficial.objects.filter(ata_ato_id=pk).order_by('tipo_ato','pessoa__nome','data')
    for ato in atos:
        try:
            membro = Membro.objects.exclude(invalido=True).get(pessoa=ato.pessoa)
            ato.matricula = membro.matricula
        except:
            pass
    return render(request, 'ata.html', {'ata': ata, 'atos': atos})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def atas(request):
    atas = Ata.objects.all().order_by('-data')
    for a in atas:
        try:
            a.atos = AtoOficial.objects.filter(ata_ato=a).count
        except:
            pass
    return render(request, 'atas.html', {'atas': atas})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def ato(request, pk):
    ato = AtoOficial.objects.get(pk=pk)
    return render(request, 'ato.html', {'ato': ato})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def new_ato(request, pk):
    ata = AtoOficial.objects.get(pk=pk)
    return render(request, 'new_ato.html', {'ata': ata})
    if request.method == 'POST':
        form = AtaForm(request.POST)
        if form.is_valid():
            ata = form.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Ata).pk,
                object_id=ata.id,
                object_repr=str(ata.identificacao),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))

        return redirect('ata', pk = ata.id)
    else:
        form = AtaForm()
    return render(request, 'new_ata.html', {'form': form})

    return render(request, 'atas.html', {'pessoas': pessoas})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def new_ato(request,pk):
    ata = Ata.objects.get(pk=pk)
    if request.method == 'POST':
        form = AtoOficialForm(request.POST)
        if form.is_valid():
            ato = form.save(commit=False)
            ato.ata_ato_id = ata.id
            ato.save()
            pessoa = ato.pessoa
            # verifica se o ato precisa alterar a categoria da pessoa em questão.
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(AtoOficial).pk,
                object_id=ato.id,
                object_repr=str(ato),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))

        return redirect('ato', pk = ato.id)
    else:
        formdata = {'data':ata.data.strftime('%d/%m/%Y')}
        form = AtoOficialForm(initial=formdata)
    return render(request, 'new_ato.html', {'form': form, 'ata':ata})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def admitir(request):
    if request.method == 'POST':
        form = AdmitirForm(request.POST)
        if form.is_valid():
            pessoa = form.cleaned_data['pessoa']
            ata_admissao = form.cleaned_data['ata_admissao']
            forma_admissao = form.cleaned_data['forma_admissao']
            membro = form.save(commit=False)
            membro.data_admissao = ata_admissao.data
            membro.save()
            if forma_admissao.id in [8,9,10]:
                tipo_ato_oficial = TipoAto.objects.get(pk=2) #membro não-comungante
                nova_categoria = Categoria.objects.get(pk=24) #membro não-comungante
            else:
                tipo_ato_oficial = TipoAto.objects.get(pk=1) #membro
                nova_categoria = Categoria.objects.get(pk=1) #membro

            tupla = AtoOficial.objects.get_or_create(pessoa = pessoa, ata_ato=ata_admissao, tipo_ato=tipo_ato_oficial, data=ata_admissao.data)
            pessoa.categoria = nova_categoria
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Membro).pk,
                object_id=membro.id,
                object_repr=str(membro),
                action_flag=ADDITION)
        else:
            return HttpResponse(str(form.errors))
        return redirect('pessoa', pk = membro.pessoa.id)
    else:
        formdata = {'matricula':Membro.objects.latest('matricula').matricula+1}
        form = AdmitirForm(initial=formdata)

    return render(request, 'admitir.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_ata'))
def demitir(request):
    if request.method == 'POST':
        try:
            membro = Membro.objects.exclude(invalido=True).get(pessoa_id = request.POST.get('pessoa'))
        except:
            return HttpResponse("Pessoa inexistente.")
        form = DemitirForm(request.POST,instance=membro)
        if form.is_valid():
            pessoa = form.cleaned_data['pessoa']
            ata_demissao = form.cleaned_data['ata_demissao']
            dados_demissao = form.cleaned_data['dados_demissao']
            forma_demissao = form.cleaned_data['forma_demissao']
            membro = form.save(commit=False)
            membro.data_demissao = ata_demissao.data
            membro.save()
            if forma_demissao.id in [7,8,9,10,11,12]:
                tipo_ato_oficial = TipoAto.objects.get(pk=27) #demissao membro não-comungante
            else:
                tipo_ato_oficial = TipoAto.objects.get(pk=5) #demissao membro
            nova_categoria = Categoria.objects.get(pk=52) #ex-membro
            tupla = AtoOficial.objects.get_or_create(pessoa = pessoa, ata_ato=ata_demissao, tipo_ato=tipo_ato_oficial, data=ata_demissao.data)
            pessoa.categoria = nova_categoria
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Membro).pk,
                object_id=membro.id,
                object_repr=str(membro),
                action_flag=CHANGE)
        else:
            return HttpResponse(str(form.errors))
        return redirect('pessoa', pk = membro.pessoa.id)
    else:
        form = DemitirForm()

    return render(request, 'demitir.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def presbiterio(request):
    solicitado = False


    admissoes_comungante_f = 0
    admissoes_comungante_m = 0
    admissoes_comungante_t = 0
    admissoes_nao_comungante_f = 0
    admissoes_nao_comungante_m = 0
    admissoes_nao_comungante_t = 0

    admissoes_total = 0


    demissoes_comungante_f = 0
    demissoes_comungante_m = 0
    demissoes_comungante_t = 0
    demissoes_nao_comungante_f = 0
    demissoes_nao_comungante_m = 0
    demissoes_nao_comungante_t = 0

    demissoes_total = 0


    #admissoes - comungante - feminino
    acf_profissao_fe = 0
    acf_profissao_fe_batismo = 0
    acf_transferencia = 0
    acf_jurisdicao = 0
    acf_restauracao = 0
    acf_designacao = 0
    #admissoes - comungante - masculino
    acm_profissao_fe = 0
    acm_profissao_fe_batismo = 0
    acm_transferencia = 0
    acm_jurisdicao = 0
    acm_restauracao = 0
    acm_designacao = 0

    #admissoes - nao comungante - feminino
    ancf_batismo = 0
    ancf_transferencia = 0
    ancf_jurisdicao = 0
    #admissoes - nao comungante - masculino
    ancm_batismo = 0
    ancm_transferencia = 0
    ancm_jurisdicao = 0

    #demissoes - comungante - feminino
    dcf_transferencia = 0
    dcf_falecimento = 0
    dcf_exclusao = 0
    dcf_ordenacao = 0
    #demissoes - comungante - masculino
    dcm_transferencia = 0
    dcm_falecimento = 0
    dcm_exclusao = 0
    dcm_ordenacao = 0

    #demissoes - nao comungante - feminino
    dncf_profissao_fe = 0
    dncf_transferencia = 0
    dncf_falecimento = 0
    dncf_exclusao = 0

    #demissoes - nao comungante - masculino
    dncm_profissao_fe = 0
    dncm_transferencia = 0
    dncm_falecimento = 0
    dncm_exclusao = 0

    #geral - comungante - feminino
    gcf_rol_separado = 0
    gcf_admissao_menos_demissao = 0
    gcf_ano_anterior = 0
    gcf_ano_atual = 0
    #geral - comungante - masculino
    gcm_rol_separado = 0
    gcm_admissao_menos_demissao = 0
    gcm_ano_anterior = 0
    gcm_ano_atual = 0

    #geral - nao comungante - feminino
    gncf_rol_separado = 0
    gncf_admissao_menos_demissao = 0
    gncf_ano_anterior = 0
    gncf_ano_atual = 0


    #geral - nao comungante - masculino
    gncm_rol_separado = 0
    gncm_admissao_menos_demissao = 0
    gncm_ano_anterior = 0
    gncm_ano_atual = 0

    data_inicio = "-"
    data_fim = "-"
    if request.method == 'POST':
        solicitado = True
        form = PresbiterioForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            data_inicio_ano_anterior = data_inicio - relativedelta(years=1)
            data_fim_ano_anterior = data_fim - relativedelta(years=1)


            admissoes_comungante_f = AtoOficial.objects.filter(tipo_ato_id = 1,ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='F').count()
            admissoes_comungante_m = AtoOficial.objects.filter(tipo_ato_id = 1, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='M').count()
            admissoes_nao_comungante_f = AtoOficial.objects.filter(tipo_ato_id = 2, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='F').count()
            admissoes_nao_comungante_m = AtoOficial.objects.filter(tipo_ato_id = 2, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='M').count()

            demissoes_comungante_f = AtoOficial.objects.filter(tipo_ato_id = 5, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='F').count()
            demissoes_comungante_m = AtoOficial.objects.filter(tipo_ato_id = 5, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='M').count()
            demissoes_nao_comungante_f = AtoOficial.objects.filter(tipo_ato_id = 27, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='F').count()
            demissoes_nao_comungante_m = AtoOficial.objects.filter(tipo_ato_id = 27, ata_ato__data__gte=data_inicio,ata_ato__data__lte=data_fim,pessoa__sexo='M').count()

            #admissoes - comungante - feminino
            acf_profissao_fe = Membro.objects.filter(forma_admissao_id = 1, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acf_profissao_fe_batismo = Membro.objects.filter(forma_admissao_id = 2, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acf_transferencia = Membro.objects.filter(forma_admissao_id = 3, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acf_jurisdicao = Membro.objects.filter(forma_admissao_id__in = [4,5], pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acf_restauracao = Membro.objects.filter(forma_admissao_id = 6, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acf_designacao = Membro.objects.filter(forma_admissao_id = 7, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            #admissoes - comungante - masculino
            acm_profissao_fe = Membro.objects.filter(forma_admissao_id = 1, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acm_profissao_fe_batismo = Membro.objects.filter(forma_admissao_id = 2, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acm_transferencia = Membro.objects.filter(forma_admissao_id = 3, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acm_jurisdicao = Membro.objects.filter(forma_admissao_id__in = [4,5], pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acm_restauracao = Membro.objects.filter(forma_admissao_id = 6, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            acm_designacao = Membro.objects.filter(forma_admissao_id = 7, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()

            #admissoes - nao comungante - feminino
            ancf_batismo = Membro.objects.filter(forma_admissao_id = 8, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            ancf_transferencia = Membro.objects.filter(forma_admissao_id = 9, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            ancf_jurisdicao = Membro.objects.filter(forma_admissao_id = 10, pessoa__sexo = 'F', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            #admissoes - nao comungante - masculino
            ancm_batismo = Membro.objects.filter(forma_admissao_id = 8, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            ancm_transferencia = Membro.objects.filter(forma_admissao_id = 9, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()
            ancm_jurisdicao = Membro.objects.filter(forma_admissao_id = 10, pessoa__sexo = 'M', data_admissao__gte = data_inicio, data_admissao__lte = data_fim).count()

            # #demissoes - comungante - feminino
            dcf_transferencia = Membro.objects.filter(forma_demissao_id__in = [4,5], pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcf_falecimento = Membro.objects.filter(forma_demissao_id = 6, pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcf_exclusao = Membro.objects.filter(forma_demissao_id__in = [1,2,3], pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcf_ordenacao = Membro.objects.filter(forma_demissao_id = 13, pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            # #demissoes - comungante - masculino
            dcm_transferencia = Membro.objects.filter(forma_demissao_id__in = [4,5], pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcm_falecimento = Membro.objects.filter(forma_demissao_id = 6, pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcm_exclusao = Membro.objects.filter(forma_demissao_id__in = [1,2,3], pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dcm_ordenacao = Membro.objects.filter(forma_demissao_id = 13, pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()

            # #demissoes - nao comungante - feminino
            dncf_profissao_fe = Membro.objects.filter(forma_demissao_id = 10, pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncf_transferencia = Membro.objects.filter(forma_demissao_id__in = [7], pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncf_falecimento = Membro.objects.filter(forma_demissao_id = 12, pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncf_exclusao = Membro.objects.filter(forma_demissao_id__in = [9,11], pessoa__sexo = 'F', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()

            # #demissoes - nao comungante - masculino
            dncm_profissao_fe = Membro.objects.filter(forma_demissao_id = 10, pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncm_transferencia = Membro.objects.filter(forma_demissao_id__in = [7], pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncm_falecimento = Membro.objects.filter(forma_demissao_id = 12, pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()
            dncm_exclusao = Membro.objects.filter(forma_demissao_id__in = [9,11], pessoa__sexo = 'M', data_demissao__gte = data_inicio, data_demissao__lte = data_fim).count()

            #geral - comungante - feminino
            gcf_rol_separado = 0
            gcf_admissao_menos_demissao = (acf_profissao_fe+acf_profissao_fe_batismo+acf_transferencia+acf_jurisdicao+acf_restauracao+acf_designacao) - (dcf_transferencia+dcf_falecimento+dcf_exclusao+dcf_ordenacao)
            gcf_ano_anterior = 0#Membro.objects.filter(pessoa__sexo = 'F').exclude(data_admissao__gte=data_inicio).exclude(data_demissao__gte=data_inicio_ano_anterior,data_demissao__lte=data_fim_ano_anterior).count()
            gcf_ano_atual = 0#Membro.objects.filter(pessoa__sexo = 'F').exclude(data_demissao__isnull=False).count()
            #geral - comungante - masculino
            gcm_rol_separado = 0
            gcm_admissao_menos_demissao = (acm_profissao_fe+acm_profissao_fe_batismo+acm_transferencia+acm_jurisdicao+acm_restauracao+acm_designacao) - (dcm_transferencia+dcm_falecimento+dcm_exclusao+dcm_ordenacao)
            gcm_ano_anterior = 0#Membro.objects.filter(pessoa__sexo = 'M').exclude(data_admissao__gte=data_inicio).exclude(data_demissao__gte=data_inicio_ano_anterior,data_demissao__lte=data_fim_ano_anterior).count()
            gcm_ano_atual = 0#Membro.objects.filter(pessoa__sexo = 'M').exclude(data_demissao__isnull=False).count()

            #geral - nao comungante - feminino
            gncf_rol_separado = 0
            gncf_admissao_menos_demissao = (ancf_batismo+ancf_transferencia+ancf_jurisdicao)-(dncf_profissao_fe+dncf_transferencia+dncf_falecimento+dncf_exclusao)
            gncf_ano_anterior = 0
            gncf_ano_atual = 0


            #geral - nao comungante - masculino
            gncm_rol_separado = 0
            gncm_admissao_menos_demissao = (ancm_batismo+ancm_transferencia+ancm_jurisdicao)-(dncm_profissao_fe+dncm_transferencia+dncm_falecimento+dncm_exclusao)
            gncm_ano_anterior = 0
            gncm_ano_atual = 0

    else:
        form = PresbiterioForm()

    return render(request, 'presbiterio.html', {
        'form': form,
        'data_inicio': data_inicio,
        'data_fim':data_fim,

        'admissoes_comungante_f':admissoes_comungante_f,
        'admissoes_comungante_m':admissoes_comungante_m,
        'admissoes_comungante_t':admissoes_comungante_f+admissoes_comungante_m,
        'admissoes_nao_comungante_f':admissoes_nao_comungante_f,
        'admissoes_nao_comungante_m':admissoes_nao_comungante_m,
        'admissoes_nao_comungante_t':admissoes_nao_comungante_f+admissoes_nao_comungante_m,
        'admissoes_total':admissoes_comungante_f+admissoes_comungante_m+admissoes_nao_comungante_f+admissoes_nao_comungante_m,

        'demissoes_comungante_f':demissoes_comungante_f,
        'demissoes_comungante_m':demissoes_comungante_m,
        'demissoes_comungante_t':demissoes_comungante_f+demissoes_comungante_m,
        'demissoes_nao_comungante_f':demissoes_nao_comungante_f,
        'demissoes_nao_comungante_m':demissoes_nao_comungante_m,
        'demissoes_nao_comungante_t':demissoes_nao_comungante_f+demissoes_nao_comungante_m,
        'demissoes_total':demissoes_comungante_f+demissoes_comungante_m+demissoes_nao_comungante_f+demissoes_nao_comungante_m,



        'solicitado':solicitado,
        'acf_profissao_fe':acf_profissao_fe,
        'act_profissao_fe':acf_profissao_fe+acm_profissao_fe,
        'acf_profissao_fe_batismo':acf_profissao_fe_batismo,
        'act_profissao_fe_batismo':acf_profissao_fe_batismo+acm_profissao_fe_batismo,
        'acf_transferencia':acf_transferencia,
        'act_transferencia':acf_transferencia+acm_transferencia,
        'acf_jurisdicao':acf_jurisdicao,
        'act_jurisdicao':acf_jurisdicao+acm_jurisdicao,
        'acf_restauracao':acf_restauracao,
        'act_restauracao':acf_restauracao+acm_restauracao,
        'acf_designacao':acf_designacao,
        'act_designacao':acf_designacao+acm_designacao,
        'acm_profissao_fe':acm_profissao_fe,
        'acm_profissao_fe_batismo':acm_profissao_fe_batismo,
        'acm_transferencia':acm_transferencia,
        'acm_jurisdicao':acm_jurisdicao,
        'acm_restauracao':acm_restauracao,
        'acm_designacao':acm_designacao,
        'ancf_batismo':ancf_batismo,
        'anct_batismo':ancf_batismo+ancm_batismo,
        'ancf_transferencia':ancf_transferencia,
        'anct_transferencia':ancf_transferencia+ancm_transferencia,
        'ancf_jurisdicao':ancf_jurisdicao,
        'anct_jurisdicao':ancf_jurisdicao+ancm_jurisdicao,
        'ancm_batismo':ancm_batismo,
        'ancm_transferencia':ancm_transferencia,
        'ancm_jurisdicao':ancm_jurisdicao,
        'dcf_transferencia':dcf_transferencia,
        'dct_transferencia':dcf_transferencia+dcm_transferencia,
        'dcf_falecimento':dcf_falecimento,
        'dct_falecimento':dcf_falecimento+dcm_falecimento,
        'dcf_exclusao':dcf_exclusao,
        'dct_exclusao':dcf_exclusao+dcm_exclusao,
        'dcm_transferencia':dcm_transferencia,
        'dcm_falecimento':dcm_falecimento,
        'dcm_exclusao':dcm_exclusao,
        'dcm_ordenacao':dcm_ordenacao,
        'dncf_profissao_fe':dncf_profissao_fe,
        'dnct_profissao_fe':dncf_profissao_fe+dncm_profissao_fe,
        'dncf_transferencia':dncf_transferencia,
        'dnct_transferencia':dncf_transferencia+dncm_transferencia,
        'dncf_falecimento':dncf_falecimento,
        'dnct_falecimento':dncf_falecimento+dncm_falecimento,
        'dncf_exclusao':dncf_exclusao,
        'dnct_exclusao':dncf_exclusao+dncm_exclusao,
        'dncm_profissao_fe':dncm_profissao_fe,
        'dncm_transferencia':dncm_transferencia,
        'dncm_falecimento':dncm_falecimento,
        'dncm_exclusao':dncm_exclusao,
        'gcf_rol_separado':gcf_rol_separado,
        'gct_rol_separado':gcf_rol_separado+gcm_rol_separado,
        'gcf_admissao_menos_demissao':gcf_admissao_menos_demissao,
        'gct_admissao_menos_demissao':gcf_admissao_menos_demissao+gcm_admissao_menos_demissao,
        'gcf_comungantes_menos_ano_anterior':gcf_ano_anterior,
        'gct_comungantes_menos_ano_anterior':gcf_ano_anterior+gcm_ano_anterior,
        'gcf_comungantes_menos_ano_atual':gcf_ano_atual,
        'gct_comungantes_menos_ano_atual':gcf_ano_atual+gcf_ano_atual,
        'gcm_rol_separado':gcm_rol_separado,
        'gcm_admissao_menos_demissao':gcm_admissao_menos_demissao,
        'gcm_comungantes_menos_ano_anterior':gcm_ano_anterior,
        'gcm_comungantes_menos_ano_atual':gcm_ano_atual,
        'gncf_rol_separado':gncf_rol_separado,
        'gnct_rol_separado':gncf_rol_separado+gncf_rol_separado,
        'gncf_admissao_menos_demissao':gncf_admissao_menos_demissao,
        'gnct_admissao_menos_demissao':gncf_admissao_menos_demissao+gncm_admissao_menos_demissao,
        'gncf_comungantes_menos_ano_anterior':gncf_ano_anterior,
        'gnct_comungantes_menos_ano_anterior':gncf_ano_anterior+gncm_ano_anterior,
        'gncf_comungantes_menos_ano_atual':gncf_ano_atual,
        'gnct_comungantes_menos_ano_atual':gncf_ano_atual+gncm_ano_atual,
        'gncm_rol_separado':gncm_rol_separado,
        'gncm_admissao_menos_demissao':gncm_admissao_menos_demissao,
        'gncm_comungantes_menos_ano_anterior':gncm_ano_anterior,
        'gncm_comungantes_menos_ano_atual':gncm_ano_atual,
        })

