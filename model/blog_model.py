from configs.config import dbconfig
from flask import make_response
import mysql.connector
from datetime import datetime
import csv

class blog_model():

    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
    
    # ***********************************************************
    # create
    # ***********************************************************
    def create_one_blog(self, data):
        data["date"]=datetime.now()
        sql_insert_query="INSERT INTO blog("
        for i in data:
            sql_insert_query+=f"{i}, "
        sql_insert_query=sql_insert_query[:-2]+") VALUES("
        for i in data:
            sql_insert_query+=f"\'{data[i]}\', "
        sql_insert_query=sql_insert_query[:-2]+")"
        self.cur.execute(sql_insert_query)
        if self.cur.rowcount>0:
            return make_response({"respons":"DATA_CREATE_SUCCESSFULLY"},201)
        else:
            return make_response({"respons":"DATA_NOT_CREATED"},204)

    def add_blog_using_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            csvreader = csv.reader(file)
            colunm_name = next(csvreader)
            colunm_name.append("date")
            sql_insert_query1="INSERT INTO blog("
            
            for i in colunm_name:
                sql_insert_query1+=f"{i}, "
            sql_insert_query1=sql_insert_query1[:-2]+") VALUES("
            sql_insert_query2=sql_insert_query1
            for row in csvreader:
                row.append(str(datetime.now()))
                for i in row:
                    sql_insert_query2+=f"\'{i}\', "
                sql_insert_query2=sql_insert_query2[:-2]+")"
                self.cur.execute(sql_insert_query2)
                if self.cur.rowcount>0:
                    pass
                else:
                    return make_response({"respons":"DATA_NOT_CREATED"},204)
                sql_insert_query2=sql_insert_query1

        
        return make_response({"respons":"DATA_CREATE_SUCCESSFULLY"},201)
        

    def add_image(self, id, image_path):
        self.cur.execute(f"UPDATE blog SET imageurl='{image_path}' WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"respons":"IMAGE_UPLOADED_SUCCESSFULLY", "path":image_path},201)
        else:
            return make_response({"respons":"NOTHING_TO_UPDATE"},204)

    # ***********************************************************
    # read
    # ***********************************************************
    def read_blog_by_id(self, id):
        self.cur.execute(f"SELECT * FROM blog WHERE id='{id}'")
        result=self.cur.fetchall()
        if len(result)>0:
            return make_response({"respons":result},200)
        else:
            return make_response({"respons":"DATA NOT FOUND"},204)

    def read_column(self, data):
        sql_query="SELECT "
        for i in data["column"]:
            sql_query+=f"{i}, "
        sql_query=sql_query[:-2]+" FROM blog"

        self.cur.execute(sql_query)
        result=self.cur.fetchall()
        if len(result)>0:
            return make_response({"respons":result},200)
        else:
            return make_response({"respons":"DATA NOT FOUND"},204)


    def read_all_blog(self):
        self.cur.execute("SELECT * FROM blog")
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"respons":result},200)
        else:
            return make_response({"respons":"DATA NOT FOUND"},204)

    def read_by_author_name(self, author_name):
        self.cur.execute(f"SELECT * FROM blog WHERE author='{author_name}'")
        result=self.cur.fetchall()
        if len(result)>0:
            return make_response({"respons":result},200)
        else:
            return make_response({"respons":"DATA NOT FOUND"},204)

    def read_by_page(self,page_number,limit):
        page_number = int(page_number)
        limit = int(limit)
        start = (page_number*limit)-limit
        query = f"SELECT * FROM blog LIMIT {start}, {limit}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"page":page_number, "per_page":limit,"this_page":len(result), "respons":result})
        else:
            return make_response({"respons":"No Data Found"}, 204)

    # ***********************************************************
    # update
    # ***********************************************************
    def update_blog_by_id(self, data):
        data["date"]=datetime.now()
        sql_update_query = "UPDATE blog SET "
        for i in data:
            if i!='id':
                sql_update_query += f"{i}='{data[i]}',"
        sql_update_query = sql_update_query[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(sql_update_query)
        if self.cur.rowcount>0:
            return make_response({"respons":"DATA_UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"respons":"NOTHING_TO_UPDATE"},204)


    # ***********************************************************
    # delete
    # ***********************************************************
    def delete_blog_by_id(self, id):
        self.cur.execute(f"DELETE FROM blog WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"respons":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER/ERROR"},500)

    def delete_all_blogs(self):
        self.cur.execute("DELETE FROM blog")
        if self.cur.rowcount>0:
            return make_response({"respons":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER/ERROR"},500)

    def delete_blog_by_author(self,  author_name):
        self.cur.execute(f"DELETE FROM blog WHERE author='{author_name}'")
        if self.cur.rowcount>0:
            return make_response({"respons":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER/ERROR"},500)
        