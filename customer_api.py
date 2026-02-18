import dotenv
import flask
from Customer import Customer
import json
import local_DB as DB
import requests
import os

app=flask.Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_default_dev_key')

dotenv.load_dotenv()
if dotenv.dotenv_values("DATA_BASE")=="LOCAL":
    import local_DB as DB
else:
    print("Cloud Database")

url="http://127.0.0.1:5000"

@app.route('/')
def main():
    return flask.render_template("index.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
    if flask.request.method=="POST":
        data = flask.request.form.to_dict()
        r=requests.post(f"{url}/validate",json=data).json()
        if r["match"]:
            return flask.render_template("home.html",context=data)
        else:
            flask.flash("Invalid username or password","danger")
            return flask.redirect("/login")

    return flask.render_template("login.html")

@app.route("/home")
def home():
    data=flask.request.data
    return flask.render_template("home.html",context=data)

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


@app.route("/update/search", methods=['GET', 'POST'])  
def updateSearch():
    customer_list=requests.get(url=f"{url}/customers").json() 
    if flask.request.method=="POST":
        data=flask.request.form.to_dict()
        r=requests.get(url=f"{url}/customerId/{data['id']}",json=data)
        if r.status_code==200 or r.status_code==201:
            message="customer found"
        else:
            message=f"error: {r.json()}"
        return flask.render_template("update_result.html",context={"message":message,"data":r.json()})
    return flask.render_template("update_search.html",context=customer_list)


@app.route("/update/result", methods=['GET', 'POST'])
def result_update():
    data=flask.request.form.to_dict()
    if flask.request.method=="POST":
        r=requests.put(url=f"{url}/update/customer/{data['id']}",json=flask.request.form)#update customer info
        if r.status_code==200 or r.status_code==201:
            message="customer successfully updated"
        else:            
            message=f"error: {r.json()}"
        return flask.render_template("update_result.html",context={"message":message,"data":r.json()})
    
    r=requests.get(url=f"{url}/customer/{data['id']}").json()#get customer info
    #r=DB.searchCustomerById(data['id'])
    return flask.render_template("update_result.html",
                                first_name=r["first_name"],
                                last_name=r["last_name"], 
                                email=r["email"],
                                phone=r["phone"],
                                address=r["address"],
                                username=r["username"],)
    

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

@app.route("/customerId/<int:id>")
def searchById(id):
    try:
        customer = DB.searchCustomerById(id)
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

@app.route('/update/customer/<int:id>', methods=['PUT'])
def update(id):
    data=flask.request.get_json()
    try:
        customer=Customer(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
            username=data["username"],
            plain_password=data["plain_password"],
        )
        customer.encrypt_password()
        DB.updateCustomer(id,customer)
        return flask.jsonify({"message":"customer successfully updated"}),201
    except Exception as ex:
            return flask.jsonify({"message":f"error:{ex}"}),500

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        DB.deleteCustomer(id)
        return flask.jsonify({"message":"customer successfully deleted from database"}),200
    except Exception as ex:
        return flask.jsonify({"message":f"error:{ex}"}),500

@app.route('/validate',methods=["POST"])
def validate():
    data=flask.request.get_json()
    if not data:
        return flask.jsonify({"error": "No data provided"}), 400
    username = data.get("username")
    password = data.get("plain_password")
    if not username or not password:
        return flask.jsonify({"error": "Missing username or password"}), 400
    customer=DB.searchCustomer(username)
    if not customer:
        return flask.jsonify({"match": False}), 404
    if customer.check_password(password):
        return flask.jsonify({"match":True}),200
    return flask.jsonify({"match":False}),401

if __name__=="__main__":
    app.run(debug=True)