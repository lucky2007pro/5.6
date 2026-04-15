from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm
from .models import CustomUser


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            return redirect('index')
        # Keep the same template for both GET and invalid POST states.
        return render(request, 'registration/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm(request=request)
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile", id=user.id)
        return render(request,"registration/login.html",{"form": form}, )


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        profile_user = get_object_or_404(CustomUser, id=id)

        # Keep profile pages private to the owner for now.
        if request.user.id != profile_user.id:
            messages.warning(request, "Faqat o'zingizning profilingizni ko'ra olasiz")
            return redirect('profile', id=request.user.id)

        return render(request, "profile.html", {
            'profile_section_title': 'My products',
            'profile_mode': 'products',
            'profile_items': profile_user.products.all(),
        })
