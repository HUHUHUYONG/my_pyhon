# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '202018/6/23 下午2:29'


from django.conf.urls import url
from statistic import views

'''
二级路由入口文件
'''

urlpatterns = [
	url(r'^index/$', views.IndexHandler),
	url(r'^histogram/', views.HistogramHandler),
]
