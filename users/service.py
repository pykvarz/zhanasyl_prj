from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
import json

from users.models import CustomUser


def add_perm(user_id, p_id):
    user = CustomUser.objects.get(id=user_id)
    user.user_permissions.add(p_id)


def check_key(key, file_path='C:/Users/tech/Desktop/ppp/generated_keys.json'):
    # Открываем файл и загружаем JSON-данные
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    if key in data['keys']:
        data['keys'] = [item for item in data['keys'] if item != key]

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return True
    else:
        return False

