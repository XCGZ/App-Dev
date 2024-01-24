from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, DecimalField

# class CreateProductsForm(Form):
#     product_name = StringField('Product Name', [validators.Length(min=1, max=30), validators.DataRequired()])
#     product_price = IntegerField('Product Price', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
#     product_quantity = IntegerField('Product Quantity', [validators.NumberRange(min=1, max=10000), validators.DataRequired()])
#     product_country = StringField('Product Country', [validators.Length(min=1, max=30), validators.DataRequired()])
#     product_type = StringField('Product Type', [validators.Length(min=1, max=500), validators.DataRequired()])
#     product_dietary = StringField('Product Dietary', [validators.Length(min=1, max=30), validators.DataRequired()])
#     product_url = StringField('Product URL')

class CreateProductsForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=1000), validators.DataRequired()])
    product_price = IntegerField('Product Price', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    product_quantity = IntegerField('Product Quantity', [validators.NumberRange(min=1, max=10000), validators.DataRequired()])

    product_country = SelectField('Product Country', [validators.DataRequired()], 
                                  choices=[
                                      ('Singapore', 'Singapore'), 
                                      ('Japan', 'Japan'), 
                                      ('China', 'China'),
                                      ('India', 'India')], default='Singapore')

    product_type = SelectField('Product Type', [validators.DataRequired()], 
                                choices=[
                                        ('Snacks', 'Snacks'),
                                        ('Drinks', 'Drinks'), 
                                        ('Frozen', 'Frozen'), 
                                        ('Fruits_&_vegetables', 'Fruits & Vegetables'), 
                                        ('Household', 'Household'), 
                                        ('Health_&_wellness', 'Health & Wellness'), 
                                        ('Meat_&_seafood', 'Meat & Seafood'), 
                                        ('Dairy_&_chilled_&_eggs', 'Dairy, Chilled & Eggs'), 
                                        ('Beer_&_wine_&_spirits', 'Beer, Wine & Spirits'), 
                                        ('Beauty_&_personal_care', 'Beauty & Personal Care'), 
                                        ('Baby_&_child_&_toys', 'Baby, Child & Toys'), 
                                        ('Rice_&_noodles_&_cooking_ingredients', 'Rice, Noodles & Cooking Ingredients')], default='Snacks')

    product_dietary = SelectField('Product Dietary', [validators.DataRequired()], 
                                  choices=[
                                      ('Halal', 'Halal'), 
                                      ('Organic', 'Organic'), 
                                      ('Halal_&_organic', 'Halal & Organic')], default='Halal')

    product_url = StringField('Product URL')

    