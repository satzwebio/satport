import os
from flask import Flask, render_template, abort, request, Blueprint, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymongo

UPLOAD_FOLDER = r"C:\Users\satzw\OneDrive\Desktop\end\portfolio\static\img\projects"
CERT_FOLDER = r"C:\Users\satzw\OneDrive\Desktop\end\portfolio\static\img\certs"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

application = Flask(__name__)


application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['CERT_FOLDER'] = CERT_FOLDER

client = pymongo.MongoClient("mongodb+srv://satzmongo:w-Zet7tVY-ZwiDZ@portfolio.wzlekmv.mongodb.net/test")



# projects = [
#     {
#         "name": "Habit tracking app with Python and MongoDB",
#         "thumb": "img/habit-tracking.png",
#         "hero": "img/habit-tracking-hero.png",
#         "categories": ["python", "web"],
#         "slug": "habit-tracking",
#         "prod": "https://udemy.com",
#     },
#     {
#         "name": "Personal finance tracking app with React",
#         "thumb": "img/personal-finance.png",
#         "hero": "img/personal-finance.png",
#         "categories": ["react", "javascript"],
#         "slug": "personal-finance",
#     },
#     {
#         "name": "REST API Documentation with Postman and Swagger",
#         "thumb": "img/rest-api-docs.png",
#         "hero": "img/rest-api-docs.png",
#         "categories": ["writing"],
#         "slug": "api-docs",
#     },
# ]

application.db = client.portfolio
slug_to_project = {project["slug"]: project for project in application.db.projects.find({})}

@application.route("/")
def home():
   return render_template("home.html", projects= application.db.projects.find())

@application.route("/certs")
def certs():
    certslist=[]
    # certfold = UPLOAD_FOLDER+'\certs'
    # certfold= r"C:\Users\satzw\OneDrive\Desktop\end\portfolio\static"
    # print(certfold)
    # The below for loop need rewrite, bcz array is building from onediiver desktop;
    # so hard coding below
    certslist=['1Azure_Fundamentals.png','2azure-administrator-associate.png','3 aapngaaa.com-4173759.png','4azure-ai-engineer-600x600-1.png', 'Terraform.png']
    # for filename in os.listdir(CERT_FOLDER):
    #     certslist.append(filename)
    return render_template("certs.html", certslist=certslist)


@application.route("/about")
def about():
    return render_template("about.html")


@application.route("/contact")
def contact():
    return render_template("contact.html")


@application.route("/add_proj/", methods=["GET", "POST"])
def add_proj():
    if (request.method == "POST"):
        if 'submit' in request.form:
    #       Thumbnail file
            thumbf = request.files['thumb']
            thfilename = secure_filename(thumbf.filename)
            thumb = '/img/projects/'+thfilename # This is to upload db with file path
            if thfilename!="":
                thumbf.save(os.path.join(application.config['UPLOAD_FOLDER'], thfilename))
                thumbf.close()

    #       Arch file 
            archf = request.files['arch']
            arfilename = secure_filename(archf.filename)
            arch = '/img/projects/'+arfilename # This is to upload db with file path
            if arfilename!="":
                archf.save(os.path.join(application.config['UPLOAD_FOLDER'], arfilename))
                archf.close()      

    #       DB Update
            mydb = client["portfolio"]
            mycol = mydb["projects"]
            mycol.insert_one({
                "projname": request.form.get("projname"),
                "projdesc": request.form.get("projdesc"),
                "thumb": thumb,
                "arch": arch,
                "tech": request.form.getlist("techused"),
                "slug": request.form.get("slug"),
                "produrl": request.form.get("produrl")
                })
        return redirect(url_for('home'))
    return render_template('add_proj.html')
   

@application.route("/add_certs/", methods=["GET", "POST"])
def add_certs():
    if (request.method == "POST"):
        if 'submit' in request.form:
    #       Cert file 
            certf = request.files['certfile']
            certfilename = secure_filename(certf.filename)
            # arch = '/img/certs/'+certfilename
            if certfilename!="":
                certf.save(os.path.join(application.config['CERT_FOLDER'], certfilename))
                certf.close()  
        return redirect(url_for('certs'))
    return render_template('add_certs.html')

# Two ways to do this:
# - either store everything about a project in Python and populate a generic `project.html` template.
# - or as done here, have separate templates for each project
# At the end of the day, we have to write the project info somewhere, and HTML is a great tool for that.
# This allows each project to be slightly different as we choose,
# And with Jinja2 we can always reuse parts of the code as macros (more on that, later!)
@application.route("/project/<string:slug>")
def project(slug):
    slug_to_project = {project["slug"]: project for project in application.db.projects.find({})}
    if slug not in slug_to_project:
        abort(404)
    return render_template("project_detail.html", project=slug_to_project[slug])




@application.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
