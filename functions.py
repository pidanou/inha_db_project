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
                              database='inha_db_project')
            
        mycursor = mydb.cursor()
        query = "INSERT INTO file (id, content, path, owner, edits, size, hotcold) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        binFile = convertToBinary(file)

        insertTuple = ("", binFile, "",id,0,os.path.getsize(file),"cold")

        result = mycursor.execute(query, insertTuple)
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


#insertBLOB("C:\\Users\\Pidanou\\Documents\\inha\\database\\inha_db_project\\testfile.txt",2)

##fonctions pour prendre un fichier en db, le storer sur le pc, l'ouvrir et l'éditer
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def updateBLOB(id, fileToSave, textToAdd):
    try:
        mydb = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='inha_db_project')  

        mycursor = mydb.cursor()

        query = "SELECT * FROM file where id = %s"
        mycursor.execute(query, (id,))

        record = mycursor.fetchall()

        for row in record:
            print(row[0])
            content = row[1]
            edits = row[4]
            print(edits)
            hotness = row[5]
            write_file(content, fileToSave)
            
        
        with open(fileToSave,"a") as f:
            f.write(textToAdd)
            f.close()
        
        newFileToDatabase = convertToBinary(fileToSave)

        if edits > 4:
            hotness = "hot"
        else:
            hotness = "cold"

        query = "UPDATE file SET content = %s, edits = %s, hotcold=%s, size=%s WHERE id=%s"
        mycursor.execute(query, (newFileToDatabase, edits+1, hotness,os.path.getsize(fileToSave),id,))
        mydb.commit()

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")

updateBLOB(0, "C:\\Users\\Pidanou\\Documents\\inha\\database\\inha_db_project\\testreadfile.txt", "\nadded text")