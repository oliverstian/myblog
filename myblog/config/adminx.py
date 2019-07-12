import xadmin
from config.models import Link, SideBar


@xadmin.sites.register(Link)
class LinkAdmin(object):
    list_display = ("title", "href", "status", "weight", "create_time")
    fields = ("title", "href", "status", "weight")

    def save_models(self):  # new_obj就是当前实例（比如新增文章的实例）
        self.new_obj.owner = self.request.user
        return super().save_models()  # 这里不能用super(LinkAdmin， self).save_models()，不知何故


@xadmin.sites.register(SideBar)
class SideBarAdmin(object):
    list_display = ("title", "display_type", "content", "created_time")
    fields = ("title", "display_type", "content")

    def save_models(self):  # new_obj就是当前实例（比如新增文章的实例）
        self.new_obj.owner = self.request.user
        return super().save_models()




















