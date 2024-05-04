from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'todoapp'

mysql = MySQL(app)

@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute("select * from todotable")
    tasks = cur.fetchall()
    return render_template("base.html", tasks = tasks)

@app.route('/add', methods = ["POST"])
def add():
    title = request.form.get("title")
    cur = mysql.connection.cursor()

    cur.execute("insert into todotable(title, complete) values(%s , %s)",(title, False))
    mysql.connection.commit()
    cur.close()

    return  redirect(url_for("main"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    cur = mysql.connection.cursor()
    cur.execute("update todotable set complete = %s  where id = %s",(True, todo_id))
    mysql.connection.commit()
    return redirect(url_for("main"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    cur = mysql.connection.cursor()
    cur.execute("delete from todotable where id = %s",[str(todo_id)])
    mysql.connection.commit()

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(debug=True)