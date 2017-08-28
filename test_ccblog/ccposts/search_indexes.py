#coding:utf-8
import datetime
from haystack import indexes
from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    last_modified_time = indexes.DateTimeField(model_attr='last_modified_time')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self):
        return self.get_model().objects.all()
