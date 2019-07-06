import mistune
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.widgets.Input(
            attrs={"class": "form-control", "style": "width:30%"}
        )
    )

    email = forms.CharField(
        label="Email",
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={"class": "form-control", "style": "width:30%"}
        )
    )

    # website = forms.CharField(
    #     label="网站",
    #     max_length=100,
    #     widget=forms.widgets.URLInput(
    #         attrs={"class": "form-control", "style": "width:60%"}
    #     )
    # )

    content = forms.CharField(
        label="内容",
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={"rows": 6, "cols": 60, "class": "form-control", "style": "width: 60%"}
        )
    )

    def clean_content(self):
        """获取content字段被清洗过后的数据（content作为后缀，指定content字段）"""
        content = self.cleaned_data.get("content")
        if len(content) < 10:
            raise forms.ValidationError("内容长度太短了")
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ["nickname", "email", "content"]









































