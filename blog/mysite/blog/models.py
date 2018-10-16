from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id号")
    username = models.CharField(max_length=20, verbose_name="用户名称")
    nickname = models.CharField(max_length=50, verbose_name="用户昵称")
    password = models.CharField(max_length=60, verbose_name="用户密码")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    # 默认是0 表示男生， 1表示女生
    gender = models.BooleanField(default=0, verbose_name='性别')
    born = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    email = models.EmailField(max_length=255, verbose_name="用户邮箱")
    # header = models.CharField(max_length=255, default=True, verbose_name="用户头像")
    header = models.ImageField(upload_to='static/images/headers/', default='static/images/1.jpg', verbose_name="用户头像")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = '用户'

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="文章标题")
    # content = models.TextField(verbose_name="文章内容")
    content = UEditorField(verbose_name="文章内容")
    publicTime = models.DateTimeField(auto_now_add=True, verbose_name="发表时间")
    modifyTime = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    # 外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-publicTime"]
        # 末尾不加s
        verbose_name_plural = '文章'
        # 末尾加s
        # verbose_name = '文章'