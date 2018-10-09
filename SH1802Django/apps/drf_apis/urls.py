# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/12 下午4:01' 

from django.conf.urls import url, include


from rest_framework.routers import DefaultRouter
from drf_apis import view_set
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register("art_user", view_set.ArtsUserViewSet)
router.register("tag", view_set.TagViewSet)
router.register("art", view_set.ArtViewSet)
router.register("chapter", view_set.ChapterViewSet)
router.register("comment", view_set.CommentViewSet)



urlpatterns = [
   url(r"^", include(router.urls)),
   url(r"^docs/", include_docs_urls("小说平台api文档")),
   url(r"^api-auth/", include('rest_framework.urls', namespace = "rest_framework")),
]

