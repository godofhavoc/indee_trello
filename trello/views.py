from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Task

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class CategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(
            user = request.user).order_by('priority')
        data = CategorySerializer(categories, many=True).data

        return Response(data)
    
    def post(self, request, cat_id=None):
        name, priority = [request.data[val] for val in ('name', 'priority')]

        if cat_id:
            category = Category.objects.get(id=cat_id)
            category.name = name
            category.priority = priority
            category.save()
        else:
            # print(request.data)
            Category.objects.create(
                user=request.user, name=name, priority=priority)

        categories = Category.objects.filter(
            user=request.user).order_by('priority')
        data = CategorySerializer(categories, many=True).data

        return Response(data)


class TaskView(APIView):
    def get(self, request):
        if request.category:
            tasks = Task.objects.filter(category=request.data['category'])
        else:
            tasks = Task.objects.filter(category__user=request.user)

        data = TaskSerializer(tasks, many=True).data

        return Response(data)

    def post(self, request, task_id=None):
        category, title, description = [request.data[val]
                                        for val in ('category', 'title', 'description')]
                                        
        if task_id:
            task = Task.objects.get(id=task_id)
            task.category = category
            task.title = title
            task.description = description
        else:
            task = Task.objects.create(
                category=category, title=title, description=description)

        tasks = Task.objects.filter(category=request.category)
        data = TaskSerializer(tasks, many=True).data

        return Response(data)
