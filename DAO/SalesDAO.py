from core.dbConexion import dbConexion
import json
from datetime import datetime
from bson.objectid import ObjectId
from DAO.ProductsDAO import ProductsDAO
from DAO.ConceptsDAO import ConceptsDAO
from DAO.SessionDAO import SessionDAO
from typing import List
connection = dbConexion("localhost", 27017, "", "", "StoreDB_Distri")

class SalesDAO:
    def __init__(self):
        pass

    def RegisterSale(self, userId, total, concepts: List[dict] ):
        connection.connect()
        query = {"Datetime": datetime.now(), "userId": userId, "total":total}
        result = connection.insert("sales", query)
        saleId = result.inserted_id 
        for requestConcept in concepts:
            product = ProductsDAO()
            producto = product.GetProductsById(requestConcept["productId"])
            conceptNew = {
                "quantity": requestConcept["quantity"],
                "saleId": saleId,
                "productId": requestConcept["productId"],
                "price": requestConcept["price"],
                "import": requestConcept["quantity"] * requestConcept["price"]
            }
            result = connection.insert("concepts", conceptNew)
            stockNow = producto["stock"] - requestConcept["quantity"]
            stockUpdate = product.UpdateProduct(requestConcept["productId"], stock=stockNow)
            
        return result.acknowledged
    
    def GetSaleOfCustomer(self,userId):
        connection.connect()
        query = {"userId": userId}
        result = connection.select("sales", query)
        saleCustomer = list()
        sales = list(result)
        for sale in sales:
            query2 = {"saleId": sale["_id"]}
            result2 = connection.select("concepts", query2)
            conceptos = list(result2)
            for concept in conceptos:
                
        return result_list
        