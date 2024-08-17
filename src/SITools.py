# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
from config import config
import sqlite3
from datetime import datetime


# -------------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "DHLForms|DHL2023"


# ---------------------------
#    Date Format
# ---------------------------
# def change_date_format(dt):
#    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

    
# -------------------------------------------------------------------------
# DB connection
# -------------------------------------------------------------------------

# ---- SQLite3 ---
# connection = sqlite3.connect('../src/db/database/DB_ITools.db')
# cursor = connection.cursor()
# print('DB connected successfully')

def dbconnection():
  # Connects to the specified SQLite database and returns a connection and cursor.
  connection = sqlite3.connect('../src/db/database/DB_ITools.db')
  cursor = connection.cursor()
  return connection, cursor

def tmpl_show_menu():
    return render_template_string(
        '''
        {%- for item in current_menu.children %}
            {% if item.active %}*{% endif %}{{ item.text }}
        {% endfor -%}
        '''
    )
    

# -------------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------------
@app.route('/')
def index():
    if session.get('user_logged') is None:
        # ---- Database Connection ----
        connection, cursor = dbconnection()
        # print('DB connected successfully')

        # ---- Database SQL Query ----
        webcall = open('../src/db/webcalls/login/warehouses_query.sql', mode='r')
        warehouses_query = webcall.read()
        webcall.close()
        cursor.execute(warehouses_query)
        warehouses_query_results = cursor.fetchall()

        # --- print(warehouses_query_results)
        return render_template('auth/login.html', warehouses_results=warehouses_query_results)
    else:
        user_logged = session.get('user_logged')
        warehouse_logged = session.get('warehouse_logged')
        return render_template('home.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged)

active_user = ''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ---- Data From HTML Form ----
        global active_user
        active_user = request.form['username']
        username = request.form['username']
        warehouses = request.form['warehouse']
        warehouse = warehouses.split()[0]
        # print(username, warehouse)
        session['user'] = username

        # ---- Database Connection ----
        connection, cursor = dbconnection()
        # print('DB connected successfully')

        # ---- Database SQL Query ----
        webcall = open('../src/db/webcalls/login/login_query.sql', mode='r')
        login_query = webcall.read()
        webcall.close()
        login_query = login_query.format(username, warehouse)
        cursor.execute(login_query)
        login_results = cursor.fetchall()
        # print(login_results)

        # ---- Login validation ----
        if len(login_results) == 0:
            print('Sorry, incorrect Credentials prohibed. Try again')
            login_error = 'User or Warehouse are not the correct one.'
            flash(login_error)
            return redirect(url_for('index'))
        else:
            # ---- Database SQL Query ----
            webcall = open('../src/db/webcalls/login/user_query.sql', mode='r')
            user_query = webcall.read()
            webcall.close()
            user_query = user_query.format(username, warehouse)
            cursor.execute(user_query)
            user_result = cursor.fetchone()
            print(user_result)
            session['user_logged'] = user_result[0]
            session['user_privileges'] = user_result[1]
            session['user_id_logged'] = username
            session['warehouse_logged'] = warehouses
            user_logged = session.get('user_logged')
            user_id_logged = session.get('user_id_logged')
            user_privileges = session.get('user_privileges')
            warehouse_logged = session.get('warehouse_logged')
            print(user_id_logged)
            return render_template("home.html", user_logged=f'{user_logged}', user_id_logged = user_id_logged,  warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        if session.get('user_logged') is None:
            return redirect(url_for('index'))
        else:
            login_error = 'User or Warehouse are not the correct one.'
            flash(login_error)
            return redirect(url_for('index'))


@app.route('/home')
def home():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        return render_template('home.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)


@app.route('/forms')
def forms():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
        connection, cursor = dbconnection()

        # ---- Database SQL Query ----
        webcall = open('../src/db/webcalls/forms/Active_forms_query.sql', mode='r')
        forms_query = webcall.read()
        webcall.close()
        forms_query = forms_query.format(warehouse)
        cursor.execute(forms_query)
        forms_results = cursor.fetchall()
        # print(forms_results)
        return render_template('forms.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, forms_results=forms_results)


@app.route('/tools')
def tools():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_id_logged = session.get('user_id_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
            # connection = sqlite3.connect('../src/db/database/DB_ITools.db')
            # cursor = connection.cursor()

        # Call the db connection function
        connection, cursor = dbconnection()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/Enabled_tools_query.sql', mode='r')
        tools_query = webcall.read()
        webcall.close()
        tools_query = tools_query.format(warehouse)
        cursor.execute(tools_query)
        enabled_tools_results = cursor.fetchall()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/not_finished_tasks_query.sql', mode='r')
        tasks_query = webcall.read()
        webcall.close()
        tasks_query = tasks_query.format(warehouse, user_id_logged)
        cursor.execute(tasks_query)
        all_tasks_results = cursor.fetchall()
        connection.close()

        boton_change = ('Done Tasks','done_tasks')
        note_change = ('Notes','notes')

        return render_template('tools.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, warehouse_logged=warehouse_logged, user_privileges=user_privileges, enabled_tools_results=enabled_tools_results, all_tasks_results=all_tasks_results, boton_change=boton_change, note_change=note_change)

@app.route('/done_tasks')
def done_tasks():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_id_logged = session.get('user_id_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
            # connection = sqlite3.connect('../src/db/database/DB_ITools.db')
            # cursor = connection.cursor()

        # Call the db connection function
        connection, cursor = dbconnection()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/Enabled_tools_query.sql', mode='r')
        tools_query = webcall.read()
        webcall.close()
        tools_query = tools_query.format(warehouse)
        cursor.execute(tools_query)
        enabled_tools_results = cursor.fetchall()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/done_tasks_query.sql', mode='r')
        tasks_query = webcall.read()
        webcall.close()
        tasks_query = tasks_query.format(warehouse, user_id_logged)
        cursor.execute(tasks_query)
        all_tasks_results = cursor.fetchall()
        connection.close()

        boton_change = ('Task To Do', 'tools')
        note_change = ('Notes', 'notes')
        return render_template('tools.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, warehouse_logged=warehouse_logged, user_privileges=user_privileges, enabled_tools_results=enabled_tools_results, all_tasks_results=all_tasks_results, boton_change=boton_change, note_change=note_change)


@app.route('/new_task')
def new_task():
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    user_id_logged = session.get('user_id_logged')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ---- Database Connection ----
    connection, cursor = dbconnection()

    # ---- Database Active tools query ----
    webcall = open('../src/db/webcalls/tools/tasks_statuses_query.sql', mode='r')
    statuses_query = webcall.read()
    webcall.close()
    cursor.execute(statuses_query)
    statuses_query_results = cursor.fetchall()

    return render_template('configuration/todo_add_task.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, user_privileges=user_privileges, warehouse_logged=warehouse_logged, warehouse=warehouse, statuses_query_results=statuses_query_results)


@app.route('/save_new_task', methods=["POST", "GET"])
def save_new_task():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # ----------------
            #    HTML Form
            # ----------------
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            usr_id = session.get('user_logged')
            user_id_logged = session.get('user_id_logged')
            todo_nam = request.form['task_nam']
            todo_description = request.form['task_description']
            todo_comments = request.form['task_comments']
            todo_status = request.form['task_status']
            target_dte = request.form['task_target_date']
            today = datetime.now()
            ins_dte = today.strftime('%Y-%m-%d')
            print(warehouse, usr_id, user_id_logged, todo_nam, todo_description, todo_comments, todo_status, target_dte, ins_dte)
            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()

            webcall = open('../src/db/webcalls/tools/new_task_insert_query.sql', mode='r')
            new_task_insert_query = webcall.read()
            webcall.close()
            insert_new_task = new_task_insert_query.format(warehouse, user_id_logged, todo_nam, todo_description, todo_comments, todo_status, target_dte, ins_dte)
            print("task {} Created".format(todo_nam))
            cursor.execute(insert_new_task)
            connection.commit()
            connection.close()

            # ----------------
            #    Login Data
            # ----------------
            user_logged = session.get('user_logged')
            user_privileges = session.get('user_privileges')
            user_id_logged = session.get('user_id_logged')
            warehouse_logged = session.get('warehouse_logged')
            warehouse = session.get('warehouse_logged').split()[0]

            connection, cursor = dbconnection()

            # ---- Database Active tools query ----
            webcall = open('db/webcalls/tools/done_tasks_query.sql', mode='r')
            tasks_query = webcall.read()
            webcall.close()
            tasks_query = tasks_query.format(warehouse, user_id_logged, warehouse, user_id_logged)
            cursor.execute(tasks_query)
            all_tasks_results = cursor.fetchall()
            connection.close()

        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('tools.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, all_tasks_results=all_tasks_results)

@app.route('/edit_task/<string:id>')
def edit_task(id):
    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    user_id_logged = session.get('user_id_logged')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ----------------
    #    DataBase
    # ----------------
    connection, cursor = dbconnection()
    
    webcall = open('../src/db/webcalls/tools/data_2_edit_tasks_query.sql', mode='r')
    edit_task_query = webcall.read()
    webcall.close()
    edit_task_query = edit_task_query.format(id, warehouse)
    cursor.execute(edit_task_query)
    data2edit = cursor.fetchall()
    stats = data2edit[0][4]


    #all statuses
    webcall = open('db/webcalls/tools/data_2_edit_task_statuses_query.sql', mode='r')
    edit_task_statuses_query = webcall.read()
    webcall.close()
    edit_task_statuses_query = edit_task_statuses_query.format(data2edit[0][4], data2edit[0][4])
    cursor.execute(edit_task_statuses_query)
    data2select = cursor.fetchall()

    # all tasks
    webcall = open('db/webcalls/tools/done_tasks_query.sql', mode='r')
    tasks_query = webcall.read()
    webcall.close()
    tasks_query = tasks_query.format(warehouse, user_id_logged, warehouse, user_id_logged)
    cursor.execute(tasks_query)
    all_tasks_results = cursor.fetchall()
    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/todo_edit_task.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, data2edit=data2edit, data2select=data2select, all_tasks_results=all_tasks_results)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    if request.method == 'POST':
        warehouse = request.form['wh_id']
        warehouse = warehouse.split()[0]
        usr_id = session.get('user_logged')
        user_id_logged = session.get('user_id_logged')
        todo_nam = request.form['task_nam']
        todo_description = request.form['task_description']
        todo_comments = request.form['task_comments']
        todo_status = request.form['task_status']
        target_dte = request.form['task_target_date']
        today = datetime.now()
        if todo_status == 'D':
            cls_dte = today.strftime('%Y-%m-%d')
        else:
            cls_dte = ''
        print(warehouse, usr_id, user_id_logged, todo_nam, todo_description, todo_comments, todo_status, target_dte, cls_dte, task_id)

        # ----------------
        #    DataBase
        # ----------------
        connection, cursor = dbconnection()
        # print('DB connected successfully - update')

        webcall = open('../src/db/webcalls/tools/update_selected_task_query.sql', mode='r')
        update_task_query = webcall.read()
        webcall.close()
        update_task_query = update_task_query.format(warehouse, user_id_logged, todo_nam, todo_description, todo_comments, todo_status, target_dte, cls_dte, task_id, warehouse)
        print(update_task_query)
        cursor.execute(update_task_query)
        connection.commit()
        connection.close()

        # all tasks
        connection, cursor = dbconnection()
        webcall = open('db/webcalls/tools/not_finished_tasks_query.sql', mode='r')
        tasks_query = webcall.read()
        webcall.close()
        tasks_query = tasks_query.format(warehouse, user_id_logged, warehouse, user_id_logged)
        cursor.execute(tasks_query)
        all_tasks_results = cursor.fetchall()
        connection.close()

        print("Task {} Modified".format(task_id))
        return redirect(url_for('tools'))

@app.route('/notes')
def notes():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_id_logged = session.get('user_id_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
            # connection = sqlite3.connect('../src/db/database/DB_ITools.db')
            # cursor = connection.cursor()

        # Call the db connection function
        connection, cursor = dbconnection()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/Enabled_tools_query.sql', mode='r')
        tools_query = webcall.read()
        webcall.close()
        tools_query = tools_query.format(warehouse)
        cursor.execute(tools_query)
        enabled_tools_results = cursor.fetchall()

        # ---- Database Active tools query ----
        webcall = open('../src/db/webcalls/tools/Active_notes_query.sql', mode='r')
        notes_query = webcall.read()
        webcall.close()
        notes_query = notes_query.format(warehouse, user_id_logged)
        cursor.execute(notes_query)
        Active_notes_query = cursor.fetchall()
        connection.close()

        boton_change = ('Task To Do', 'tools')
        note_change = ('New Note', 'new_note')

        return render_template('notes.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, warehouse_logged=warehouse_logged, user_privileges=user_privileges, enabled_tools_results=enabled_tools_results, Active_notes_query=Active_notes_query, boton_change=boton_change, note_change=note_change)


@app.route('/new_note')
def new_note():
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    user_id_logged = session.get('user_id_logged')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    return render_template('configuration/add_new_note.html', user_logged=f'{user_logged}', user_id_logged=user_id_logged, user_privileges=user_privileges, warehouse_logged=warehouse_logged, warehouse=warehouse)

@app.route('/save_new_note', methods=["POST", "GET"])
def save_new_note():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # ----------------
            #    HTML Form
            # ----------------
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            usr_id = session.get('user_logged')
            user_id_logged = session.get('user_id_logged')
            note_title = request.form['note_title']
            note_description = request.form['note_description']
            print(warehouse, usr_id, user_id_logged, note_title, note_description)
            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()

            webcall = open('../src/db/webcalls/tools/new_note_insert_query.sql', mode='r')
            new_note_insert_query = webcall.read()
            webcall.close()
            insert_new_note = new_note_insert_query.format(warehouse, user_id_logged, note_title, note_description)
            print("task {} Created".format(note_title))
            cursor.execute(insert_new_note)
            connection.commit()
            connection.close()

            # ----------------
            #    Login Data
            # ----------------
            user_logged = session.get('user_logged')
            user_privileges = session.get('user_privileges')
            user_id_logged = session.get('user_id_logged')
            warehouse_logged = session.get('warehouse_logged')
            warehouse = session.get('warehouse_logged').split()[0]

            connection, cursor = dbconnection()

            # ---- Database Active tools query ----
            webcall = open('db/webcalls/tools/Active_notes_query.sql', mode='r')
            notes_query = webcall.read()
            webcall.close()
            notes_query = notes_query.format(warehouse, user_id_logged)
            cursor.execute(notes_query)
            Active_notes_query = cursor.fetchall()
            connection.close()

            boton_change = ('Task To Do', 'tools')
            note_change = ('New Note', 'new_note')

        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('notes.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, Active_notes_query=Active_notes_query, note_change=note_change, boton_change=boton_change )


@app.route('/edit_note/<string:id>')
def edit_note(id):
    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    user_id_logged = session.get('user_id_logged')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ----------------
    #    DataBase
    # ----------------
    connection, cursor = dbconnection()

    webcall = open('../src/db/webcalls/tools/data_2_edit_note_query.sql', mode='r')
    edit_note_query = webcall.read()
    webcall.close()
    edit_note_query = edit_note_query.format(id, user_id_logged, warehouse)
    cursor.execute(edit_note_query)
    data2edit = cursor.fetchall()

    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged,
                               user_privileges=user_privileges)
    else:
        return render_template('configuration/tools_edit_note.html', user_logged=f'{user_logged}',
                               warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse,
                               user_id_logged=user_id_logged, data2edit=data2edit)


@app.route('/update_note/<note_id>', methods=["POST", "GET"])
def update_note(note_id):
    print(request.form)
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            usr_id = session.get('user_logged')
            user_id_logged = session.get('user_id_logged')
            note_title = request.form['note_title']
            note_description = request.form['note_description']
            print(warehouse, usr_id, user_id_logged, note_title, note_description, note_id)
            print(request.form)

            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()
            # print('DB connected successfully - update')

            webcall = open('../src/db/webcalls/tools/update_selected_note_query.sql', mode='r')
            update_note_query = webcall.read()
            webcall.close()
            update_note_query = update_note_query.format(note_title, note_description, note_id, warehouse, user_id_logged)
            print(update_note_query)
            cursor.execute(update_note_query)
            connection.commit()
            connection.close()

            print("Note {} Modified".format(note_id))
            return redirect(url_for('notes'))




@app.route('/delete_note/<note_id>')
def delete_note(note_id):
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        user_id_logged = session.get('user_id_logged')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]
        print(warehouse, user_id_logged, note_id)
        print(request.form)

        # ----------------
        #    DataBase
        # ----------------
        connection, cursor = dbconnection()
        # print('DB connected successfully - delete')

        webcall = open('../src/db/webcalls/tools/delete_selected_note_query.sql', mode='r')
        delete_note_query = webcall.read()
        webcall.close()
        delete_note_query = delete_note_query.format(note_id, warehouse, user_id_logged)
        print(delete_note_query)
        cursor.execute(delete_note_query)
        connection.commit()
        connection.close()

        print("Note {} Deleted".format(id))
        return redirect(url_for('notes'))


@app.route('/configuration')
def configuration():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access this way.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)

@app.route('/logout')
def logout():
    # Remove all session variables
    session.pop('user_logged', None)
    session.pop('user_privileges', None)
    session.pop('warehouse_logged', None)
    return redirect(url_for('index'))


# ---- Configuration Menu ---
@app.route('/configuration_home')
def configuration_home():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
        connection, cursor = dbconnection()

        # ---- Database Users by Role query ----

        webcall = open('../src/db/webcalls/summary/users_by_role_summary.sql', mode='r')
        wh_users_role_query = webcall.read()
        webcall.close()
        wh_users_role_query = wh_users_role_query.format(warehouse, warehouse)
        cursor.execute(wh_users_role_query)
        wh_role_users_results = cursor.fetchall()

        # ---- Database Users by Hierarchy query ----
        webcall = open('../src/db/webcalls/summary/users_by_hierarchy_summary.sql', mode='r')
        wh_users_hierarchy_query = webcall.read()
        webcall.close()
        wh_users_hierarchy_query = wh_users_hierarchy_query.format(warehouse, warehouse)
        cursor.execute(wh_users_hierarchy_query)
        wh_hierarchy_users_results = cursor.fetchall()

        # ---- Database Summary query ----
        webcall = open('../src/db/webcalls/summary/summary.sql', mode='r')
        wh_summary_query = webcall.read()
        webcall.close()
        wh_summary_query = wh_summary_query.format(warehouse, warehouse, warehouse)
        cursor.execute(wh_summary_query)
        wh_summary_query_results = cursor.fetchall()

        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration/configuration_home.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, wh_role_users_results=wh_role_users_results, wh_hierarchy_users_results=wh_hierarchy_users_results, wh_summary_query_results=wh_summary_query_results)


@app.route('/warehouse_configuration')
def warehouse_configuration():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        if session.get('user_privileges') == 'R' or session.get('user_privileges') == 'E':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration/warehouse_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)


@app.route('/forms_config')
def forms_config():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access with no user identified.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
        connection, cursor = dbconnection()

        # ---- Database Active forms query ----
        webcall = open('../src/db/webcalls/forms/All_forms_query.sql', mode='r')
        forms_query = webcall.read()
        webcall.close()
        forms_query = forms_query.format(warehouse)
        cursor.execute(forms_query)
        all_forms_results = cursor.fetchall()
        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged,user_privileges=user_privileges)
        else:
            return render_template('configuration/forms_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, all_forms_results=all_forms_results)


@app.route('/forms_configuration', methods=["POST", "GET"])
def forms_configuration():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # ----------------
            #    HTML Form
            # ----------------
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            form_name = request.form['form_nam']
            form_contact = request.form['form_contact']
            telephone = request.form['form_tlf']
            form_id = request.form['form_id']
            description = request.form['form_inc']
            form_url = request.form['form_url']
            form_url = str(form_url)
            form_toolkit = request.form['form_toolkit']
            print(warehouse, form_name, form_contact, telephone, form_id, description, form_url, form_toolkit)
            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()
            
            webcall = open('../src/db/webcalls/forms/new_form_query.sql', mode='r')
            new_form_query = webcall.read()
            webcall.close()
            new_form = new_form_query.format(warehouse, form_name, form_contact, telephone, form_id, description, form_url, form_toolkit)
            print("Form {} Created".format(new_form[5]))
            cursor.execute(new_form)
            connection.commit()
            connection.close()

        # ----------------
        #    Login Data
        # ----------------
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]
        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration/forms_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse)


@app.route('/edit_forms/<string:id>')
def edit_forms(id):
    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ----------------
    #    DataBase
    # ----------------
    connection, cursor = dbconnection()
    
    webcall = open('../src/db/webcalls/forms/data_2_edit_forms_query.sql', mode='r')
    edit_form_query = webcall.read()
    webcall.close()
    edit_form_query = edit_form_query.format(id, warehouse)
    cursor.execute(edit_form_query)
    data2edit = cursor.fetchall()
    # all forms
    webcall = open('../src/db/webcalls/forms/All_forms_query.sql', mode='r')
    forms_query = webcall.read()
    webcall.close()
    forms_query = forms_query.format(warehouse)
    cursor.execute(forms_query)
    all_forms_results = cursor.fetchall()
    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/forms_edit_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, data2edit=data2edit, all_forms_results=all_forms_results)


@app.route('/update_form/<form_id>', methods=['POST'])
def update_form(form_id):
    if request.method == 'POST':
        warehouse = request.form['wh_id']
        warehouse = warehouse.split()[0]
        form_name = request.form['form_nam']
        form_contact = request.form['form_contact']
        telephone = request.form['form_tlf']
        form_id = request.form['form_id']
        description = request.form['form_inc']
        form_url = str(request.form['form_url'])
        form_toolkit = request.form['form_toolkit']
        if request.form['status'] == 'Enabled':
            form_status = 1
        else:
            form_status = 0
            # print(warehouse, form_name, form_contact, telephone, form_id, description, form_url, form_toolkit, form_status)

        connection, cursor = dbconnection()
        
        # print('DB connected successfully - update')
        webcall = open('../src/db/webcalls/forms/update_selected_form_query.sql', mode='r')
        update_form_query = webcall.read()
        webcall.close()
        update_form_query = update_form_query.format(form_name, form_contact, telephone, form_id, description, form_url, form_toolkit, form_status, warehouse, form_id, warehouse)
        cursor.execute(update_form_query)
        connection.commit()
        connection.close()
        print("Form {} Modified".format(form_id))
        return redirect(url_for('forms_config'))
        # render_template('configuration/forms_configuration.html')


@app.route('/tools_config')
def tools_config():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access with no user identified.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
        connection, cursor = dbconnection()

        # ---- Database Active forms query ----
        webcall = open('../src/db/webcalls/tools/All_tools_query.sql', mode='r')
        tools_query = webcall.read()
        webcall.close()
        tools_query = tools_query.format(warehouse)
        cursor.execute(tools_query)
        all_tools_results = cursor.fetchall()
        if session.get('user_privileges') == 'R':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration/tools_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, all_tools_results=all_tools_results)


@app.route('/tools_configuration', methods=["POST", "GET"])
def tools_configuration():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # ----------------
            #    HTML Form
            # ----------------
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            tool_name = request.form['tool_button_name']
            tool_url = request.form['tool_button_url']
            print(warehouse, tool_name, tool_url)
            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()
            
            webcall = open('../src/db/webcalls/tools/new_tool_button_query.sql', mode='r')
            new_tool_button_query = webcall.read()
            webcall.close()
            new_button = new_tool_button_query.format(warehouse, tool_name, tool_url, warehouse)
            print("Button {} Created".format(new_button[2]))
            cursor.execute(new_button)
            connection.commit()
            connection.close()

        # ----------------
        #    Login Data
        # ----------------

    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    warehouse_logged = session.get('warehouse_logged')
    # ---- Database Connection ----
    connection = sqlite3.connect('../src/db/database/DB_ITools.db')
    cursor = connection.cursor()

    # ---- Database Active forms query ----
    webcall = open('../src/db/webcalls/tools/All_tools_query.sql', mode='r')
    tools_query = webcall.read()
    webcall.close()
    tools_query = tools_query.format(warehouse)
    cursor.execute(tools_query)
    all_tools_results = cursor.fetchall()
    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/tools_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges,  all_tools_results=all_tools_results)


@app.route('/edit_tools/<string:id>')
def edit_tools(id):
    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ----------------
    #    DataBase
    # ----------------
    connection, cursor = dbconnection()
    
    webcall = open('../src/db/webcalls/tools/data_2_edit_tools_query.sql', mode='r')
    edit_tools_query = webcall.read()
    webcall.close()
    edit_tools_query = edit_tools_query.format(id, warehouse)
    cursor.execute(edit_tools_query)
    data2edit = cursor.fetchall()
    # all forms
    webcall = open('../src/db/webcalls/tools/All_tools_query.sql', mode='r')
    tools_query = webcall.read()
    webcall.close()
    tools_query = tools_query.format(warehouse)
    cursor.execute(tools_query)
    all_tools_results = cursor.fetchall()
    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/tools_edit_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, data2edit=data2edit, all_tools_results=all_tools_results)


@app.route('/update_tool/<tool_num>', methods=['POST'])
def update_tool(tool_num):
    if request.method == 'POST':
        warehouse = request.form['wh_id']
        warehouse = warehouse.split()[0]
        tool_num = request.form['tool_num']
        tool_name = request.form['tool_name']
        tool_url = request.form['tool_url']
        if request.form['status'] == 'Enabled':
            tool_active = 1
        else:
            tool_active = 0

        # ----------------
        #    DataBase
        # ----------------
        connection, cursor = dbconnection()
        
        # print('DB connected successfully - update')
        webcall = open('../src/db/webcalls/tools/update_selected_tool_query.sql', mode='r')
        update_tool_query = webcall.read()
        webcall.close()
        update_tool_query = update_tool_query.format(tool_num, tool_name, tool_url, tool_active, warehouse, tool_num, warehouse)
        cursor.execute(update_tool_query)
        connection.commit()
        connection.close()
        print("Button {} Modified".format(tool_name))
        return redirect(url_for('tools_config'))


@app.route('/users_config')
def users_config():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access with no user identified.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        user_logged = session.get('user_logged')
        user_privileges = session.get('user_privileges')
        warehouse_logged = session.get('warehouse_logged')
        warehouse = session.get('warehouse_logged').split()[0]

        # ---- Database Connection ----
        connection, cursor = dbconnection()

        # ---- Database Active forms query ----
        webcall = open('../src/db/webcalls/users/All_users_query.sql', mode='r')
        users_query = webcall.read()
        webcall.close()
        users_query = users_query.format(warehouse)
        cursor.execute(users_query)
        all_users_results = cursor.fetchall()

        # hierarchies
        webcall = open('../src/db/webcalls/users/get_all_hiearchies.sql', mode='r')
        get_hierarchies = webcall.read()
        webcall.close()
        cursor.execute(get_hierarchies)
        hierarchies_to_select = cursor.fetchall()
        print(hierarchies_to_select)

        # roles (privileges)
        webcall = open('../src/db/webcalls/users/get_all_roles.sql', mode='r')
        get_roles = webcall.read()
        webcall.close()
        cursor.execute(get_roles)
        role_to_select = cursor.fetchall()
        print(role_to_select)

        if session.get('user_privileges') == 'R' or session.get('user_privileges') == 'E':
            return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
        else:
            return render_template('configuration/users_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, all_users_results=all_users_results, hierarchies_to_select=hierarchies_to_select, role_to_select=role_to_select)


@app.route('/users_configuration', methods=["POST", "GET"])
def users_configuration():
    if session.get('user_logged') is None:
        login_error = 'Is not possible to access without an user.'
        flash(login_error)
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # ----------------
            #    HTML Form
            # ----------------
            warehouse = request.form['wh_id']
            warehouse = warehouse.split()[0]
            usr_id = request.form['usr_id']
            usr_nam = request.form['usr_nam']
            usr_surnam = request.form['usr_surnam']
            hie_nam = request.form['hie_nam']
            pri_nam = request.form['pri_nam']
            print(warehouse, usr_id, usr_nam, usr_surnam, hie_nam, pri_nam)
            # ----------------
            #    DataBase
            # ----------------
            connection, cursor = dbconnection()

            webcall = open('../src/db/webcalls/users/new_user_query.sql', mode='r')
            new_user_query = webcall.read()
            webcall.close()
            new_user = new_user_query.format(usr_id, usr_nam, usr_surnam, warehouse, hie_nam, pri_nam)
            print("User {} Created".format(new_user[0]))
            cursor.execute(new_user)
            connection.commit()
            connection.close()


    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    warehouse_logged = session.get('warehouse_logged')

    # ---- Database Connection ----
    connection = sqlite3.connect('../src/db/database/DB_ITools.db')
    cursor = connection.cursor()

    # ---- Database Active users query ----
    webcall = open('../src/db/webcalls/users/All_users_query.sql', mode='r')
    users_query = webcall.read()
    webcall.close()
    users_query = users_query.format(warehouse)
    cursor.execute(users_query)
    all_users_results = cursor.fetchall()

    if session.get('user_privileges') == 'R' or session.get('user_privileges') == 'E':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/users_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges,  all_users_results=all_users_results)

@app.route('/edit_users/<string:id>')
def edit_users(id):
    # ----------------
    #    Login Data
    # ----------------
    user_logged = session.get('user_logged')
    user_privileges = session.get('user_privileges')
    warehouse_logged = session.get('warehouse_logged')
    warehouse = session.get('warehouse_logged').split()[0]

    # ----------------
    #    DataBase
    # ----------------
    connection, cursor = dbconnection()

    webcall = open('../src/db/webcalls/users/data_2_edit_user_query.sql', mode='r')
    edit_users_query = webcall.read()
    webcall.close()
    edit_users_query = edit_users_query.format(id, warehouse)
    cursor.execute(edit_users_query)
    data2edit = cursor.fetchall()

    #hierarchies
    webcall = open('../src/db/webcalls/users/get_hiearchies_per_user_update.sql', mode='r')
    get_hierarchies = webcall.read()
    webcall.close()
    get_hierarchies = get_hierarchies.format(id, warehouse, id, warehouse)
    cursor.execute(get_hierarchies)
    hierarchies_to_update = cursor.fetchall()

    # roles (privileges)
    webcall = open('../src/db/webcalls/users/get_role_per_user_update.sql', mode='r')
    get_role = webcall.read()
    webcall.close()
    get_role = get_role.format(id, warehouse, id, warehouse)
    cursor.execute(get_role)
    role_to_update = cursor.fetchall()

    # all forms
    webcall = open('../src/db/webcalls/users/All_users_query.sql', mode='r')
    users_query = webcall.read()
    webcall.close()
    users_query = users_query.format(warehouse)
    cursor.execute(users_query)
    all_users_results = cursor.fetchall()
    if session.get('user_privileges') == 'R':
        return render_template("home.html", user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges)
    else:
        return render_template('configuration/users_edit_configuration.html', user_logged=f'{user_logged}', warehouse_logged=warehouse_logged, user_privileges=user_privileges, warehouse=warehouse, data2edit=data2edit, hierarchies_to_update=hierarchies_to_update, role_to_update=role_to_update, all_users_results=all_users_results)

@app.route('/update_user/<usr_id>', methods=['POST'])
def update_user(usr_id):
    if request.method == 'POST':
        warehouse = request.form['wh_id']
        warehouse = warehouse.split()[0]
        user_id = request.form['usr_id']
        usr_name = request.form['usr_nam']
        usr_name = request.form['usr_nam']
        usr_surname = request.form['usr_surnam']
        hie_name = request.form['hie_id']
        pri_name = request.form['pri_id']
        if request.form['status'] == 'Enabled':
            usr_active = 1
        else:
            usr_active = 0

        check = request.form['status']
        print(check)

        # ----------------
        #    DataBase
        # ----------------
        connection, cursor = dbconnection()

        # print('DB connected successfully - update')
        webcall = open('../src/db/webcalls/users/update_selected_user_query.sql', mode='r')
        update_user_query = webcall.read()
        webcall.close()
        update_user_query = update_user_query.format(user_id, usr_name, usr_surname, warehouse, hie_name, pri_name, usr_active, user_id, warehouse)
        print(update_user_query)
        cursor.execute(update_user_query)
        connection.commit()
        connection.close()
        print("User {} Modified".format(user_id))
        return redirect(url_for('users_config'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

# config.py
DEVELOPMENT = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 4000,
}