# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/12 上午11:12' 

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import json
from arts_app.models import Cart, Art, LineItem, ProductOrder, OrderItemRelation
from SH1802Django.utils import check_user_login, flash, create_order_id
from arts_app import forms
from django.views.decorators.csrf import csrf_exempt

'''
查看购物车
接口：/art/cart/view
'''
@check_user_login
def ViewCartHandler(request):
	user = request.session.get("muser")
	(total_price, product_list) =  Cart.get_products(user)
	context = dict(
		user = user,
		total_price = total_price,
		product_list = product_list,
	)
	return render(request, "view_cart.html", context=context)


'''
添加商品到购物车
接口：/art/cart/add?id=小说id
'''
@check_user_login
def AddCartHandler(request):
	art_id = int(request.GET.get("id", 0))
	if art_id == 0:
		return HttpResponseRedirect("/art/index")
	product = Art.objects.get(id = art_id)
	user = request.session.get("muser")
	Cart.add_product(product, user)
	return ViewCartHandler(request)

'''
清空购物车
'''
@check_user_login
def CleanCartHandler(request):
	#del request.session['cart']
	user = request.session.get("muser")
	#line_items = LineItem.objects.filter(user=user.id)
	#删除用户对应的订单信息
	#[ProductOrder.objects.filter(order_id=item.product_order_id).delete()   for item in line_items]
	#删除购物车条目信息
	LineItem.objects.filter(user=user.id).delete()
	return ViewCartHandler(request)


'''
订单功能
'''
@check_user_login
def CartOrderHandler(request):
	user = request.session.get("muser")
	(total_price, product_list) = Cart.get_products(user)
	order_form = forms.OrderForms()

	context = dict(
		user = user,
		total_price = total_price,
		product_list = product_list,
		form = order_form,
	)
	return render(request, "product_order.html", context=context)



'''
提交订单功能
'''
@csrf_exempt
@check_user_login
def OrderSubmitHandler(request):
	url = request.path
	print(f"OrderSubmitHandler submit ok {url}")
	if request.method == "POST":
		order_form = forms.OrderForms(data=request.POST)
		if not order_form.is_valid():
			flash(request, "error", f"用户提交订单失败！")
			return CartOrderHandler(request)
		address = order_form.cleaned_data.get("address")
		pay_type = int(order_form.cleaned_data.get("pay_type"))
		phone = int(order_form.cleaned_data.get("phone"))
		order_id = create_order_id()
		prod_order = ProductOrder(order_id=order_id, address=address, pay_type=pay_type, phone=phone)
		prod_order.save()
		user = request.session.get("muser")
		line_items = LineItem.objects.filter(user=user.id)
		[OrderItemRelation(line_item_id=int(line_item.id), product_order_id=prod_order.id).save()  for  line_item  in  line_items]
		flash(request, "success", f"用户提交订单成功!,订单号为:{order_id}")
	return CartOrderHandler(request)

