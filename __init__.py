from flask import Flask, render_template, Blueprint, url_for, request, redirect, g, session, jsonify
from Forms import CreateProductsForm
import shelve, Products
from collections import defaultdict
import datetime
from datetime import timedelta
import stripe
import os, json
import copy
from collections import deque

# stripe keys
stripe.api_key = 'sk_test_51NWbl0AnVKG20ORq9QphGdcLFqPO2HRhjy41sGhDfYgvHbYo1XCDexufEI66WfTfTpIuoP9MJ5VzJrqimEOgQVQC00BthrQoiF'
# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_9ebffe26292e074fcdc124cc40c4762726aed215af0f9a81f218f4d5721aa049'
# stripe keys end

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='Products/templates'

)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=200)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True


# Homepage route
@app.route('/')
def home():
    return 'Hello Wwworwww'
# Homepage route end

# Products_listing route. This page lists all the products on the website. It is the main page
@app.route('/Products', methods=['GET', 'POST'])
def products():
    db = shelve.open('products.db', 'c')
    products_dict = {}
    try:
        if 'Products' in db:
            products_dict = db['Products']
        else:
            db['Products'] = products_dict
    except:
        print('Error in retrieving products from products.db.')
    
    if "cart_products" not in session:
            session["cart_products"] = {}

    if "cart_products" in session:
        cart_session = session["cart_products"]
        
    # product filters on this page
    if request.method == 'POST':
        country_value = request.form.getlist('country')
        dietary_value = request.form.getlist('dietary')
        type_value = request.form.getlist('type')
        filtered_products = {}


        if country_value == [] and dietary_value == [] and type_value == []:
            filtered_products = products_dict

        # Country Only
        elif country_value != [] and dietary_value == [] and type_value == []:

            country_values_to_check = ['Singapore','Japan', 'China', 'India']
            for country_value_to_check in country_values_to_check:
                if country_value_to_check in country_value:
                    country_products = {key: value for key, value in products_dict.items() if value.get_country() == country_value_to_check}
                    filtered_products.update(country_products)

        # Dietary Only
        elif country_value == [] and dietary_value != [] and type_value == []:
            
            dietary_values_to_check = ['Halal', 'Organic', 'Halal_&_organic']
            for dietary_value_to_check in dietary_values_to_check:
                if dietary_value_to_check in dietary_value:
                    dietary_products = {key: value for key, value in products_dict.items() if value.get_dietary() == dietary_value_to_check}
                    filtered_products.update(dietary_products)

        # type Only
        elif country_value == [] and dietary_value == [] and type_value != []:
            type_values_to_check = ['Snacks', 
                                    'Drinks',
                                    'Frozen', 
                                    'Fruits_&_vegetables', 
                                    'Household', 
                                    'Health_&_wellness', 
                                    'Meat_&_seafood', 
                                    'Dairy_&_chilled_&_eggs', 
                                    'Beer_&_wine_&_spirits', 
                                    'Beauty_&_personal_care', 
                                    'Baby_&_child_&_toys', 
                                    'Rice_&_noodles_&_cooking_ingredients']
            for type_value_to_check in type_values_to_check:
                if type_value_to_check in type_value:
                    type_products = {key: value for key, value in products_dict.items() if value.get_type() == type_value_to_check}
                    filtered_products.update(type_products)

        # Country and Dietary
        # elif country_value == [] and dietary_value == [] and type_value != []:

        elif country_value != [] and dietary_value != [] and type_value == []:
            dietary_values_to_check = ['Halal', 'Organic', 'Halal_&_organic']
            country_values_to_check = ['Singapore', 'Japan', 'China', 'India']

            for country_value_to_check in country_values_to_check:
                for dietary_value_to_check in dietary_values_to_check:
                    if country_value_to_check in country_value and dietary_value_to_check in dietary_value:
                        country_dietary_products = {key: value for key, value in products_dict.items() if value.get_country() == country_value_to_check and value.get_dietary() == dietary_value_to_check}
                        filtered_products.update(country_dietary_products)
        
        # Country and type
        
        elif country_value != [] and dietary_value == [] and type_value != []:
            country_values_to_check = ['Singapore', 'Japan', 'China', 'India']
            type_values_to_check = ['Snacks', 
                                    'Drinks',
                                    'Frozen', 
                                    'Fruits_&_vegetables', 
                                    'Household', 
                                    'Health_&_wellness', 
                                    'Meat_&_seafood', 
                                    'Dairy_&_chilled_&_eggs', 
                                    'Beer_&_wine_&_spirits', 
                                    'Beauty_&_personal_care', 
                                    'Baby_&_child_&_toys', 
                                    'Rice_&_noodles_&_cooking_ingredients']

            for country_value_to_check in country_values_to_check:
                for type_value_to_check in type_values_to_check:
                    if country_value_to_check in country_value and type_value_to_check in type_value:
                        country_type_products = {key: value for key, value in products_dict.items() if value.get_country() == country_value_to_check and value.get_type() == type_value_to_check}
                        filtered_products.update(country_type_products)

        # type and Dietary
                        
        elif country_value == [] and dietary_value != [] and type_value != []:
            dietary_values_to_check = ['Halal', 'Organic', 'Halal_&_organic']
            type_values_to_check = ['Snacks', 
                                    'Drinks',
                                    'Frozen', 
                                    'Fruits_&_vegetables', 
                                    'Household', 
                                    'Health_&_wellness', 
                                    'Meat_&_seafood', 
                                    'Dairy_&_chilled_&_eggs', 
                                    'Beer_&_wine_&_spirits', 
                                    'Beauty_&_personal_care', 
                                    'Baby_&_child_&_toys', 
                                    'Rice_&_noodles_&_cooking_ingredients']

            for dietary_value_to_check in dietary_values_to_check:
                for type_value_to_check in type_values_to_check:
                    if dietary_value_to_check in dietary_value and type_value_to_check in type_value:
                        dietary_type_products = {key: value for key, value in products_dict.items() if value.get_dietary() == dietary_value_to_check and value.get_type() == type_value_to_check}
                        filtered_products.update(dietary_type_products)
                        
        # Country and type and Dietary
                        
        elif country_value != [] and dietary_value != [] and type_value != []:
            country_values_to_check = ['Singapore', 'Japan', 'China', 'India']
            dietary_values_to_check = ['Halal', 'Organic', 'Halal_&_organic']
            type_values_to_check = ['Snacks', 
                                    'Drinks',
                                    'Frozen', 
                                    'Fruits_&_vegetables', 
                                    'Household', 
                                    'Health_&_wellness', 
                                    'Meat_&_seafood', 
                                    'Dairy_&_chilled_&_eggs', 
                                    'Beer_&_wine_&_spirits', 
                                    'Beauty_&_personal_care', 
                                    'Baby_&_child_&_toys', 
                                    'Rice_&_noodles_&_cooking_ingredients']

            for country_value_to_check in country_values_to_check:
                for dietary_value_to_check in dietary_values_to_check:
                    for type_value_to_check in type_values_to_check:
                        if country_value_to_check in country_value and dietary_value_to_check in dietary_value and type_value_to_check in type_value:
                            country_dietary_type_products = {key: value for key, value in products_dict.items() if value.get_country() == country_value_to_check and value.get_dietary() == dietary_value_to_check and value.get_type() == type_value_to_check}
                            filtered_products.update(country_dietary_type_products)
            

        return render_template('products_list.html', products_dict=filtered_products, country_value = country_value, dietary_value = dietary_value, type_value = type_value, cart_session=cart_session)
    # product filters on this page ends
    
    db.close()
    return render_template('products_list.html', products_dict=products_dict, cart_session = cart_session)

# Products_listing route. This page lists all the products on the website. It is the main page end


# Adding a product from products_listing to the cart
@app.route('/addProductCart', methods=['GET','POST'])
def add_product_cart():
    if request.method == 'POST':
        # Get the product id (id of the product) from submit button(Add to cart button) on the products_listing page
        product_id = request.form.get("id")

        # Get the product id from submit button(Add to cart button) on the products_listing page end

        cart_products_dict = {}
        
        # Open the db that stores all the products from products list page/createproducts from employees
        db = shelve.open('products.db', 'c')
        products_dict = {}
        try:
            products_dict = db['Products']
        except:
            print('Error in retrieving products from products.db.')
        
        # Open the db that stores all the products from products list page/createproducts from employees end

        # Check if the product id is stored in the session. if it is not, it adds the product id to the session as well as the data (type, quantity, etc)
        if product_id not in session["cart_products"]:


            intproduct_id = int(product_id)
            cart_products_dict[product_id] = products_dict[intproduct_id].__dict__

        # check if key "cart_products" in session. if not inside, initialize the session to a dict."
            if "cart_products" not in session:
                session["cart_products"] = {}
            session["cart_products"].update(cart_products_dict)
            session.permanent = True
            session.modified = True
            if "cart_products" in session:
                cart_session = session["cart_products"]
            db.close()
        
        if "cart_products" in session:
            cart_session = session["cart_products"]

         # cart_quantity stores the quantity that is selected by user in the cartproducts page. 
        # (Example, customer wants to buy 10 of product1. quantity of 10 with key of product 1 will be stored in cart quantity)
        cart_quantity_dict = {}
        # check if key "cart_quantity" in session. if not inside, initialize the session to a dict."
        if "cart_quantity" not in session:
            session["cart_quantity"] = {}
        if "cart_quantity" in session:
            cart_quantity_dict = session["cart_quantity"]

        # check if product (key ) in cart_session can be found in cart_quantity_dict. if product cannot be found, enter the details into cart_quantity_dict.
        # Without this line of code, if cart_quantity_dict is empty, there will be an error generated because the html cannot find the key since the dictionary has nothing.
        # So this ensures theres default values stored in the cart_quantity_dict
        for key in cart_session:
            if key not in cart_quantity_dict:
                cart_items = Products.Cart(1, key)
                cart_quantity_dict[key] = cart_items.__dict__


        return redirect(url_for('cart_Products'))
    

# This route, when customer adds a product, they will be directed here, with the product in the cart.
@app.route('/cartProducts', methods=['GET','POST'])
def cart_Products():

    # Open the db that stores all the products from products list page/createproducts from employees
    db = shelve.open('products.db', 'r')
    products_dict = {}
    try:
        products_dict = db['Products']
    except:
        print('Error in retrieving products from products.db.')
    # Open the db that stores all the products from products list page/createproducts from employees ends
        

    # checks whether the product in "cart_products" session has the same quantity as the quantity of the product in products_dict.
    # There is a possiblity when customer checks out and buys the item and the quantity of the product decreases in products_dict but does not decrease the quantity of the session.
    # Because of this, it will mess up the max a customer can select of a product because the quantity does not decrease. 
    for key in products_dict:
        if str(key) in session["cart_products"]:
            if session["cart_products"][str(key)]['_Products__quantity'] !=  products_dict[key].get_quantity():
                session["cart_products"][str(key)]['_Products__quantity'] = products_dict[key].get_quantity()
                session["cart_quantity"][str(key)]['_Cart__cart_quantity'] = 1

    # This checks if product in products_dict is in "cart_products"
    # After that, it checks if the product in the databse has  a quantity of 0. if it does have a quantity of 0, remove the item from the cart as the customer should not be able to checkout an item with no quantity  (out of stock)
        if str(key) in session["cart_products"]:
            if products_dict[key].get_quantity() <= 0:
                session["cart_quantity"].pop(str(key))
                session["cart_products"].pop(str(key))


    if "cart_products" in session:
        cart_session = session["cart_products"]
    if "cart_quantity" in session:
        cart_quantity_session = session["cart_quantity"]



    # stripe_products_dict = {}

    # db_stripe = shelve.open('stripeproducts.db', 'c')
    # try:
    #     if 'stripeProducts' in db_stripe:
    #         stripe_products_dict = db_stripe['stripeProducts']
    #     else:
    #         db_stripe['stripeProducts'] = stripe_products_dict
    # except:
    #     print('Error in retrieving products from products.db.')
        

    
    return render_template('cartProducts.html', cart_session=cart_session, cart_quantity_session = cart_quantity_session)



# might not need this route anymore
@app.route('/cartQuantity', methods=['GET','POST'])
def cart_quantity():

    if request.method == 'POST':
        if "cart_products" in session:
            cart_session = session["cart_products"]
        cart_quantity_dict = {}
        quantity = request.form.getlist("quantity")
        product_id = request.form.getlist("key")
        
        for item_id, item_quantity in zip(product_id, quantity):
            cart_items = Products.Cart(item_quantity, item_id)
            cart_quantity_dict[cart_items.get_cart_id()] = cart_items.__dict__

        if "cart_quantity" not in session:
            session["cart_quantity"] = {}
        
        session["cart_quantity"] = cart_quantity_dict
        # session["cart_quantity"].update(cart_quantity_dict)
        session.permanent = True
        session.modified = True
        if "cart_quantity" in session:
            cart_quantity_session = session["cart_quantity"]
    return cart_quantity_session
        
# @app.route('/cartCheckout', methods=['GET','POST'])
# def cart_checkout():
#     if "cart_products" in session:
#         cart_session = session["cart_products"]
#     if "cart_quantity" in session:
#         cart_quantity_session = session["cart_quantity"]
#     db = shelve.open('products.db', 'c')
#     products_dict = {}
#     try:
#         products_dict = db['Products']
#     except:
#         print('Error in retrieving products from products.db.')


    

#     return render_template('cartCheckout.html', cart_quantity_session = cart_quantity_session, cart_session=cart_session)
    
# @app.route('/displayProduct', methods=['GET','POST'])
# def display_product():
#     db_cart = shelve.open('cart_products.db', 'c')
#     cart_products_dict = {}
#     try:
#         if 'cart_products' in db_cart:
#             cart_products_dict = db_cart['cart_products']
#         else:
#             db_cart['cart_products'] = cart_products_dict
#     except:
#         print('Error in retrieving products from cart_products.db.')
#     cart_products_list = []
#     for key in cart_products_dict:
#         cart_products = cart_products_dict.get(key)
#         cart_products_list.append(cart_products)

#     return render_template('products_list.html', cart_products_list = cart_products_list)



@app.route('/createProducts', methods=['GET', 'POST'])
def create_products():
    create_products_form = CreateProductsForm(request.form)
    if request.method == 'POST' and create_products_form.validate():
        products_dict = {}
        db = shelve.open('products.db', 'c')

        try:
            products_dict = db['Products']

        except:
            print('Error in retrieving products from products.db.')



        product = Products.Products(create_products_form.product_name.data.capitalize(), create_products_form.product_price.data, create_products_form.product_quantity.data, create_products_form.product_country.data.capitalize(), create_products_form.product_type.data.capitalize(), create_products_form.product_dietary.data.capitalize())
        product.set_type(product.get_type().replace(' ','_'))
        product.set_url(f'./static/Images/{product.get_name().replace(" ","_")}.jpg')
        product.set_id(product.generate_product_id())
        products_dict[product.get_id()] = product

        enumerated_dict = products_dict
        for key in products_dict:
            index = list(products_dict).index(key)
            if index != key:
                enumerated_dict = {index: products_dict[key_inner] for index, key_inner in enumerate(products_dict)}

        products_dict = enumerated_dict
        for key in products_dict:
            products_dict[key].set_id(key)
        db['Products'] = products_dict


        

        

        # for key in products_dict:
        #     if key != list(products_dict.keys())[-1]:
        #         if key >= 0:
        #             key_to_check_positive = key + 1
        #     if key > 1:
        #         key_to_check_negative = key - 1


        #     if key_to_check_positive not in products_dict:
        #         enumerated_dict = {index: products_dict[key] for index, key in enumerate(products_dict)}
        #     if key_to_check_negative not in products_dict:
        #         enumerated_dict = {index: products_dict[key] for index, key in enumerate(products_dict)}
    

        db.close()

        return redirect(url_for('retrieve_products'))
    
    return render_template('createProducts.html', form=create_products_form)



@app.route('/retrieveProducts')
def retrieve_products():
    products_dict = {}
    db = shelve.open('products.db', 'c')

    try:
        products_dict = db['Products']

    except:
        print('Error in retrieving products from products.db.')




    db_stripe = shelve.open('stripeproducts.db', 'c')
    stripe_products_dict = {}
    try:
        if 'stripeProducts' in db_stripe:
            stripe_products_dict = db_stripe['stripeProducts']
        else:
            db_stripe['stripeProducts'] = stripe_products_dict
    except:
        print('Error in retrieving products from products.db.')
    # Stripe products creation
    for key in products_dict:
        product_id = products_dict[key].get_id()
        product_name = products_dict[key].get_name()
        product_price_cents = products_dict[key].get_price()
        product_price_dollars = int(product_price_cents * 100)
        product_image_url = products_dict[key].get_url()
        # Example: Creating a product with the Stripe API
        product = stripe.Product.create(
            name = product_name,
            type='service',
            images=[product_image_url] # Adjust the type as needed
            # Add more details like description, images, etc.
        )

        price = stripe.Price.create(
            currency = "sgd",
            unit_amount = product_price_dollars,
            product = product.id,
        )
        
        product_dict = product.to_dict()
        price_dict = price.to_dict()
        stripe_products_dict[product_id] = {'product': product_dict, 'price': price_dict}
    remove_keys = []
    for key in stripe_products_dict:
        if key not in products_dict:
            remove_keys.append(key)
    for key in remove_keys:
        stripe_products_dict.pop(key)

    db_stripe['stripeProducts'] = stripe_products_dict

    # Stripe products creation ends

    enumerated_dict = products_dict
    for key in products_dict:
        index = list(products_dict).index(key)
        for item in list(session["cart_products"]):
            if int(item) not in products_dict:
                session["cart_products"].pop(item)

        for item in list(session["cart_quantity"]):
            if int(item) not in products_dict:
                session["cart_quantity"].pop(item)

        if index != key:
            enumerated_dict = {index: products_dict[key_inner] for index, key_inner in enumerate(products_dict)}

    products_dict = enumerated_dict
    for key in products_dict:
        products_dict[key].set_id(key)
        products_dict[key].set_url(f'Images/{products_dict[key].get_name().replace(" ","_").lower()}.jpg')
    db['Products'] = products_dict




    
            
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    if "cart_products" in session:
        cart_session = session["cart_products"]
    db.close()

    db_stripe.close()



    
    return render_template('retrieveProducts.html', count=len(products_list), products_list=products_list)


@app.route('/updateProducts/<int:id>/', methods=['GET', 'POST'])
def update_products(id):
    update_products_form = CreateProductsForm(request.form)

    db = shelve.open('products.db', 'c')
    products_dict = {}
    try:
        if 'Products' in db:
            products_dict = db['Products']
        else:
            db['Products'] = products_dict
    except:
        print('Error in retrieving products from products.db.')
    finally:
        db.close()

    if request.method == 'POST' and update_products_form.validate():
        products_dict = {}
        db = shelve.open('products.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_name(update_products_form.product_name.data.capitalize())
        product.set_country(update_products_form.product_country.data)
        product.set_type(update_products_form.product_type.data)
        product.set_type(product.get_type().replace(' ','_').capitalize())
        product.set_dietary(update_products_form.product_dietary.data)
        product.set_price(update_products_form.product_price.data)
        product.set_quantity(update_products_form.product_quantity.data)
        product.set_url(update_products_form.product_url.data)


        db['Products'] = products_dict
        db.close()
        return redirect(url_for('retrieve_products'))
    else:
        products_dict = {}
        db = shelve.open('products.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        update_products_form.product_name.data = product.get_name()
        update_products_form.product_country.data = product.get_country()
        update_products_form.product_type.data = product.get_type()
        update_products_form.product_dietary.data = product.get_dietary()
        update_products_form.product_price.data = product.get_price()
        update_products_form.product_quantity.data = product.get_quantity()
        update_products_form.product_url.data = product.get_url()

        return render_template('updateProducts.html', form=update_products_form)



@app.route('/deleteProducts/<int:id>', methods=['GET','POST'])
def delete_products(id):
    db = shelve.open('products.db', 'c')
    products_dict = {}
    try:
        if 'Products' in db:
            products_dict = db['Products']
        else:
            db['Products'] = products_dict
    except:
        print('Error in retrieving products from products.db.')

    products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('retrieve_products'))



@app.route('/Base')
def base():
    return render_template('base.html')


YOUR_DOMAIN = 'http://localhost:5000'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    remove_id = request.form.get("remove_id")
    if remove_id != None:
        if remove_id in session["cart_products"]:
            session["cart_products"].pop(remove_id)
            if "cart_products" in session:
                cart_session = session["cart_products"]

        if "cart_quantity" not in session:
            session["cart_quantity"] = {}
        
        if remove_id in session["cart_quantity"]:
            session["cart_quantity"].pop(remove_id)
            if "cart_quantity" in session:
                cart_quantity_session = session["cart_quantity"]
    

        return redirect(url_for('cart_Products'))
    
    # if request.method == 'POST':
    #     if "cart_products" in session:
    #         cart_session = session["cart_products"]
    #     cart_quantity_dict = {}
    #     quantity = request.form.getlist("quantity")
    #     product_id = request.form.getlist("key")
    #     for item_id, item_quantity in zip(product_id, quantity):
    #         cart_items = Products.Cart(item_quantity, item_id)
    #     cart_quantity_dict[cart_items.get_cart_id()] = cart_items.__dict__

    #     if "cart_quantity" not in session:
    #         session["cart_quantity"] = {}
        
    #     session["cart_quantity"] = cart_quantity_dict
    #     # session["cart_quantity"].update(cart_quantity_dict)
    #     session.permanent = True
    #     session.modified = True
    #     if "cart_quantity" in session:
    #         cart_quantity_session = session["cart_quantity"]
        
    #     print(cart_quantity_session)
    if "cart_products" not in session:
        session["cart_products"] = {}

    if "cart_products" in session:
        cart_session = session["cart_products"]

    cart_quantity_session = cart_quantity()
    stripe_products_dict = {}

    db = shelve.open('stripeproducts.db', 'c')
    try:
        if 'stripeProducts' in db:
            stripe_products_dict = db['stripeProducts']
        else:
            db['stripeProducts'] = stripe_products_dict
    except:
        print('Error in retrieving products from products.db.')


    line_items = []
    metadata = {}
    images = {}
    for key in stripe_products_dict:
        if str(key) in cart_session:
            metadata[key] = cart_quantity_session[str(key)]['_Cart__cart_quantity']
            line_items.append({'price': stripe_products_dict[key]['price']['id'], 'quantity' : cart_quantity_session[str(key)]['_Cart__cart_quantity'], })
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_intent_data = {
                "metadata": metadata
            },
            invoice_creation={"enabled": True},
            billing_address_collection='auto',
            shipping_address_collection={
              'allowed_countries': ['SG'],
            },
            shipping_options=[
                {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 0, "currency": "sgd"},
                    "display_name": "Free shipping",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 5},
                    "maximum": {"unit": "business_day", "value": 7},
                    },
                },
                },
                {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 500, "currency": "sgd"},
                    "display_name": "Next Day Ground Shipping",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 1},
                    },
                },
                },
            ],
            line_items = line_items,
            # line_items=[
            #     {
            #         # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
            #         'price': 'price_1OZciFAnVKG20ORqARSOVblF',
            #         'quantity': 10,
            #     },
            # ],
            mode='payment',
            custom_text={
    "shipping_address": {
      "message":
      "Please note that we can't guarantee 2-day delivery for PO boxes at this time.",
    },
    "submit": {"message": "We'll email you instructions on how to get started."},
  },

            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cart_Products', _external=True),
        )
    
        
    except Exception:
        return render_template('checkoutError.html')

    
    
    
        


    return redirect(checkout_session.url, code=303)



@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    # Handle the event
    line_items = None

    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        line_items = stripe.checkout.Session.list_line_items(session_id)
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        selected_shipping_rate = stripe.ShippingRate.retrieve(checkout_session.shipping_cost.shipping_rate)
        fixed_amount = (selected_shipping_rate.get("fixed_amount", {}).get("amount", 0))/100

    

        db_session_id = shelve.open('session_id.db', 'c')
        session_id_dict = {}
        try:
            if 'session_id' in db_session_id:
                session_id_dict = db_session_id['session_id']
            else:
                db_session_id['session_id'] = session_id_dict
        except:
            print('Error in retrieving products from products.db.')

        db = shelve.open('products.db', 'w')
        products_dict = {}
        try:
            products_dict = db['Products']
        except:
            print('Error in retrieving products from products.db.')
            
        db['Products'] = products_dict

        # target_description_array = []
        # for item in line_items:
        #     target_description_array.append(line_items[item]['data'][0]['description'])

        # for item in session_id_dict:
        #     if session_id_dict[item]['data'][0]['description'] not in session_id_dict:
        shipping_amount = 0
        total_price = 0
        order_date = datetime.date.today()
        arrive_by_days = datetime.timedelta(days=7)
        arrive_by_date = order_date + arrive_by_days
        for item in line_items['data']:
            description = item['description']
            amount_total = item['amount_total'] / 100
            quantity = item['quantity']
            if session_id not in session_id_dict:
                total_price = 0
                shipping_amount = 0
                shipping_amount = fixed_amount
                total_price += amount_total
                total_price += shipping_amount

                for key in products_dict:
                    if products_dict[key].get_name() == description:
        # If not, create a new entry with a list containing the current item
                        session_id_dict[session_id] = [{
                            'id' : session_id,
                            'name': description,
                            'price': amount_total,
                            'total_price': total_price,
                            'quantity': quantity,
                            'image': products_dict[key].get_url(),
                            'order_date': order_date,
                            'arrive_date': arrive_by_date,

                        }]
            else:
                total_price += amount_total
                for key in products_dict:
                    if products_dict[key].get_name() == description:
        # If not, create a new entry with a list containing the current item
                        session_id_dict[session_id].append({
                            'id' : session_id,
                            'name': description,
                            'price': amount_total,
                            'total_price': total_price,
                            'quantity': quantity,
                            'image': products_dict[key].get_url(),
                            'order_date': order_date,
                            'arrive_date': arrive_by_date,
                        })



                
                

        # items_dict = {}
        # items_list = []
        # for item in line_items['data']:
        #     description = item['description']
        #     amount_total = item['amount_total']
        #     quantity = item['quantity']
        #     items_dict.update({'name': description, 'amount_total': amount_total, 'quantity': quantity})
        # print(items_dict)
        # print(session_id)
        # for item in session_id_dict:
        #     session_id_dict[session_id] = items_dict
        #     print(session_id_dict)
        
        
        db_session_id['session_id'] = session_id_dict
        db_session_id.close()
        

        

    if event['type'] == 'payment_intent.succeeded':
        intent_id = event['data']['object']['id']
        intent = stripe.PaymentIntent.retrieve(intent_id)
        print('hello')

        db = shelve.open('products.db', 'w')
        products_dict = {}
        try:
            products_dict = db['Products']
        except:
            print('Error in retrieving products from products.db.')
            
        db['Products'] = products_dict


        db_stripe = shelve.open('stripeproducts.db', 'c')
        stripe_products_dict = {}
        try:
            if 'stripeProducts' in db_stripe:
                stripe_products_dict = db_stripe['stripeProducts']
            else:
                db_stripe['stripeProducts'] = stripe_products_dict
        except:
            print('Error in retrieving products from products.db.')

        metadata = intent.get('metadata', {})
        for key in products_dict:
            if str(key) in metadata:
                if str(key) in metadata:
                    user_quantity = metadata[str(key)]
                    db_quantity = products_dict[int(key)].get_quantity()
                    new_db_quantity = db_quantity - int(user_quantity)
                    products_dict[key].set_quantity(new_db_quantity)
                    print(products_dict[key].get_quantity())

        
        db['Products'] = products_dict
        db.close()

        print('email sent')

    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

@app.route('/boughtProducts', methods=['GET', 'POST'])
def bought_products():

    db_session_id = shelve.open('session_id.db', 'c')
    session_id_dict = {}
    try:
        if 'session_id' in db_session_id:
            session_id_dict = db_session_id['session_id']
        else:
            db_session_id['session_id'] = session_id_dict
    except:
        print('Error in retrieving products from products.db.')

    db_stripe = shelve.open('stripeproducts.db', 'c')
    stripe_products_dict = {}
    try:
        if 'stripeProducts' in db_stripe:
            stripe_products_dict = db_stripe['stripeProducts']
        else:
            db_stripe['stripeProducts'] = stripe_products_dict
    except:
        print('Error in retrieving products from products.db.')

    if "bought_products" not in session:
        session["bought_products"] = {}
    session["bought_products"] = session_id_dict

    session_bought_products = session["bought_products"]


    if request.method == 'POST':
        remove_history = request.form.get("Remove_history")
        if remove_history == "Remove Cart History":
            session["bought_products"].clear()
            db_session_id.clear()


    db_session_id.close()

    
    today = datetime.date.today()



    
    # for item in stripe_products_dict:
    #     if stripe_products_dict[item]['product']['name'] in session_id_dict.values():
    #         product_name = stripe_products_dict[item]['product']['name']

    #         bought_products_dict[product_name] = { 
    #                 'amount_total': session_id_dict[product_name]['amount_total'],
    #                 'quantity': session_id_dict[product_name]['quantity'],
    #                 'image': stripe_products_dict[item]['product']['images']
    #         }

    # session["bought_products"] = bought_products_dict
    return render_template('boughtProducts.html', session_bought_products = session_bought_products, today= today)

@app.route('/cancel', methods=['GET'])
def cancel():
    return render_template('cancel.html')

@app.route('/success', methods=['GET'])
def success():
    if "cart_products" in session:
        session["cart_products"].clear()
    print(session["cart_products"])

    if "cart_quantity" in session:
        session["cart_quantity"].clear()    
    print(session["cart_quantity"])

    return render_template('success.html')

if __name__ == '__main__':
    app.run(port = 5000,debug = True)
