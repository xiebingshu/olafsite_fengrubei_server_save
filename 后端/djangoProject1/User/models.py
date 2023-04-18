from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="用户名", db_index=True)
    password = models.CharField(max_length=64,verbose_name="密码")
    emailbox = models.CharField(max_length=64,verbose_name="邮箱")

    def __str__(self):
        return self.name