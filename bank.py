from flask import Flask, jsonify, request, abort
from passlib.hash import pbkdf2_sha256 as hasher

app = Flask(__name__)

with app.app_context():
    customer_list = []
    customer_list.append({'holder': 'ALPEREN KANTARCI', 'expiration': "1219", 'number': hasher.hash("5105105105105105"),'cvc':"510",'balance':20})
    customer_list.append({'holder': 'AHMET YASIN KUL', 'expiration': "0820", 'number': hasher.hash("1231231231231231"),'cvc':"123",'balance':500})
    customer_list.append({'holder': 'SADIK EKIN OZBAY', 'expiration': "0520", 'number': hasher.hash("0520520520520520"),'cvc':"052",'balance':1500})
    customer_list.append({'holder': 'ECEM GULDOSUREN', 'expiration': "1123", 'number': hasher.hash("1234567890123456"),'cvc':"112",'balance':4000})



@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400


@app.route('/creditcard/balance', methods=['GET'])
def balance():
    if not request.json:
        abort(400)
   
    for customer in customer_list:
        if customer['holder'] == request.json['holder'] and customer['expiration'] == request.json['expiration'] and customer['cvc'] == request.json['cvc']:
            if hasher.verify(customer['number'],request['number']):
                return jsonify({'result': 'Success','balance':customer['balance']}), 200 

    return jsonify({'result': 'Invalid credentials'}), 400 # Password does not match

    

@app.route('/creditcard/pay', methods=['POST'])
def pay():
    with app.app_context():
        if not request.json:
            abort(400)

        for customer in customer_list:
            if customer['holder'] == request.json['holder'] and customer['expiration'] == request.json['expiration'] and customer['cvc'] == request.json['cvc']:
                if hasher.verify(request.json['number'],customer['number']):                    
                    if customer['balance'] >= int(request.json['cost']):
                        customer['balance'] -= int(request.json['cost'])
                        return jsonify({'result': 'Success'}), 200 
                    else:
                        return jsonify({'result': 'Lack of balance'}), 200 


        return jsonify({'result': 'Invalid credentials'}), 400 

if __name__ == '__main__':
    app.run(debug=True, port=7000) 