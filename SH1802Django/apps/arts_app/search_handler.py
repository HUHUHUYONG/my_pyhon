# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/11 上午10:03' 

from django.shortcuts import render, HttpResponseRedirect
from .models import Tag, Art
from django.db.models import Q

'''
页面搜索功能：

      接口URL：  /art/search?key=XXX&page=1

      方法：GET

      输入参数说明：

          key: 搜索的关键词

          page: 获取第几页

     输出：

          渲染搜索列表页面
'''



def SearchHandler(request):
	key = request.GET.get("key", "")  ##获取输入参数key对应的值，默认为空
	if key == "":
		return HttpResponseRedirect("/art/index")
	else:
		page = request.GET.get("page", 1)
		page = int(page)
		# 查询数据，或操作
		art_sets = Art.objects.filter(Q(a_title__contains=str(key))
									  | Q(a_content__contains=str(key))
									  | Q(a_info__contains=str(key))).distinct()
		# 查询数据，与操作
		# mdict = {
		#    'a_title':str(key),
		#    'a_content':str(key)
		# }
		# Art.objects.filter(mdict)

		total = art_sets.count()
	shownum = 10
	import math
	pagenum = int(math.ceil(total / shownum))
	if page < 1:
		return HttpResponseRedirect(request.path + "?page=%d&key=%s" % (1, key))
	if (total > 0) and (page > pagenum):
		return HttpResponseRedirect(request.path + "?page=%d&key=%s" % (pagenum, key))

	if total == 0:
		context = dict(
			pagenum=1,
			total=0,
			prev=1,
			next=1,
			pagerange=range(1, 2),
			data=[],
			url=request.path,
			key=key,
			page=1
		)
		return render(request, "search_handler.html", context=context)

	offset = (page - 1) * shownum

	data = art_sets[offset:(shownum + offset)]
	btnnum = 5
	if btnnum > pagenum:
		firstpage = 1
		lastpage = pagenum
	else:
		if page == 1:
			firstpage = 1
			lastpage = btnnum
		else:
			firstpage = page - 2
			lastpage = page + btnnum - 3
			if firstpage < 1:
				firstpage = 1
			if lastpage > pagenum:
				lastpage = pagenum
	prev = page - 1
	next = page + 1
	if prev < 1:
		prev = 1
	if next > pagenum:
		next = pagenum
	context = dict(
		pagenum=pagenum,
		total=total,
		prev=prev,
		next=next,
		pagerange=range(firstpage, lastpage + 1),
		data=data,
		url=request.path,
		key=key,
		page=page
	)

	return render(request, "search_handler.html", context=context)