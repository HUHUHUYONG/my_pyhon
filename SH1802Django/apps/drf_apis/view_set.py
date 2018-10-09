# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/12 下午3:53' 

'''
使用视图集来进行逻辑处理
'''

from rest_framework import viewsets
from rest_framework import permissions

from arts_app.models import ArtsUser, Tag, Art, Chapter, ProductOrder, LineItem
from drf_apis.permissions import IsOwnerOrReadOnly
from comments.models import Comment
from drf_apis import serializers



class ArtsUserViewSet(viewsets.ModelViewSet):
	queryset = ArtsUser.objects.all()
	serializer_class = serializers.ArtsUserSerializer

	permission_classes = (IsOwnerOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class =  serializers.TagSerializer

	permission_classes = (IsOwnerOrReadOnly,)


class ArtViewSet(viewsets.ModelViewSet):
	queryset = Art.objects.all()
	serializer_class =  serializers.ArtSerializer

	permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly)


class ChapterViewSet(viewsets.ModelViewSet):
	queryset = Chapter.objects.all()
	serializer_class = serializers.ChapterSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = serializers.CommentSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)









