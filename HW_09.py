'''
На первом этапе наш бот-ассистент должен уметь:
 - сохранять имя и номер телефона, 
 - находить номер телефона по имени,
 - изменять записанный номер телефона,
 - выводить в консоль все записи, которые сохранил. 
 
 Чтобы реализовать такую несложную логику, воспользуемся словарем. 
 В словаре будем хранить имя пользователя как ключ и номер телефона как значение.
'''

#import shutil
from pathlib import Path
import os
import platform # для clearscrean()

persons = {}   # "name": "0975634583"



# Головна функція роботи CLI(Command Line Interface - консольного скрипту)  
def main():
    cmd = [""]
    
    path = Path("D:\Git\HW_09\database_09.csv")
    load_phoneDB(path)
    
    # головний цикл обробки команд користувача
    while True:
        
        # 1. Отримаємо команду від користувача
        cmd = input(">> ")    
        
        # 2. Виконуємо розбір командної строки
        cmd, prm = parcer_commands(cmd)
        
        # 3. Виконуємо ДІЮ handler_functions
        handler = get_handler(cmd)
        
        if cmd in ["add", "change", "phone", "show all"]:
            handler(prm)
        else:
            handler()
                
        # 4. Друкуємо результати або повідомлення
    
 
def clear_screen():
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        os.system('cls')
    elif os_name == 'linux' or os_name == 'darwin':
        os.system('clear')
        
         
#=========================================================
# Функція читає базу даних з файлу
#========================================================= 
def load_phoneDB(path):
    #dct = {}
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
        print(f"Database is loaded = {len(persons)} records")
    except FileNotFoundError: print("Database isn't founded.")
    #finally: return dct

#=========================================================
#
#========================================================= 
def save_applicant_data(source, output):
    lst = []
    with open(output, "w") as f_out:
        for student in source:
            line = ",".join(str(value) for value in student.values())
            line += "\n"
            f_out.write(line)
    f_out.close()
       
#=========================================================
# >> "good bye", "close", "exit"
# По любой из этих команд бот завершает свою роботу 
# после того, как выведет в консоль "Good bye!".
#=========================================================
def func_exit():
    print("func Good bye!")
    pass

#=========================================================
# >> hello
# Отвечает в консоль "How can I help you?"
#=========================================================
def func_greeting():
    print("How can I help you?")
    pass

#=========================================================
# >> add ...  
# По этой команде бот сохраняет в памяти (в словаре например) новый контакт. 
# Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
#=========================================================
def func_add():
    print("func Add")
    pass

#=========================================================
# >> change ...
# По этой команде бот сохраняет в памяти новый номер телефона 
# для существующего контакта. Вместо ... пользователь вводит 
# имя и номер телефона, 
# Внимание: обязательно через пробел!!!
#=========================================================
def func_change():
    print("func Change")
    pass

#=========================================================
# >> phone ...
# По этой команде бот выводит в консоль номер телефона для указанного контакта.
# Вместо ... пользователь вводит имя контакта, чей номер нужно показать.
#=========================================================
def func_phone(prm):
    #print("func Phone")
    print(persons[prm])

#=========================================================
# >> show all
# По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.
#=========================================================
def func_all_phone(prm):
    #print("func All Phone")
    for person in persons:
        print(f"{person} - {persons[person]}")



def get_handler(operator):
    return OPERATIONS[operator]


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
        elif tmp[0] in COMMANDS:
            cmd = tmp[0].lower()
            prm = cmd_line.partition(" ")[2]
    return cmd, prm


COMMANDS = ["goodbye", "close", "exit",
            "hello", "add", "change", "phone", "show all"]

# OPERATIONS = {"good bye": func_exit, "close": func_exit, "exit": func_exit,
#               "hello": func_greeting, 
#               "add": func_add, 
#               "change": func_change,
#               "phone": func_phone, 
#               "show all": func_all_phone}

OPERATIONS = {func_exit : ["good bye", "close", "exit"],
              func_greeting : ["hello"],
              func_add : ["add"],
              func_change : ["change"],
              func_phone : ["phone"],
              func_all_phone : ["show all"]}
        
if __name__ == "__main__":
    main()