from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Todo


def index(request):
    return redirect('todo_list')


def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'hello/todo_list.html', {'todos': todos})


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            Todo.objects.create(title=title, description=description)
        return redirect('todo_list')
    return render(request, 'hello/todo_form.html', {'action': 'Create', 'todo': None})


def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        completed = request.POST.get('completed') == 'on'
        if title:
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.save()
        return redirect('todo_list')
    return render(request, 'hello/todo_form.html', {'action': 'Edit', 'todo': todo})


def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'hello/todo_confirm_delete.html', {'todo': todo})
