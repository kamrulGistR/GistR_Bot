import telebot
import json
import random

# Bot Token
TOKEN = "7550241284:AAFRukpg7felOh2AgM3meWWd_3riF-N8Uu0"
bot = telebot.TeleBot(TOKEN)

# Temporary storage for user data
users = {}
restaurants = {}
riders = {}
orders = {}
admin_id = "6458422220"  # Replace with your admin's Telegram ID

# Save data to JSON files
def save_data(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)

# Load data from JSON files
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Load existing data
users = load_data("users.json")
restaurants = load_data("restaurants.json")
riders = load_data("riders.json")
orders = load_data("orders.json")

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "স্বাগতম GistR বটে!\n\nআপনার প্রয়োজনীয় অপশনটি বেছে নিন:\n"
        "/register - কাস্টমার রেজিস্ট্রেশন\n"
        "/track - অর্ডার ট্র্যাকিং\n"
        "/restaurant - রেস্টুরেন্ট রেজিস্ট্রেশন\n"
        "/rider - রাইডার রেজিস্ট্রেশন\n"
        "/help - সহায়তা পেতে\n"
        "/admin - অ্যাডমিন প্যানেল (শুধু অ্যাডমিনদের জন্য)"
    )

# Admin Panel
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.chat.id) == admin_id:
        bot.reply_to(
            message,
            "স্বাগতম অ্যাডমিন প্যানেলে!\n"
            "/approve_restaurant - রেস্টুরেন্ট ভেরিফাই করুন\n"
            "/approve_rider - রাইডার ভেরিফাই করুন\n"
            "/view_orders - সমস্ত অর্ডার দেখুন"
        )
    else:
        bot.reply_to(message, "আপনার এই অপশনটি ব্যবহারের অনুমতি নেই।")

@bot.message_handler(commands=['approve_restaurant'])
def approve_restaurant(message):
    if str(message.chat.id) == admin_id:
        unverified = [k for k, v in restaurants.items() if not v.get("verified")]
        if unverified:
            for r_id in unverified:
                restaurants[r_id]["verified"] = True
            save_data(restaurants, "restaurants.json")
            bot.reply_to(message, f"{len(unverified)} রেস্টুরেন্ট সফলভাবে ভেরিফাই হয়েছে!")
        else:
            bot.reply_to(message, "কোনো অযাচাইকৃত রেস্টুরেন্ট নেই।")
    else:
        bot.reply_to(message, "আপনার এই অপশনটি ব্যবহারের অনুমতি নেই।")

@bot.message_handler(commands=['approve_rider'])
def approve_rider(message):
    if str(message.chat.id) == admin_id:
        unverified = [k for k, v in riders.items() if not v.get("verified")]
        if unverified:
            for r_id in unverified:
                riders[r_id]["verified"] = True
            save_data(riders, "riders.json")
            bot.reply_to(message, f"{len(unverified)} রাইডার সফলভাবে ভেরিফাই হয়েছে!")
        else:
            bot.reply_to(message, "কোনো অযাচাইকৃত রাইডার নেই।")
    else:
        bot.reply_to(message, "আপনার এই অপশনটি ব্যবহারের অনুমতি নেই।")

# User Registration
@bot.message_handler(commands=['register'])
def register_user(message):
    users[message.chat.id] = {"step": "name"}
    bot.reply_to(message, "আপনার নাম দিন:")

@bot.message_handler(func=lambda message: users.get(message.chat.id, {}).get("step") == "name")
def get_user_name(message):
    users[message.chat.id]["name"] = message.text
    users[message.chat.id]["step"] = "phone"
    bot.reply_to(message, "আপনার ফোন নম্বর দিন:")

@bot.message_handler(func=lambda message: users.get(message.chat.id, {}).get("step") == "phone")
def get_user_phone(message):
    users[message.chat.id]["phone"] = message.text
    users[message.chat.id]["step"] = "address"
    bot.reply_to(message, "আপনার ঠিকানা দিন:")

@bot.message_handler(func=lambda message: users.get(message.chat.id, {}).get("step") == "address")
def get_user_address(message):
    users[message.chat.id]["address"] = message.text
    users[message.chat.id]["step"] = None
    save_data(users, "users.json")
    bot.reply_to(message, "রেজিস্ট্রেশন সম্পন্ন হয়েছে!")

# Restaurant Registration
@bot.message_handler(commands=['restaurant'])
def register_restaurant(message):
    restaurants[message.chat.id] = {"step": "name"}
    bot.reply_to(message, "আপনার রেস্টুরেন্টের নাম দিন:")

@bot.message_handler(func=lambda message: restaurants.get(message.chat.id, {}).get("step") == "name")
def get_restaurant_name(message):
    restaurants[message.chat.id]["name"] = message.text
    restaurants[message.chat.id]["step"] = "address"
    bot.reply_to(message, "রেস্টুরেন্টের ঠিকানা দিন:")

@bot.message_handler(func=lambda message: restaurants.get(message.chat.id, {}).get("step") == "address")
def get_restaurant_address(message):
    restaurants[message.chat.id]["address"] = message.text
    restaurants[message.chat.id]["step"] = "phone"
    bot.reply_to(message, "রেস্টুরেন্টের ফোন নম্বর দিন:")

@bot.message_handler(func=lambda message: restaurants.get(message.chat.id, {}).get("step") == "phone")
def get_restaurant_phone(message):
    restaurants[message.chat.id]["phone"] = message.text
    restaurants[message.chat.id]["step"] = None
    save_data(restaurants, "restaurants.json")
    bot.reply_to(message, "আপনার রেস্টুরেন্ট রেজিস্টার করা হয়েছে! আমাদের ভেরিফিকেশন টিম আপনার সাথে যোগাযোগ করবে।")

# Rider Registration
@bot.message_handler(commands=['rider'])
def register_rider(message):
    riders[message.chat.id] = {"step": "name"}
    bot.reply_to(message, "আপনার নাম দিন:")

@bot.message_handler(func=lambda message: riders.get(message.chat.id, {}).get("step") == "name")
def get_rider_name(message):
    riders[message.chat.id]["name"] = message.text
    riders[message.chat.id]["step"] = "phone"
    bot.reply_to(message, "আপনার ফোন নম্বর দিন:")

@bot.message_handler(func=lambda message: riders.get(message.chat.id, {}).get("step") == "phone")
def get_rider_phone(message):
    riders[message.chat.id]["phone"] = message.text
    riders[message.chat.id]["step"] = "area"
    bot.reply_to(message, "আপনার কাজের এরিয়া দিন:")

@bot.message_handler(func=lambda message: riders.get(message.chat.id, {}).get("step") == "area")
def get_rider_area(message):
    riders[message.chat.id]["area"] = message.text
    riders[message.chat.id]["step"] = None
    save_data(riders, "riders.json")
    bot.reply_to(message, "আপনার আবেদন গ্রহণ করা হয়েছে! আমাদের টিম থেকে শীঘ্রই আপনার সাথে যোগাযোগ করা হবে।")

# Place Order
@bot.message_handler(commands=['place_order'])
def place_order(message):
    user = users.get(message.chat.id)
    if user:
        tracking_code = f"TRACK_{random.randint(1000, 9999)}"
        orders[tracking_code] = {
            "status": "Pending",
            "address": user["address"],
            "customer_id": message.chat.id
        }
        save_data(orders, "orders.json")
        bot.reply_to(message, f"আপনার অর্ডার প্লেস করা হয়েছে! ট্র্যাকিং কোড: {tracking_code}")
    else:
        bot.reply_to(message, "অর্ডার প্লেস করার আগে রেজিস্ট্রেশন করুন।")

# Track Order
@bot.message_handler(commands=['track'])
def track_order(message):
    bot.reply_to(message, "আপনার ট্র্যাকিং কোড দিন:")

@bot.message_handler(func=lambda message: message.text.startswith("TRACK_"))
def get_order_status(message):
    tracking_code = message.text
    if tracking_code in orders:
        order = orders[tracking_code]
        bot.reply_to(
            message,
            f"অর্ডার স্ট্যাটাস: {order['status']}\nডেলিভারির ঠিকানা: {order['address']}"
        )
    else:
        bot.reply_to(message, "এই ট্র্যাকিং কোডের সাথে কোনো অর্ডার পাওয়া যায়নি।")

# Notify Admin
def notify_admin(text):
    bot.send_message(admin_id, text)

# Run the Bot
bot.polling()