from django.shortcuts import redirect
from django.views.generic import TemplateView
from blog.models import Article
from comment.models import ArticleComment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import CommentForm


@login_required
@require_POST
def add_comment_view(request):
    if request.is_ajax():
        data = request.POST
        new_user = request.user
        new_content = data.get('content')
        article_id = data.get('article_id')
        rep_id = data.get('rep_id')
        the_article = Article.objects.get(id=article_id)
        if not rep_id:
            new_comment = ArticleComment(author=new_user, content=new_content, belong=the_article,
                                         rep_to=None)
        else:
            new_rep_to = ArticleComment.objects.get(id=rep_id)
            new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
            new_comment = ArticleComment(author=new_user, content=new_content, belong=the_article, parent=new_parent,
                                         rep_to=new_rep_to)
        new_comment.save()
        new_point = '#comment-id-' + str(new_comment.id)
        return JsonResponse({'msg': '评论提交成功！', "new_point": new_point})
    return JsonResponse({'msg': '评论失败！'})


# class CommentView(TemplateView):
#     http_method_names = ["post"]  # 重写了View类的http_method_names，只允许post方法
#     template_name = "comment/result.html"
#
#     def post(self, request, *args, **kwargs):
#         comment_form = CommentForm(request.POST)  # 新建CommentForm实例，并将其用POST数据填充
#         target = request.POST.get("target")
#
#         if comment_form.is_valid():
#             instance = comment_form.save(commit=False)
#             instance.target = target
#             instance.save()
#             succeed = True
#             return redirect(target)
#         else:
#             succeed = False
#
#         context = {
#             "succeed": succeed,
#             "form": comment_form,
#             "target": target,
#         }
#         return self.render_to_response(context)
































