import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Connection:

    def __init__(self):
        self.connection = None

        port = os.environ.get("DATABASE_PORT")
        if port is None:
        	port = 3306
        else:
        	port = int(port)

        try:
            self.connection = mysql.connector.connect(
                user=os.environ.get("DATABASE_USER"),
                password=os.environ.get("DATABASE_PASSWORD"),
                host=os.environ.get("DATABASE_HOST"),
                port=port,
                database=os.environ.get("DATABASE_NAME")
            )
        except Exception as e:
            print("WARNING: Unable to connected to database. Bot will still work, but it won't store any data")
            print(e)


    def query(self, sql, params = tuple(), commit = True):
        result = []
        if self.connection is None:
            return result

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        for touple in cursor:
            result.append(touple)

        if commit:
            self.connection.commit()
        cursor.close()

        return result

    def getFactories(self):
        sql = "SELECT F.Author, F.Name AS name, P.Name AS product FROM Factory F JOIN Product P ON F.Product = P.IdProduct"

        factories = self.query(sql)
        result = {}
        for (Author, Name, Product) in factories:
            result[Author] = {
                "name": Name,
                "product": Product
            }

        return result

    def getInventories(self):
        sql = "SELECT I.Owner, P.Name as product, I.Amount as amount FROM Inventory I JOIN Product P ON I.Product = P.IdProduct"

        inventories = self.query(sql)
        result = {}
        for (Owner, Product, Amount) in inventories:
            if not Owner in result:
                result[Owner] = {}
            result[Owner][Product] = Amount

        return result

    def insertProduct(self, name, inventor):
        sql = "INSERT IGNORE INTO Product (Name, Inventor) VALUES (%s, %s)"

        response = self.query(sql, tuple([name, inventor]))

    def getProductByName(self, name):
        sql = "SELECT IdProduct FROM Product WHERE Name = %(name)s"

        response = self.query(sql, {"name": name})
        if len(response) > 0:
            for (IdProduct, ) in response:
                return IdProduct
        else:
            return None

    def insertFactory(self, author, name, productName):
        self.insertProduct(productName, author)
        product = self.getProductByName(productName)

        sql = "INSERT INTO Factory (Author, Name, Product) VALUES (%s, %s, %s)"
        result = self.query(sql, tuple([author, name, product]))

        if len(result) == 0:
            return False
        return True

    def deleteFactory(self, author):
        sql = "DELETE FROM Factory WHERE Author = %(author)s"
        result = self.query(sql, {"author": author})

        if len(result) == 0:
            return False
        return True

    def createInventory(self, owner, productName, amount):
    	product = self.getProductByName(productName)
    	sql = "INSERT IGNORE INTO Inventory (Owner, Product, Amount) VALUES (%s, %s, %s)"
    	self.query(sql, tuple([owner, product, amount]))

    def updateInventory(self, owner, productName, amount):
    	product = self.getProductByName(productName)
    	sql = "UPDATE Inventory SET Amount = %s WHERE Owner = %s AND Product = %s"
    	self.query(sql, tuple([amount, owner, product]))

    def kakeraList(self):
        sql = "SELECT User, Channel FROM Kakera"
        return self.query(sql)

    def kakeraSubscribe(self, userId, channelId):
        sql = "INSERT IGNORE INTO Kakera (User, Channel) VALUES (%(userId)s, %(channelId)s)"
        result = self.query(sql, {"userId": userId, "channelId": channelId})
        return len(result) > 0

    def kakeraUnsubscribe(self, userId, channelId):
        sql = "DELETE FROM Kakera WHERE User = %(userId)s AND Channel = %(channelId)s"
        result = self.query(sql, {"userId": userId, "channelId": channelId})
        return len(result) > 0

