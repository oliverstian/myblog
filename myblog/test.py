# class CommonViewMixin:
#     def get_context_date(self):
#         print("enter CommonViewMixin..self is %s" % self)
#         super(CommonViewMixin, self).get_context_date()
#
#     def __str__(self):
#         return "CommonViewMixin"
#
#
# class ContextMixin:
#     def get_context_date(self):
#         print("enter ContextMixin..self is %s" % self)
#
#     def __str__(self):
#         return "ContextMixin"
#
#
# class MultipleObjectMixin(ContextMixin):
#     def get_context_date(self):
#         print("enter MultipleObjectMixin..self is %s" % self)
#         return super(MultipleObjectMixin, self).get_context_date()
#
#     def __str__(self):
#         return "MultipleObjectMixin"
#
#
# class BaseListView(MultipleObjectMixin):
#     def get(self):
#         self.get_context_date()
#
#     def __str__(self):
#         return "BaseListView"
#
#
# class IndexView(CommonViewMixin, BaseListView):
#     def __init__(self):
#         self.get()
#
#     def __str__(self):
#         return "IndexView"
#
#
# indexview = IndexView()


# class Test:
#     def __init__(self):
#         print("start to init..")
#
#     @classmethod
#     def run(cls):
#         print("i am running..")
#
#
# Test.run()

def func1():
    print("func1")


def func2():
    print("func2")


test_ls = [
    func1(),
    func2(),
]

















