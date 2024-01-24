import __init__ as products
import Products_adding as product
import shelve

db = shelve.open('data1_db', 'r')
data_dict = {}
P = product.Product()
data_dict = P
data_dict = db['data']
print(data_dict)
