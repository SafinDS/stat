import pandas as pd


class ParsingMailMagnit():
    __addr_shop = 4
    __inn = 3
    __name_shop = 5
    __data_check = 6
    __num_check = 7
    # self.__email - следующая строчка после:
    __email_str = 'ЭЛ.АДР.ОТПРАВИТЕЛЯ:'
    # первое вхождение для тела чека
    __first_body_str = 'СУММА ПР.'
    # останавливаемся на ИТОГО
    __last_body_str = 'ИТОГО:'

    def __init__(self, pars_str: pd.Series):
        self.pars_str = pars_str
        self.__email = int(pars_str[pars_str == self.__email_str].index.item())+1
        self.__summ = int(pars_str[pars_str == self.__last_body_str].index.item())+1
        self.title_check = self.get_title_check()
        self.body_check = []

    def get_title_check(self):
        data = {}

        data.setdefault('addr', self.pars_str[self.__addr_shop])
        data.setdefault('inn', self.pars_str[self.__inn])
        data.setdefault('name_shop', self.pars_str[self.__name_shop])
        data.setdefault('data_check', self.pars_str[self.__data_check])
        data.setdefault('num_check', self.pars_str[self.__num_check])
        data.setdefault('email_prov', self.pars_str[self.__email])
        data.setdefault('summ', float(self.pars_str[self.__summ]))

        return data


    def get_check_body(self):
        ds = self.pars_str

        x = ds[ds == 'СУММА ПР.'].index.item()

        y = ds[ds == 'ИТОГО:'].index.item()

        ds1 = ds.loc[x + 1:y - 1]

        fl = True
        cnt_ind = 0
        data = []
        while fl:
            str_ = dict()

            ### ищем есть ли доп строка "РЕЗ. ПРОВ. СВЕД. О ТОВАРЕ" для меры веса
            if 'РЕЗ. ПРОВ. СВЕД. О ТОВАРЕ' in ds1.values:  # проверяем есть ли она вообще
                index_rez = int(ds1[ds1 == 'РЕЗ. ПРОВ. СВЕД. О ТОВАРЕ'].index[0])
                ind_ = index_rez - int(ds1.index[0])
                if ind_ >= 10:
                    ind_mera_kol = 10
                else:
                    ind_mera_kol = 12
            else:
                ind_mera_kol = 10

            ###########
            #print(ds1.values[0])
            #print(type(ds1))


            # print(ds1[1])
            # print(ds1[2])
            # print(ds1[3])
            # print(ds1[4])
            # print(ds1[ind_mera_kol])
            #['Круассан с варен сгущ 0,075кг п/уп (Краснодар', '1', '15.99', '15.99', 'НДС 10%', 'шт. или ед.', '4607104244635']

            str_ = {'name': ds1.values[0],
                    'quan': ds1.values[1],
                    'price': ds1.values[2],
                    'summ': ds1.values[3],
                    'nds': ds1.values[4],
                    'ind_mera_kol': ds1.values[ind_mera_kol]}



            ## Проверяем есть ли вообще "Код ТОВАРА", если нет, то всегда код товара будет None
            if 'КОД ТОВАРА' in ds1.values:

                index_kod_prod = int(ds1[ds1 == 'КОД ТОВАРА'].index[0])
                fl_kod_prod = index_kod_prod - int(ds1.index.values[0])
            else:
                fl_kod_prod = 15  # кода товара нет

            if fl_kod_prod <= 13:
                kod = ds1.values[fl_kod_prod + 1]
                if (fl_kod_prod + 2) >= len(ds1):
                    a = ds1.values[fl_kod_prod + 1]
                else:
                    a = ds1.values[fl_kod_prod + 2]

                x = ds1[ds1 == a].index.item()

            else:
                kod = 'None'
                #print('ds1 ==', len(ds1))
                if len(ds1) <= 11:
                    a = ds1.values[0]
                else:
                    a = ds1.values[11]

                if len(ds1[ds1 == a].index) > 1:
                    cnt_ind += 1
                else:
                    cnt_ind = 0

                x = ds1[ds1 == a].index[cnt_ind]

            str_.setdefault('kod', kod)
            data.append(str_)
            lst_imk = ds1.index[ind_mera_kol]
            ds1 = ds1.loc[x : y - 1]
            #print(ds1)
            #  print('last ', (int(y) - 1) - int(x))
            #print('f l ind ', ds1.index[-1], lst_imk)
            if ((int(y) - 1) - int(x)) < 10 or (ds1.index[-1] == lst_imk):
                fl = False
        self.body_check = data
        return data


