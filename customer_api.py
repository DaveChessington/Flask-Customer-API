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
            #user_exists = DB.searchCustomer(data['username'])
            #if user_exists:
            #    flask.flash(f"El usuario '{data['username']}' ya está registrado.", "danger")
            #    return flask.redirect("/new")
            #DB.newCustomer(Customer(**data))
            response=requests.post(url=f"{url}/customer",json=data)
            if response.status_code==200 or response.status_code==201 :
                message="customer succesfully added"
            elif response.status_code==409:
                message="username already exists"
            else:
                message=f"error: {response}"
        except Exception as ex:
            message=f"An error ocured:{ex}"
        return flask.render_template("new.html",response=message)

    return flask.render_template("new.html")

@app.route("/search",methods=['GET', 'POST'])
def search_ui():
    if flask.request.method=="POST":
        print(flask.request)
        data=flask.request.form
        try:
            user_exists = requests.request(method="GET",url=f"{url}/customers")#DB.searchCustomer(data['username'])
            #message=f"fetched user's data:{user_exists.__str__() if user_exists else "user not found"}"
            message=f"fetched user's data:{user_exists.content}"
        except Exception as ex:
            message=f"An error ocured:{ex}"
        return flask.render_template("customer.html",response=message)
    return flask.render_template("customer.html")

@app.route("/list")
def list_ui():
    response=requests.get(url=f"{url}/customers").json()
    return flask.render_template("customers.html",context=response)

@app.route("/delete", methods=['GET', 'POST'])
def delete_ui():
    if flask.request.method=="POST":
        data=flask.request.form
        response=requests.delete(f"{url}/customer/{data['id']}")
        if response.status_code == 200:
            message="User successfully deleted"
        else:
            message = "Error while deleting user"
        return flask.render_template("delete.html",response=message)
    return flask.render_template("delete.html")

####Customer's API#####

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
        user_exists = DB.searchCustomer(request["username"])
        if user_exists:
            return flask.jsonify({"message":"error:user already exists"}),409
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