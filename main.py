from flask import Flask,render_template,request

app = Flask("__main__")


tasks = []

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        task =request.form.get("task")
        tasks.insert(0,task)
        return render_template("home.html",tasks=tasks)
    else:
        
        return render_template("Home.html")



if __name__ == "__main__":
    app.run(debug=True)
