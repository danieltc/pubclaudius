from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from rest_framework import routers
from rol import views


router = routers.DefaultRouter()
router.register(r'membros', views.MembroViewSet)
router.register(r'pessoas', views.PessoaViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    url(r'^password/ok/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_ok.html'),name='password_change_done'),
    
    url(r'^pessoas/$', views.pessoas, name='pessoas'),
    url(r'^pessoas/membros/$', views.pessoas_membros, name='pessoas_membros'),
    url(r'^pessoas/visitantes/$', views.pessoas_visitantes, name='pessoas_visitantes'),
    url(r'^pessoas/outros/$', views.pessoas_outros, name='pessoas_outros'),
    url(r'^pessoas/new/$', views.new_pessoa, name='new_pessoa'),
    url(r'^pessoa/(?P<pk>\d+)/$', views.pessoa, name='pessoa'),
    url(r'^pessoa/(?P<pk>\d+)/edit/$', views.edit_pessoa, name='edit_pessoa'),
    url(r'^pessoa/(?P<pk>\d+)/simple_edit/$', views.simple_edit_pessoa, name='simple_edit_pessoa'),
    
    
    url(r'^informacoes/aniversarios/$', views.aniversarios, name='aniversarios'),
    url(r'^informacoes/rol/(?P<tipo>\w+)$', views.rol_publico, name='rol_publico'),
    url(r'^informacoes/rol/$', views.rol_publico, name='rol_publico'),
    url(r'^informacoes/relatorios/$', views.relatorios, name='relatorios'),

    url(r'^informacoes/relatorios/(?P<tipo>\w+)$', views.relatorio_padrao, name='relatorio_padrao'),
    url(r'^informacoes/relatorios/(?P<tipo>\w+)/(?P<titulo>\w+)$', views.relatorio_padrao, name='relatorio_padrao'),

    url(r'^personalizado/new/$', views.new_relatorio, name='new_relatorio'),
    url(r'^personalizado/edit/(?P<pk>\d+)$', views.edit_relatorio, name='edit_relatorio'),
    url(r'^personalizado/delete/(?P<pk>\d+)$', views.del_relatorio, name='del_relatorio'),
    url(r'^personalizado/(?P<pk>\d+)$', views.relatorio_personalizado, name='relatorio_personalizado'),
    url(r'^personalizado/(?P<pk>\d+)/(?P<pdf>\w+)/$', views.relatorio_personalizado, name='relatorio_personalizado_pdf'),


    url(r'^atas/$', views.atas, name='atas'),
    url(r'^ata/(?P<pk>\d+)/$', views.ata, name='ata'),
    url(r'^ata/new$', views.new_ata, name='new_ata'),
    url(r'^ato/(?P<pk>\d+)/$', views.ato, name='ato'),
    url(r'^ata/(?P<pk>\d+)/new_ato/$', views.new_ato, name='new_ato'),

    url(r'^admitir/$', views.admitir, name='admitir'),
    url(r'^demitir/$', views.demitir, name='demitir'),

    url(r'^presbiterio/$', views.presbiterio, name='presbiterio'),

    url(r'^lista_rol/$', views.lista_rol, name='lista_rol'),

    url(r'^debug/$', views.debug, name='debug'),
    url(r'^debug/basicos$', views.debug_basicos, name='debug_basicos'),
    url(r'^debug/geral$', views.debug_geral, name='debug_geral'),
    url(r'^debug/foto$', views.debug_foto, name='debug_foto'),

    url(r'^frequencia/$', views.frequencia, name='frequencia'),
    url(r'^frequencia/culto/(?P<turno>\w+)$', views.freq_culto, name='freq_culto'),
    url(r'^frequencia/ebd$', views.freq_ebd, name='freq_ebd'),
    url(r'^frequencia/turma/(?P<pk>\d+)$', views.freq_turma, name='freq_turma'),

    url(r'^grupos/(?P<pk>\d+)$', views.grupo, name='grupo'),
    url(r'^grupos/$', views.grupos, name='grupos'),
    url(r'^grupos/(?P<pk>\d+)/relatorio/$', views.relatorio_padrao_grupo, name='relatorio_grupo'),

    url(r'^grupos/(?P<pk>\d+)/novo/$', views.new_turma, name='new_turma'),
    url(r'^turma/(?P<pk>\d+)$', views.turma, name='turma'),
    url(r'^turma/(?P<pk>\d+)/del_pessoa/(?P<pessoa>\d+)$', views.del_pessoa_turma, name='del_pessoa_turma'),
    url(r'^turma/(?P<pk>\d+)/del_lider/(?P<lider>\d+)$', views.del_lider_turma, name='del_lider_turma'),
    url(r'^turma/(?P<pk>\d+)/add_pessoa/(?P<pessoa>\d+)$', views.add_pessoa_turma, name='add_pessoa_turma'),
    url(r'^turma/(?P<pk>\d+)/add_pessoa/$', views.selecionar_participante, name='selecionar_participante'),
    url(r'^turma/(?P<pk>\d+)/add_lider/(?P<lider>\d+)$', views.add_lider_turma, name='add_lider_turma'),
    url(r'^turma/(?P<pk>\d+)/add_lider/$', views.selecionar_lider, name='selecionar_lider'),
    url(r'^turma/(?P<pk>\d+)/relatorio/$', views.relatorio_padrao_turma, name='relatorio_turma'),
    url(r'^turma/(?P<pk>\d+)/editar/$', views.edit_turma, name='edit_turma'),
    url(r'^turma/(?P<pk>\d+)/remover/$', views.del_turma, name='del_turma'),
    url(r'^turma/pessoa/(?P<pessoa>\d+)/add/(?P<turma>\d+)/tipo/(?P<tipo>\d+)$',views.add_pessoa_turma_tipo, name='add_pessoa_turma_tipo'),
    url(r'^turma/pessoa/(?P<pessoa>\d+)/del/(?P<turma>\d+)/tipo/(?P<tipo>\d+)$',views.del_pessoa_turma_tipo, name='del_pessoa_turma_tipo'),
    url(r'^seleciona_turma/pessoa/(?P<pessoa>\d+)/(?P<tipo>\d+)$',views.select_turma_pessoa_tipo, name='select_turma_pessoa_tipo'),
    url(r'^seleciona_turma/relatorio/(?P<pk>\d+)/(?P<turma>\d+)$',views.add_relatorio_turma, name='add_relatorio_turma'),
    url(r'^seleciona_turma/relatorio/(?P<pk>\d+)/$',views.select_relatorio_turma, name='select_relatorio_turma'),
    

    url(r'^igrejas/$', views.igrejas, name='igrejas'),
    url(r'^igreja/new$', views.new_igreja, name='new_igreja'),
    url(r'^igreja/(?P<pk>\d+)/editar$', views.edit_igreja, name='edit_igreja'),
    
    url(r'^carros/$', views.carros, name='carros'),
    url(r'^talentos/$', views.talentos, name='talentos'),
    url(r'^add_talentos/$', views.add_talentos, name='add_talentos'),


    url(r'^admin/', admin.site.urls),
    url(r'api/', include(router.urls)),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
