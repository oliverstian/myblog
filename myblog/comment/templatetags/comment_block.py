from django import template

from comment.forms import CommentForm
from comment.models import Comment, ArticleComment

register = template.Library()


@register.inclusion_tag("comment/block.html")
def comment_block(target):
    return{
        "target": target,
        "comment_form": CommentForm(),
        "comment_list": Comment.get_by_target(target)
    }


@register.simple_tag
def total_parent_comment(article):
    return article.article_comments.filter(status=ArticleComment.STATUS_NORMAL).filter(parent=None)


@register.simple_tag
def total_comment_num(article):
    return article.article_comments.filter(status=ArticleComment.STATUS_NORMAL).count()


@register.simple_tag
def total_child_comment(pcomment):
    """找到父评论对应的所有子评论,自关联"""
    return pcomment.articlecomment_child_comments.filter(status=ArticleComment.STATUS_NORMAL)


@register.simple_tag
def total_user_num(article):
    """获取几人参与评论"""
    user = []
    comments = article.article_comments.filter(status=ArticleComment.STATUS_NORMAL)
    for comment in comments:
        if comment.author not in user:
            user.append(comment.author)
    return len(user)


@register.simple_tag
def shorttime(longtime):
    return str(longtime).split(" ")[0]






















