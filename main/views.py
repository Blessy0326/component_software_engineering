
from django.shortcuts import render, redirect
import importlib

def login_view(request):
    return render(request, 'login.html')

def login_logic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin@gmail.com' and password == 'pass123':
            request.session['logged_in'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('index')

PROTECTED_PAGES = [
    'admin_dashboard', 'manage_users', 'provider_dashboard',
    'edit_client_profile', 'edit_provider_profile'
]

def page_view(request, page):
    if page in PROTECTED_PAGES and not request.session.get('logged_in'):
        return redirect('login')

    try:
        logic_module = importlib.import_module(f"main.pojos.{page}")
        context = logic_module.get_context() if hasattr(logic_module, 'get_context') else {}
    except ModuleNotFoundError:
        context = {}
    return render(request, f"{page}.html", context)
