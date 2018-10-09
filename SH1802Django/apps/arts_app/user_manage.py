# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/10 上午11:37' 


from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from arts_app import forms
from arts_app import models
from django.views.decorators.csrf import csrf_exempt
from SH1802Django.utils import flash

'''
加密算法：
可逆加密算法：BASE-64
不可逆加密算法: MD5
'''

'''
会员注册功能
支持方法：
GET --- 获取空注册表单
POST --- 提交注册表单
表单：forms.ArtsUserRegForm
数据模型:models.ArtsUser
'''
def create_pwd_md5(str_password):
	import hashlib
	h1 = hashlib.md5()
	h1.update(str_password.encode(encoding="utf-8"))
	return h1.hexdigest()


@csrf_exempt
def RegisterHandler(request):
	reg_form = forms.ArtsUserRegForm()
	method = request.method
	if method == "POST":
		reg_form = forms.ArtsUserRegForm(data=request.POST)
		if not reg_form.is_valid():
			#return HttpResponse("form is not valid")
			flash(request, "error", f"用户注册校验失败！")
			context = dict(form=forms.ArtsUserRegForm(data=request.POST))
			return render(request, "register_handler.html", context=context)
		username = reg_form.cleaned_data.get("username")
		password = create_pwd_md5(reg_form.cleaned_data.get("password"))
		email = reg_form.cleaned_data.get("email")
		user = models.ArtsUser(username=username, password=password, email=email)
		user.save()
		flash(request, "success", f"恭喜，注册用户{username}成功！！")
	context = dict(form = reg_form)

	return render(request, "register_handler.html", context=context)


@csrf_exempt
def LoginHandler(request):
	login_form = forms.ArtsUserLoginForm()
	if request.method == "POST":
		login_form = forms.ArtsUserLoginForm(data = request.POST)
		if not login_form.is_valid():
			flash(request, "error", f"用户登录校验失败！")
			context = dict(form=forms.ArtsUserLoginForm())
			return render(request, "login_handler.html", context=context)
		username = login_form.cleaned_data.get("username")
		password = create_pwd_md5(login_form.cleaned_data.get("password"))
		user = models.ArtsUser.objects.filter(username=username, password=password)
		user_first = user.first()
		if user_first:  #登录验证成功，用户名和密码都正确
			request.session["muser"] = user_first
			return HttpResponseRedirect("/art/index")
		flash(request, "error", f"用户{username}登录失败！")

	context = dict(form = login_form)
	return render(request, "login_handler.html", context=context)


def LogoutHandler(request):
	del request.session["muser"]
	return HttpResponseRedirect("/art/login")


