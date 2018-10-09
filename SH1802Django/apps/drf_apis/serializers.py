# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/7/12 下午3:36'
'''
序列化
类似于form
form                 serializer

html模板页面           api动态数据
'''

from rest_framework import serializers
from arts_app.models import ArtsUser, Tag, Art, Chapter, ProductOrder, LineItem

from comments.models import Comment


class ArtsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtsUser
        fields = [
            'id',
            'username',
            'password',
            'email',
            'createtime',
            'flag'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            't_name',
            't_info',
            't_createtime',
            't_flag',
        ]


class ArtSerializer(serializers.ModelSerializer):
    operator = serializers.ReadOnlyField(source="operator.username")

    class Meta:
        model = Art
        fields = [
            'id',
            'a_title',
            'a_info',
            'a_content',
            'a_img',
            'a_createtime',
            'a_tag',
            'a_price',
            'a_flag',
            'operator',
        ]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            'id',
            'art',
            'title',
            'content',
            'create_time',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'name',
            'title',
            'text',
            'created_time',
            'art',
            'flag',
        ]
