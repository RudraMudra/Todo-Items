# import pymysql
from mysql.connector import cursor

from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import json


# create To_Do_List
@app.route('/create', methods=['POST'])
def create_toDoList():
    try:
        _json = request.json
        print("JSON: " + json.dumps(_json))
        _list_name = _json['list_name']
        _is_checked = _json['is_checked']
        _status = _json['status_field']
        _priority = _json['item_priority']
        _activity_type_array = _json['item_activityType']
        _activity_type = (','.join(str(x) for x in _activity_type_array))

        # inserting records in database
        # sqlQuery = "INSERT INTO to_do_list(Todo_list_Name, Is_Checked, status_field, Priority, Activity_Type) VALUES(" \
        #            "%s, %s, %s, %s, %s) "
        sqlQuery = "CALL Insert_todoList(%s, %s, %s, %s, %s)"
        print("SQL Query :" + sqlQuery)
        data = (_list_name, _is_checked, _status, _priority, _activity_type)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery, data)
        conn.commit()
        response = jsonify('list created successfully')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# getting all list
@app.route('/getAllList', methods=['GET'])
def get_toDoList():
    try:
        # getting all lists
        sqlQuery = "SELECT * FROM to_do_list"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# deleting a particular item in database
@app.route('/deleteItem/<string:todoListName>', methods=['DELETE'])
def delete_toDoList(todoListName):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("CALL Delete_todoList(%s)", (todoListName))
        conn.commit()
        response = jsonify('List Name deleted Successfully.')
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# deleting all records in database
@app.route('/deleteAll', methods=['DELETE'])
def deleteAll_toDoList():
    try:
        sqlQuery = "DELETE FROM to_do_list"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        conn.commit()
        response = jsonify('All Data deleted Successfully.')
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# updating records in database
@app.route('/updateEntry/<string:todoListId>', methods=['PUT'])
def update_toDoListName(todoListId):
    try:
        _json = request.json
        print("JSON: " + json.dumps(_json))
        _list_name = _json['list_name']
        print("List Name: " + _list_name)
        _status_field = _json['status_field']
        print("Status: " + _status_field)
        _priority = _json['item_priority']
        print("Priority: " + _priority)
        _activity_type_array = _json['item_activityType']
        _activity_type = (','.join(str(x) for x in _activity_type_array))

        # sqlQuery = "UPDATE to_do_list SET Todo_List_Name=%s, status_field=%s, Priority=%s, Activity_Type=%s where " \
        #            "Todo_List_Id=%s "
        sqlQuery = "CALL Update_Todo_List(%s, %s, %s, %s, %s)"
        data = (_list_name, _status_field, _priority, _activity_type, todoListId)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery, data)
        conn.commit()
        response = jsonify('list updated successfully.')
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
