from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ["post"]  # 重写了View类的http_method_names，只允许post方法
    template_name = "comment/result.html"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)  # 新建CommentForm实例，并将其用POST数据填充
        target = request.POST.get("target")

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            "succeed": succeed,
            "form": comment_form,
            "target": target,
        }
        return self.render_to_response(context)
































