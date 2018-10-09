# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/11 下午2:32' 

from django.conf.urls import url, include
from comments import views

app_name = "comments"

urlpatterns = [
	url(r"^art/(?P<art_pk>[0-9]+)/$", views.art_comment, name="art_comment")
]
