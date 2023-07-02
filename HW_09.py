'''
На первом этапе наш бот-ассистент должен уметь:
 - сохранять имя и номер телефона, 
 - находить номер телефона по имени,
 - изменять записанный номер телефона,
 - выводить в консоль все записи, которые сохранил. 
 
 Чтобы реализовать такую несложную логику, воспользуемся словарем. 
 В словаре будем хранить имя пользователя как ключ и номер телефона как значение.
'''

from pathlib import Path
import os
import platform  # для clearscrean()

persons = {}   # "name": "0975634583"
path = Path("D:\Git\HW_09\database_09.csv")


# Головна функція роботи CLI(Command Line Interface - консольного скрипту)  
def main():
    cmd = ""
    
    # головний цикл обробки команд користувача
    while True:
        
        # 1. Отримаємо команду від користувача
        cmd = input(">> ")    
        
        # 2. Виконуємо розбір командної строки
        cmd, prm = parcer_commands(cmd)
        
        # 3. Отримуємо handler_functions тобто ДІЮ
        if cmd: handler = get_handler(cmd)
        else: 
            print("Command was not recognized")
            continue
            
        # 4. Визначемо параметри для handler() 
        #    та виконаємо Команду користувача
        if run_handler(handler, cmd, prm) == "Good bye!":
            print("Good bye!")
            break
        
        
        
# Декоратор для Обробки командної строки
def input_error(func):
    def inner(handler, cmd, prm):
        try:
            result = func(handler, cmd, prm)
            if not result == "Good bye!": print(result) 
            else: return result
        
        # Обробка виключних ситуацій
        except FileNotFoundError:    # Файл бази даних Відсутній
            print("The database isn't found")
        except ValueError:
            print("Incorect data or unsupported format while writing to the file")
        except KeyError:
            print("Record isn't in the database")
    return inner


# Декоратор для Збереження бази даних у файл
def dec_save_phoneDB(func):
    def inner(path):
        return func(path)   # print(func(path))
    return inner 
 
 
 # Декоратор для Завантаження бази даних із файлу
def dec_load_phoneDB(func):
    def inner(path):
        return func(path)
    return inner


# Декоратор для Завершення роботи      
def dec_func_exit(func):
    def inner(_):
        return func(_)  
    return inner


# Декоратор для команди Вітання      
def dec_func_greeting(func):
    def inner(_):
        return func(_)
    return inner
 
 
# Декоратор для Додавання нової людини у базу
def dec_func_add(func):
    def inner(prm):
        return func(prm)
    return inner


# Декоратор для Внесення змін у базу даних
def dec_func_change(func):
    def inner(prm):
        return func(prm)
    return inner
 
 
 # Декоратор для Знайденя телефону за Ім'ям особи
def dec_func_phone(func):
    def inner(prm):
        return func(prm)
    return inner


# Декоратор для Друкування всієї бази даних
def dec_func_all_phone(func):
    def inner(_):
        return func(_)
    return inner


# -------------------------------------------- 
@input_error 
def run_handler(handler, cmd, prm):
    if cmd in ["add", "change", "phone"]:
        result = handler(prm)
    elif cmd in ["close", "exit", "good bye"]:
        result = handler("")
    elif cmd in ["save", "load"]:
        result = handler(path)            
    elif cmd in ["show all", "hello"]:
        result = handler("")
    return result
     
     
# Повертає адресу функції, що обробляє команду користувача
def get_handler(operator):
    return OPERATIONS[operator]    


#=========================================================
# Функція читає базу даних з файлу - ОК
#========================================================= 
@dec_load_phoneDB
def load_phoneDB(path):
    with open(path, "r") as f_read:
        while True:                
            line = f_read.readline()
            if not line:
                break
            if line[-1] == "\n":
                line = line[:-1]
            pos = line.find(":")
            persons[line[:pos]] = line[pos+1:]
    return f"The database has been loaded = {len(persons)} records"
    
    
#=========================================================
# Функція виконує збереження бази даних у файл *.csv - OK
#========================================================= 
@dec_save_phoneDB
def save_phoneDB(path):
    with open(path, "w") as f_out:
        f_out.write("\n".join([":".join([person, value]) for person, value in persons.items()]))
    return f"The database is saved = {len(persons)} records"  
       
    
#=========================================================
# >> "good bye", "close", "exit"
# По любой из этих команд бот завершает свою роботу 
# после того, как выведет в консоль "Good bye!".
#=========================================================
@dec_func_exit
def func_exit(_):
    return "Good bye!"


#=========================================================
# >> hello
# Отвечает в консоль "How can I help you?"
#=========================================================
@dec_func_greeting
def func_greeting(_):
    return "How can I help you?"


#=========================================================
# >> add ...  
# По этой команде бот сохраняет в памяти (в словаре например) новый контакт. 
# Вместо ... пользователь вводит ИМЯ и НОМЕР телефона, обязательно через пробел.
#=========================================================
@dec_func_add
def func_add(prm):
    
    # порахуємо кількість параметрів
    count_prm = get_count_prm(prm)
        
    if prm and (count_prm >= 2):
        # Якщо ключ (ІМ'Я) що користувач хоче ДОДАТИ не ІСНУЄ тобто можемо додавати
        if not prm.partition(" ")[0].capitalize() in persons:
            persons[prm.partition(" ")[0].capitalize()] = prm.partition(" ")[2]    # Додаємо нову людину
            return "1 record was successfully added"
        else: return "Person is already in database"  # Повернемо помилку -> "Неможливо дадати існуючу людину"
    else:
        return f"Expected 2 arguments, but {count_prm} was given.\nHer's an example >> add Name 0499587612"
    


#=========================================================
# >> change ...
# По этой команде бот сохраняет в памяти новый номер телефона 
# для существующего контакта. 
# Вместо ... пользователь вводит Имя и Номер телефона, 
# Внимание: обязательно через пробел!!!
#=========================================================
@dec_func_change  
def func_change(prm):
    
    # порахуємо кількість параметрів
    count_prm = get_count_prm(prm)
    
    if prm and (count_prm >= 2):
        name = prm.partition(" ")[0].lower().capitalize()
        # Якщо ключ (ІМ'Я) що користувач хоче ЗМІНИТИ ІСНУЄ, тобто можемо Змінювати
        if  name in persons:
            persons[name] = prm.partition(" ")[2]
            return f"Record for {name} was successfully changed"
        else:
            return f"The record wasn't found in the database"
    else: 
        return f"Expected 2 arguments, but {count_prm} was given.\nHer's an example >> change Name 0499587612"
    

#=========================================================
# >> phone ...
# По этой команде бот выводит в консоль номер телефона для указанного контакта.
# Вместо ... пользователь вводит Имя контакта, чей номер нужно показать.
#=========================================================
@dec_func_phone
def func_phone(prm):
    # порахуємо кількість параметрів
    count_prm = get_count_prm(prm)
    
    if prm: return persons[prm.partition(" ")[0].capitalize()]
    else: return f"Expected 1 argument, but 0 was given.\nHer's an example >> phone Name"


#=========================================================
# >> show all
# По этой команде бот выводит все сохраненные контакты 
# с номерами телефонов в консоль.
#=========================================================
@dec_func_all_phone
def func_all_phone(_)->str:
    result =  "\n".join([f"{person} - {persons[person]}" for person in persons])
    if result == "": return "The database is empty"
    else: return result


# Рахує кількість параметрів
def get_count_prm(prm):
    if len(prm) > 0: 
        count_prm = prm.count(" ", 0, -1) + 1
    else: count_prm = 0
    return count_prm


#=========================================================
# Функція виконує парсер команд та відповідних параметрів
#=========================================================
def parcer_commands(cmd_line):
    lst, tmp, cmd, prm  = [[], [], "", ""]
    
    if cmd_line:
        tmp = cmd_line.split()
        
        # перевіремо ПОДВІЙНУ команду
        if len(tmp) > 1 and f"{tmp[0]} {tmp[1]}".lower() in COMMANDS:
            cmd = f"{tmp[0]} {tmp[1]}".lower()
            
        # перевіремо ОДИНАРНУ команду
        elif tmp[0].lower() in COMMANDS:
            cmd = tmp[0].lower()
            prm = cmd_line.partition(" ")[2]
    return cmd, prm


COMMANDS = ["good bye", "close", "exit",
            "hello", "add", "change", "phone", "show all", "save", "load"]

OPERATIONS = {"good bye": func_exit, "close": func_exit, "exit": func_exit,
              "hello": func_greeting, 
              "add": func_add, 
              "change": func_change,
              "phone": func_phone, 
              "show all": func_all_phone,
              "save": save_phoneDB,
              "load": load_phoneDB}

# OPERATIONS = {func_exit : ["good bye", "close", "exit"],
#               func_greeting : ["hello"],
#               func_add : ["add"],
#               func_change : ["change"],
#               func_phone : ["phone"],
#               func_all_phone : ["show all"]}
        
if __name__ == "__main__":
    main()