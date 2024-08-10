from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_for_invalid_user(email="invalid_email", password="invalid_password"):
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа равен 403
    assert status == 403

def test_get_all_pets_with_invalid_key():
    invalid_auth_key = {'key': 'invalid_auth_key'}

    status, result = pf.get_list_of_pets(invalid_auth_key)

    assert status == 403

def test_add_new_pet_with_missing_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    name = ''
    animal_type = 'двортерьер'
    age = '4'

    with pytest.raises(Exception):
        _, _ = pf.add_new_pet(auth_key, name=name, animal_type=animal_type, age=age)

def test_successful_upload_photo():

    _, auth_key = pf.get_api_ky(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        image_path = os.path.join(os.path.dirname(__file__), 'images/cat1.jpg')

        response_code, result = pf.upload_pet_photo(pet_id, image_path)

    assert response_code == 200

def test_delete_pet_with_invalid():
    invalid_auth_key = {'key': 'invalid_auth_key'}

    _, my_pets = pf.get_list_of_pets(invalid_auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pet(invalid_auth_key, pet_id)

    assert status == 403