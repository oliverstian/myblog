# from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget  # 这个wiget没有上传图片功能

from django import forms

from .models import Category, Tag, Article


class ArticleAdminForm(forms.ModelForm):
    """覆盖默认的form field"""
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)  # required=False对应model中的blank=True
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        # widget=autocomplete.ModelSelect2(url='category-autocomplete'),  # 这个是django-autocomplete-light的内容
        label='分类',  # 对应model中的verbose_name
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        # widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article  # 指定该form对应哪个model，如果不覆盖上面的字段，那将使用默认的字段设置（model映射到form有默认字段映射关系）
        fields = (
            'category', 'tag', 'desc', 'title',
            'is_md', 'content', 'content_md', 'content_ck',
            'status'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:  # 当前文章的实例，这里意思是点进某篇文章编辑页，框中应显示原文
            if instance.is_md:
                initial['content_md'] = instance.content  # 初始化字段，如果是md，则初始化conten_md字段（注意这个字段不存在于model中）
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        """
        每个model form实例都包含一个实例属性以提供一些操作相应的model的方法，比如这个
        model form提供的clean方法，实际是model类中的clean方法，这个方法使用户自定义
        一些校验规则，在save()方法调用之后调用clean()，具体再看官网。
        """
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)  # 此处保存到将内容保存到content
        if not content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js', )  # 意思是会在相应的HTML页面中增加一个<link href="{{ static 'js/post_editor.js' }}">


# from django import forms
#
#
# class ArticleAdminForm(forms.ModelForm):
#     desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)
