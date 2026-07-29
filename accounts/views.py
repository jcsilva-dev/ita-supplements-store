from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(
                request,
                'Sua conta foi criada com sucesso! Agora ela está aguardando aprovação '
                'do administrador. Assim que for aprovada, você poderá acessar o sistema normalmente.'
            )
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            messages.error(request, 'Usuário ou senha inválidos.')
        elif not user.is_active:
            messages.warning(request, 'Sua conta ainda está aguardando aprovação do administrador.')
        elif not user.check_password(password):
            messages.error(request, 'Usuário ou senha inválidos.')
        else:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('supplements')
            messages.error(request, 'Usuário ou senha inválidos.')

    login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('supplements')