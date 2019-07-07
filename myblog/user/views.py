import re
from django.shortcuts import render, HttpResponse, redirect
from user.models import User
from django.urls import reverse
from django.views.generic import View
from myblog.settings import base
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class RegisterView(View):
    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):
        user_name = request.POST.get("user_name")
        passwd = request.POST.get("pwd")
        cpasswd = request.POST.get("cpwd")
        email = request.POST.get("email")

        if not all([user_name, passwd, cpasswd, email]):
            return render(request, "user/register.html", {"msg": "信息填写不完整"})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, "user/register.html", {"msg": "邮箱格式不正确"})

        if passwd != cpasswd:
            return render(request, "user/register.html", {"msg": "两次密码填写不一致"})

        try:
            User.objects.get(username=user_name)
            return render(request, "user/register.html", {"msg": "用户名已存在"})
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(user_name, email, passwd)
        user.is_active = 1  # 暂时未开启邮箱验证，默认注册用户全部已激活
        user.save()

        userlogin = authenticate(username=user_name, password=passwd)
        login(request, userlogin)  # 让刚注册的用户登陆，否则user.is_authticated=false，导致无法跳转到正常已登陆页面

        return redirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        if "username" in request.COOKIES:
            username = request.COOKIES.get("user_name")
            remember = {"username": "value=%s" % username, "checked": "checked"}
        else:
            remember = {"username": "", "checked": ""}
        return render(request, "user/login.html", remember)

    def post(self, request):
        username = request.POST.get("user_name")
        passwd = request.POST.get("pwd")

        user = authenticate(username=username, password=passwd)
        if user is not None:
            if user.is_active == 1:
                login(request, user)  # 设置session信息等
                # 若没登陆，则跳转到登录页，且url会传入?next=“当前访问页面的url”
                next_url = request.GET.get('next', reverse('index'))  # 如果有next参数，说明是别的页面跳转来的，没有next参数则说明是正常登录页提交的请求
                print(next_url + " : " + str(request.GET))
                response = redirect(next_url)  # 如果是跳转来登录页，则登录后还需要重定向到原来的页面
                remember = request.POST.get("remember")

                if remember == "on":
                    response.set_cookie("username", username, max_age=7*24*3600)
                else:
                    response.delete_cookie("username")

                return response
            else:
                return render(request, "user/login.html", {"msg": "账户未激活"})
        else:
            return render(request, "user/login.html", {"msg": "用户名或密码错误"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("index"))


class UserInfoView(View):
    def get(self, request):
        return render(request, "user/userinfo.html")
