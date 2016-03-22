from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from node_list.views import nodes, node_destroy
from cluster_create.views import cluster_creator
from aws_cluster_create.views import aws_cluster_creator_step0, aws_cluster_creator_step1, aws_cluster_creator_step2,\
    aws_cluster_creator_step3, aws_cluster_creator_step4
from azure_cluster_create.views import azure_cluster_creator_step1, azure_cluster_creator_step2,\
    azure_cluster_creator_step3


urlpatterns = [
    url(r'^$', 'home.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'provisioning_tool.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    #Comienza Simple_Server
    url(r'^list_server$', nodes, name='node_list'),
    url(r'^node_destroy$', node_destroy, name='node_destroy'),
    url(r'^cluster_create$', cluster_creator, name='cluster_creator'),
    url(r'^aws_cluster_creator_step0$', aws_cluster_creator_step0, name='aws_cluster_creator_step0'),
    url(r'^aws_cluster_creator_step1$', aws_cluster_creator_step1, name='aws_cluster_creator_step1'),
    url(r'^aws_cluster_creator_step2$', aws_cluster_creator_step2, name='aws_cluster_created_step2'),
    url(r'^aws_cluster_creator_step3$', aws_cluster_creator_step3, name='aws_cluster_created_step3'),
    url(r'^aws_cluster_creator_step4$', aws_cluster_creator_step4, name='aws_cluster_created_step4'),
    url(r'^azure_cluster_creator_step1$', azure_cluster_creator_step1, name='azure_cluster_creator_step1'),
    url(r'^azure_cluster_creator_step2$', azure_cluster_creator_step2, name='azure_cluster_created_step2'),
    url(r'^azure_cluster_creator_step3$', azure_cluster_creator_step3, name='azure_cluster_created_step3'),
    #test
    url(r'^aws_log$', 'aws_cluster_create.views.seelog', name='seelog'),
    url(r'^aws_log_page$','aws_cluster_create.views.logpage', name='logpage'),
    url(r'^azure_log$', 'azure_cluster_create.views.seeazurelog', name='seeazurelog'),
    url(r'^azure_log_page$', 'azure_cluster_create.views.azurelogpage', name='azurelogpage'),

    
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)