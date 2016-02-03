"""simple_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from home.views import Home
from node_list.views import nodes, node_destroy
from cluster_create.views import cluster_creator
from aws_cluster_create.views import aws_cluster_creator_step0, aws_cluster_creator_step1, aws_cluster_creator_step2,\
    aws_cluster_creator_step3
from azure_cluster_create.views import azure_cluster_creator_step1, azure_cluster_creator_step2, azure_cluster_creator_step3

urlpatterns = [
    url(r'^$', Home.as_view()),
    url(r'^list_server$', nodes, name='node_list'),
    url(r'^node_destroy$', node_destroy, name='node_destroy'),
    url(r'^cluster_create$', cluster_creator, name='cluster_creator'),
    url(r'^aws_cluster_creator_step0$', aws_cluster_creator_step0, name='aws_cluster_creator_step0'),
    url(r'^aws_cluster_creator_step1$', aws_cluster_creator_step1, name='aws_cluster_creator_step1'),
    url(r'^aws_cluster_creator_step2$', aws_cluster_creator_step2, name='aws_cluster_created_step2'),
    url(r'^aws_cluster_creator_step3$', aws_cluster_creator_step3, name='aws_cluster_created_step3'),
    url(r'^azure_cluster_creator_step1$', azure_cluster_creator_step1, name='azure_cluster_creator_step1'),
    url(r'^azure_cluster_creator_step2$', azure_cluster_creator_step2, name='azure_cluster_created_step2'),
    url(r'^azure_cluster_creator_step3$', azure_cluster_creator_step3, name='azure_cluster_created_step3'),

]
