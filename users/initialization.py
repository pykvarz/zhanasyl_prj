from django.contrib.auth.models import Group

# Создаем группу "Root"
root_group, created = Group.objects.get_or_create(name='Root')

# Создаем группу "User"
user_group, created = Group.objects.get_or_create(name='User')

has_key_group, created = Group.objects.get_or_create(name='User_has_key')




