
import hashlib
import json
import math
import os
from datetime import datetime

import config



all_data = {}
current_user = {}
dollar_rate_toman = config.DEFAULT_DOLLAR_RATE
rate_source_text = config.t("rate_default")



def get_now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")



def format_dollar(amount_dollar):
    return f"{amount_dollar:,.2f} " + config.t("dollar_unit")


def format_toman(amount_toman):
    return f"{amount_toman:,.0f} " + config.t("toman_unit")


def format_distance(distance_in_km):
    return f"{distance_in_km:,.1f} " + config.t("km_unit")


def format_weight(weight_in_kg):
    return str(weight_in_kg) + " " + config.t("weight_unit")



def get_data_file_path():
    program_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(program_folder, config.DATA_FILE_NAME)


def make_empty_data():
    empty_data = {
        "users": [],
        "orders": [],
        "tickets": [],
        "settings": {
            "dollar_rate": config.DEFAULT_DOLLAR_RATE,
            "next_order_number": 1001,
            "next_ticket_number": 1,
        },
    }
    return empty_data


def load_all_data():
    print("در حال خواندن فایل اطلاعات...")
    file_path = get_data_file_path()

    if not os.path.exists(file_path):
        print("فایل اطلاعات وجود نداشت؛ یک فایل خالی ساخته می‌شود.")
        return make_empty_data()

    try:
        file = open(file_path, "r", encoding="utf-8")
        file_text = file.read()
        file.close()
        data = json.loads(file_text)
    except Exception as error:
        print("خواندن فایل اطلاعات ممکن نشد:", error)
        return make_empty_data()

    if "users" not in data:
        data["users"] = []
    if "orders" not in data:
        data["orders"] = []
    if "tickets" not in data:
        data["tickets"] = []
    if "settings" not in data:
        data["settings"] = make_empty_data()["settings"]

    return data


def save_all_data():
    file_path = get_data_file_path()

    try:
        file_text = json.dumps(all_data, ensure_ascii=False, indent=2)
        file = open(file_path, "w", encoding="utf-8")
        file.write(file_text)
        file.close()
        print("اطلاعات با موفقیت ذخیره شد.")
        return True
    except Exception as error:
        print("خطا در ذخیرهٔ اطلاعات:", error)
        return False



def make_password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def find_user_by_name(user_name):
    wanted_name = user_name.strip().lower()
    for user in all_data["users"]:
        saved_name = user["username"].strip().lower()
        if saved_name == wanted_name:
            return user
    return None


def create_default_admin():
    admin_user = find_user_by_name("admin")
    if admin_user is not None:
        return

    print("حساب مدیر ساخته می‌شود...")
    new_admin = {
        "username": "admin",
        "password": make_password_hash("admin123"),
        "role": "admin",
        "language": "fa",
        "phone": "",
        "created_at": get_now_text(),
    }
    all_data["users"].append(new_admin)
    save_all_data()


def sign_up_user(user_name, password, repeated_password, phone_number):
    user_name = user_name.strip()
    phone_number = phone_number.strip()

    if len(user_name) < 3:
        return False, "username_short_err"
    if len(password) < 4:
        return False, "password_short_err"
    if password != repeated_password:
        return False, "password_mismatch_err"
    if find_user_by_name(user_name) is not None:
        return False, "username_taken_err"

    print("حساب جدید ساخته می‌شود:", user_name)
    new_user = {
        "username": user_name,
        "password": make_password_hash(password),
        "role": "customer",
        "language": config.current_language,
        "phone": phone_number,
        "created_at": get_now_text(),
    }
    all_data["users"].append(new_user)
    save_all_data()
    return True, ""


def check_login(user_name, password):
    user = find_user_by_name(user_name)
    if user is None:
        return None

    entered_hash = make_password_hash(password)
    if user["password"] != entered_hash:
        return None

    return user


def change_user_role(user_name, new_role):
    user = find_user_by_name(user_name)
    if user is None:
        return False, "not_found"

    if user["username"] == current_user["username"]:
        return False, "cant_change_self"

    admin_count = 0
    for one_user in all_data["users"]:
        if one_user["role"] == "admin":
            admin_count = admin_count + 1

    if user["role"] == "admin":
        if new_role == "customer":
            if admin_count <= 1:
                return False, "cant_remove_last_admin"

    user["role"] = new_role
    save_all_data()
    print("نقش کاربر", user_name, "به", new_role, "تغییر کرد.")
    return True, ""



def fetch_dollar_rate_from_internet():
    print("در حال گرفتن نرخ دلار از اینترنت...")

    try:
        from pahlavi import get_today_price

        price_text = get_today_price("USD")
        clean_text = price_text.replace(",", "")
        price_number = int(clean_text)

        print("نرخ دلار از اینترنت گرفته شد:", price_number)
        return price_number
    except Exception as error:
        print("گرفتن نرخ دلار ناموفق بود:", error)
        return 0


def set_dollar_rate(new_rate):
    global dollar_rate_toman, rate_source_text

    if new_rate > 0:
        dollar_rate_toman = new_rate
        rate_source_text = config.t("rate_internet")
        all_data["settings"]["dollar_rate"] = new_rate
        save_all_data()
    else:
        rate_source_text = config.t("rate_saved")

    return dollar_rate_toman



def calculate_distance_in_km(start_latitude, start_longitude, end_latitude, end_longitude):
    earth_radius = 6371.0

    start_lat_rad = math.radians(start_latitude)
    end_lat_rad = math.radians(end_latitude)
    delta_lat_rad = math.radians(end_latitude - start_latitude)
    delta_lng_rad = math.radians(end_longitude - start_longitude)

    part_one = math.sin(delta_lat_rad / 2) ** 2
    part_two = math.cos(start_lat_rad) * math.cos(end_lat_rad)
    part_three = math.sin(delta_lng_rad / 2) ** 2
    haversine_value = part_one + part_two * part_three

    angle = 2 * math.asin(math.sqrt(min(1.0, haversine_value)))
    distance = earth_radius * angle
    return distance


def calculate_cost(distance_in_km, weight_in_kg, parcel_type_key):
    base_cost = config.BASE_FEE_DOLLAR
    weight_cost = config.DOLLAR_PER_KILOGRAM * weight_in_kg

    distance_blocks = math.ceil(distance_in_km / 5)
    distance_cost = distance_blocks * config.DOLLAR_PER_FIVE_KILOMETERS

    factor = config.PARCEL_TYPE_FACTORS[parcel_type_key]
    total_dollar = (base_cost + weight_cost + distance_cost) * factor

    cost_details = {
        "base_cost": base_cost,
        "weight_cost": weight_cost,
        "distance_blocks": distance_blocks,
        "distance_cost": distance_cost,
        "factor": factor,
        "total_dollar": round(total_dollar, 2),
        "total_toman": int(round(total_dollar * dollar_rate_toman)),
    }
    return cost_details



def make_new_order_code():
    next_number = all_data["settings"]["next_order_number"]
    all_data["settings"]["next_order_number"] = next_number + 1
    return "PP-" + str(next_number)


def make_new_ticket_number():
    next_number = all_data["settings"]["next_ticket_number"]
    all_data["settings"]["next_ticket_number"] = next_number + 1
    return next_number


def find_order_by_code(order_code):
    wanted_code = order_code.strip().upper()
    for order in all_data["orders"]:
        if order["code"].upper() == wanted_code:
            return order
    return None


def find_ticket_by_number(ticket_number):
    for ticket in all_data["tickets"]:
        if ticket["number"] == ticket_number:
            return ticket
    return None


def create_new_order(start_point, end_point, weight_in_kg, parcel_type_key,
                     receiver_name, receiver_phone, notes):
    if start_point is None:
        return None, "need_origin"
    if end_point is None:
        return None, "need_destination"
    if weight_in_kg <= 0:
        return None, "weight_positive_err"

    distance = calculate_distance_in_km(
        start_point["latitude"], start_point["longitude"],
        end_point["latitude"], end_point["longitude"],
    )

    if distance < 1:
        return None, "same_point"

    cost = calculate_cost(distance, weight_in_kg, parcel_type_key)
    order_code = make_new_order_code()

    new_order = {
        "code": order_code,
        "username": current_user["username"],
        "origin_name": find_city_name(start_point["latitude"], start_point["longitude"]),
        "origin_latitude": start_point["latitude"],
        "origin_longitude": start_point["longitude"],
        "destination_name": find_city_name(end_point["latitude"], end_point["longitude"]),
        "destination_latitude": end_point["latitude"],
        "destination_longitude": end_point["longitude"],
        "distance_km": round(distance, 1),
        "weight_kg": weight_in_kg,
        "parcel_type": parcel_type_key,
        "receiver_name": receiver_name,
        "receiver_phone": receiver_phone,
        "notes": notes,
        "cost_dollar": cost["total_dollar"],
        "cost_toman": cost["total_toman"],
        "dollar_rate": dollar_rate_toman,
        "status": "registered",
        "created_at": get_now_text(),
        "history": [
            {"status": "registered", "date": get_now_text()},
        ],
    }

    all_data["orders"].append(new_order)
    save_all_data()
    print("مرسولهٔ جدید ثبت شد:", order_code)
    return order_code, ""


def add_status_to_history(order, new_status):
    order["status"] = new_status
    order["history"].append({"status": new_status, "date": get_now_text()})
    save_all_data()
    print("وضعیت مرسوله", order["code"], "به", new_status, "تغییر کرد.")


def find_city_name(latitude, longitude):
    closest_key = "custom_point"
    closest_distance = 9999

    for city in config.CITY_LIST:
        distance = calculate_distance_in_km(latitude, longitude,
                                            city["latitude"], city["longitude"])
        if distance < closest_distance:
            closest_distance = distance
            closest_key = city["name"]

    if closest_distance > 100:
        return "custom_point"

    return closest_key



def get_bot_answer(message_text):
    text = message_text.strip()

    if text == "":
        return config.t("bot_fallback")

    if "PP-" in text.upper():
        return get_bot_answer_about_tracking(text)

    if "سلام" in text or "درود" in text or "hello" in text.lower() or "hi" in text.lower():
        return config.t("bot_greeting")

    if "هزینه" in text or "قیمت" in text or "تعرفه" in text or "price" in text.lower() or "cost" in text.lower():
        return config.t("bot_price")

    if "رهگیری" in text or "کد" in text or "کجاست" in text or "track" in text.lower() or "where" in text.lower():
        return config.t("bot_tracking_help")

    if "تحویل" in text or "چند روز" in text or "زمان" in text or "delivery" in text.lower():
        return config.t("bot_delivery_time")

    if "تیکت" in text or "پشتیبان" in text or "ادمین" in text or "ticket" in text.lower() or "admin" in text.lower():
        return config.t("bot_ticket")

    if "لغو" in text or "cancel" in text.lower():
        return config.t("bot_cancel")

    if "ممنون" in text or "مرسی" in text or "تشکر" in text or "thanks" in text.lower():
        return config.t("bot_thanks")

    return config.t("bot_fallback")


def get_bot_answer_about_tracking(message_text):
    words = message_text.replace("؟", " ").replace("،", " ").split()

    for word in words:
        if word.upper().startswith("PP-"):
            order = find_order_by_code(word)
            if order is None:
                return config.t("bot_code_not_found").replace("{code}", word)

            origin_text = config.city_text(order["origin_name"])
            destination_text = config.city_text(order["destination_name"])
            status_text = config.status_text(order["status"])
            cost_text = format_toman(order["cost_toman"])

            answer = config.t("bot_code_found")
            answer = answer.replace("{code}", order["code"])
            answer = answer.replace("{status}", status_text)
            answer = answer.replace("{origin}", origin_text)
            answer = answer.replace("{destination}", destination_text)
            answer = answer.replace("{cost}", cost_text)
            return answer

    return config.t("bot_tracking_help")
