
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.db import models

# class UserManager(BaseUserManager):
# 	def create_user(self, username, password=None, **extra_fields):
# 		if not username:
# 			raise ValueError('The Username must be set')
# 		user = self.model(username=username, **extra_fields)
# 		user.set_password(password)
# 		user.save(using=self._db)
# 		return user

# 	def create_superuser(self, username, password=None, **extra_fields):
# 		extra_fields.setdefault('role', 'Admin')
# 		extra_fields.setdefault('is_staff', True)
# 		extra_fields.setdefault('is_superuser', True)
# 		return self.create_user(username, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
# 	ROLE_CHOICES = (
# 		('Admin', 'Admin'),
# 		('Staff', 'Staff'),
# 	)
# 	name = models.CharField(max_length=100)
# 	employee_id = models.CharField(max_length=50, unique=True)
# 	date_of_joining = models.DateField()
# 	username = models.CharField(max_length=150, unique=True)
# 	password = models.CharField(max_length=128)
# 	address = models.TextField()
# 	phone_number = models.CharField(max_length=20)
# 	role = models.CharField(max_length=10, choices=ROLE_CHOICES)
# 	is_active = models.BooleanField(default=True)
# 	is_staff = models.BooleanField(default=False)

# 	USERNAME_FIELD = 'username'
# 	REQUIRED_FIELDS = ['name', 'employee_id', 'date_of_joining', 'address', 'phone_number', 'role']

# 	objects = UserManager()


# 	def __str__(self):
# 		return self.username


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    # Basic Info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()

    # Login Info
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)  # ✅ added email field
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    # Contact Info
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    # Additional Info
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'employee_id', 'date_of_joining', 'address', 'phone_number', 'role']

    objects = UserManager()

    def __str__(self):
        return self.username


# StockOpening model
class StockOpening(models.Model):
	medal = models.CharField(max_length=100)
	item = models.CharField(max_length=100)
	final_weight = models.DecimalField(max_digits=10, decimal_places=2)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.medal} - {self.item}"


from django.db import models
from django.conf import settings


class UserDocuments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='user_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.document_name}"

# todoapp/models.py

# This block should NOT be in serializers.py
from django.db import models

class TodoTask(models.Model):
    task = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task