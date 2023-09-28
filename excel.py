import pandas as pd

products_and_services = [
    {"name": "Dilmah Tea - Green", "price": 4.0, "quantity": 50, "supplier": "Tea Co.", "is_product": True,
     "definition": "Dilmah Green Tea is a refreshing and healthy beverage made from green tea leaves."},
    {"name": "Dilmah Tea - Black", "price": 3.5, "quantity": 60, "supplier": "Tea Co.", "is_product": True,
     "definition": "Dilmah Black Tea is a classic tea with a rich flavor and aroma."},
    {"name": "Dilmah Tea - Herbal", "price": 4.5, "quantity": 40, "supplier": "Tea Co.", "is_product": True,
     "definition": "Dilmah Herbal Tea is a caffeine-free herbal infusion with natural flavors."},
    {"name": "Ahmad Tea - Earl Grey", "price": 5.0, "quantity": 30, "supplier": "Tea Co.", "is_product": True,
     "definition": "Ahmad Tea Earl Grey is a traditional black tea flavored with bergamot oil."},
    {"name": "Ahmad Tea - English Breakfast", "price": 4.5, "quantity": 35, "supplier": "Tea Co.",
     "is_product": True,
     "definition": "Ahmad Tea English Breakfast is a strong and robust black tea."},
    {"name": "Ahmad Tea - Jasmine Green", "price": 4.8, "quantity": 25, "supplier": "Tea Co.", "is_product": True,
     "definition": "Ahmad Tea Jasmine Green is a fragrant green tea with jasmine blossoms."},
    {"name": "Delivery Service", "price": 10.0, "quantity": 100, "supplier": "Your Shop", "is_product": False,
     "definition": "Delivery Service includes safe and timely delivery of your orders to your doorstep."},
    {"name": "Gift Wrapping", "price": 2.0, "quantity": 200, "supplier": "Your Shop", "is_product": False,
     "definition": "Gift Wrapping service includes beautifully wrapping your items for special occasions."},
    {"name": "Tea Tasting Experience", "price": 15.0, "quantity": 50, "supplier": "Your Shop", "is_product": False,
     "definition": "Tea Tasting Experience allows you to sample a variety of tea flavors and learn about their unique characteristics."}
]
products_and_services_2 = [
    {"name": "Coffee Beans", "price": 7.0, "quantity": 80, "supplier": "Coffee Co.", "is_product": True,
     "definition": "Freshly roasted coffee beans for a rich and aromatic coffee experience."},
    {"name": "Teapot", "price": 20.0, "quantity": 15, "supplier": "Kitchen Supplies", "is_product": True,
     "definition": "A high-quality teapot for steeping your favorite teas."},
    {"name": "Coffee Grinder", "price": 15.0, "quantity": 25, "supplier": "Kitchen Supplies", "is_product": True,
     "definition": "An electric coffee grinder for grinding coffee beans to perfection."},
    {"name": "Mug Set", "price": 12.0, "quantity": 50, "supplier": "Kitchen Supplies", "is_product": True,
     "definition": "A set of stylish ceramic mugs for enjoying your hot beverages."},
    {"name": "Cappuccino Machine", "price": 150.0, "quantity": 10, "supplier": "Coffee Co.", "is_product": True,
     "definition": "An espresso machine with a milk frother for making delicious cappuccinos."},
    {"name": "Tea Infuser", "price": 5.0, "quantity": 100, "supplier": "Kitchen Supplies", "is_product": True,
     "definition": "A convenient tea infuser for brewing loose-leaf teas."},
    {"name": "Delivery Service", "price": 10.0, "quantity": 100, "supplier": "Your Shop", "is_product": False,
     "definition": "Delivery Service includes safe and timely delivery of your orders to your doorstep."},
    {"name": "Gift Wrapping", "price": 2.0, "quantity": 200, "supplier": "Your Shop", "is_product": False,
     "definition": "Gift Wrapping service includes beautifully wrapping your items for special occasions."},
    {"name": "Coffee Tasting Experience", "price": 20.0, "quantity": 30, "supplier": "Coffee Co.", "is_product": False,
     "definition": "Coffee Tasting Experience allows you to sample a variety of coffee beans and brews."},
]

def create_excel(dictionary, name_file):
    df_first = pd.DataFrame(dictionary)
    df_first.to_excel(f"{name_file}.xlsx", index=False)

# create_excel(products_and_services_2, name_file='product_coffee')







