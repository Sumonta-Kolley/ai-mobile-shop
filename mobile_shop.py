import os
from google import genai

# MOBILE DATA
mobiles = [
    {"id": 1, "brand": "Samsung", "model": "Galaxy S25", "price": 79999, "ram": "12GB", "storage": "256GB",
     "rating": 4.7, "stock": 10},
    {"id": 2, "brand": "Apple", "model": "iPhone 16", "price": 79900, "ram": "8GB", "storage": "128GB", "rating": 4.8,
     "stock": 8},
    {"id": 3, "brand": "OnePlus", "model": "OnePlus 13", "price": 69999, "ram": "12GB", "storage": "256GB",
     "rating": 4.6, "stock": 12},
    {"id": 4, "brand": "Google", "model": "Pixel 9", "price": 74999, "ram": "12GB", "storage": "256GB", "rating": 4.5,
     "stock": 7},
    {"id": 5, "brand": "Xiaomi", "model": "Xiaomi 15", "price": 59999, "ram": "12GB", "storage": "256GB", "rating": 4.4,
     "stock": 15},
    {"id": 6, "brand": "Realme", "model": "GT 7", "price": 42999, "ram": "12GB", "storage": "256GB", "rating": 4.3,
     "stock": 20}
]

# GEMINI SETUP
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


# BASIC MOBILE FUNCTIONS
def get_all_mobiles():
    return mobiles


def search_mobile(keyword):
    keyword = keyword.lower()
    result = list(
        filter(lambda mobile: keyword in mobile["brand"].lower() or keyword in mobile["model"].lower(), mobiles))
    return result


def search_by_budget(budget):
    result = list(filter(lambda mobile: mobile["price"] <= budget, mobiles))
    # Highest rating first
    result = sorted(result, key=lambda mobile: mobile["rating"], reverse=True)
    return result


# ADD MOBILE
def add_mobile(brand, model, price, ram, storage, rating, stock):
    new_id = max([mobile["id"] for mobile in mobiles], default=0) + 1
    mobile = {
        "id": new_id,
        "brand": brand,
        "model": model,
        "price": int(price),
        "ram": ram,
        "storage": storage,
        "rating": float(rating),
        "stock": int(stock)
    }
    mobiles.append(mobile)
    return mobile


# DELETE MOBILE
def delete_mobile(mobile_id):
    for mobile in mobiles:
        if mobile["id"] == mobile_id:
            mobiles.remove(mobile)
            return True
    return False


# PURCHASE MOBILE
def purchase_mobile(mobile_id):
    for mobile in mobiles:
        if mobile["id"] == mobile_id:
            if mobile["stock"] > 0:
                mobile["stock"] -= 1
                return {"success": True, "message": "Purchase successful", "mobile": mobile}
            return {"success": False, "message": "Mobile is out of stock"}
    return {"success": False, "message": "Mobile not found"}


# SHOP STATISTICS
def shop_statistics():
    total_models = len(mobiles)
    total_stock = sum(mobile["stock"] for mobile in mobiles)
    average_price = sum(mobile["price"] for mobile in mobiles) / total_models
    highest_rated = max(mobiles, key=lambda mobile: mobile["rating"])
    return {
        "total_models": total_models,
        "total_stock": total_stock,
        "average_price": average_price,
        "highest_rated": highest_rated
    }


# GEMINI AI FUNCTION
def ask_gemini(question):
    if client is None:
        return "Gemini API key is not configured."
    inventory = str(mobiles)
    prompt = f"""
You are an AI assistant for a mobile phone shop.
Available mobile inventory:
{inventory}
Customer question:
{question}
Instructions:
Recommend only phones available in the inventory.
Consider price, RAM, storage, rating and stock.
Do not invent specifications.
Give a simple explanation.
Use Indian Rupees.
Answer the customer.
"""
    response = client.models.generate_content(model="gemini-3.7-flash", contents=prompt)
    return response.text


# AI RECOMMENDATION
def ai_recommendation(budget, usage):
    available = search_by_budget(budget)
    if not available:
        return "No mobile available within this budget."
    prompt = f"""
You are a mobile phone expert.
Customer budget:
{budget}
Customer usage:
{usage}
Available phones:
{available}
Select the best phone.
Explain:
1. Recommended phone
2. Why it is suitable
3. Alternative phone
Use only the supplied inventory.
"""
    if client is None:
        return "Gemini API key is not configured."
    response = client.models.generate_content(model="gemini-3.7-flash", contents=prompt)
    return response.text


# AI COMPARISON
def compare_mobiles(phone1, phone2):
    mobile1 = None
    mobile2 = None
    for mobile in mobiles:
        name = (mobile["brand"] + " " + mobile["model"]).lower()
        if name == phone1.lower():
            mobile1 = mobile
        if name == phone2.lower():
            mobile2 = mobile
    if mobile1 is None:
        return "First mobile not found."
    if mobile2 is None:
        return "Second mobile not found."
    if client is None:
        return "Gemini API key is not configured."

    prompt = f"""
Compare these two mobile phones.
PHONE 1:
{mobile1}
PHONE 2:
{mobile2}
Compare:
Price
RAM
Storage
Rating
Stock
Value for money
Give a final recommendation.
Do not invent specifications.
"""
    response = client.models.generate_content(model="gemini-3.7-flash", contents=prompt)
    return response.text