import imap_tools
from imap_tools import MailBox
from imap_tools import A, AND, OR, NOT
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

import sql_conn


def get_list_mail(imap, mail_login, passw, folder='INBOX', is_seen=False, date=None):
   # now = date.today()
    # get list of email bodies from INBOX folder
    with MailBox(imap).login(mail_login, passw, folder) as mailbox:

        bodies = [msg.text or msg.html for msg in mailbox.fetch()]
        if len(bodies) > 0:

            lst_of_checks = []
            cnt = 0
            for i in bodies:
                contents = bodies[cnt]
                cnt = cnt + 1
                soup = BeautifulSoup(contents, 'html.parser')
                lst_of_checks.append([text for text in soup.stripped_strings])

            print('Всего чеков ', cnt)
            #print(lst_of_checks[0], )
            data = pd.DataFrame(lst_of_checks)
            return data
        else:
            print('Писем нет')








# conn = sql_conn.Create_connection('imap.yandex.ru', 's4fin.dmitry@yandex.ru', 'ynavmqpgzjvurqje')