from flask import Flask, render_template, request, redirect,url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key="asdf-ghjkl"

DB_HOST="localhost"
DB_NAME="sql_demo"
DB_USER="postgres"
DB_PASS="jda19@krj"

conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)

@app.route("/")
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s="SELECT * FROM todotask ORDER BY sno ASC"
    cur.execute(s)
    list_users=cur.fetchall()
    return render_template('index.html', list_users=list_users)

@app.route('/add_task',methods=['POST'])
def add_task():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        
        title=request.form['title']
        desc=request.form['desc']
        cur.execute("INSERT INTO todotask(title, description) VALUES (%s,%s)",(title,desc))
        conn.commit()
        flash('Your task was added successfully')
        return redirect(url_for('Index'))





@app.route('/update/<sno>',methods=['POST', 'GET'])
def get_task(sno):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM todotask WHERE sno = %s' % (sno))
    data=cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('update.html', task=data[0])




@app.route('/update1/<sno>',methods=['POST'])
def update_task(sno):
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE todotask
            SET title = %s,
                description = %s
            
            WHERE sno= %s 
        """,(title, desc, sno)) 
        
        flash('Your task was updated successfully')
        conn.commit()
        return redirect(url_for('Index'))



@app.route('/delete/<string:sno>', methods = ['POST','GET'])
def delete_student(sno):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM todotask WHERE sno = {0}'.format(sno))
    conn.commit()
    flash('Task Removed Successfully')
    return redirect(url_for('Index'))        


if __name__=="__main__":
    app.run(debug=True, port=5000)    