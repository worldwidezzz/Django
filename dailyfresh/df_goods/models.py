from __future__ import unicode_literals
from django.db import models
from tinymce.models import HTMLField


# 商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')


# 商品
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    # 图片位置
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 单位
    gunit = models.CharField(max_length=20, default='500g')
    # 点击量　用于排序
    gclick = models.IntegerField()
    # 简介
    gjianjie = models.CharField(max_length=200)
    # 库存
    gkucun = models.IntegerField()
    # 详细介绍
    gcontent = HTMLField()
    # 创建一个外键
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.gtitle.encode('utf-8')
