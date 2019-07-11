
class BaseOwnerXadmin(object):  # 继承object
    """
    1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
    2、用来针对queryset过滤当前用户的数据
    """
    # fields = ("...", "...")  # 界面显示出的需要用户编辑的字段，有些字段没必要用户填写或 null=true
    exclude = ("owner", )  # 跟fields相反洛，“排除之意”

    def get_list_queryset(self):  # 只展示当前作者的文章（无权修改他人文章）
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):  # new_obj就是当前实例（比如新增文章的实例）
        self.new_obj.owner = self.request.user
        return super(BaseOwnerXadmin, self).save_models()




















