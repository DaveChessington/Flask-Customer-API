import dotenv
import flask
from Customer import Customer
import json
import local_DB as DB
import requests

app=flask.Flask(__name__)

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