import mysql.connector
import os

# fonction pour envoyer un fichier en db

def convertToBinary(filename):
        with open(filename, 'rb') as file:
                binaryData = file.read()
        return binaryData

def insertBLOB(file, id):
    
    try:
        mydb = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='mydatabase')
            
        mycursor = mydb.cursor()
        #query = "INSERT INTO file (id, content, path, owner_id, edits, size, hotcold) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        #binFile = convertToBinary(file)
        query1 = "INSERT INTO user (id, username, password, user_type, spaceleft) VALUES (3, 'admin1', 'admin1', 0, 100);"
        #insertTuple = (1, binFile, "",id,0,os.path.getsize(file),"cold")

        #result = mycursor.execute(query, insertTuple)
        result = mycursor.execute(query1)
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


insertBLOB("/Users/theorolino/Documents/GitHub/inha_db_project/testText.txt",2)

##fonctions pour prendre un fichier en db, le storer sur le pc, l'ouvrir et l'éditer
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def updateBLOB(id, fileToSave, textToAdd):
    try:
        mydb = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='db_project_inha')  

        mycursor = mydb.cursor()

        query = "SELECT * FROM file where id = %s"
        mycursor.execute(query, (id,))

        record = mycursor.fetchall()

        for row in record:
            content = row[1]
            edits = row[4]
            print(edits)
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
            print(buffersize)

        if os.path.getsize(fileToSave) < buffersize:
            query = "UPDATE file SET content = %s, edits = %s, hotcold=%s, size=%s WHERE id=%s"
            mycursor.execute(query, (newFileToDatabase, edits+1, hotness,os.path.getsize(fileToSave),id,))
        else :
            query = "UPDATE file SET path = %s, edits = %s, hotcold=%s, size=%s WHERE id=%s"
            mycursor.execute(query, (fileToSave, edits+1, hotness, os.path.getsize(fileToSave), id,))

        
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")

#updateBLOB(1, "C:\\Users\\Pidanou\\Documents\\inha\\database\\inha_db_project\\testreadfile.txt", "\nadded text")