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
from django.conf.urls import include, url
from home.views import Home
from node_list.views import NodeList
from node_creator.views import creator_step1, creator_step2, creator_step3

urlpatterns = [
    url(r'^$', Home.as_view()),
    url(r'^list_server$', NodeList.as_view()),
    url(r'^creator_step1$', creator_step1, name='creator_step1'),
    url(r'^creator_step2$', creator_step2, name='created_step2'),
    url(r'^creator_step3$', creator_step3, name='created_step3'),

]
