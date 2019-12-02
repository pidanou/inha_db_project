import mysql.connector
import os

mydb = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='mydatabase')
            
mycursor = mydb.cursor()

def verif_user(name, id_user): #la valeur name est jamais utiliser juste a cause du switch je dois le mettre 
    os.system ('clear')
    print("log in")
    user = input("username:")
    password = input("password:")
    sql_user = "select user_type,username,id from user where username=%s and password=%s"
    sql_user_values = (user, password)

    mycursor.execute(sql_user, sql_user_values)

    myresult = mycursor.fetchall() # recuperation du user 
    print(myresult)
    res = len(myresult)

    if (res == 0): # on verifie que le user exist
        print("no user find")
        os.system ('clear')
        verif_user("", 0) # pas de user 
    else:
        verif_type(myresult[0][0], myresult[0][1], myresult[0][2])# user valider

def verif_type(type_user, username, id_user):
    choices = {'add': add, 'get': get, 'updt': update, 'del': delete, 'logout': verif_user, 'size': size}
    #os.system ('clear')
    CRED1 = "\033[91m"
    CEND = "\033[0m"
    value = ""
    while (value != "exit"):
        #os.system ('clear')
        print("Option:\nadd a file:\n\tadd [file_name]\n\nget files:\n\tget [hot/cold] [small/big] \n\nupdate a file:\n\tupdt [id_file] [file_name_temp] [textToAdd]\n\ndelete a file:\n\tdel [id_file]")
        value = input(CRED1 + username + ":" + CEND) #recuperation de l'action
        option = value.split(' ') # split l'action
        result = choices.get(option[0], 'default') # switch improvisé
        try:
            result(option, id_user, type_user) # lancement de la function en fonction  de l'action
        except:
             os.system ('clear')

def get(option, id_user, type_user):
    if (option[1] == "hot"):
        if (option[2] == "big"):
            getCountHotBig()
        elif (option[2] == "small"):
            getCountHotSmall()
        else:
            print("not good parameter")
    elif (option[1] == "cold"):
        if (option[2] == "big"):
            getCountColdBig()
        elif (option[2] == "small"):
            getCountColdSmall()
        else:
            print("not good parameter")
    else:
        print("not good parameter")

def size(option, id_user, type_user):
    if (type_user == 0):
        if (option[1] == "buffer"):
            changeBufferSize(option[2])
        elif (option[1] == "space"):
            changeSpaceAllowed(option[2])
        else:
            print("not good parameter")
    else:
        print("not authorized")


def add(option, id_user, type_user):
    file = option[1]
    try:
        query = "INSERT INTO file (content, path, owner_id, edits, size, hotcold) VALUES (%s,%s,%s,%s,%s,%s)"

        binFile = convertToBinary(file)

        insertTuple = (binFile, "",id_user,0,os.path.getsize(file),"cold")

        mycursor.execute(query, insertTuple)
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")

def convertToBinary(filename):
        with open(filename, 'rb') as file:
                binaryData = file.read()
        return binaryData

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def update(option, id_user, type_user):
    id_file = option[1]
    fileToSave = option[2]
    textToAdd = option[3]
    try:

        query = "SELECT * FROM file where id = %s"
        mycursor.execute(query, (id_file, ))

        record = mycursor.fetchall()
        for row in record:
            content = str.encode(row[1])
            edits = row[4]
            hotness = row[5]
            write_file(content, fileToSave)
            
        filesize = os.path.getsize(fileToSave)
        print(filesize)

        with open(fileToSave,"a") as f:
            f.write(textToAdd)
            f.close()
        
        newFileToDatabase = convertToBinary(fileToSave)

        if edits > 4:
            hotness = "hot"
        else:
            hotness = "cold"

        querySize = "SELECT value from dbsettings where name= 'buffersize'"
        mycursor.execute(querySize)
        r = mycursor.fetchall()
        for row in r:
            buffersize = row[0]

        if os.path.getsize(fileToSave) < buffersize:
            query = "UPDATE file SET content = %s, edits = %s, hotcold=%s, size=%s WHERE id=%s"
            mycursor.execute(query, (newFileToDatabase, edits+1, hotness,os.path.getsize(fileToSave),id_file,))
        else :
            query = "UPDATE file SET path = %s, edits = %s, hotcold=%s, size=%s WHERE id=%s"
            mycursor.execute(query, (fileToSave, edits+1, hotness, os.path.getsize(fileToSave), id_file,))

        
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


def delete(option, id_user, type_user):
    sql_for_del = "DELETE from file where id=%s"
    sql_for_del_value = (option[1])
    mycursor.execute(sql_for_del, (sql_for_del_value, ))
    mydb.commit()


def getCountColdSmall():
    query = "SELECT count(edits) FROM file WHERE hotcold = 'cold' AND size not in (SELECT value from dbsettings where name= 'buffersize')"
    mycursor.execute(query)

    result = mycursor.fetchall()
    for r in result:
        result = (r[0])
    return result

def getCountColdBig():
    query = "SELECT count(edits) FROM file WHERE hotcold = 'cold' AND size in (SELECT value from dbsettings where name= 'buffersize')"
    mycursor.execute(query)

    result = mycursor.fetchall()
    for r in result:
        result = (r[0])
    return result

def getCountHotSmall():
    query = "SELECT count(edits) FROM file WHERE hotcold = 'hot' AND size in (SELECT value from dbsettings where name= 'buffersize')"
    mycursor.execute(query)

    result = mycursor.fetchall()
    for r in result:
        result = (r[0])
    return result

def getCountHotBig():
    query = "SELECT count(edits) FROM file WHERE hotcold = 'hot' AND size not in (SELECT value from dbsettings where name= 'buffersize')"
    mycursor.execute(query)

    result = mycursor.fetchall()
    for r in result:
        result = (r[0])
    return result

def changeBufferSize(size):
    query = "UPDATE dbsettings SET value = %s WHERE name='buffersize'"
    mycursor.execute(query, (size,))
    mydb.commit()

def changeSpaceAllowed(size):
    query = "UPDATE dbsettings SET value = %s WHERE name='spaceallow'"
    mycursor.execute(query, (size,))
    mydb.commit()

verif_user("", 0)

mydb.close()