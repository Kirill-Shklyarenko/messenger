import datetime as dt

import pytz
from django.test import TransactionTestCase, TestCase

from api.models import Recipient, Message


class RecipientModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipient.objects.create(username='TestUser', service='telegram')

    def test_username_max_length(self):
        recipient = Recipient.objects.get(id=1)
        max_length = recipient._meta.get_field('username').max_length
        self.assertEquals(max_length, 50)

    def test_service_max_length(self):
        recipient = Recipient.objects.get(id=1)
        max_length = recipient._meta.get_field('service').max_length
        self.assertEquals(max_length, 8)

    def test_recipient_representation(self):
        recipient = Recipient.objects.get(id=1)
        expected_object_name = f'{recipient.username} | {recipient.service}'
        self.assertEquals(expected_object_name, str(recipient))


class MessageModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        recipients = Recipient.objects.create(username='TestUser2', service='viber')
        Message.objects.create(text='TestText!@#$%^&*()',
                               deferred_time=dt.datetime.now(tz=pytz.UTC),
                               status=1,
                               recipients=recipients)

    def test_fields_recipients(self):
        message = Message.objects.get(id=1)
        self.assertEqual(message.recipients.username, 'TestUser2')
        self.assertEqual(message.recipients.service, 'viber')

    def test_message_representation(self):
        message = Message.objects.get(id=1)
        expected_object_name = f'{message.text}'
        self.assertEquals(expected_object_name, str(message))


class TestsThatDependsOnPrimaryKeySequences(TransactionTestCase):
    reset_sequences = True

    def test_message_pk(self):
        recipient = Recipient.objects.create(username='Dev', service='viber')
        message = Message.objects.create(text='Hello, Dev, how are you?',
                                         deferred_time=dt.datetime.now(tz=pytz.UTC),
                                         status=3,
                                         recipients=recipient)
        self.assertEqual(message.pk, 1)
