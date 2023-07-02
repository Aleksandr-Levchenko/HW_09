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
import platform # для clearscrean()

persons = {}   # "name": "0975634583"



# Головна функція роботи CLI(Command Line Interface - консольного скрипту)  
def main():
    cmd = ""
    
    path = Path("D:\Git\HW_09\database_09.csv")
    
    # головний цикл обробки команд користувача
    while True:
        
        # 1. Отримаємо команду від користувача
        cmd = input(">> ")    
        
        # 2. Виконуємо розбір командної строки
        cmd, prm = parcer_commands(cmd)
        
        # 3. Отримуємо handler_functions тобто ДІЮ
        handler = get_handler(cmd)
        
        # 4. Визначемо параметри для handler() 
        #    та виконаємо Команду користувача
        run_handler(handler)
        
        if cmd in ["add", "change", "phone"]:
            print(handler(prm))
        elif cmd in ["close", "exit", "good bye"]:
            print(handler(""))
            break
        elif cmd in ["save", "load"]:
            handler(path)            
        elif cmd in ["show all", "hello"]:
            print(handler(""))
            
            
            
# Повертає адресу функції, що обробляє команду користувача
def get_handler(operator):
    return OPERATIONS[operator]        
 

# Декоратор для Обробки командної строки
def input_error(func):
    def inner(cmd_line):
        result = func(cmd_line)
        return result
    return inner
 
 
@input_error 
def run_handler(handler):
    pass
    
     
def clear_screen():
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        os.system('cls')
    elif os_name == 'linux' or os_name == 'darwin':
        os.system('clear')


# Декоратор для Завантаження бази даних із файлу
def dec_load_phoneDB(func):
    def inner(path):
        print(func(path))
    return inner
        
         
#=========================================================
# Функція читає базу даних з файлу
#========================================================= 
@dec_load_phoneDB
def load_phoneDB(path):
    try:
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
    except FileNotFoundError: return "The database isn't found."


# Декоратор для Збереження бази даних у файл
def dec_save_phoneDB(func):
    def inner(path):
        print(func(path))
    return inner


#=========================================================
# Функція виконує збереження бази даних у файл *.csv
#========================================================= 
@dec_save_phoneDB
def save_phoneDB(path):
    with open(path, "w") as f_out:
        f_out.write("\n".join([":".join([person, value]) for person, value in persons.items()]))
    return f"The database is saved = {len(persons)} records"  
       
       
# Декоратор для Завершення роботи      
def dec_func_exit(func):
    def inner():
        print(func())
    return inner
    
    
#=========================================================
# >> "good bye", "close", "exit"
# По любой из этих команд бот завершает свою роботу 
# после того, как выведет в консоль "Good bye!".
#=========================================================
@dec_func_exit
def func_exit(_):
    return "Good bye!"


# Декоратор для команди Вітання      
def dec_func_greeting(func):
    def inner():
        print(func())
    return inner


#=========================================================
# >> hello
# Отвечает в консоль "How can I help you?"
#=========================================================
@dec_func_greeting
def func_greeting(_):
    return "How can I help you?"


# Декоратор для Додавання нової людини у базу
def dec_func_add(func):
    def inner(prm):
        print(func(prm))
    return inner
    
#=========================================================
# >> add ...  
# По этой команде бот сохраняет в памяти (в словаре например) новый контакт. 
# Вместо ... пользователь вводит ИМЯ и НОМЕР телефона, обязательно через пробел.
#=========================================================
@dec_func_add
def func_add(prm):
    if prm and len(prm) > 2:
        # Якщо ключ (ІМ'Я) що користувач хоче ДОДАТИ не ІСНУЄ тобто можемо додавати
        if not prm.partition(" ")[0] in persons:
            persons[prm.partition(" ")[0]] = prm.partition(" ")[2]    # Додаємо нову людину
        else: return "Person is already in database"  # Повернемо помилку -> "Неможливо дадати існуючу людину"
    else:
        return "Expected 2 parameters >> add name phone"
    return ""


# Декоратор для Внесення змін у базу даних
def dec_func_change(func):
    def inner(prm):
        print(func(prm))
    return inner
    
    
#=========================================================
# >> change ...
# По этой команде бот сохраняет в памяти новый номер телефона 
# для существующего контакта. 
# Вместо ... пользователь вводит Имя и Номер телефона, 
# Внимание: обязательно через пробел!!!
#=========================================================
@dec_func_change
def func_change(prm):
    persons[prm.partition(" ")[0]] = prm.partition(" ")[2]
    return f"Records for {prm.partition(' ')[0]} is changed"


# Декоратор для Знайденя телефону за Ім'ям особи
def dec_func_phone(func):
    def inner(prm):
        print(func(prm))
    return inner


#=========================================================
# >> phone ...
# По этой команде бот выводит в консоль номер телефона для указанного контакта.
# Вместо ... пользователь вводит имя контакта, чей номер нужно показать.
#=========================================================
@dec_func_phone
def func_phone(prm):
    return persons[prm]


# Декоратор для Друкування всієї бази даних
def dec_func_all_phone(func):
    def inner():
        print(func())
    return inner


#=========================================================
# >> show all
# По этой команде бот выводит все сохраненные контакты 
# с номерами телефонов в консоль.
#=========================================================
@dec_func_all_phone
def func_all_phone(_)->str:
    return "\n".join([f"{person} - {persons[person]}" for person in persons])



    

#=========================================================
# Функція виконує парсер команд та відповідних параметрів
#=========================================================
@input_error
def parcer_commands(cmd_line):
    lst, tmp, cmd, prm  = [[], [], "", ""]
    
    if cmd_line:
        tmp = cmd_line.split()
        
        # перевіремо ПОДВІЙНУ команду
        if len(tmp) > 1 and f"{tmp[0]} {tmp[1]}".lower() in COMMANDS:
            cmd = f"{tmp[0]} {tmp[1]}".lower()
            
        # перевіремо ОДИНАРНУ команду
        elif tmp[0] in COMMANDS:
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