import xadmin

# Register your models here.
from xadmin import views
from .import models

class UserAdmin(object):
    list_display = ['username', 'age', 'nickname']
    list_per_page = 5

    # 增加和修改的属性
    fields = ["nickname", "age"]
    # 注意，fields 和 fieldsets 不能同时出现
    # fieldsets = [("base", {"fields": ["age", "birthday"]}),
    #              ("other", {"fields": ["name", "nickname"]}),
    #              ]

class ArticleAdmin(object):
    list_display = ['title', 'author']
    list_per_page = 5
    list_editable = ['title']


class GlobalSetting(object):
    site_title = "博客后台管理系统"
    site_footer = "2018@lss.com"
    menu_style = "accordion"

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(models.User, UserAdmin)
xadmin.site.register(models.Article, ArticleAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
