from django.db import models

# Create your models here.


class MissionInfo(models.Model):
    user_project = models.CharField(max_length=96, verbose_name="用户_项目名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="任务名称", db_index=True)
    discription = models.CharField(max_length=500, verbose_name="任务描述")
    text = models.CharField(max_length=5000, verbose_name="上传文本")

    def __str__(self):
        return self.name

class Missions(models.Model):
    user_project = models.CharField(max_length=96, verbose_name="用户_项目名", db_index=True)
    name = models.CharField(max_length=64, verbose_name="任务名称", db_index=True)
    discription = models.CharField(max_length=500, verbose_name="任务描述")
    text = models.CharField(max_length=5000, verbose_name="上传文本")

    def __str__(self):
        return self.name
