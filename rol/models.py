from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    nome = models.CharField(max_length=256)
    detalhes = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['pk']

class Ata(models.Model):
    data = models.DateField()
    identificacao = models.CharField(max_length=256,unique=True)
    numero = models.IntegerField(unique=True)

    def __str__(self):
        return self.identificacao

    class Meta:
        ordering = ['identificacao']

class AgregadorCategoria(models.Model):
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return self.descricao

class Categoria(models.Model):
    descricao = models.CharField(max_length=256)
    agregador = models.ForeignKey(AgregadorCategoria, related_name="categorias", on_delete=models.DO_NOTHING)
    detalhes = models.CharField(max_length=256, null=True,blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']


class TipoAdmissao(models.Model):
    descricao = models.CharField(max_length=256)
    relativo_a = models.CharField(max_length=3, choices=[('MNC','Membro Não Comungante'),('MC','Membro Comungante')], null=True,blank=True)
    fonte = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']


class TipoDemissao(models.Model):
    descricao = models.CharField(max_length=256)
    relativo_a = models.CharField(max_length=3, choices=[('MNC','Membro Não Comungante'),('MC','Membro Comungante')], null=True,blank=True)
    fonte = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.descricao
    class Meta:
        ordering = ['descricao']


class TipoAto(models.Model):
    descricao = models.CharField(max_length=256, null=True,blank=True)
    detalhes = models.CharField(max_length=256, null=True,blank=True)
    precedente = models.ForeignKey('self', related_name='ato_precedente', null=True,blank=True, on_delete=models.DO_NOTHING)
    presbiterio = models.NullBooleanField(null=True,blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']


class TipoContato(models.Model):
    descricao = models.CharField(max_length=256)
    desc_legado = models.CharField(max_length=256)
    desc_sistema = models.CharField(max_length=256)
    detalhes = models.CharField(max_length=256, null=True,blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']


class TipoEstadoCivil(models.Model):
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']

class TipoEstadoCivilComplemento(models.Model):
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']

class TipoGrupo(models.Model):
    nome = models.CharField(max_length=256)
    descricao = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['nome']

class Igreja(models.Model):
    nome = models.CharField(max_length=256)
    cidade = models.CharField(max_length=256, null=True,blank=True)
    uf = models.CharField(max_length=4, null=True,blank=True)
    ipb = models.BooleanField(default=False)
    nome_secretario_conselho = models.CharField(max_length=256, null=True,blank=True)
    email_secretario_conselho = models.CharField(max_length=256, null=True,blank=True)
    observacao = models.TextField(null=True,blank=True)
    endereco = models.CharField(max_length=256, null=True,blank=True)
    classe = models.CharField(max_length=256, null=True,blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

class CategoriaTalento(models.Model):
    descricao = models.CharField(max_length=256)
    def __str__(self):
        return self.descricao

class Talento(models.Model):
    descricao = models.CharField(max_length=256)
    categoria = models.ForeignKey(CategoriaTalento, related_name='categoria_talento', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.categoria.descricao+": "+self.descricao


class Pessoa(models.Model):
    def pic_pessoa_id(self, filename):
        return 'pics/{0}'.format(self.id)

    nome = models.CharField(max_length=256)
    nome_ascii = models.CharField(max_length=256, null=True,blank=True)
    apelido = models.CharField(max_length=256, null=True,blank=True)
    sexo = models.CharField(max_length=1, choices=[('M','Masculino'),('F','Feminino')], null=True,blank=True)
    comungante = models.NullBooleanField(null=True,blank=True)
    categoria = models.ForeignKey(Categoria, related_name='pessoas', null=True,blank=True, on_delete=models.DO_NOTHING)
    foto = models.ImageField(upload_to=pic_pessoa_id, null=True,blank=True)
    pai = models.ForeignKey('self', related_name='filhos_p', null=True,blank=True, on_delete=models.DO_NOTHING)
    mae = models.ForeignKey('self', related_name='filhos_m', null=True,blank=True, on_delete=models.DO_NOTHING)
    chefe_familia = models.ForeignKey('self', related_name='membros_da_familia', null=True,blank=True, on_delete=models.DO_NOTHING)
    pai_biologico = models.ForeignKey('self', related_name='filhos_biologicos_p', null=True,blank=True, on_delete=models.DO_NOTHING)
    mae_biologica = models.ForeignKey('self', related_name='filhos_biologicos_m', null=True,blank=True, on_delete=models.DO_NOTHING)
    data_nascimento = models.DateField(null=True,blank=True)
    data_falecimento = models.DateField(null=True,blank=True)
    forma_admissao_pretendida = models.ForeignKey(TipoAdmissao, related_name='pessoas', null=True,blank=True, on_delete=models.DO_NOTHING)
    entrevista_admissao_realizada = models.NullBooleanField(null=True,blank=True)
    carta_transferencia_requisitada = models.NullBooleanField(null=True,blank=True)
    cpf = models.CharField(max_length=14, null=True,blank=True)
    rg = models.CharField(max_length=30, null=True,blank=True)
    estado_civil = models.ForeignKey(TipoEstadoCivil, related_name='pessoas', null=True,blank=True, on_delete=models.DO_NOTHING)
    conjuge = models.ForeignKey('self', related_name='pessoa_conjuge', null=True,blank=True, on_delete=models.DO_NOTHING)
    nao_conjuge = models.ForeignKey('self', related_name='pessoa_nao_conjuge', null=True,blank=True, on_delete=models.DO_NOTHING)
    estado_civil_complemento = models.ForeignKey(TipoEstadoCivilComplemento, related_name='pessoas', null=True,blank=True, on_delete=models.DO_NOTHING)
    data_inicio_relacionamento = models.DateField(null=True,blank=True)
    igreja_origem = models.ForeignKey(Igreja, related_name='pessoas', null=True,blank=True, on_delete=models.DO_NOTHING)
    batismo_quando = models.CharField(max_length=256, null=True,blank=True)
    batismo_onde = models.CharField(max_length=256, null=True,blank=True)
    profissao_fe_quando = models.CharField(max_length=256, null=True,blank=True)
    profissao_fe_onde = models.CharField(max_length=256, null=True,blank=True)
    razoes_pedido_admissao = models.TextField(null=True,blank=True)
    observacoes_legado = models.TextField(null=True,blank=True)
    data_pedido_admissao = models.DateField(null=True,blank=True)
    tem_filhos = models.NullBooleanField(null=True,blank=True)
    naturalidade = models.CharField(max_length=256, null=True,blank=True)
    data_update = models.DateField(null=True,blank=True)
    user_update = models.ForeignKey(User, related_name='atualizado_por', null=True, blank=True, on_delete=models.DO_NOTHING)
    rol = models.ForeignKey(Rol, related_name='pessoas_rol', on_delete=models.DO_NOTHING)
    talentos = models.ManyToManyField(Talento,related_name='banco_talentos')
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome_ascii']


class Membro(models.Model):
    matricula = models.IntegerField(unique=True) #id_legado
    pessoa = models.ForeignKey(Pessoa, related_name='membro', on_delete=models.DO_NOTHING)
    forma_admissao = models.ForeignKey(TipoAdmissao, related_name='membros', on_delete=models.DO_NOTHING)
    dados_admissao = models.CharField(max_length=512, null=True,blank=True)
    ata_admissao = models.ForeignKey(Ata, related_name='admitidos', on_delete=models.DO_NOTHING)
    data_admissao = models.DateField(null=True,blank=True)
    forma_demissao = models.ForeignKey(TipoDemissao, related_name='ex_membros_demitidos', null=True,blank=True, on_delete=models.DO_NOTHING)
    dados_demissao = models.CharField(max_length=512, null=True,blank=True)
    ata_demissao = models.ForeignKey(Ata, related_name='demitidos', null=True,blank=True, on_delete=models.DO_NOTHING)
    data_demissao = models.DateField(null=True,blank=True)
    transferido_para = models.ForeignKey(Igreja, related_name='ex_membros_transferidos', null=True,blank=True, on_delete=models.DO_NOTHING)
    rol_separado = models.BooleanField(default=False)
    invalido = models.BooleanField(default=False)

    def __str__(self):
        return self.pessoa.nome

    class Meta:
        ordering = ['matricula']


class Oficialato(models.Model):
    pessoa = models.ForeignKey(Pessoa, related_name='oficial', on_delete=models.DO_NOTHING)
    cargo_atual = models.CharField(max_length=256, choices=[
                                                ('diacono','Diácono'),
                                                ('diacono_disp','Diácono em disponibilidade'),
                                                ('pastor_aux','Pastor Auxiliar'),
                                                ('pastor_evang','Pastor Evangelista'),
                                                ('pastor_titular','Pastor Titular'),
                                                ('presbitero','Presbítero'),
                                                ('presbitero_disp','Presbítero em disponibilidade'),
                                                ('presb_diac_disp','Presbítero/Diácono em disponibilidade'),
                                                ('licenciado','Licenciado'),
                                            ])
    data_inicio_mandato = models.DateField(null=True,blank=True)
    data_fim_mandato = models.DateField(null=True,blank=True)
    ordenacao_historico = models.CharField(max_length=256,  choices=[
                                                ('diaconato','Diaconato'),
                                                ('diaconato_presbiterato','Diaconato e Presbiterato'),
                                                ('diaconato_pastorado','Diaconato e Pastorado'),
                                                ('diaconato_presbiterato_pastorado','Diaconato, Presbiterato e Pastorado'),
                                                ('pastorado','Pastorado'),
                                                ('presbiterato','Presbiterato'),
                                                ('presbiterato_pastorado','Presbiterato e Pastorado'),
                                            ])
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.pessoa.nome

class AtoOficial(models.Model):
    data = models.DateField(null=True,blank=True)
    pessoa = models.ForeignKey(Pessoa, related_name='atos_oficiais', on_delete=models.DO_NOTHING)
    dados_ato = models.TextField(null=True,blank=True)
    tipo_ato = models.ForeignKey(TipoAto, related_name='atos_oficiais_realizados', on_delete=models.DO_NOTHING)
    celebrante = models.ForeignKey(Pessoa, related_name='atos_oficiais_celebrados', on_delete=models.DO_NOTHING, null=True,blank=True)
    detalhes = models.TextField(null=True,blank=True)
    dt_hora_legado = models.DateTimeField(null=True,blank=True)
    ata_ato = models.ForeignKey(Ata, related_name='ata_do_ato', on_delete=models.DO_NOTHING, null=True,blank=True)

    def __str__(self):
        return self.pessoa.nome + self.tipo_ato.descricao

    class Meta:
        ordering = ['tipo_ato','pessoa']


class Contato(models.Model):
    tipo = models.ForeignKey(TipoContato, on_delete=models.DO_NOTHING)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING)
    conteudo = models.CharField(max_length=256)
    usa_de = models.ForeignKey(Pessoa, null=True,blank=True, related_name='parente', on_delete=models.DO_NOTHING)
    # usa_de significa que esse dado veio de outra pessoa.
    # nao sei bem como usar esse campo por agora, mas vou guardar.


    def __str__(self):
        return self.pessoa.nome + self.tipo.descricao

class TurmaFrequencia(models.Model): #grupo generico para frequencia ou qualquer outra coisa
    titulo = models.CharField(max_length=256)
    dt_inicio = models.DateField()
    dt_fim = models.DateField(null=True,blank=True)
    descricao = models.CharField(max_length=512)
    tipo = models.CharField(max_length=8, choices=[
                                                ('culto','Culto'),
                                                ('bercario','Berçário'),
                                                ('ebd','Escola Bíblica Dominical'),
                                                ('ebdi','Escola Bíblica Dominical Infantil'),
                                                ('gf','Grupos Familiares'),
                                                ('si','Sociedades Internas'),
                                                ('outro','Outros Grupos'),
                                            ])
    tipo_grupo = models.ForeignKey(TipoGrupo, on_delete=models.DO_NOTHING,null=True,blank=True)
    participantes = models.ManyToManyField(Pessoa,related_name='turmas_membro')
    lideranca = models.ManyToManyField(Pessoa,related_name='turmas_lider')
    restrito = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Frequencia(models.Model):#contagem total de pessoas presentes em um grupo
    turma = models.ForeignKey(TurmaFrequencia, on_delete=models.DO_NOTHING)
    data = models.DateField()
    quantidade = models.IntegerField()
    def __str__(self):
        return self.turma.titulo +' - '+ str(self.data) +': '+ str(self.quantidade)

class Presenca(models.Model):#registro de presenca individual de uma pessoa em um grupo
    turma = models.ForeignKey(TurmaFrequencia, on_delete=models.DO_NOTHING)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING)
    data = models.DateField()
    def __str__(self):
        return self.pessoa.nome +' presente no grupo ' + str(self.turma.titulo) +' em '+ str(self.data)

class Relatorio(models.Model):
    CAMPOS_RELATORIO = [
        ('nome','Nome'),
        ('foto','Foto'),
        ('sexo','Sexo'),
        ('comungante','Membro Comungante'),
        ('categoria','Categoria'),
        ('idade','Idade'),
        ('data_nascimento','Aniversário'),
        ('data_falecimento','Data de Falecimento'),
        ('forma_admissao_pretendida','Forma de Admissão Pretendida'),
        ('estado_civil','Estado Civil'),
        ('estado_civil_complemento','Namoro e Noivado'),
        ('data_inicio_relacionamento','Aniversário do Relacionamento'),
        ('data_pedido_admissao','Data do Pedido de Admissao'),
        ('tem_filhos','Tem Filho[s]'),
        ('rol','Rol'),
        ('forma_admissao','Forma de Admissão'),
        ('data_admissao','Data de Admissão'),
        ('forma_demissao','Forma de Demissão'),
        ('data_demissao','Data de Demissão'),
        ('celular','Celular'),
        ('email','Email'),
        ('endereco','Endereço'),
    ]
    titulo = models.CharField(max_length=256)
    sexo = models.CharField(max_length=1, choices=[('M','Masculino'),('F','Feminino')], null=True,blank=True)
    comungante = models.NullBooleanField(null=True,blank=True)
    categorias = models.ManyToManyField(Categoria, related_name='categorias_relatorio', blank=True)
    idade_minima = models.IntegerField(null=True,blank=True)
    idade_maxima = models.IntegerField(null=True,blank=True)
    data_falecimento_inicial = models.DateField(null=True,blank=True)
    data_falecimento_final = models.DateField(null=True,blank=True)
    formas_admissao_pretendida = models.ManyToManyField(TipoAdmissao, related_name='formaadmissao_relatorio', blank=True)
    entrevista_admissao_realizada = models.NullBooleanField(null=True,blank=True)
    carta_transferencia_requisitada = models.NullBooleanField(null=True,blank=True)
    estados_civis = models.ManyToManyField(TipoEstadoCivil, related_name='estadocivil_relatorio', blank=True)
    estados_civis_complementos = models.ManyToManyField(TipoEstadoCivilComplemento, related_name='complementoestadocivil_relatorio', blank=True)
    data_inicio_relacionamento_inicial = models.DateField(null=True,blank=True)
    data_inicio_relacionamento_final = models.DateField(null=True,blank=True)
    data_pedido_admissao_inicial = models.DateField(null=True,blank=True)
    data_pedido_admissao_final = models.DateField(null=True,blank=True)
    tem_filhos = models.NullBooleanField(null=True,blank=True)
    user_update = models.ForeignKey(User, related_name='criado_por',on_delete=models.DO_NOTHING)
    rols = models.ManyToManyField(Rol, related_name='rols_relatorio',blank=True)
    formas_admissao = models.ManyToManyField(TipoAdmissao, related_name='formasadmissao_relatorio',blank=True)
    data_admissao_inicial = models.DateField(null=True,blank=True)
    data_admissao_final = models.DateField(null=True,blank=True)
    formas_demissao = models.ManyToManyField(TipoDemissao, related_name='formasdemissao_relatorio', blank=True)
    data_demissao_inicial = models.DateField(null=True,blank=True)
    data_demissao_final = models.DateField(null=True,blank=True)
    rol_separado = models.NullBooleanField(default=False,null=True,blank=True)
    invalido = models.NullBooleanField(default=False,null=True,blank=True)
    chefe_familia = models.NullBooleanField(default=False,null=True,blank=True)
    campo1 = models.CharField(max_length=50,choices=CAMPOS_RELATORIO)
    campo2 = models.CharField(max_length=50,choices=CAMPOS_RELATORIO, null=True,blank=True)
    campo3 = models.CharField(max_length=50,choices=CAMPOS_RELATORIO, null=True,blank=True)
    campo4 = models.CharField(max_length=50,choices=CAMPOS_RELATORIO, null=True,blank=True)    
    turma_grupo = models.ForeignKey(TurmaFrequencia, related_name='turma_grupo_relatorio',on_delete=models.DO_NOTHING,  null=True,blank=True)
    total = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.titulo

