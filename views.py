from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.utils import timezone
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Todo

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('home')  # Redirect already logged-in users

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()       # Save the user
#             login(request, user)     # Automatically log in the user
#             return redirect('home')  # Redirect to home page
#     else:
#         form = UserCreationForm()

#     return render(request, 'tasks/signup.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')  # after logout go to login page

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Automatically log in the user
        login(request, user)

        # Redirect to home page
        return redirect('home')

    return render(request, 'tasks/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # after logout go to login page

@login_required
def home(request):
    today = timezone.localdate()

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        if not date:
            date = today
        else:
            date = timezone.datetime.strptime(date, '%Y-%m-%d').date()

        Todo.objects.create(user=request.user, title=title, description=description, date=date)
        return redirect('home')

    # Get the date filter from GET parameters (optional)
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        except:
            selected_date = today
    else:
        selected_date = today

    tasks = Todo.objects.filter(user=request.user, date=selected_date).order_by('id')

    context = {
        'tasks': tasks,
        'today': today,
        'selected_date': selected_date,
    }
    return render(request, 'tasks/home.html', context)

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Todo.objects.create(user=request.user, title=title, description=description)
        return redirect('home')
    return render(request, 'tasks/home.html')

@login_required
def update_todo(request, id):
    todo = Todo.objects.get(id=id)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.completed = 'completed' in request.POST
        todo.save()
        return redirect('home')
    return render(request, 'tasks/home.html', {'todo': todo})

@login_required
def delete_todo(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('home')


@login_required
def add_task_ajax(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        if title:
            task = Todo.objects.create(user=request.user, title=title, description=description)
            return JsonResponse({
                "id": task.id,
                "title": task.title,
                "description": task.description,
            })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def completed_tasks(request):
    completed = Todo.objects.filter(user=request.user, completed=True)  # ✅ only completed
    return render(request, 'tasks/completed_tasks.html', {'completed': completed})


@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    task.completed = not task.completed  # flip between True/False
    task.save()
    return redirect('home')  # back to homepage

def upcoming_tasks(request):
    # Get all upcoming tasks
    tasks = Todo.objects.filter(date__gte=timezone.now()).order_by('date')
    
    # Group tasks by date
    grouped_tasks = defaultdict(list)
    for task in tasks:
        grouped_tasks[task.date].append(task)
    
    # Convert to sorted list of tuples for template
    grouped_tasks = sorted(grouped_tasks.items())
    
    return render(request, 'tasks/upcoming_tasks.html', {'grouped_tasks': grouped_tasks})

def today_tasks(request):
    today = timezone.now().date()
    tasks_today = Todo.objects.filter(date=today)
    return render(request, 'tasks/today_tasks.html', {'tasks_today': tasks_today})