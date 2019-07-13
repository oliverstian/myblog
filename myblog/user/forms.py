from django import forms
from .models import User
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserForm(forms.ModelForm):
    website = forms.URLField(
        label="更改网站",
        max_length=100,
        required=False,  # 有些字段可以为空，不写这个false提交时将报错
        widget=forms.widgets.URLInput(
            attrs={"placeholder": "http(s) 可为空", "class": "form-control mb-2", "style": "width:60%"}
        )
    )

    avatar = ProcessedImageField(spec_id='user:User:avatar',  # 不知道干嘛的，可以看下源码contribute_to_class()这个函数干嘛的
                                 processors=[ResizeToFill(80, 80)],
                                 format='PNG',
                                 options={'quality': 60},
                                 label="更改头像",
                                 required=False,
                                 widget=forms.widgets.FileInput(attrs={"class": "d-block"}),
                                 )

    def clean_content(self):
        """
        获取content字段被清洗过后的数据（content作为后缀，指定content字段）。
        非本form类使用的函数，保留作为参考。is_validate校验过后的表单数据会
        传递给cleaned_data属性
        """
        content = self.cleaned_data.get("content")
        if len(content) < 10:
            raise forms.ValidationError("内容长度太短了")
        # content = mistune.markdown(content)
        return content

    class Meta:
        model = User
        fields = ["website", "avatar"]









































