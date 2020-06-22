import json

from django.test import TestCase
from rest_framework.reverse import reverse

from api.tasks import send_message_task, message_checker_task


class TasksTestCase(TestCase):

    def setUp(self) -> None:
        url = reverse('sendmsg')
        data = {
            "text": "Салам, Hello, Bonjour, Namaste, Konnichi wa",
            "recipients": {
                "username": "Dude",
                "service": "whatsapp"
            }
        }
        response = self.client.post(  # noqa
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

    def test_send_message_task(self):
        task = send_message_task.s(message_pk=1).apply()
        self.assertEqual(task.result, 'SUCCESS')

    def test_message_checker_task(self):
        task = message_checker_task.s().apply()
        self.assertEqual(task.result, 'SUCCESS')
