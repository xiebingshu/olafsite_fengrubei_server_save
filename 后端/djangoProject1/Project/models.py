from django.db import models

# Create your models here.

class ProjectInfo(models.Model):
    user = models.CharField(max_length=32, verbose_name="用户名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="项目名称", db_index=True)
    mood = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class EntityInfo(models.Model):
    user_project = models.CharField(max_length=96, verbose_name="用户_项目名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="实体名称", db_index=True)
    discription = models.CharField(max_length=500, verbose_name="实体描述")

    def __str__(self):
        return self.name


class DataInfo(models.Model):
    user_project = models.CharField(max_length=96, verbose_name="用户_项目名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="任务名称", db_index=True)
    type = models.IntegerField(default=0)
    discription = models.CharField(max_length=500, verbose_name="任务描述")
    text = models.CharField(max_length=5000, verbose_name="处理文本")

    def __str__(self):
        return self.name


class RelInfo(models.Model):
    user_project = models.CharField(max_length=96, verbose_name="用户_项目名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="关系名称", db_index=True)
    discription = models.CharField(max_length=500, verbose_name="关系描述")
    obj = models.CharField(max_length=500, verbose_name="关系主体", db_index=True)
    sub = models.CharField(max_length=500, verbose_name="关系客体", db_index=True)

    def __str__(self):
        return self.name

