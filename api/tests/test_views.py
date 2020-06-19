import datetime as dt
import json

import pytz
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Message, Recipient


class CreateNewMessageTest(APITestCase):
    url = reverse('sendmsg')

    def test_message_is_unique(self):
        self.recipient = Recipient.objects.create(username='Dev', service='viber')
        self.message = Message.objects.create(text='Hello, Dev, how are you?',
                                              deferred_time=dt.datetime.now(tz=pytz.UTC),
                                              status=3,
                                              recipients=self.recipient)
        unique_together = self.message._meta.unique_together
        self.assertEquals(unique_together[0], ('text', 'recipients',))

    def test_create_message_with_multiple_recipients(self):
        data = {
            "text": "Салам, Hello, Hola, Aloha, Shalom, Hola, Ciao, Ave, Lab dien, Guten Tag,"
                    " Goddag, Dzien dobry, Ola, Buna, Здраво, Dobryden, Салам алейкум, Привіт,"
                    " Bonjour, Namaste, Konnichi wa",
            "recipients": [
                {
                    "username": "Jhon",
                    "service": "telegram"
                },
                {
                    "username": "Jhon",
                    "service": "viber"
                }
            ],
            "deferred_time": "2020-06-18T9:41:00.000Z"
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 - cause 2 message objects for each recipient
        self.assertEqual(Message.objects.count(), 2)

    def test_create_message_with_single_recipient(self):
        data_listed = {
            "text": "Салам, Hello, Hola, Aloha, Shalom, Hola, Ciao, Ave, Lab dien, Guten Tag,"
                    " Goddag, Dzien dobry, Ola, Buna, Здраво, Dobryden, Салам алейкум, Привіт,"
                    " Bonjour, Namaste, Konnichi wa",
            "recipients": [
                {
                    "username": "Jhon Dow",
                    "service": "telegram"
                }
            ],
            "deferred_time": "2020-06-18T9:41:00.000Z"
        }
        response_listed = self.client.post(
            self.url,
            data=json.dumps(data_listed),
            content_type='application/json'
        )
        self.assertEqual(response_listed.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1)

        data_dicted = {
            "text": "Салам, Hello, Bonjour, Namaste, Konnichi wa",
            "recipients": {
                "username": "Dude",
                "service": "whatsapp"
            },
            "deferred_time": "2020-06-18T9:41:00.000Z"
        }
        response_listed = self.client.post(
            self.url,
            data=json.dumps(data_dicted),
            content_type='application/json'
        )
        self.assertEqual(response_listed.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 2)

    def test_create_invalid_message(self):
        data = {
            "text": "Bad",
            "recipients": [
                {
                    "username": "Jhon",
                    "service": ""
                },
                {
                    "username": "",
                    "service": "viber"
                }
            ],
            "deferred_time": "2020-06-18T9:41:00.000Z"
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 2 - cause 2 message objects for each recipient
        self.assertEqual(Message.objects.count(), 0)
