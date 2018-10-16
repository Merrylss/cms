from django.contrib import admin

# Register your models here.

from .import models

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'age', 'nickname']
    list_per_page = 5

    # 增加和修改的属性
    fields = ["nickname", "age"]
    # 注意，fields 和 fieldsets 不能同时出现
    # fieldsets = [("base", {"fields": ["age", "birthday"]}),
    #              ("other", {"fields": ["name", "nickname"]}),
    #              ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Article)
