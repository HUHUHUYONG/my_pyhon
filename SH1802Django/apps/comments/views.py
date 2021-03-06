from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from arts_app import models
from comments.models import Comment
from comments.forms import CommentForm
from SH1802Django.utils import flash

def art_comment(request, art_pk):
	#art = models.Art.objects.filter(id=int(art_pk))   #方法1
	art = get_object_or_404(models.Art, pk=art_pk)     #方法2
	if request.method == "POST":
		form = CommentForm(data=request.POST)
		if form.is_valid():  #评论表单合法
			cmt = Comment(name=form.cleaned_data['name'],
						  title=form.cleaned_data['title'],
						  text=form.cleaned_data['text'],
						  art=art)
			cmt.save()
			comment_list = art.comment_set.all()  #通过外键反查所有评论
			comment_count = comment_list.count(),
			context = dict(
				art=art,
				form=form,
				comment_list=comment_list,
				comment_count=comment_count,
			)
			return render(request, "detail_handler.html", context=context)
		else:
			comment_list = art.comment_set.all()  # 通过外键反查所有评论
			comment_count = comment_list.count(),
			context = dict(
				art=art,
				form=form,
				comment_list=comment_list,
				comment_count=comment_count,
			)
			flash(request, "error", "用户提交评论失败！")
			return render(request, "detail_handler.html", context=context)

	return redirect(art)