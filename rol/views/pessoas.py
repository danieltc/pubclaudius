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

from rol.models import Rol, TipoGrupo, Categoria, Pessoa, Contato, TipoContato, Ata, AtoOficial, Membro, TipoAto, TurmaFrequencia, Frequencia
from rol.forms import PessoaSimplesForm, PessoaForm, PresbPessoaForm, AtaForm, AtoOficialForm, AdmitirForm, DemitirForm, FreqCultoForm

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def lista_rol(request):
    membros = Membro.objects.all().order_by('-matricula')
    return render(request, 'lista_rol.html', {'pessoas': membros })

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def pessoas(request):
    pessoas = Pessoa.objects.exclude(categoria_id__in=[15,]).order_by('categoria','nome')
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'categorias':"Todas as Pessoas"})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def pessoas_membros(request):
    pessoas = Pessoa.objects.exclude(categoria = None).exclude(categoria_id__in=[15,5,7,48,50,52,67,12]).order_by('categoria','nome')
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'categorias':"Membros, Pastores e Admitendos"})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def pessoas_visitantes(request):
    pessoas = Pessoa.objects.exclude(categoria = None).exclude(categoria_id__in=[15,1,9,20,24,25,37,38,39,40,42,44,45,46,47,49,51,52,54,58,59,60,61,62,63,64,65,66,68,69,70]).order_by('-categoria','nome')
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'categorias':"Visitantes"})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def pessoas_outros(request):
    pessoas = Pessoa.objects.exclude(categoria_id__in=[12,5,7,48,50,67,15,1,9,20,24,25,37,38,39,40,42,44,45,46,47,49,51,54,58,59,60,61,62,63,64,65,66,68,69,70]).order_by('categoria','nome')
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'categorias':"Recém-cadastrados, ex-membros e outras pessoas"})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def new_pessoa(request):
    tipos_contato = TipoContato.objects.all()

    formdata = {}

    for t in tipos_contato:
        formdata.update({t.desc_sistema:''})

    if request.method == 'POST':
        
        form = PessoaSimplesForm(request.POST,request.FILES)
    
        if form.is_valid():
            pessoa = form.save(commit=False)
            if form.cleaned_data['pai'] is None and form.cleaned_data['inserir_novo_pai'].strip() is not '':
                pai = Pessoa()
                pai.nome = form.cleaned_data['inserir_novo_pai']
                pai.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', pai.nome) if unicodedata.category(c) != 'Mn'))
                pai.rol = pessoa.rol
                pai.sexo = 'M'
                pai.tem_filhos = True
                pai.user_update = request.user
                pai.data_update = date.today()
                pai.save()
                pessoa.pai = pai
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                    object_id=pai.id,
                    object_repr=str(pai.nome),
                    action_flag=ADDITION)
            if form.cleaned_data['mae'] is None and form.cleaned_data['inserir_nova_mae'].strip() is not '':
                mae = Pessoa()
                mae.nome = form.cleaned_data['inserir_nova_mae']
                mae.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', mae.nome) if unicodedata.category(c) != 'Mn'))
                mae.rol = pessoa.rol
                mae.sexo = 'F'
                mae.tem_filhos = True
                mae.user_update = request.user
                mae.data_update = date.today()
                mae.save()
                pessoa.mae = mae
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                    object_id=mae.id,
                    object_repr=str(mae.nome),
                    action_flag=ADDITION)
            pessoa.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', pessoa.nome) if unicodedata.category(c) != 'Mn'))
            pessoa.user_update = request.user
            pessoa.data_update = date.today()
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                object_id=pessoa.id,
                object_repr=str(pessoa.nome),
                action_flag=ADDITION)
            for t in tipos_contato:
                try:
                    if form.cleaned_data[t.desc_sistema] != '':
                        c = Contato.objects.create(tipo_id = t.id, pessoa_id = pessoa.id, conteudo=form.cleaned_data[t.desc_sistema])
                        # LogEntry.objects.log_action(
                        #     user_id=request.user.id,
                        #     content_type_id=ContentType.objects.get_for_model(Contato).pk,
                        #     object_id=pessoa_contato.id,
                        #     object_repr=str(pessoa.nome + '-' + c.tipo.desc_sistema),
                        #     action_flag=ADDITION)
                except:
                    pass
        else:
            return HttpResponse(str(form.errors))
        return redirect('pessoa', pk = pessoa.id)
    else:
        form = PessoaSimplesForm()
    return render(request, 'new_pessoa.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def edit_pessoa(request, pk):
    pessoa = Pessoa.objects.get(id=pk)
    contatos = list(Contato.objects.filter(pessoa=pk))
    tipos_contato = TipoContato.objects.all()
    formdata = {}
    for t in tipos_contato:
        try:
            pessoa_contato = Contato.objects.get(tipo=t.id, pessoa_id=pessoa.id)
            formdata.update({pessoa_contato.tipo.desc_sistema:pessoa_contato.conteudo})
        except:
            formdata.update({t.desc_sistema:''})
    if request.method == 'POST':
        if request.user.has_perm('rol.add_ata'):
            form = PresbPessoaForm(request.POST,request.FILES,instance=pessoa)
        else:
            form = PessoaForm(request.POST,request.FILES,instance=pessoa)
        if form.is_valid():
            pessoa = form.save(commit=False)
            pessoa.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', pessoa.nome) if unicodedata.category(c) != 'Mn'))
            pessoa.user_update = request.user
            pessoa.data_update = date.today()
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                object_id=pessoa.id,
                object_repr=str(pessoa.nome),
                action_flag=CHANGE)

            for t in tipos_contato:
                try:
                    pessoa_contato = Contato.objects.get(tipo=t.id, pessoa_id=pessoa.id)
                    pessoa_contato.conteudo = form.cleaned_data[t.desc_sistema]
                    pessoa_contato.save()
                except:
                    if form.cleaned_data[t.desc_sistema] != '':
                        c = Contato.objects.create(tipo_id = t.id, pessoa_id = pessoa.id, conteudo=form.cleaned_data[t.desc_sistema])
            #distribuindo contatos do chefe de familia
            if pessoa.chefe_familia:
                if pessoa.chefe_familia.id == pessoa.id:
                    erros = ""
                    familia = Pessoa.objects.filter(chefe_familia_id=pessoa.id).exclude(pk=pessoa.id)

                    default_endereco,c1 = Contato.objects.get_or_create(tipo_id=6, pessoa_id=pessoa.id)
                    de = {'conteudo':default_endereco.conteudo}
                    default_telefone,c2 = Contato.objects.get_or_create(tipo_id=12, pessoa_id=pessoa.id)
                    dt = {'conteudo':default_telefone.conteudo}
                    default_cidadeestado,c3 = Contato.objects.get_or_create(tipo_id=7, pessoa_id=pessoa.id)
                    dce = {'conteudo':default_cidadeestado.conteudo}
                    default_cep,c4 = Contato.objects.get_or_create(tipo_id=8, pessoa_id=pessoa.id)
                    dc = {'conteudo':default_cep.conteudo}

                    for p in familia:
                        try:
                            p_endereco, end_criado = Contato.objects.update_or_create(tipo_id=6, pessoa_id=p.id, defaults=de)
                        except:
                            erros += "endereco pessoa "+str(p)+", "

                        try:
                            p_telefone, telef_criado = Contato.objects.update_or_create(tipo_id=12, pessoa_id=p.id, defaults=dt)
                        except:
                            erros += "telefone pessoa "+str(p)+", "

                        try:
                            p_cidadeestado, cidest_criado = Contato.objects.update_or_create(tipo_id=7, pessoa_id=p.id, defaults=dce)
                        except:
                            erros += "cidadeestado pessoa "+str(p)+", "

                        try:
                            p_cep, cep_criado = Contato.objects.update_or_create(tipo_id=8, pessoa_id=p.id, defaults=dc)
                        except:
                            erros += "cep pessoa "+str(p)+", "

                        try:
                            pessoa.user_update = request.user
                            pessoa.data_update = date.today
                        except:
                            pass

                    if erros != "":
                        return HttpResponse(erros)
        else:
            return HttpResponse(str(form.errors))

        return redirect('pessoa', pk = pessoa.id)
    else:
        if request.user.has_perm('rol.add_ata'):
            form = PresbPessoaForm(initial=formdata,instance=pessoa)
        else:
            form = PessoaForm(initial=formdata,instance=pessoa)
    return render(request, 'edit_pessoa.html', {'form': form, 'pessoa': pessoa,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def simple_edit_pessoa(request, pk):
    pessoa = Pessoa.objects.get(id=pk)
    contatos = list(Contato.objects.filter(pessoa=pk))
    arr_contatos_basicos = ['email','celular','endereco','cidade_estado','cep']
    # arr_contatos_basicos = ['endereco','cidade_estado','cep']
    tipos_contato = TipoContato.objects.filter(desc_sistema__in=arr_contatos_basicos)
    # tipos_contato = TipoContato.objects.all()
    formdata = {}
    for t in tipos_contato:
        try:
            pessoa_contato = Contato.objects.get(tipo=t.id, pessoa_id=pessoa.id)
            formdata.update({pessoa_contato.tipo.desc_sistema:pessoa_contato.conteudo})
        except:
            formdata.update({t.desc_sistema:''})
    if request.method == 'POST':
        form = PessoaSimplesForm(request.POST,request.FILES,instance=pessoa)
        if form.is_valid():
            pessoa = form.save(commit=False)
            if form.cleaned_data['pai'] is None and form.cleaned_data['inserir_novo_pai'].strip() is not '':
                pai = Pessoa()
                pai.nome = form.cleaned_data['inserir_novo_pai']
                pai.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', pai.nome) if unicodedata.category(c) != 'Mn'))
                pai.rol = pessoa.rol
                pai.sexo = 'M'
                pai.tem_filhos = True
                pai.user_update = request.user
                pai.data_update = date.today()
                pai.save()
                pessoa.pai = pai
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                    object_id=pai.id,
                    object_repr=str(pai.nome),
                    action_flag=ADDITION)
            if form.cleaned_data['mae'] is None and form.cleaned_data['inserir_nova_mae'].strip() is not '':
                mae = Pessoa()
                mae.nome = form.cleaned_data['inserir_nova_mae']
                mae.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', mae.nome) if unicodedata.category(c) != 'Mn'))
                mae.rol = pessoa.rol
                mae.sexo = 'F'
                mae.tem_filhos = True
                mae.user_update = request.user
                mae.data_update = date.today()
                mae.save()
                pessoa.mae = mae
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                    object_id=mae.id,
                    object_repr=str(mae.nome),
                    action_flag=ADDITION)

            pessoa.nome_ascii = ''.join((c for c in unicodedata.normalize('NFD', pessoa.nome) if unicodedata.category(c) != 'Mn'))
            pessoa.user_update = request.user
            pessoa.data_update = date.today()
            pessoa.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Pessoa).pk,
                object_id=pessoa.id,
                object_repr=str(pessoa.nome),
                action_flag=CHANGE)

            for t in tipos_contato:
                try:
                    pessoa_contato = Contato.objects.get(tipo=t.id, pessoa_id=pessoa.id)
                    pessoa_contato.conteudo = form.cleaned_data[t.desc_sistema]
                    pessoa_contato.save()
                except:
                    if form.cleaned_data[t.desc_sistema] != '':
                        c = Contato.objects.create(tipo_id = t.id, pessoa_id = pessoa.id, conteudo=form.cleaned_data[t.desc_sistema])
                    pass
            #distribuindo contatos do chefe de familia
            if pessoa.chefe_familia:
                if pessoa.chefe_familia.id == pessoa.id:
                    erros = ""
                    familia = Pessoa.objects.filter(chefe_familia_id=pessoa.id).exclude(pk=pessoa.id)

                    default_endereco,c1 = Contato.objects.get_or_create(tipo_id=6, pessoa_id=pessoa.id)
                    de = {'conteudo':default_endereco.conteudo}
                    default_telefone,c2 = Contato.objects.get_or_create(tipo_id=12, pessoa_id=pessoa.id)
                    dt = {'conteudo':default_telefone.conteudo}
                    default_cidadeestado,c3 = Contato.objects.get_or_create(tipo_id=7, pessoa_id=pessoa.id)
                    dce = {'conteudo':default_cidadeestado.conteudo}
                    default_cep,c4 = Contato.objects.get_or_create(tipo_id=8, pessoa_id=pessoa.id)
                    dc = {'conteudo':default_cep.conteudo}

                    for p in familia:
                        try:
                            p_endereco, end_criado = Contato.objects.update_or_create(tipo_id=6, pessoa_id=p.id, defaults=de)
                        except:
                            erros += "endereco pessoa "+str(p)+", "

                        try:
                            p_telefone, telef_criado = Contato.objects.update_or_create(tipo_id=12, pessoa_id=p.id, defaults=dt)
                        except:
                            erros += "telefone pessoa "+str(p)+", "

                        try:
                            p_cidadeestado, cidest_criado = Contato.objects.update_or_create(tipo_id=7, pessoa_id=p.id, defaults=dce)
                        except:
                            erros += "cidadeestado pessoa "+str(p)+", "

                        try:
                            p_cep, cep_criado = Contato.objects.update_or_create(tipo_id=8, pessoa_id=p.id, defaults=dc)
                        except:
                            erros += "cep pessoa "+str(p)+", "

                        try:
                            pessoa.user_update = request.user
                            pessoa.data_update = date.today
                        except:
                            pass

                    if erros != "":
                        return HttpResponse(erros)
        else:
            return HttpResponse(str(form.errors))

        return redirect('pessoa', pk = pessoa.id)
    else:
        form = PessoaSimplesForm(initial=formdata,instance=pessoa)
    return render(request, 'simple_edit_pessoa.html', {'form': form, 'pessoa': pessoa,})

@login_required
@user_passes_test(lambda u: u.has_perm('rol.add_pessoa'))
def pessoa(request, pk):
    detalhes = get_object_or_404(Pessoa, pk=pk)
    contatos = detalhes.contato_set.all()
    if detalhes.sexo is 'F':
        artigo = 'a'
        contra_artigo = 'o'
    else:
        artigo = 'o'
        contra_artigo = 'a'

    if detalhes.estado_civil_complemento:
        if detalhes.estado_civil_complemento.id is 1: #namorando
            detalhes.estado_civil_complemento_texto = "Namorando"
            detalhes.estado_civil_complemento_pessoa = "Namorad"+contra_artigo
        elif detalhes.estado_civil_complemento.id is 2: #noivo
            detalhes.estado_civil_complemento_texto = "Noiv"+artigo
            detalhes.estado_civil_complemento_pessoa = "Noiv"+contra_artigo
    if detalhes.estado_civil:
        if detalhes.estado_civil.id is 14:
            detalhes.estado_civil_texto = detalhes.estado_civil.descricao
        else:
            detalhes.estado_civil_texto = detalhes.estado_civil.descricao[0:len(detalhes.estado_civil.descricao)-1]+artigo
    
    try:
        familia = list(Pessoa.objects.filter(chefe_familia_id=detalhes.chefe_familia_id))
    except Pessoa.DoesNotExist:
        familia = None
    try:
        today = date.today()
        idade = today.year - detalhes.data_nascimento.year - ((today.month, detalhes.data_nascimento.day) < (detalhes.data_nascimento.month, detalhes.data_nascimento.day))
    except:
        idade = 0

    #agregador
    try:
        agregador = detalhes.categoria.agregador.id
    except:
        agregador = 9


    #problemas relacionados a categoria (especificos para membros).
    problemas = ""
    dados_matricula = "SEM MATRÍCULA."
    if agregador in [2,3,4]:
        try:
            ato = AtoOficial.objects.filter(pessoa_id = detalhes.id, tipo_ato__in=[1,2]).order_by('-id')[0]
            problemas += "Ato Oficial de admissão registrado na ata "+ato.ata_ato.identificacao+" em "+ato.data.strftime('%d/%m/%Y')+". "
        except:
            problemas += "ERRO: Ato Oficial de admissão não registrado. "
        try:
            membro = Membro.objects.exclude(invalido=True).get(pessoa_id = detalhes.id, ata_demissao__isnull=True, ata_admissao__isnull=False)
            problemas += "Matrícula de membro: "+str(membro.matricula)+". "
            dados_matricula = str(membro.matricula)+". "

        except Membro.DoesNotExist:
            problemas += "ERRO: Pessoa não tem registro de admissão na tabela de Rol. "
    else: #pra mostrar matricula de ex-membro
        try:
            exmembro = Membro.objects.exclude(invalido=True).get(pessoa_id = detalhes.id, ata_demissao__isnull=False, ata_admissao__isnull=False)
            dados_matricula = "(EX-MEMBRO) "+str(exmembro.matricula)+". "
        except Membro.DoesNotExist:
            pass
    try:
        dados_filh = "filh"+artigo
        dados_nascid = "nascid"+artigo
        
        if detalhes.nome is None:
            dados_nome = " INFORMAR_NOME "
        else:
            dados_nome = detalhes.nome.upper()
        if detalhes.pai is None:
            dados_pai = " INFORMAR_PAI "
        else:
            dados_pai = detalhes.pai.nome
        if detalhes.mae is None:
            dados_mae = " INFORMAR_MAE "
        else:
            dados_mae = detalhes.mae.nome
        if detalhes.estado_civil is None:
            dados_estado_civil = " INFORMAR_ESTADO_CIVIL "
        else:
            dados_estado_civil = detalhes.estado_civil.descricao[0:len(detalhes.estado_civil.descricao)-1]+artigo
        if detalhes.data_nascimento is None:
            dados_data_nascimento = " INFORMAR_DATA_NASCIMENTO "
        else:
            dados_data_nascimento = detalhes.data_nascimento.strftime('%d/%m/%Y')
        tipo_logradouro = TipoContato.objects.get(desc_legado = "Residência.Logradouro")
        try:
            pessoa_logradouro = Contato.objects.get(tipo=tipo_logradouro.id, pessoa_id=detalhes.id)
        except Contato.DoesNotExist:
            pessoa_logradouro = None
        if pessoa_logradouro is None:
            dados_logradouro = " INFORMAR_LOGRADOURO "
        else:
            dados_logradouro = pessoa_logradouro.conteudo
        tipo_cidade_uf = TipoContato.objects.get(desc_legado = "Residência.CidadeEstado")
        try:
            pessoa_cidade_uf = Contato.objects.get(tipo=tipo_cidade_uf.id, pessoa_id=detalhes.id)
        except Contato.DoesNotExist:
            pessoa_cidade_uf = None
        if pessoa_cidade_uf is None:
            dados_cidade_uf = " INFORMAR_CIDADE_UF "
        else:
            dados_cidade_uf = pessoa_cidade_uf.conteudo
        tipo_cep = TipoContato.objects.get(desc_legado = "Residência.CEP")
        try:
            pessoa_cep = Contato.objects.get(tipo=tipo_cep.id, pessoa_id=detalhes.id)
        except Contato.DoesNotExist:
            pessoa_cep = None
        if pessoa_cep is None:
            dados_cep = " INFORMAR_CEP "
        else:
            dados_cep = pessoa_cep.conteudo

        try:
            if detalhes.sexo == 'M':
                dados_sexo = "do sexo Masculino, "
            elif detalhes.sexo == 'F':
                dados_sexo = "do sexo Feminino, "
            else:
                dados_sexo = " INFORMAR SEXO "
        except:
            dados_sexo = " INFORMAR SEXO "


        dados_ata = dados_matricula+dados_nome+', '+dados_sexo+dados_filh+' de '+dados_pai+'/'+dados_mae+', '+dados_nascid+' em '+dados_data_nascimento+', '+dados_estado_civil+', com residência e domicílio em '+dados_logradouro+', '+dados_cidade_uf+', CEP '+dados_cep+'.'
    except:
        dados_ata = "Nenhuma informação disponível."

    turmas_membro = detalhes.turmas_membro.all()
    turmas_lider = detalhes.turmas_lider.all()

    filhos = []
    if detalhes.tem_filhos:
        if detalhes.sexo is 'M':
            filhos = detalhes.filhos_p.all()
        else:
            filhos = detalhes.filhos_m.all()

    return render(
        request,
        'pessoa.html',
        {
            'filhos':filhos,
            'detalhes': detalhes,
            'idade': idade,
            'lista_detalhes': vars(detalhes),
            'contatos': contatos,
            'familia': familia,
            'dados_ata': dados_ata,
            'agregador': agregador,
            'problemas': problemas,
            'turmas_membro': turmas_membro,
            'turmas_lider': turmas_lider,
        }
        )
