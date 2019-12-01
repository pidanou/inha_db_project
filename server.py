import mysql.connector
import os

mydb = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='mydatabase')
            
mycursor = mydb.cursor()

def verif_user(name): #la valeur name est jamais utiliser juste a cause du switch je dois le mettre 
    os.system ('clear')
    print("log in")
    user = input("username:")
    password = input("password:")

    sql_user = "select user_type,username from user where username=%s and password=%s"
    sql_user_values = (user, password)

    mycursor.execute(sql_user, sql_user_values)

    myresult = mycursor.fetchall() # recuperation du user 

    res = len(myresult)

    if (res == 0): # on verifie que le user exist
        print("no user find")
        os.system ('clear')
        verif_user("") # pas de user 
    else:
        verif_type(myresult[0][0], myresult[0][1])# user valider

def verif_type(type_user, username):
    choices = {'add': add, 'get': get, 'updt': update, 'del': delete, 'logout': verif_user}
    os.system ('clear')
    CRED1 = "\033[91m"
    CEND = "\033[0m"
    value = ""
    while (value != "exit"):
        #os.system ('clear')
        print("Option:\nadd a file:\n\tadd [name] [file_name]\n\nget a file:\n\tget [name]\n\nupdate a file:\n\tupdt [name] [file_name] [file]\n\ndelete a file:\n\tdel [name] [file_name]")
        value = input(CRED1 + username + ":" + CEND) #recuperation de l'action
        option = value.split(' ') # split l'action
        result = choices.get(option[0], 'default') # switch improvisé
        result(option) # lancement de la function en fonction  de l'action

def get(option):
    print(type(option[1]))
    sql_file = "select route from files where filename=%s"
    sql_file_value = (option[1])

    mycursor.execute(sql_file, sql_file_value)
    myresult = mycursor.fetchall()
    print(myresult)

def add(option):

    sql_file = "insert into files (name, route, ??)"
    sql_file_value = (option[1])

    mycursor.execute(sql_file, sql_file_value)
    myresult = mycursor.fetchall()
    print(myresult)

def update(option):
    sql_file = "update files set route=%s,file=%s where name=%s"
    sql_file_value = (option[1])

    mycursor.execute(sql_file, sql_file_value)
    myresult = mycursor.fetchall()
    print(myresult)
    
def delete(option):
    sql_file = "delete from files where name=%s"
    sql_file_value = (option[1])

    mycursor.execute(sql_file, sql_file_value)
    myresult = mycursor.fetchall()
    print(myresult)

#def add_file():

#def update_file():


#def delete_file(name):  

verif_user("")

mydb.close()