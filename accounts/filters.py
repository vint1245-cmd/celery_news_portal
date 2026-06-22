import django_filters as filters
from django.db import models
from .models import Post
from django import forms

class CharFilterInFilter(filters.BaseInFilter,filters.CharFilter):
    pass


class PostFilter(filters.FilterSet):
    #category = CharFilterInFilter(field_name='category__category_name',lookup_expr='in')
    time_of_posting =filters.DateFilter(field_name='time_of_posting',widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
               lookup_expr='gt', label='Начальная дата')
    class Meta:
        model = Post
        fields = {'title': ['icontains'],'author': ['in']}


