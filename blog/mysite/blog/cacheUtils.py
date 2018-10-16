from django.core.cache import cache

from . import models

def get_all_article(change=False):
    """
    缓存所有文章
    :return:
    """
    print("获取缓存数据")
    # 获取所有文章
    articles = cache.get("allArticle")
    # 如果文章为空，则从数据库获取文章
    if articles is None or change:
        print("缓存中没有，从数据库查询。。")
        articles = models.Article.objects.all()
        print("获取到数据，将数据同步到缓存中。。")
        cache.set("allArticle", articles)

    # 返回缓存中的文章
    return articles