from email.mime import image
from app import app
from model.blog_model import blog_model
from flask import request
from datetime import datetime


blog_obj=blog_model()


# ***********************************************************
# create
# ***********************************************************
@app.route("/create/one", methods=["POST"])
def create_one_blog():
    return blog_obj.create_one_blog(request.json)


@app.route("/add/usingcsv", methods=["POST"])
def add_blog_using_csv():
    csv_file=request.files['csv']
    csv_file_path="csv_file/csv_data.csv"
    csv_file.save(csv_file_path)
    return blog_obj.add_blog_using_csv(csv_file_path)


@app.route("/add/imagebyid/<id>", methods=["PATCH"])
def add_image(id):
    image_file = request.files['image']
    image_new_name =  str(datetime.now().timestamp()).replace(".", "")
    split_filename = image_file.filename.split(".")
    image_extension=len(split_filename)-1 
    image_extension=split_filename[image_extension]
    image_path=f"blog_images/{image_new_name}.{image_extension}"
    image_file.save(image_path)
    return blog_obj.add_image(id, image_path)


# ***********************************************************
# read
# ***********************************************************
@app.route("/read/byid/<id>")
def read_blog_by_id(id):
    return blog_obj.read_blog_by_id(id)

@app.route("/read/bycolumn")
def read_column():
    return blog_obj.read_column(request.json)

@app.route("/read/all")
def read_all_blog():
    return blog_obj.read_all_blog()

@app.route("/read/byname/<author_name>")
def read_by_author_name(author_name):
    return blog_obj.read_by_author_name(author_name)

@app.route("/read/page/<page_number>/limit/<limit>")
def read_by_page(page_number,limit):
    return blog_obj.read_by_page(page_number, limit)


# ***********************************************************
# update
# ***********************************************************
@app.route("/update/byid", methods=["PUT"])
def update_blog_by_id():
    return blog_obj.update_blog_by_id(request.json)


# ***********************************************************
# delete
# ***********************************************************
@app.route("/delete/byid/<id>", methods=["DELETE"])
def delete_blog_by_id(id):
    return blog_obj.delete_blog_by_id(id)

@app.route("/delete/all", methods=["DELETE"])
def delete_all_blogs():
    return blog_obj.delete_all_blogs()


@app.route("/delete/byname/<author_name>", methods=["DELETE"])
def delete_blog_by_author(author_name):
    return blog_obj.delete_blog_by_author(author_name)
    

