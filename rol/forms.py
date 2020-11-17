from django import forms
from django.db.models import Q
from .models import Igreja, Relatorio, Pessoa, Ata, AtoOficial, Membro, TipoAto, TurmaFrequencia, TurmaFrequencia, Talento
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.admin.widgets import AdminDateWidget

class PessoaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PessoaForm, self).__init__(*args, **kwargs)
        self.fields['pai'].queryset = Pessoa.objects.exclude(sexo='F')
        self.fields['mae'].queryset = Pessoa.objects.exclude(sexo='M')
        for key in self.fields:
            self.fields[key].required = False
        self.fields['nome'].required = True
        self.fields['rol'].required = True
        self.fields['rol'].initial = 1

    #contatos
    data_nascimento = forms.DateField(input_formats=['%d/%m/%Y'])
    data_falecimento = forms.DateField(input_formats=['%d/%m/%Y'])
    data_pedido_admissao = forms.DateField(input_formats=['%d/%m/%Y'])
    email = forms.CharField()
    email_secundario = forms.CharField()
    celular = forms.CharField()
    celular_secundario = forms.CharField()
    celular_outro = forms.CharField()
    endereco = forms.CharField()
    cidade_estado = forms.CharField()
    cep = forms.CharField()
    telefone = forms.CharField()
    trabalho_local = forms.CharField()
    trabalho_email = forms.CharField()
    trabalho_telefone = forms.CharField()
    facebook = forms.CharField()
    googleplus = forms.CharField()
    linkedin = forms.CharField()
    skype = forms.CharField()
    pagina_pessoal = forms.CharField()
    alergias = forms.CharField()
    dados_adicionais = forms.CharField()
    carro = forms.CharField()
    foto = forms.ImageField()

    class Meta:
        model = Pessoa
        fields = [
            'rol',
            'nome',
            'apelido',
            'foto',
            'sexo',
            'tem_filhos',
            #'categoria',
            'pai',
            'mae',
            'chefe_familia',
            'pai_biologico',
            'mae_biologica',
            'data_nascimento',
            'data_falecimento',
            'forma_admissao_pretendida',
            'entrevista_admissao_realizada',
            'carta_transferencia_requisitada',
            'cpf',
            'rg',
            'estado_civil',
            'conjuge',
            'estado_civil_complemento',
            'nao_conjuge',
            'data_inicio_relacionamento',
            'igreja_origem',
            'batismo_quando',
            'batismo_onde',
            'profissao_fe_quando',
            'profissao_fe_onde',
            'razoes_pedido_admissao',
            'data_pedido_admissao',
            'observacoes_legado',
            'naturalidade',
            
            ]


class PresbPessoaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PresbPessoaForm, self).__init__(*args, **kwargs)

        self.fields['pai'].queryset = Pessoa.objects.exclude(sexo='F')
        self.fields['mae'].queryset = Pessoa.objects.exclude(sexo='M')
        
        for key in self.fields:
            self.fields[key].required = False
        self.fields['nome'].required = True
        self.fields['rol'].required = True
        self.fields['rol'].initial = 1

    foto = forms.ImageField()
    #contatos
    email = forms.CharField()
    email_secundario = forms.CharField()
    celular = forms.CharField()
    celular_secundario = forms.CharField()
    celular_outro = forms.CharField()
    endereco = forms.CharField()
    cidade_estado = forms.CharField()
    cep = forms.CharField()
    telefone = forms.CharField()
    trabalho_local = forms.CharField()
    trabalho_email = forms.CharField()
    trabalho_telefone = forms.CharField()
    facebook = forms.CharField()
    googleplus = forms.CharField()
    linkedin = forms.CharField()
    skype = forms.CharField()
    pagina_pessoal = forms.CharField()
    alergias = forms.CharField()
    dados_adicionais = forms.CharField()
    carro = forms.CharField()

    class Meta:
        model = Pessoa
        fields = [
            'rol',
            'nome',
            'apelido',
            'foto',
            'sexo',
            'tem_filhos',
            'categoria',
            'pai',
            'mae',
            'chefe_familia',
            'pai_biologico',
            'mae_biologica',
            'data_nascimento',
            'data_falecimento',
            'forma_admissao_pretendida',
            'entrevista_admissao_realizada',
            'carta_transferencia_requisitada',
            'cpf',
            'rg',
            'estado_civil',
            'conjuge',
            'estado_civil_complemento',
            'nao_conjuge',
            'data_inicio_relacionamento',
            'igreja_origem',
            'batismo_quando',
            'batismo_onde',
            'profissao_fe_quando',
            'profissao_fe_onde',
            'razoes_pedido_admissao',
            'data_pedido_admissao',
            'observacoes_legado',
            'naturalidade',

            ]

class PessoaSimplesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PessoaSimplesForm, self).__init__(*args, **kwargs)
        self.fields['pai'].queryset = Pessoa.objects.filter(tem_filhos=True).filter(sexo='M')
        self.fields['mae'].queryset = Pessoa.objects.filter(tem_filhos=True).filter(sexo='F')
        for key in self.fields:
            self.fields[key].required = False
        self.fields['nome'].required = True
        self.fields['rol'].required = True
        self.fields['rol'].initial = 1
        self.fields['inserir_novo_pai'].help_text = "Use este campo apenas se não encontrar a pessoa no campo anterior. Para usar este campo, deixe o campo anterior vazio (---------)."
        self.fields['inserir_nova_mae'].help_text = "Use este campo apenas se não encontrar a pessoa no campo anterior. Para usar este campo, deixe o campo anterior vazio (---------)."

    foto = forms.ImageField()
    #contatos
    endereco = forms.CharField()
    cidade_estado = forms.CharField()
    cep = forms.CharField()
    celular = forms.CharField()
    email = forms.CharField()

    #campos de inserir gente que não existe
    inserir_novo_pai = forms.CharField()
    inserir_nova_mae = forms.CharField()
    class Meta:
        model = Pessoa
        fields = [
            'rol',
            'foto',
            'nome',
            'data_nascimento',
            'naturalidade',
            'pai',
            'inserir_novo_pai',
            'mae',
            'inserir_nova_mae',
            'sexo',
            'estado_civil',
            ]


class AtaForm(forms.ModelForm):
    class Meta:
        model = Ata
        fields = ['data','numero']

class AtoOficialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AtoOficialForm, self).__init__(*args, **kwargs)
        self.fields['tipo_ato'].queryset = TipoAto.objects.exclude(id__in = [1,2,5,27])
        for key in self.fields:
            self.fields[key].required = False
        self.fields['tipo_ato'].required = True
        self.fields['pessoa'].required = True
        self.fields['data'].required = True
        self.fields['tipo_ato'].help_text = "Para ADMISSÃO ou DEMISSÃO, utilize os respectivos itens do menu 'conselho'."

    class Meta:
        model = AtoOficial
        fields = [
            'pessoa',
            'dados_ato',
            'tipo_ato',
            'celebrante',
            'data',
            'detalhes'
        ]

class AdmitirForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdmitirForm, self).__init__(*args, **kwargs)
        self.fields['pessoa'].queryset = Pessoa.objects.filter(categoria_id__in=[20,42,44,45,46,47,49,54,58,60,61,66,68])
        self.fields['pessoa'].help_text = "Somente pessoas com categoria 'Admitendo' (ou equivalente) aparecem nesta lista."
        self.fields['ata_admissao'].queryset = Ata.objects.order_by('-id')
        self.fields['matricula'].help_text = "Este número é gerado automaticamente. Só altere se tiver certeza do que está fazendo."
        self.fields['forma_admissao'].help_text = "Selecione uma forma de admissão coerente com a pessoa selecionada."
        self.fields['dados_admissao'].help_text = "Caso queira, pode copiar os dados na página da pessoa e depois voltar aqui."
        self.fields['dados_admissao'].required = False
        self.fields['ata_admissao'].help_text = "Se na ata selecionada não existir um Ato Oficial de admissão, será registrado um."

    class Meta:
        model = Membro
        fields = [
            'matricula',
            'pessoa',
            'forma_admissao',
            'dados_admissao',
            'ata_admissao'
        ]


class DemitirForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DemitirForm, self).__init__(*args, **kwargs)
        membros_nao_demitidos = Membro.objects.filter(data_demissao__isnull=True).exclude(invalido=True).values_list('pessoa', flat=True)
        self.fields['pessoa'].queryset = Pessoa.objects.filter(id__in = membros_nao_demitidos)
        self.fields['pessoa'].help_text = "Somente membros que não foram demitidos aparecem nesta lista."
        self.fields['ata_demissao'].queryset = Ata.objects.order_by('-id')
        self.fields['ata_demissao'].help_text = "Se na ata selecionada não existir um Ato Oficial de demissão, será registrado um."
        self.fields['forma_demissao'].help_text = "Selecione uma forma de admissão coerente com a pessoa selecionada."
        self.fields['dados_demissao'].help_text = "Campo opcional."
        self.fields['dados_demissao'].required = False

    def clean(self):
        cleaned_data = super(DemitirForm, self).clean()
        return cleaned_data


    class Meta:
        model = Membro
        fields = [
            'pessoa',
            'forma_demissao',
            'dados_demissao',
            'ata_demissao',
        ]

class FreqCultoForm(forms.Form):
    data = forms.DateField(label='Data')
    culto = forms.IntegerField(label='Pessoas presentes no culto')
    bercario = forms.IntegerField(label='Bebês no berçário')

class FreqEbdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FreqEbdForm, self).__init__(*args, **kwargs)
        turmas = TurmaFrequencia.objects.filter(tipo = 'ebd').filter( dt_inicio__lte=date.today()).exclude(dt_fim__lte=date.today()).order_by('-id')
        for t in turmas:
            self.fields["turma"+str(t.id)] = forms.IntegerField(label=t.titulo, initial=0)

    data = forms.DateField(label='Data',initial=date.today)

class FreqTurmaForm(forms.Form):
    data = forms.DateField(label='Data', initial=date.today)
    quantidade = forms.IntegerField(label='Presenças', initial=0)

class PresbiterioForm(forms.Form):
    data_inicio = forms.DateField(label='Data Inicial', initial=(datetime.now()-relativedelta(years=1)))
    data_fim = forms.DateField(label='Data Final', initial=date.today)

class RelatorioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RelatorioForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].help_text = "CAMPO OBRIGATÓRIO"
        self.fields['turma_grupo'].help_text = "!!! Caso este campo seja selecionado, os outros filtros serão ignorados !!!"
        self.fields['turma_grupo'].initial = None
        self.fields['turma_grupo'].queryset=TurmaFrequencia.objects.filter(restrito=False)
        self.fields['rol_separado'].initial = None
        self.fields['chefe_familia'].initial = None
        self.fields['campo1'].help_text = "itens Campo1 a Campo4 são os campos que vão aparecer no relatório. O campo 1 funciona também como link."
        self.fields['campo1'].initial = 'nome'
        self.fields['campo2'].help_text = "opcional - itens Campo1 a Campo4 são os campos que vão aparecer no relatório."
        self.fields['campo3'].help_text = "opcional - itens Campo1 a Campo4 são os campos que vão aparecer no relatório."
        self.fields['campo4'].help_text = "opcional - itens Campo1 a Campo4 são os campos que vão aparecer no relatório."
        self.fields['categorias'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        # self.fields['categorias'].widget = forms.SelectMultiple()
        self.fields['formas_admissao_pretendida'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        self.fields['estados_civis'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        self.fields['estados_civis_complementos'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        self.fields['rols'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        self.fields['formas_admissao'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        self.fields['formas_demissao'].help_text = "Mantenha a tecla CONTROL pressionada para selecionar mais de um item."
        

    class Meta:
        model = Relatorio
        fields = '__all__'
        exclude = ['user_update','total'] 


class TurmaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)
        
        permitidos_queryset = Pessoa.objects.filter(Q(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70])|Q(id = 888)).order_by('nome_ascii')
        self.fields['titulo'].help_text = "CAMPO OBRIGATÓRIO - Se for EBD, favor seguir o padrão 'EBD - Nome da turma - ano(AAAA).período(1 ou 2)'. Este valor (como todos os outros) poderá ser editado posteriormente."
        self.fields['dt_inicio'].help_text = "CAMPO OBRIGATÓRIO - Se for EBD, informar data do início da EBD. Senão, informar data de hoje. Formato: DD/MM/AAAA"
        self.fields['dt_inicio'].initial = date.today
        self.fields['dt_fim'].help_text = "ATENÇÃO - este campo só deve ser informado após o término das atividades desta turma (via 'editar'). Formato: DD/MM/AAAA"
        self.fields['descricao'].help_text = "CAMPO OBRIGATÓRIO - Breve descrição da finalidade desta turma."
        self.fields['tipo'].help_text = "CAMPO OBRIGATÓRIO - Se não for EBD, _provavelmente_ você deve selecionar 'Outros Grupos'."
        self.fields['tipo'].initial = 'outro'
        self.fields['restrito'].help_text = "ATENÇÃO: Marque esta caixinha se esta turma for de visualização restrita aos pastores e presbíteros."
        
    class Meta:
        model = TurmaFrequencia
        fields = '__all__'
        exclude = ['tipo_grupo','participantes','lideranca'] 


class IgrejaForm(forms.ModelForm):
    class Meta:
        model = Igreja
        fields = '__all__'

class TalentoForm(forms.Form):
    pessoa = forms.ModelChoiceField(label='Pessoa', queryset=Pessoa.objects.filter(categoria_id__in=[1,9,24,37,38,39,40,51,59,62,63,64,65,69,70]).order_by('nome_ascii'))
    talentos = forms.ModelMultipleChoiceField(label='Talentos', queryset=Talento.objects.all())
    
