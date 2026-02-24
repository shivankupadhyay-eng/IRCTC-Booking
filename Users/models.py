from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username=None
    first_name=models.CharField(max_length=30,blank=False)
    last_name=models.CharField(max_length=30,blank=True)
    email=models.EmailField(unique=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    objects= CustomUserManager()
