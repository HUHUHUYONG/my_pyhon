# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/11 下午3:21' 


from django.conf.urls import url, include
from message import views


urlpatterns = [
	url(r"^$", views.MessageSubmitHandlerV2, name="msg_form"),
]
