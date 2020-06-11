### Ваша задача: создать прототип микросервиса, обеспечивающий эмуляцию отправки сообщений в популярные мессенджеры (Viber, Telegram, WhatsApp).

Приложение должно обладать следующим функционалом:

* прием сообщений по API и отправка их в мессенджеры (с указанием
  идентификатора пользователя для каждого мессенджера);
* возможность отложенной отправки сообщений по дате/времени;
* в случае неудачной отправки сообщения, нужно повторить попытку N-ое
  количество раз, но это не должно влиять на доставляемость других
  сообщений;
* исключение возможности многократной отправки одного и того же
  сообщения (с одним и тем же содержимым) одному получателю;
* возможность отправки одного сообщения нескольким получателям на
  несколько мессенджеров в рамках одного запроса;
* после рестарта сервиса не должны пропасть "отложенные сообщения" или
  сообщения "в процессе отправки".

* написаны Unit-тесты по ключевому функционалу


#### Важно: сделать именно эмуляцию отправки, непосредственную интеграцию с мессенджерами делать не нужно.

* БОНУС: использование Docker.
* Задание нужно прислать нам вместе с README, в котором должна быть
  инструкция по развертыванию/запуску и описание API-запросов.
* Использование любых инструментов — на вашей совести,
однако выбор необходимо будет обосновать там же в README.


models:
-------

    class Account(models.Model):
    auth_user = models.OneToOneField(User,
                                     on_delete=models.CASCADE,
                                     null=True)
    telegramm = models.SlugField(blank=True, null=True)
    viber = models.SlugField(blank=True, null=True)
    whatsapp = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.auth_user.username


    class Messenger(models.Model):
        msg = models.OneToOneField('Message',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   )
        telegramm = models.BooleanField(default=False)
        viber = models.BooleanField(default=False)
        whatsapp = models.BooleanField(default=False)

        def __str__(self):
            return f'{self.telegramm}{self.viber}{self.whatsapp}'


    class Message(models.Model):
        STATUS = [
            ('DEFFERED', 'Deffered...'),
            ('SENDING', 'Sending...'),
            ('DELIVERED', 'Delivered!'),
            ('FAILED', 'FAILED!!!'),
            ('WAITING', 'waiting...'),
        ]

        id = models.UUIDField(primary_key=True,
                              default=uuid.uuid4,
                              editable=False)
        message = models.TextField()
        account = models.ForeignKey(Account,
                                    on_delete=models.CASCADE,
                                    related_name='Sender')
        status = models.CharField(max_length=10,
                                  choices=STATUS,
                                  default='DEFFERED')
        deffered_time = models.DateTimeField(null=True, blank=True)
        receivers_list = models.ManyToManyField(Account)
        messengers_list = models.ManyToManyField(Messenger)


прием сообщений по API
----------------------

[webhook?](https://developers.viber.com/docs/api/python-bot-api/#setting-a-webhook)

и отправка их в мессенджеры
---------------------------

    class Message(models.Model):
    ...
        |—messengers_list
    ...


    "messengers_list":[  
    "whatsapp,  
       "Telegramm"
       ],

(с указанием идентификатора пользователя для каждого мессенджера);
------------------------------------------------------------------

    class Message(models.Model):
    ...
        |— users_list
    ...


    "users_list":[
          "EGAZ3SZRi6zW1D0uNYhQHg==",
          "kBQYX9LrGyF5mm8JTxdmpw=="
       ],

возможность отложенной отправки сообщений по дате/времени;
----------------------------------------------------------

    class Message(models.Model):
    ...
        |— deffered_time
    ...


        if Message.deffered_time != "blank" or "null":
            status = "Deffered"

в случае неудачной отправки сообщения, нужно повторить попытку N-ое количество раз, это не должно влиять на доставляемость других сообщений;
--------------------------------------------------------------------------------------------------------------------------------------------

    class Message(models.Model):
    ...
        |— is_sended
    ...
        
            is_sended = False
            if Message.status == "Delivered":
                is_sended = True

после рестарта сервиса не должны пропасть "отложенные сообщения" или сообщения "в процессе отправки"
----------------------------------------------------------------------------------------------------

[Celery](https://stackoverflow.com/a/44429064/9785224)

[RabbitMQ](https://www.rabbitmq.com/reliability.html)

    class Message(models.Model):
    ...
        |— status
    ...

           status can be "Deffered" \ "Delivered" \ "Sending"

исключение возможности многократной отправки одного и того же сообщения (с одним и тем же содержимым) одному получателю;
------------------------------------------------------------------------------------------------------------------------

        Хранить в базе связь id_сообщения и id_получателя? 
        Сверять не отправляли-ли мы уже это сообщение?(опять же status???)

возможность отправки одного сообщения нескольким получателям на несколько мессенджеров в рамках одного запроса;
---------------------------------------------------------------------------------------------------------------

    POST http://localhost/api/sendmsg
    content-type: application/json

    {
       "sender":{
          "id":"234234235",
          "name":"John McClane",
       },
       "messengers_list":[
             "Whatsapp",
             "Viber,
             "Telegramm"
        ],
       "users_list":[
          "pttm25kSGUo1919sBORWyA==",
          "2yBSIsbzs7sSrh4oLm2hdQ==",
          "EGAZ3SZRi6zW1D0uNYhQHg==",
          "kBQYX9LrGyF5mm8JTxdmpw=="
       ],
       "deffered_time":"",
        "is_sended":"",
        "status":""

    }

Параметры запроса должны проходить валидацию (требования валидации на ваше усмотрение).
---------------------------------------------------------------------------------------

* есть API, например /sendmsg
* если по этому API передаются неправильные параметры, то должен
  вернуться ответ, о том, что такой параметр неправильный

