import re
from django.shortcuts import render, HttpResponse, redirect
from user.models import User
from django.urls import reverse
from django.views.generic import View
from myblog.settings import base
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .forms import UserForm


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


class ChangeInfo(View):
    def get(self, request):
        """
        instance可以绑定原始数据到form（图片字段不会展示，只会展示网站），如果要把原始图片也绑定到表单
        则需要指定一个第二参数，用SimpleUploadedFile把图片转换一下，参考官网：
        https://docs.djangoproject.com/en/2.2/ref/forms/api/#binding-uploaded-files
        """
        form = UserForm(instance=request.user)
        return render(request, "user/change_userinfo.html", {"forms": form})

    def post(self, request):
        """
        上传的图片是作为文件保存在request.FILES中，其余表单数据保存在request.POST。
        官网意思是ImageField需要比普通Filed多绑定文件数据，文件数据和表单数据是分开
        处理的，所以实例化一个form时需要指定两个参数（即表单数据和文件数据）。
        参考官网form基础使用那里：https://docs.djangoproject.com/en/2.2/topics/forms/#more-on-fields
        """
        form = UserForm(request.POST, request.FILES, instance=request.user)  # This is called “binding data to the form” (it is now a bound form)（官网form overview那里）
        if form.is_valid():
            form.save()
            return redirect(reverse("userinfo"))  # 修改成功重定向到资料页
        else:
            content = {
                "forms": form,
                "msg": "操作失败，请正确填写！"
            }
            return render(request, "user/change_userinfo.html", content)

