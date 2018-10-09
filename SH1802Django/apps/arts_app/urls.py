# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/10 上午10:14' 

from django.conf.urls import url, include
from arts_app import user_manage
from arts_app import index_handler
from arts_app import search_handler
from arts_app import detail_handler
from arts_app import views
from arts_app import cart_handler

urlpatterns = [
	url(r"^index/$", index_handler.IndexHandler),
	url(r'^search', search_handler.SearchHandler),
	url(r"^register/$", user_manage.RegisterHandler, name="user_register"),
	url(r"^login/$", user_manage.LoginHandler, name="user_login"),
	url(r'^logout/$', user_manage.LogoutHandler),
	url(r'^detail/$', detail_handler.DetailHandler),
	url(r'^capter/$', detail_handler.ArtCapterHandler),
	url(r'^test_param/(?P<art_pk>[0-9]+)/$', views.test_param, name="art_param"),
	url(r'^cart/view/$', cart_handler.ViewCartHandler),
	url(r'^cart/add/$', cart_handler.AddCartHandler),
	url(r'^cart/clean/$', cart_handler.CleanCartHandler),
	url(r'^cart/order/$', cart_handler.CartOrderHandler),
	url(r'^cart/submit_order/$', cart_handler.OrderSubmitHandler, name="product_order"),
]