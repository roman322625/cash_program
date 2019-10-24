
# импортируем нужные базы

import tkinter as tk
from tkinter import ttk
from datetime import date

import json
from tkinter import messagebox as mb
import sqlite3



# Создание файла с записями имен пользователей
try:  # открыть файл и передать содержимое в переменую names
    names_list = open('users_name.txt', 'r')
    names = names_list.read().split()
    names_list.close()
except FileNotFoundError:  # в случае отсутствия файла создать новый пустой файл
    names_list = open('users_name.txt', 'w')
    names = []
    names_list.close()

# Хранение списка продуктов в файле json. создание и перезапись файла json
try:
    with open ('full_products.json') as r_p:
        f_r_p = json.load(r_p)
except FileNotFoundError:
    dic = {}
    with open ('full_products.json', 'w') as r_p:
        json.dump(dic, r_p)
    with open ('full_products.json') as r_p:
        f_r_p = json.load(r_p)

# Список всех продуктов
full_products = list(f_r_p.items())
full_products.sort()

# Список наиболее покупаемых товаров
popular_product = []
fp = list(f_r_p.items()) # items переганяет словарь в набор кортежей, list-в список
# {kluch1:[45, 3], kluch2:[4, 33]} >items>  [('kluch1', [45, 3]), ('kluch2', [4, 33])]
fp.sort(key=lambda x: x[1][1], reverse=True)

for i in fp[0:48]:
    popular_product.append(i[0] + '   ' + str(i[1][0]))
popular_product.sort()


# Окно отчета о сделаных покупках и растартах
def report_shop():     # root  'ОТЧЕТ'
    global data_entry_from, data_entry_to, name_entry, db_place, total_products
    global price_entry_from, price_entry_to, products_entry, total_sum, total_name

    # внесение изменения в сумарные подщеты колонок
    def change_total(a, b, c, d):

        total_day.config(text=(max(a) - min(a)))
        total_name.config(text=len(b))
        total_products.config(text=len(c))
        total_sum.config(text=round(sum(d), 2))

    def pry(event):
        if db_place.identify_region(event.x, event.y) == 'heading':
            pr = int((db_place.identify_column(event.x)[1]))
            # print(pr)
            items_dbplace = []
            for idb in db_place.get_children():
                items_dbplace.append(db_place.item(idb)['values'])
            db_place.delete(*db_place.get_children())
            for it in items_dbplace:
                it[4] = float(it[4])
            items_dbplace.sort(key=lambda x: x[pr-1])
            for row in items_dbplace:
                db_place.insert('', 'end', values=row)
        else:
            pass
    shoping = tk.Toplevel(bg='SeaGreen')
    shoping.title("Покупки")
    shoping.geometry("639x640")
    shoping.grab_set()
    shoping.focus_set()
    db_place = ttk.Treeview(shoping, height=25, show='headings')
    db_place['columns'] = ('Id', 'Name', 'Data', 'Products', 'Price')
    db_place.grid(row=3, column=0, columnspan=10, padx=3)
    db_place.column('Id', width=80)
    db_place.column('Data', width=150)
    db_place.column('Name', width=100)
    db_place.column('Products', width=200)
    db_place.column('Price', widt=100)
    db_place.heading('Id', text='Id')
    db_place.heading('Data', text='Имя')
    db_place.heading('Name', text='Дата')
    db_place.heading('Products', text='Покупки')
    db_place.heading('Price', text='Цена')
    cash_db = sqlite3.connect('paragons_db')
    curso = cash_db.cursor()
    curso.execute('SELECT * FROM allParagons')
    z = curso.fetchall()
    day = []
    name = set()
    prod = []
    money = []
    for row in z:
        day.append(row[1])
        name.add(row[2])
        prod.append(row[3])
        money.append(row[4])
        row = list(row)
        row[1] = date.fromordinal(row[1])
        db_place.insert('', 'end', values=row)
    curso.close()
    cash_db.close()
    db_place.bind('<Button-1>', pry)

# Filters: блок Два окна фрейм с фильтрами
    filter_frame = tk.Frame(shoping, bg='#4682B4')
    filter_frame.grid(row=1, column=0, columnspan=10, padx=1)
    apply_button = tk.Button(filter_frame, width=11, text='Применить :', command=apply)
    apply_button.grid(row=0, column=0, padx=5, pady=2)
    spase_label = tk.Label(filter_frame, bg='#4682B4', width=4)
    spase_label.grid(row=0, column=1)
    data_label = tk.Label(filter_frame, width=9, text='Период')
    data_label.grid(row=0, column=2, padx=4)
    data_entry_from = tk.Entry(filter_frame, width=9)
    data_entry_from.grid(row=0, column=4, padx=2)
    data_entry_from.insert(0, date.today().strftime('%d.%m.%Y'))
    data_entry_to = tk.Entry(filter_frame, width=9)
    # Уменьшаем дату по умолчанию на один месяц
    gii = str(int(date.today().strftime('%m'))-1)
    if gii == '0':
        gii = '12'
    gii = date.today().strftime('%d.') + gii + date.today().strftime('.%Y')
    data_entry_to.grid(row=0, column=3, padx=2)
    data_entry_to.insert(0, gii)
    spase_label = tk.Label(filter_frame, bg='#4682B4', width=5)
    spase_label.grid(row=0, column=5)
    name_label = tk.Label(filter_frame, width=13, text='Имя покупателя')
    name_label.grid(row=0, column=6, padx=2)
    name_entry = tk.Entry(filter_frame, width=15)
    name_entry.grid(row=0, column=7, padx=5)
    name_entry.insert(0, 'Dj Aligator')
    spase_label = tk.Label(filter_frame, bg='#4682B4', width=7)
    spase_label.grid(row=0, column=8)
    filter_frame2 = tk.Frame(shoping, bg='#4682B4')
    filter_frame2.grid(row=2, column=0, columnspan=10, padx=1)
    spase_label = tk.Label(filter_frame2, bg='#4682B4', width=18)
    spase_label.grid(row=0, column=0, columnspan=2)
    products_label = tk.Label(filter_frame2, width=9, text=" Продукты ")
    products_label.grid(row=0, column=2, padx=5)
    products_entry = tk.Entry(filter_frame2, width=20)
    products_entry.grid(row=0, column=3, pady=5)
    spase_label = tk.Label(filter_frame2, bg='#4682B4', width=5)
    spase_label.grid(row=0, column=4)
    price_label = tk.Label(filter_frame2, width=13, text="Укажите цену")
    price_label.grid(row=0, column=5)
    price_entry_from = tk.Entry(filter_frame2, width=9)
    price_entry_from.grid(row=0, column=6, padx=5)
    price_entry_from.insert(0, 0)
    price_entry_to = tk.Entry(filter_frame2, width=9)
    price_entry_to.grid(row=0, column=7, padx=5)
    price_entry_to.insert(0, 100000)
    spase_label = tk.Label(filter_frame2, bg='#4682B4', width=3)
    spase_label.grid(row=0, column=8)
    total_day = tk.Label(shoping, text='0', width=7)
    total_day.grid(row=4, column=2)
    total_name = tk.Label(shoping, text='0', width=7)
    total_name.grid(row=4, column=3)
    total_products = tk.Label(shoping, text='0', width=10)
    total_products.grid(row=4, column=6)
    total_sum = tk.Label(shoping, text='0', width=10)
    total_sum.grid(row=4,column=9)
    change_total(day, name, prod, money)

def apply():
    # CREATE qwestion
# record from '''data_entry_from'''
    db_place.delete(*db_place.get_children())
    df = data_entry_from.get().split('.')
    df1, df2, df3 = list(map(int, df))
    dfi = date.toordinal(date(df3, df2, df1))
    now = date.today().toordinal()
    if dfi > now or dfi < 737304:
        dfi = now
# record from '''data_entry_to'''
    dt = data_entry_to.get().split('.')
    dt1, dt2, dt3 = list(map(int, dt))
    dti = date.toordinal(date(dt3, dt2, dt1))
    if dti > dfi or dti < 737304 and dti != 0:
        dti = dfi - 30
# record from '''name_entry'''
    n_e = name_entry.get()
    n_z = ' AND Name == "{0}"'.format(n_e)
    if n_e not in names:
        n_z = ''
# record from '''products_entry'''
    p_e = products_entry.get()
    p_z = ' AND Products LIKE "%{}%" '.format(p_e)
    for ow in full_products:
        if p_e in ow[0]:
            p_z = ' AND Products LIKE "%{ogi}%" '
            p_z = p_z.format(ogi=p_e)
    if p_e == '':
        p_z = ''
# record from '''products_entry'''
    pf = price_entry_from.get()
    if not pf.isdigit():
        pf = 0
        price_entry_from.insert(0, 0)
    pf = int(float(pf))
# record from '''products_entry'''
    pt = price_entry_to.get()
    if not pt.isdigit():
        pt = 100000
        price_entry_to.insert(0, 100000)
    pt = int(float(pt))
    if pf > pt:
        pf = 0
        price_entry_from.delete(0, 'end')
        price_entry_from.insert(0, 0)

    sq = 'SELECT * FROM allParagons WHERE Date BETWEEN {0} AND {1} {2} {3} ' \
         'AND Price BETWEEN {4} AND {5}'.format(dti, dfi, n_z, p_z, pf, pt)
    cash_db = sqlite3.connect('paragons_db')
    curs = cash_db.cursor()
    curs.execute(sq)
    s = curs.fetchall()
    s_price = 0
    s_name = []
    for row in s:
        row = list(row)
        row[1] = date.fromordinal(row[1]).strftime('%d.%m.%Y')
        db_place.insert('', 'end', values=row)
        s_price += row[4]
        s_name.append(row[2])
    curs.close()
    cash_db.close()
    total_sum.config(text=round(s_price, 2))
    total_products.config(text=len(s))
    total_name.config(text=len(set(s_name)))


# Удаление покупки из списка
def dell_buy():   # root  'уд покупку '
    try:
        ind = shop_list.curselection()[0]
        price_minus = shop_list.get(ind)
        price_minus = price_minus.split('  ')
        price_minus = float(price_minus[-1])
        shop_list.delete(ind)
        total_price.config(text=tot_pri - price_minus)
    except:
        pass


# Изменение покупки из списка
def cheng_buy():   # root 'изм покупку'

    def buton_ch():
        global tot_pri
        cg2 = str(round(float(price_place.get()), 2))
        spac = (25 - (len(ct1) + len(cg2))) * ' '
        apend_str = ct1 + spac + cg2
        if len(cg2.split('.')[0]) < 6 and len(cg2.split('.')[1]) < 3:
            shop_list.delete(ch1)
            shop_list.insert(ch1, apend_str)
            tot_pri -= float(cg1)
            tot_pri += float(cg2)
            total_price.configure(text=str(tot_pri))
            window_change.destroy()
    try:
        ch1 = shop_list.curselection()[0]
        cr1 = shop_list.get(ch1)
        ct1 = cr1.split('  ')[0]
        cg1 = cr1.split('  ')[-1]
        window_change = tk.Toplevel()
        window_change.title('Редактирование цены')
        window_change.geometry('300x80')
        window_change.grab_set()
        name_label = tk.Label(window_change, text=ct1, font='11', width=18)
        name_label.grid(row=0, column=0, padx=5, pady=10)
        recomend_label = tk.Label(window_change, text='Цена не больше \n 99999.99')
        recomend_label.grid(row=1, column=0)
        price_place = tk.Entry(window_change, width=10)
        price_place.grid(row=0, column=1)
        price_place.focus()
        price_place.insert(0, cg1)
        button_change = tk.Button(window_change, text='    изменить цену ', command=buton_ch)
        button_change.grid(row=1, column=1)
    except:
        pass


# Сохраниить отчет. Добавить в SQLite
def save_parag():    # root   'сохранить чек'
    cash_db = sqlite3.connect('paragons_db')
    curs = cash_db.cursor()
    try:
        curs.execute('''CREATE TABLE allParagons(Id INTEGER PRIMARY KEY AUTOINCREMENT,
         Date INTEGER, Name TEXT, Products TEXT, Price REAL)''')
    except:
        pass

    sh = shop_list.get(0, 'end')
    for sl in sh:
        h = [date.today().toordinal(), user_name]
        sn, sp = sl.split('  ')[0], sl.split('  ')[-1]
        f_r_p[sn] = [float(sp), int(f_r_p.get(sn, '0')[1]) + 1]
        with open('full_products.json', 'w') as fj:
            json.dump(f_r_p, fj)
        print(f_r_p)
        h.append(sn)
        h.append(float(sp))
        curs.execute('''INSERT INTO allParagons (Date, Name, Products, Price)
         VALUES (?, ?, ?, ?)''', h)
        cash_db.commit()
    curs.close()
    cash_db.close()
    mess = mb.showinfo(message='Товарный чек сохранен в базу данных')
    shop_list.delete(0, 'end')
    total_price.config(text=0)


#Выбор имени покупателя
def chois_nam(): # name   'выбрать имя'
    global user_name, name
    try:
        a = list_box.curselection()[0]  # получаем индекс выделеного элемента
        a = list_box.get(a)  # методом гет из лист бокса получаем выделеное значение
        select_name.configure(bg='#F0E68C', text=a)
        user_name = a
    except IndexError:
        select_name.configure(text='не выбрано')
    finally:
        name.destroy()


# Добавление покупателя в базу
def addname():  # name  'добавить имя'
    global names, list_box
    c = entry_place.get()
    try:
        if c[0].isalpha() and names.count(c) == 0:  #проверка:1'c' буквы?, 2нет ли такогоже имени
            names.append(c)  # добавляем введеное имя в список имен
            list_box.insert('end', c)  # добавляем введеное имя в листбокс
            add_list = open('users_name.txt', 'a')
            add_list.write(c)
            add_list.write(' ')
            add_list.close()
    except:
        entry_place.focus_set()


# Удаление имени покупателя из базы
def dele_nam():  # name   'удалить имя'
    global names, list_box
    try:
        a = list_box.curselection()[0]
        list_box.delete(a)
        del names[a]
        user_file = open('users_name.txt', 'w')
        user_file.write(' '.join(names))
        user_file.close()
    except:
        pass


# Добавить товар к общей базе продуктов
def neww_position(x=None, m=None):   # psewdo_google    'новый товар'
    global psewdo_google, input_place, f_r_p, full_products
    price = 0
    try:
        w = input_place.get()
    except:
        w = x
        price = m
    if len(w) > 3 and w[0:3].isalpha() and len(w) < 16 and f_r_p.get(w) == None:
        f_r_p[w] = [price, 0]
        with open('full_products.json', 'w') as frp:
            json.dump(f_r_p, frp)
        full_products.append((w,[price, 0]))
        sms = mb.showinfo(message=w + " добавлен ")
        input_place.delete(0, 'end')
    else:
        pass


# Функция живого поиска товара в базе для окна psewdo_google
def found(event):   # psewdo_google| Событие -  нажатие любой клавиши в поисковой строке
    global psewdo_google, input_place, full_products
    z = []  # локальная переменная найденых соответствий
    trr = input_place.get().lower()

    if '  ' in trr:
        k = trr.find('  ')
        input_place.delete(k)
    if len(trr) > 1:
        for q in full_products:
            if trr in q[0]:
                s = q[0] + '  ' + str(q[1][0])
                z.append(s)
            else:
                pass
        matches.delete(0, 'end')
        for x in z:
            matches.insert('end', x)
    elif len(trr) < 2:
        matches.delete(0, 'end')
    input_place.delete(15)


# Функция добавления цены и добавления в товарный чек
def append_bill(x,y):   # psewdo_google -> 'добавить в чек'

    def plus_bill():  # new_pos    'добавить'
        global tot_pri
        try:
            price = str(round(float(in_place.get()), 2))
            # price = price1[0] + '.' + price1[1][0:2]
            trr3 = (25 - (len(x) + len(price))) * ' '
            trr0 = x + trr3 + price
            shop_list.insert('end', trr0)
            tot_pri += float(price)
            total_price.configure(text=str(tot_pri))
            new_pos.destroy()
            psewdo_google.destroy()       #задокоментировать чтобы остаться в строке поиска
            # input_place.delete(0, 'end') #роздокументировать для очистки строки поиска
            for pi in full_products:
                if pi[0]== x:
                    full_products[full_products.index(pi)][1][0] = float(price)
            if x not in full_products:
                neww_position(x, float(price))
        except:
            pass

    def pl_bil(event):
        plus_bill()

    def ooo(event):
        p = in_place.get()
        if len(p) > 5 and not '.' in p[0:6]:
            in_place.insert(5, '.')
        elif len(in_place.get()) > 7:
            in_place.delete(7)
        else:
            pass

    def change_price(event):
        in_place.delete(0, 'end')
        in_place.bind('<Key>', ooo)
    #  создаем окно добавления цены
    new_pos = tk.Toplevel()
    new_pos.title('new_pos')
    new_pos.geometry("220x100")
    new_pos.grab_set()
    label_message1 = tk.Label(new_pos, text='Новая позиция будет добавлена')
    label_message1.grid(row=0, column=0, columnspan=3)
    label_message2 = tk.Label(new_pos, text='Введите цену формата  99512.75')
    label_message2.grid(row=1, column=0, columnspan=3)
    label_name = tk.Label(new_pos, bg="aqua", width=20, text=x)
    label_name.grid(row=2, column=0, pady=3)
    in_place = tk.Entry(new_pos, width=10)
    in_place.grid(row=2, column=1)
    in_place.focus_set()
    plusbill = tk.Button(new_pos, bg='gold', text='добавить', command=plus_bill)
    plusbill.grid(row=3, column=0)
    in_place.insert(0, y)
    in_place.bind('<Key>', change_price)
    in_place.bind('<Return>', pl_bil)

# Функция проверяет данные от поля ввода и листбокса и передает дальше
def add_bill_button():    # psewdo_google -> 'добавить в чек'
    if matches.get(0)[0:3].isalpha():
        b = matches.get(0).split('  ')[0]
        c = matches.get(0).split('  ')[-1]
        if c == b:
            c = 0.00
        append_bill(b, c)
    elif len(input_place.get()) > 3 and len(input_place.get()) < 16 and input_place.get()[0:3].isalpha():
        append_bill(input_place.get(), '0')

# Переводит энтер на кнопку add_bill_button 'добавить в чек'
def add_bill_enter(event):
    add_bill_button()

# Переводит ЛКМ на add_bill_button 'добавить в чек'
def add_bill_mouse(event):
    try:
        b = matches.curselection()[0]  # получаем индекс выделеного элемента
        c = matches.get(b)  # методом гет из лист бокса получаем выделеное значение
        d = c.split('  ')[0]
        e = c.split('  ')[-1]
        append_bill(d, e)
    except:
        pass

# Найти наименование товара в базе
def found_buy():   # root    ' найти товар '
    global psewdo_google, input_place, matches
    psewdo_google = tk.Toplevel()
    psewdo_google.title("Poisk")
    psewdo_google.geometry("127x240+600+200")
    psewdo_google.grab_set()  # делаем name модальным(нельзя переключиться на главное окно)
    psewdo_google.focus_set()  # переносим фокус на окно name
    input_place = tk.Entry(psewdo_google)
    input_place.pack()
    input_place.focus_set()
    matches = tk.Listbox(psewdo_google)
    matches.pack()
    add_to_bill = tk.Button(psewdo_google, bg='light grey', width=14, text='добавить в чек', command=add_bill_button)
    add_to_bill.pack()
    #  Создание кнопки 'новый товар'
    new_buy = tk.Button(psewdo_google, bg='light grey', width=14, text='новый товар', command=neww_position)
    new_buy.pack()
    psewdo_google.bind('<Key>', found)
    psewdo_google.bind('<Return>', add_bill_enter)
    matches.bind('<Button-1>', add_bill_mouse)


def prod_list1_mouse(event):
    try:
        c = prod_list1.curselection()[0]
        f = prod_list1.get(c)
        q = f.split('  ')[0]
        z = f.split('  ')[-1]
        append_bill(q, z)
    except IndexError:
        pass


def prod_list2_mouse(event):
    try:
        c = prod_list2.curselection()[0]
        f = prod_list2.get(c)
        q = f.split('  ')[0]
        z = f.split('  ')[-1]
        append_bill(q, z)
    except IndexError:
        pass


def prod_list3_mouse(event):
    try:
        c = prod_list3.curselection()[0]
        f = prod_list3.get(c)
        q = f.split('  ')[0]
        z = f.split('  ')[-1]
        append_bill(q, z)
    except IndexError:
        pass


#Окно управлени именами пользователей
def select():       # root 'Выберите имя'
    global list_box, entry_place, names, name
    name = tk.Toplevel()
    name.title("Выбор имени")
    name.geometry("300x200")
    name.grab_set()  #  делаем name модальным(нельзя переключиться на главное окно)
    name.focus_set()  # переносим фокус на окно name
    frame_list = tk.Frame(name, bg="yellow", width=140, heigh=190)
    frame_list.grid(row=0, column=0, padx=5, pady=5)
    frame_button = tk.Frame(name, bg="brown", width=140, heigh=190)
    frame_button.grid(row=0, column=1, padx=5, pady=5)
    list_box = tk.Listbox(frame_list, height=11)
    list_box.grid(row=1, column=1, padx=1, pady=1)
    list_box.bind("<Double-Button-1>", lambda event: chois_nam())
    entry_place = tk.Entry(frame_button, bg='#e6ddd6', width=24)
    entry_place.grid(row=0, column=0)
    add_name = tk.Button(frame_button, width=20, text='добавить имя', command=addname)
    add_name.grid(row=1, column=0)
    choise_name = tk.Button(frame_button, width=20, text='выбрать имя', command=chois_nam)
    choise_name.grid(row=2, column=0, pady=1)
    delet_name = tk.Button(frame_button, width=20, text='удалить имя', command=dele_nam)
    delet_name.grid(row=3, column=0)
    for nam in names:
        list_box.insert('end', nam)


# Создаем главное окно программы
root = tk.Tk()
root.title("ПОДСЧЕТ РАСХОДОВ")
root.geometry('885x470')
root['bg'] = '#66b369'
root.bind('z', lambda event: found_buy())


# добавление даты в главное окно
dat = date.today().strftime('%d.%m.%Y')
data = tk.Label(root, bg="green", text=dat)
data.grid(row=0, column=3, columnspan=3, padx=3, pady=5)


# имя пользователя сделавшего покупки
f_name = tk.Label(root, text='Имя покупателя:', width=15)
f_name.grid(row=1, column=0, padx=3)

# s_name = tk.Label(root, width=20, bg='yellow', text="нет имени")
# s_name.grid(row=1, column=1, columnspan=2, padx=2, pady=2)
# s_name.bind('<Double-Button-1>', lambda event: select())

# выбор имени купившего
user_name = 'no name'  # Переменная с выбраным именем пользователя
select_name = tk.Button(root, bg='yellow', width=20, text='Выберите имя', command=select)
select_name.grid(row=1, column=1, columnspan=2, padx=5)

# Фрейм для листбоков со списком продуктов
frame_list = tk.LabelFrame(root, text='Список наиболее покупаемых продуктов', bg='#DAA520', width=800, heigh=309)
frame_list.grid(row=3, column=0, columnspan=9, padx=1, pady=1)
# Создание листбокса1 со списком товаров из общей базы
prod_list1 = tk.Listbox(frame_list, font= '11', height=16, width=23)
prod_list1.grid(row=0, column=0, columnspan=3, rowspan=10, padx=2, pady=1)
#          листбокса2
prod_list2 = tk.Listbox(frame_list, font= '11', height=16, width=23)
prod_list2.grid(row=0, column=3, columnspan=3, rowspan=10, padx=2, pady=1)
#          листбокса3 со списком товаров из общей базы
prod_list3 = tk.Listbox(frame_list, font= '11', height=16, width=23)
prod_list3.grid(row=0, column=6, columnspan=3, rowspan=10, padx=2, pady=1)
# биндуем до продуктовых листов ЛКМ
prod_list1.bind('<Double-Button-1>', prod_list1_mouse)
prod_list2.bind('<Double-Button-1>', prod_list2_mouse)
prod_list3.bind('<Double-Button-1>', prod_list3_mouse)

for j in popular_product[0:16]:
    prod_list1.insert('end', j)
for j in popular_product[16:32]:
    prod_list2.insert('end', j)
for j in popular_product[32:48]:
    prod_list3.insert('end', j)

# Сделаные покупки. Окно ОТЧЕТа о сделаных покупках и растартах
report = tk.Button(root, bg='aqua', text='АРХИВ', command=report_shop, width=10)
report.grid(row=0, column=10, padx=5)

# Создание листбокса ТОВАРНОГО ЧЕКА  со списком покупок
shop_list = tk.Listbox(root, font='monaco 11', height=18, width=25)
shop_list.grid(row=3, column=10, columnspan=5, rowspan=10, padx=1, pady=1)

# Создание кнопки УДАЛЕНИЕ ПОКУПКИ из списка чека
del_buy = tk.Button(root, bg='grey', width=14, text='удалить покупку ', command=dell_buy)
del_buy.grid(row=2, column=10, padx=1, pady=1)

# Создание кнопки изминения товара из списка чека
changed_buy = tk.Button(root, bg='grey', width=15, text=' изменить покупку', command=cheng_buy)
changed_buy.grid(row=2, column=11, padx=1, pady=1)

#  Создание кнопки добавить товар в чек
ffound_buy = tk.Button(root, bg='grey', width=14, text=' добавить в чек ', command=found_buy)
ffound_buy.grid(row=1, column=7, padx=1, pady=1)
tip = tk.Label(root, text='press  "Z"', bg='#66b369', fg='#66b369')
tip.grid(row=1, column=8)
ffound_buy.bind('<Enter>', lambda x: tip.config(fg='white'))
ffound_buy.bind('<Leave>', lambda x: tip.config(fg='#66b369'))

# Создаем кнопку сохранения чека
saver_paragon = tk.Button(root, bg='tomato', text='сохранить чек', width=15, command=save_parag)
saver_paragon.grid(row=13, column=8, columnspan=4, padx=1, pady=1)

# Создание метки с надписью 'Всего' возле общей суммы в чеке
# total = tk.F(root, bg='aqua', text='Всего')
# total.grid(row=13, column=10)

# Создание метки с общей сумой покупок в чек листе
tot_pri = 0
total_price = tk.Label(root, bg='aqua', width=10, text=round(float(tot_pri), 2))
total_price.grid(row=13, column=11)


root.mainloop()

