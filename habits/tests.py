from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Reward, Habit
from users.models import User


class HabitOwnerTestCase(APITestCase):
    """Класс для тестирования модели Привычки с пользователем-владельцем"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', password='qwerty', telegram_chat_id=1710780709)

        self.reward = Reward.objects.create(pk=1, title='test reward', description='test desc')
        self.habit = Habit.objects.create(pk=1, owner=self.user, related_habit=None, reward=self.reward, is_pleasant=False,
                                          is_public=True, activity='присесть 10 раз', time='15:00:00', place='home',
                                          duration='60', periodicity="Раз в день")
        self.client.force_authenticate(user=self.user)

    def test_habit_public_list(self):
        """Тест на получение списка публичных привычек"""
        url = reverse('habits:habit_public_list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()[0].get('activity'),
            self.habit.activity
        )
        self.assertTrue(
            response.json()[0].get('reward'),
        )

    def test_habit_owner_list(self):
        """Тест на получение списка привычек пользователя с пагинацией"""
        url = reverse('habits:habit_owner_list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('count'),
            1
        )
        self.assertEqual(
            response.json().get('results')[0].get('duration'),
            '00:01:00'
        )

    def test_habit_retrieve(self):
        """Тест на получение отдельной привычки"""
        url = reverse('habits:habit_retrieve', args=(self.habit.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('place'),
            self.habit.place
        )

    def test_habit_update(self):
        """Тест на обновление привычки"""
        url = reverse('habits:habit_update', args=(self.habit.pk,))
        data = {
            'place': 'park',
            'duration': '90'
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('place'),
            'park'
        )
        self.assertEqual(
            response.json().get('duration'),
            '00:01:30'
        )

    def test_habit_delete(self):
        """Тест на удаление привычки"""
        url = reverse('habits:habit_delete', args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Habit.objects.all().count(),
            0
        )

    def test_habit_create(self):
        """Тест на создание привычки"""
        url = reverse('habits:habit_create')
        data = {
            'activity': 'пробежать вокруг дома',
            'periodicity': "Раз в четыре дня"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json().get('activity'),
            'пробежать вокруг дома'
        )
        self.assertEqual(
            response.json().get('duration'),
            None
        )
        self.assertEqual(
            response.json().get('owner'),
            self.user.pk
        )
        self.assertFalse(
            response.json().get('is_public'),
        )

    def test_habit_create_validators(self):
        url = reverse('habits:habit_create')
        Habit.objects.create(pk=10, activity='pleasant test', is_pleasant=True)
        data = {
            "activity": 'useful test',
            "reward": 1,
            "related_habit": 10
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json().get('non_field_errors'),
            ['У привычки может быть только вознаграждение или только связанная привычка, не оба пункта вместе']
        )

        data2 = {
            "activity": 'useful test',
            "duration": "150"
        }
        response2 = self.client.post(url, data2)

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response2.json().get('non_field_errors'),
            ['Продолжительность привычки не может быть больше 120 секунд']
        )

        data3 = {
            "activity": 'useful test',
            "related_habit": 1
        }
        response3 = self.client.post(url, data3)

        self.assertEqual(
            response3.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response3.json().get('non_field_errors'),
            ['В связанные привычки можно указывать только приятные привычки']
        )

        data4 = {
            "activity": 'useful test',
            "is_pleasant": True,
            "reward": 1
        }
        response4 = self.client.post(url, data4)

        self.assertEqual(
            response4.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response4.json().get('non_field_errors'),
            ['У приятной привычки не может быть вознаграждения или связанной привычки']
        )


class HabitNotOwnerTestCase(APITestCase):
    """Класс для тестирования модели Привычки с пользователем НЕ владельцем"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', password='qwerty', telegram_chat_id=1710780709)
        self.user2 = User.objects.create(email='test2@mail.ru', password='123456', telegram_chat_id=1710780710)

        self.reward = Reward.objects.create(title='test reward', description='test desc')
        self.habit = Habit.objects.create(owner=self.user, related_habit=None, reward=self.reward, is_pleasant=False,
                                          is_public=True, activity='присесть 10 раз', time='15:00:00', place='home',
                                          duration='60', periodicity="Раз в день")
        self.client.force_authenticate(user=self.user2)

    def test_habit_public_list(self):
        """Тест на получение списка публичных привычек"""
        url = reverse('habits:habit_public_list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()[0].get('activity'),
            self.habit.activity
        )
        self.assertTrue(
            response.json()[0].get('reward'),
        )

    def test_habit_owner_list(self):
        """Тест на получение списка привычек пользователя с пагинацией"""
        url = reverse('habits:habit_owner_list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('count'),
            0
        )

    def test_habit_retrieve(self):
        """Тест на получение отдельной привычки"""
        url = reverse('habits:habit_retrieve', args=(self.habit.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_update(self):
        """Тест на обновление привычки"""
        url = reverse('habits:habit_update', args=(self.habit.pk,))
        data = {
            'place': 'park',
            'duration': '90'
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_delete(self):
        """Тест на удаление привычки"""
        url = reverse('habits:habit_delete', args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_create(self):
        """Тест на создание привычки"""
        url = reverse('habits:habit_create')
        data = {
            'activity': 'пробежать вокруг дома',
            'periodicity': "Раз в четыре дня"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json().get('activity'),
            'пробежать вокруг дома'
        )
        self.assertEqual(
            response.json().get('owner'),
            self.user2.pk
        )
        self.assertFalse(
            response.json().get('is_public'),
        )


class RewardTestCase(APITestCase):
    """ Класс для тестирования модели Награды """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', password='qwerty', telegram_chat_id=1710780709)

        self.reward = Reward.objects.create(title='Торт', description='Можно съест торт')
        self.client.force_authenticate(user=self.user)

    def test_reward_create(self):
        """ Тест на создание награды """
        url = '/rewards/'
        data = {
            'title': 'новая наклейка на ноут',
            'description': 'можно достать новую наклейку и приклеить к своему ноуту'
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.json().get('title'),
            'новая наклейка на ноут'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_reward_list(self):
        """ Тест на получения спсика наград """
        url = '/rewards/'
        response = self.client.get(url)

        self.assertEqual(
            response.json()[0].get('description'),
            'Можно съест торт'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            Reward.objects.all().count(),
            1
        )

    def test_reward_retrieve(self):
        """ Тест на получение информации о конкретной награде """
        url = f'/rewards/{self.reward.pk}/'
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('title'),
            'Торт'
        )

    def test_reward_update(self):
        """ Тест на обновление награды """
        url = f'/rewards/{self.reward.pk}/'
        data = {
            'title': 'Пирожок'
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('title'),
            'Пирожок'
        )

    def test_reward_delete(self):
        """ Тест на удаление награды """
        url = f'/rewards/{self.reward.pk}/'
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Reward.objects.all().count(),
            0
        )
