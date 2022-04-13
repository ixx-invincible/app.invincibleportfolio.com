# from fastapi import BackgroundTasks
import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

fastmail_conf = ConnectionConfig(
    MAIL_USERNAME = "noreply@ixx.cc",
    MAIL_PASSWORD = "rb58i1^D",
    MAIL_FROM = "noreply@ixx.cc",
    MAIL_PORT = 587,
    MAIL_SERVER = "mail.ixx.cc",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)



def send_marksix(email, background_tasks):
    random_list = random.sample(range(13, 50), 37)

    random_pos = random.sample(range(0, 36), 5)

    for i in random_pos:
        random_list.append(random_list[i])

    # for i in range(7):
    #     print('#', i+1, random_list[i*6 : (i+1)*6])

    html = """
    #1 %s<br>
    #2 %s<br>
    #3 %s<br>
    #4 %s<br>
    #5 %s<br>
    #6 %s<br>
    #7 %s<br>
    """ % (
        str(random_list[0:6]),
        str(random_list[6:12]),
        str(random_list[12:18]),
        str(random_list[18:24]),
        str(random_list[24:30]),
        str(random_list[30:36]),
        str(random_list[36:42])
    )

    message = MessageSchema(
        subject="超級聰明投注組合",
        recipients=[email],
        html=html,
        subtype="html"
    )

    fm = FastMail(fastmail_conf)

    background_tasks.add_task(fm.send_message, message)
