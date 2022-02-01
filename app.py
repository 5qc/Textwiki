import os, re
from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder="templates")

pagesDir = "pages"

@app.errorhandler(404)
def error404():
    return render_template("404.html")

@app.route("/")
def index():
    return redirect("/index", 302)
@app.route("/<string:page>")
def getPage(page):
    for file in os.listdir(pagesDir):
        if page in file:
            with open(f"{pagesDir}/{page}.txt") as f:
                content = f.read()
                content = content.replace("\n", "<br />")

                italic = re.compile(r"\*(.*?)\*")
                bold   = re.compile(r"\*\*(.*?)\*\*")
                underline = re.compile(r"\_(.*?)\_")
                strike = re.compile(r"\-(.*?)\-")
                sub = re.compile(r"\^(.*?)\^")
                sup = re.compile(r"\^\^(.*?)\^\^")
                heading1 = re.compile(r"#(.*?)#")
                heading2 = re.compile(r"##(.*?)##")
                heading3 = re.compile(r"###(.*?)###")
                heading4 = re.compile(r"####(.*?)####")
                heading5 = re.compile(r"#####(.*?)#####")
                heading6 = re.compile(r"######(.*?)######")

                content = re.sub(bold, r"<b>\1</b>", content)
                content = re.sub(italic, r"<i>\1</i>", content)
                content = re.sub(underline, r"<u>\1</u>", content)
                content = re.sub(strike, r"<s>\1</s>", content)
                content = re.sub(sup, r"<sup>\1</sup>", content)
                content = re.sub(sub, r"<sub>\1</sub>", content)
                content = re.sub(heading6, r"<h6>\1</h6>", content)
                content = re.sub(heading5, r"<h5>\1</h5>", content)
                content = re.sub(heading4, r"<h4>\1</h4>", content)
                content = re.sub(heading3, r"<h3>\1</h3>", content)
                content = re.sub(heading2, r"<h2>\1</h2>", content)
                content = re.sub(heading1, r"<h1>\1</h1>", content)

                # Links
                link = re.compile(r"\[(.+?)\]\((.*?)\)")
                content = re.sub(link, r'<a href="\2">\1</a>', content)

                # Images
                image = re.compile(r"\{(.*?)\}")
                image2 = re.compile(r"\{(.*?)\}(.*?)(?= )")
                image3 = re.compile(r"\{(.*?)\}(.*?),(.*?)(?= )")

                content = re.sub(image3, r'<img src="/static/img/\1" class="\2" width="\3px" alt="\1" />', content)
                content = re.sub(image2, r'<img src="/static/img/\1" class="\2" alt="\1" />', content)
                content = re.sub(image, r'<img src="/static/img/\1" alt="\1" />', content)

                # Return Content
                return render_template("page.html", title=page, content=content)
    
@app.route("/s:create")
def createPage():
    return render_template("create-page.html")
