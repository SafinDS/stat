import pandas as pd

import sql_conn
import get_mail as gm
import parsing_mail as pm
from datetime import datetime as dt
import mysql_actions as exec_sql
import mysql_actions as msa

id_user = 1

def get_id_provider():
    query = f"""select insert_provider( '{check.title_check['name_shop']}',
                             '{check.title_check['addr']}',
                             '{check.title_check['email_prov']}', {1} ) """
    id_provider = mySQL.execute_function(query)
    return id_provider

def insert_body_check(id_check: int, body_check: list):
    for value in body_check:


        query = f"""select insert_product ('{value['name']}', 
                                                    '{value['kod']}',
                                                    '{'UnKnown'}',
                                                    {1},
                                                    '{value['nds']}',
                                                    '{value['ind_mera_kol']}'
                                             )"""
        id_product = mySQL.execute_function(query)
        insert = f"""insert into check_body (id_check, id_product, quan, price) values 
                        ({id_check},
                         {id_product},
                          {value['quan']},
                           {value['price']});
                    """
        mySQL.insert(insert)





def get_number_chek(id_provider: int):

        date_check = dt.strptime(check.title_check['data_check'], '%d.%m.%Y %H:%M')
        num_check = check.title_check['num_check']
        summ = check.title_check['summ']

        query = f"""select insert_check ({id_provider}, {summ}, '{num_check}', '{date_check}', {id_user} )
                    """
        id_check = mySQL.execute_function(query)
        return id_check




mySQL = msa.MysqlActions()
mail_list = mySQL.query_all('select imap, email, folder, pass from email where id_users = 1')

for email in mail_list:

    mail_data = gm.get_list_mail(email[0], email[1], email[3], email[2])

    #curs = my_con.query('Select * from provider')
    #data_s = pd.DataFrame(curs)

    if mail_data is not None:
        for i in range(len(mail_data.index)):
            # проверяем магазин и добавляем его
            check = pm.ParsingMailMagnit(mail_data.iloc[i])


            id_provider =  get_id_provider()
            id_check = get_number_chek(id_provider)
            check.get_check_body()
            insert_body_check(id_check, check.body_check)

        # mail_data.info()
        # mail_data.to_csv('mail.csv', encoding='utf-8')
        # for i in range(len(mail_data)):
        #
        #     pars_string(mail_data.iloc[i])
        #
        #     # print('===================',type(mail_data.iloc[i]))
        #     # print(mail_data.iloc[i])




    else:
        print('пусто')

    # query = """
    #         insert into provider (name_provider, addr_provider, email_provider ) values ('magnit','krasnodar','m@mail.ru')
    #         """
    # my_con.insert(query)


# sql_conn.Create_connection('localhost', 'root', 'merhaba0109', 'checks')
