# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/11 上午11:03' 
from django.shortcuts import render, HttpResponseRedirect
from arts_app import models
from comments import forms
from comments.models import Comment
'''
详情页面功能：

       接口URL：  /art/detail?id=7

      方法：GET

      输入参数说明：

          id： 文章id，（点击某一个具体的文章，传入文章id)

     输出：

          渲染详情页面
'''

def DetailHandler(request):
	art_id = int(request.GET.get("id", 0))
	if art_id == 0:
		return HttpResponseRedirect("/art/index")
	#获取小说详情
	art_queryset = models.Art.objects.get(id = art_id)

	#获取小说对应的章节
	art_capters = models.Chapter.objects.filter(art=art_id)

	#获取评论表单
	comment_form = forms.CommentForm()
	comment_list = Comment.objects.filter(art = art_id)
	context = dict(
		art = art_queryset,
		art_capters = art_capters,
		form = comment_form,
		comment_list = comment_list,
		comment_count = comment_list.count(),
	)

	return render(request, "detail_handler.html", context=context)


'''
小说章节
/art/capter?id=capter_id
'''
def ArtCapterHandler(request):
	capter_id = int(request.GET.get("id", 0))
	if capter_id == 0:
		return  DetailHandler(request)
	art_capter = models.Chapter.objects.get(id = capter_id)
	context = dict(
		art_capter = art_capter
	)
	return render(request, "capter_handler.html", context=context)

