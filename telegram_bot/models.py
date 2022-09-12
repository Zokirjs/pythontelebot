from django.db import models

class BotUser(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    step = models.IntegerField(default=-1)
    file_id = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Foydalanuvchilar"
        verbose_name = "Foydalanuvchi"  

class RegisteredUser(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"  