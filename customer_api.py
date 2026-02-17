import dotenv
import flask
from Customer import Customer
import json
import local_DB as DB
import requests

app=flask.Flask(__name__)


dotenv.load_dotenv()
if dotenv.dotenv_values("DATA_BASE")=="LOCAL":
    import local_DB as DB
else:
    print("Cloud Database")

url="http://127.0.0.1:5000"



@app.route('/')
def main():
    return flask.render_template("index.html")

@app.route("/login")
def login():
    return flask.render_template("login.html")

@app.route("/home")
def home():
    return flask.render_template("home.html")

@app.route("/new",methods=['GET', 'POST'])
def new_ui():
    if flask.request.method=="POST":
        print(flask.request)
        data=flask.request.form
        try:
            user_exists = DB.searchCustomer(data['username'])
            if user_exists:
                flask.flash(f"El usuario '{data['username']}' ya está registrado.", "danger")
                return flask.redirect("/new")
            DB.newCustomer(Customer(**data))
            message="customer succesfully added"
        except Exception as ex:
            message=f"An error ocured:{ex}"
        return flask.render_template("new.html",response=message)

    return flask.render_template("new.html")

@app.route("/search")
def search_ui():
    return flask.render_template("customer.html")

@app.route("/list")
def list_ui():
    response=requests.request(method="GET",url=f"{url}/customers").json()
    return flask.render_template("customers.html",context=response)

@app.route("/delete")
def delte_ui():
    return flask.render_template("delete.html")


@app.route('/customers')
def list():
    try:
        return flask.jsonify([customer.to_dict() for customer in DB.listCustomers()]),200
    except Exception as ex:
        return flask.jsonify({"message":f"error:{ex}"}),500

@app.route("/customer/<string:username>")
def search(username):
    try:
        customer = DB.searchCustomer(username)
        if customer:
            return flask.jsonify(customer.to_dict()), 200
        return flask.jsonify({"message": "User not found"}), 404
    except Exception as ex:
        return flask.jsonify({"message":f"error:{ex}"}),500

@app.route('/customer', methods=['POST'])
def add():
    request=flask.request.get_json()
    try:
        DB.newCustomer(Customer(**request))
        return flask.jsonify({"message":"customer successfully added to database"}),201
    except Exception as ex:
        return flask.jsonify({"message":f"error:{ex}"}),500

"""
@app.route('/update/customer/id', methods=['PUT'])
def update():
    request=flask.request.get_json()
    try:
        DB.newCustomer(Customer(**request))
        return flask.jsonify({"message":"customer successfully added to database"}),201
    except Exception as ex:
            return flask.jsonify({"message":f"error:{ex}"}),500
"""

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        DB.deleteCustomer(id)
        return flask.jsonify({"message":"customer successfully deleted from database"}),200
    except Exception as ex:
        return flask.jsonify({"message":f"error:{ex}"}),500


if __name__=="__main__":
    app.run(debug=True)