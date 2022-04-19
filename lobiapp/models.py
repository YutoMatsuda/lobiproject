from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=20)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    image = models.ImageField(blank=True, upload_to='')
    profile = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Group(models.Model):
    PUBLIC = 0
    PRIVATE = 1
    SECRET_CHOICES = ((PUBLIC, '公開'),(PRIVATE,'プライベート'))
    name = models.CharField(max_length=40)
    secret = models.IntegerField(choices=SECRET_CHOICES, default=PUBLIC)
    image = models.ImageField(upload_to='')
    memo = models.TextField(blank=True)
    leader = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ManyToManyField(MyUser)

class ChatMessage(models.Model):
    chat = models.TextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatReply(models.Model):
    chat = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to='')

class Meta:
    ordering = ['-created_at']

def __str__(self):
    return self.reply

class ChatBookmark(models.Model):
    chat = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

class Evaluation(models.Model):
    GOOD = 0
    BAD = 1
    EVALUATION_CHOICES = ((GOOD, '高評価'), (BAD, '低評価'))
    chat = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    evaluation = models.IntegerField(choices=EVALUATION_CHOICES)