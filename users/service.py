import json
from users.models import CustomUser
from django.contrib.auth.models import Group


# def test_func(self):
#     return not self.request.user.groups.filter(pk=self.group_id)
def add_perm(user_id, group_id):
    user = CustomUser.objects.get(id=user_id)
    user.groups.add(group_id)
# def add_perm(user_id, group_id):
#     try:
#         user = CustomUser.objects.get(id=user_id)
#         group = Group.objects.get(id=group_id)
#         user.groups.add(group)
#     except CustomUser.DoesNotExist:
#         print(f"Пользователь с id={user_id} не найден.")
#     except Group.DoesNotExist:
#         print(f"Группа с id={group_id} не найдена.")
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")


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
