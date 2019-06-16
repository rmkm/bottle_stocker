from bottle import route, run, auth_basic, get, post, request

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
    if (None in [name, price] 
        or name not in stock 
        or price<=0 ):
        return "ERROR\n"

    if amount is None:
        amount = 1
    elif amount > 0 and amount.is_integer():
        amount = int(amount)
    else: #amount is float
        return "ERROR\n"

    global sales

    if amount is None and stock[name] > 0:
        stock[name] -= 1
        sales += price
    elif stock[name] >= amount:
        stock[name] -= amount
        sales += price * amount
    else:
        return "ERROR\n"

def checksales():
    return "sales: {}\n".format(sales)

def deleteall():
    global stock
    global sales
    stock = {}
    sales = 0

@route('/')
def say_AMAZON():
    return "AMAZON\n"

@route('/secret')
@auth_basic(checkauth)
def say_SUCCESS():
    return "SUCCESS\n"
    
@route('/calc')
def calculation():
    formula = request.query.get('input', type = str)
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
