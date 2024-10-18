from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserAccountManager(BaseUserManager): 
    def create_user(self, email, password=None, user_type=None, **extra_fields): 
        if not email:
            raise ValueError('The Email field must be set')
        if not user_type:
            raise ValueError('The User Type field must be set')
        if user_type not in Account.user_types:
            raise ValueError('Invalid User Type')

        email = self.normalize_email(email)

        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', Account.Manager) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save()

        ManagerProfile.objects.create(user=user)
        # from .signals import user_account_saved
        # user_account_saved.send(sender=self.__class__, user=user, user_type=Account.SuperAdmin, created=True)

        return user

class Account(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)

    Manager = 1
    Operator = 2

    user_types = [Manager, Operator]

    user_type = models.PositiveSmallIntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = UserAccountManager()

    # class Meta:
    #     permissions = (
    #         ('assign_secteur_to_livreur', 'Can a secteur to a livreur'),
    #         ('change_livreur_days_off', 'Can change livreur days off'),
    #     )

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=255)
    machine_id = models.CharField(max_length=255, unique=True)
    operators = models.ManyToManyField(Account, related_name='teams')

class ManagerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='manager_profile')

class OperatorProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='operator_profile')
