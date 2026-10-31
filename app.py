import gradio as gr
from mobile_shop import (
    get_all_mobiles,
    search_mobile,
    search_by_budget,
    add_mobile,
    delete_mobile,
    purchase_mobile,
    shop_statistics,
    ask_gemini,
    ai_recommendation,
    compare_mobiles
)

# DISPLAY HELPER
def display_mobiles(data):
    if not data:
        return "🚫 **No mobiles found.**"
    text = ""
    for mobile in data:
        text += f"""
---
### 📱 {mobile['brand']} {mobile['model']}
* **ID:** {mobile['id']}
* **Price:** 💰 ₹{mobile['price']:,}
* **RAM:** ⚡ {mobile['ram']}
* **Storage:** 💾 {mobile['storage']}
* **Rating:** ⭐ {mobile['rating']}
* **Stock:** 📦 {mobile['stock']}
"""
    return text

# INVENTORY
def show_inventory():
    data = get_all_mobiles()
    return display_mobiles(data)

# SEARCH
def search_ui(keyword):
    data = search_mobile(keyword)
    return display_mobiles(data)

# BUDGET
def budget_ui(budget):
    data = search_by_budget(budget)
    return display_mobiles(data)

# ADD MOBILE
def add_ui(brand, model, price, ram, storage, rating, stock):
    mobile = add_mobile(brand, model, price, ram, storage, rating, stock)
    return f"✅ **Mobile successfully added!**\n\n{mobile}"

# DELETE
def delete_ui(mobile_id):
    result = delete_mobile(int(mobile_id))
    if result:
        return "🗑️ **Mobile deleted successfully.**"
    return "❌ **Mobile not found. Check the ID.**"

# PURCHASE
def purchase_ui(mobile_id):
    result = purchase_mobile(int(mobile_id))
    if result["success"]:
        return f"🎉 **{result['message']}**"
    return f"⚠️ **{result['message']}**"

# STATISTICS
def statistics_ui():
    data = shop_statistics()
    return f"""
## 📊 Shop Statistics

* **📱 Total Models in Store:** {data['total_models']}
* **📦 Total Units in Stock:** {data['total_stock']}
* **💵 Average Price:** ₹{data['average_price']:,.2f}
* **🏆 Highest Rated Phone:** {data['highest_rated']['brand']} {data['highest_rated']['model']} (⭐ {data['highest_rated']['rating']})
"""

# CUSTOM THEME (Modern Dashboard Look)
custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    
)
# GRADIO APPLICATION
with gr.Blocks(title="AI Mobile Shop", theme=custom_theme) as app:
    
    with gr.Row():
        gr.Markdown(
            """
            <div style="text-align: center; padding: 20px;">
                <h1>🤖 AI Mobile Shop Management System</h1>
                <p style="font-size: 16px; color: gray;">Powered by Python Lists, Dictionaries & Google Gemini AI</p>
            </div>
            """
        )
    
    # INVENTORY TAB
    with gr.Tab("📋 Inventory"):
        gr.Markdown("### Browse the current mobile stock")
        show_button = gr.Button("🔄 Show All Mobiles", variant="primary")
        inventory_output = gr.Markdown()
        show_button.click(show_inventory, outputs=inventory_output)

    # SEARCH TAB
    with gr.Tab("🔍 Search"):
        gr.Markdown("### Search by Brand or Model Name")
        keyword = gr.Textbox(label="Brand / Model", placeholder="e.g. Samsung, iPhone, Pixel...")
        search_button = gr.Button("🔍 Search Catalog", variant="primary")
        search_output = gr.Markdown()
        search_button.click(search_ui, inputs=keyword, outputs=search_output)

    # BUDGET TAB
    with gr.Tab("💰 Budget"):
        gr.Markdown("### Find phones within your price range")
        budget = gr.Number(label="Maximum Budget (₹)", value=50000)
        budget_button = gr.Button("🔎 Find Mobiles", variant="primary")
        budget_output = gr.Markdown()
        budget_button.click(budget_ui, inputs=budget, outputs=budget_output)

    # ADD TAB
    with gr.Tab("➕ Add Mobile"):
        gr.Markdown("### Register a new mobile phone to the inventory")
        with gr.Row():
            brand = gr.Textbox(label="Brand")
            model = gr.Textbox(label="Model")
            price = gr.Number(label="Price (₹)")
        with gr.Row():
            ram = gr.Textbox(label="RAM (e.g. 8GB)")
            storage = gr.Textbox(label="Storage (e.g. 128GB)")
            rating = gr.Number(label="Rating (out of 5.0)", value=4.0)
            stock = gr.Number(label="Stock Quantity", value=10)
        add_button = gr.Button("✅ Add Mobile to Inventory", variant="primary")
        add_output = gr.Textbox(label="System Output")
        add_button.click(add_ui, inputs=[brand, model, price, ram, storage, rating, stock], outputs=add_output)

    # DELETE TAB
    with gr.Tab("🗑️ Delete"):
        gr.Markdown("### Remove a mobile from the system")
        mobile_id = gr.Number(label="Mobile ID to delete")
        delete_button = gr.Button("⚠️ Delete Mobile", variant="stop")
        delete_output = gr.Textbox(label="System Output")
        delete_button.click(delete_ui, inputs=mobile_id, outputs=delete_output)

    # PURCHASE TAB
    with gr.Tab("🛒 Purchase"):
        gr.Markdown("### Process a customer purchase (Reduces stock by 1)")
        purchase_id = gr.Number(label="Mobile ID to purchase")
        purchase_button = gr.Button("💳 Process Purchase", variant="primary")
        purchase_output = gr.Textbox(label="Transaction Status")
        purchase_button.click(purchase_ui, inputs=purchase_id, outputs=purchase_output)

    # STATISTICS TAB
    with gr.Tab("📈 Statistics"):
        gr.Markdown("### Generate shop performance and inventory metrics")
        stats_button = gr.Button("📊 Generate Shop Statistics", variant="primary")
        stats_output = gr.Markdown()
        stats_button.click(statistics_ui, outputs=stats_output)

    # GEMINI ASSISTANT
    with gr.Tab("✨ Gemini AI Assistant"):
        gr.Markdown("### Ask our AI anything about the current inventory")
        question = gr.Textbox(label="Ask Gemini", placeholder="Which phone has the best camera and costs under ₹60,000?", lines=3)
        ai_button = gr.Button("✨ Ask Gemini", variant="primary")
        ai_output = gr.Markdown()
        ai_button.click(ask_gemini, inputs=question, outputs=ai_output)

    # AI RECOMMENDATION
    with gr.Tab("🎯 AI Recommendation"):
        gr.Markdown("### Get a personalized phone recommendation based on needs")
        with gr.Row():
            ai_budget = gr.Number(label="Budget (₹)", value=70000)
            ai_usage = gr.Textbox(label="Usage Requirements", placeholder="Gaming / Photography / Office Work / General Use")
        recommendation_button = gr.Button("🎯 Get AI Recommendation", variant="primary")
        recommendation_output = gr.Markdown()
        recommendation_button.click(ai_recommendation, inputs=[ai_budget, ai_usage], outputs=recommendation_output)

    # AI COMPARISON
    with gr.Tab("⚖️ AI Comparison"):
        gr.Markdown("### Let AI compare two phones head-to-head")
        with gr.Row():
            phone1 = gr.Textbox(label="Phone 1", placeholder="e.g. Samsung Galaxy S25")
            phone2 = gr.Textbox(label="Phone 2", placeholder="e.g. OnePlus 13")
        compare_button = gr.Button("⚖️ Compare Phones", variant="primary")
        compare_output = gr.Markdown()
        compare_button.click(compare_mobiles, inputs=[phone1, phone2], outputs=compare_output)

# START
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0")