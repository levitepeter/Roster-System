from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name,email,phonenumber,is_soundhead,is_setuphead,is_teamadmin,is_active, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            phonenumber = phonenumber,
            is_soundhead=is_soundhead,
            is_setuphead=is_setuphead,
            is_teamadmin = is_teamadmin,
            is_active = is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name,email,phonenumber,is_soundhead,is_setuphead,is_teamadmin,is_active, password=None):
        user = self.create_user(
        	name=name,
            email=email,
            password=password,
            phonenumber=phonenumber,
            is_soundhead=is_soundhead,
            is_setuphead=is_setuphead,
            is_teamadmin = True,
            is_active = is_active,

        )
        user.is_superuser = True
        user.save(using=self._db)
        return user