from datetime import date
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Article, Tag, Category
from config.models import SideBar, Link
from django.views.generic import DetailView, ListView
from django.db.models import Q, F

from comment.models import Comment
from comment.forms import CommentForm

from django.core.cache import cache


class CommonViewMixin:
    """把侧边栏数据获取放到context中，因为很多页面都共用这些数据"""
    def get_context_data(self, **kwargs):
        context = super(CommonViewMixin, self).get_context_data(**kwargs)
        context.update({
            # "sidebars": SideBar.get_all()  # 把所有需要显示的侧栏数据行都拿到
            "latest_articles": Article.get_newest_article(),  # 获取最新文章
            "hot_articles": Article.hot_article(),  # 获取最热文章
            "all_tags": Tag.get_all(),  # 获取所有标签
            "friend_links": Link.get_all(),  # 获取所有友链
        })
        context.update(Category.get_navs())  # 把上导航和下导航的数据拿到
        return context


class IndexView(CommonViewMixin, ListView):
    """
    对比上面的article_list()，相似的功能（这里还加了分页功能）代码却少了很多。
    之所以代码少，是因为ListView里面实现了get方法，只需要人为地设置少量参数，ListView
    自动将选数据，渲染数据，返回response全包干了
    """
    queryset = Article.latest_article()  # 如果指定model=Article，等价于queryset = Article.objects.all()
    paginate_by = 5
    context_object_name = "article_ls"  # 模板中使用的变量名(即context={"article_ls": queryset})
    template_name = "blog/list.html"


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")  # 就是url解析器捕获的关键字参数
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            "category": category,
        })
        return context

    def get_queryset(self):
        """
        根据分类过滤
        就是重写MultipleObjectMixin的get_queryset,该方法在BaseListView的get方法中被调用
        该方法作用就是根据用户重写的queryset属性取出所有的数据对象，如果用户没有重写queryset
        那就是取出所有数据，源码一目了然。
        或者这个函数也可以用以下两行代替：
        category_id = self.kwargs.get("category_id") # 这行需插入到get方法，不合理
        queryset = Category.object.filter(category_id=category_id)

        注意这里queryset是继承了IndexView中的queryset = Article.latest_article()
        """
        queryset = super(CategoryView, self).get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)  # 取出分类下的所有文章


class TagView(IndexView):  # 逻辑跟CategoryView一样
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            "tag": tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据标签过滤"""
        queryset = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get("tag_id")
        """
        跨关系查找都是双下划线+对方字段名。再如tag__status。容易混淆就是那个owner = models.ForeignKey()字段，
        数据库中保存该字段是owner_id，这是数据库中就保存了owner_id字段名，用来代表外键的主键，上面说的那是跨关系查找了。
        考虑这两种查找效果一样：user__id=1和owner_id=1，都是表示关联表中id=1的数据行
        """
        return queryset.filter(tag__id=tag_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        context.update({
            "keyword": self.request.GET.get("keyword", "")
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get("keyword")
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get("owner_id")
        return queryset.filter(owner_id=author_id)


class ArticleDetailView(CommonViewMixin, DetailView):
    # model = Article
    queryset = Article.latest_article()
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = "article_id"

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = "pv:%s:%s" % (uid, self.request.path)
        uv_key = "uv:%s:%s:%s" % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 一分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24*60*60)  # 24小时有效

        if increase_pv and increase_uv:  # 避免短时间内重复访问也算访问量
            Article.objects.filter(pk=self.object.id).update(pv=F("pv") + 1,
                                                             uv=F("uv") + 1)
        elif increase_pv:
            Article.objects.filter(pk=self.object.id).update(pv=F("pv") + 1)
        elif increase_uv:
            Article.objects.filter(pk=self.object.id).update(uv=F("uv") + 1)


class ArticleListView(ListView):
    queryset = Article.latest_article()
    paginate_by = 1  # 设置分页，每页数量为1
    context_object_name = "article_ls"  # 设置模板中使用的变量名
    template_name = "blog/list.html"









































