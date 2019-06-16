from bottle import route, run, auth_basic, get, post, request
import math

USERNAME = "amazon"
PASSWORD = "candidate"

calc_symbol_list = ['+', '-', '*', '/', '(', ')','0','1','2','3','4','5','6','7','8','9']

stock = {}
sales = 0 

def checkauth(username, password):
    return username == USERNAME and password == PASSWORD

def addstock(name, amount):
    if name is None:
        return "ERROR\n"

    if amount is None:
        amount = 1 
    elif amount > 0 and amount.is_integer():
        amount = int(amount)
    else: #amount is float
        return "ERROR\n"

    if name in stock:
        stock[name] += amount
    else:
        stock.update({name : amount})
    
def checkstock(name):
    if name is None:
        ret = ''
        for key in sorted(stock.keys()) :
            if stock[key] is not 0:
                ret += "{}: {}\n".format(key, stock[key])
        return ret 
    else: # name was specified
        if name in stock:
            return "{}: {}\n".format(name, stock[name])
        else:
            return "ERROR\n"

def sell(name, amount, price):
    if (None in [name] 
        or name not in stock ):
        return "ERROR\n"

    if amount is None:
        amount = 1
    elif amount > 0 and amount.is_integer():
        amount = int(amount)
    else: #amount is float
        return "ERROR\n"

    global sales

    if stock[name] >= amount:
        stock[name] -= amount
        if price is not None and price >= 0:
            sales += price * amount
    else:
        return "ERROR\n"

def checksales():
    if sales.is_integer():
        return "sales: {}\n".format(int(sales))
    return "sales: {}\n".format(math.ceil(sales*100)/100)

def deleteall():
    global stock
    global sales
    stock = {}
    sales = 0

@route('/')
def say_AMAZON():
    return "AMAZON\n"

@route('/secret/')
@auth_basic(checkauth)
def say_SUCCESS():
    return "SUCCESS\n"
    
@route('/calc')
def calculation():
    formula = request.query.get('input', type = str)
    """ Replace whitespace with '+', since
    '+' is treated as whitespace in URL 
    """
    formula = formula.replace(' ', '+')
    for char in formula:
        if not char in calc_symbol_list:
            return "ERROR\n"
    answer = "{}\n".format(eval(formula))
    return answer

@route('/stocker')
def stocker():
    function = request.query.get('function', type = str)
    name = request.query.get('name', type = str)
    amount = request.query.get('amount', type = float)
    price = request.query.get('price', type = float)
    if function == "addstock":
        return addstock(name, amount)
    elif function == "checkstock":
        return checkstock(name)
    elif function == "sell":
        return sell(name, amount, price)
    elif function == "checksales":
        return checksales()
    elif function == "deleteall":
        return deleteall()
    else:
        return "ERROR\n"

run(host='172.31.10.40', port=8080)
