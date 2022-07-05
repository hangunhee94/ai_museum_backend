from django.contrib import admin

from .models import Article as ArticleModel
from .models import Comment as CommentModel

# Register your models here.
admin.site.register(ArticleModel)
admin.site.register(CommentModel)