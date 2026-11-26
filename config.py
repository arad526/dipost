


DATA_FILE_NAME = "data.json"

MAP_IMAGE_FILE_NAME = "iran-provinces-web.png"



BASE_FEE_DOLLAR = 2.0
DOLLAR_PER_KILOGRAM = 1.5
DOLLAR_PER_FIVE_KILOMETERS = 1.0

DEFAULT_DOLLAR_RATE = 100000



PARCEL_TYPE_KEYS = ["letter", "parcel", "fragile", "express"]
PARCEL_TYPE_FACTORS = {
    "letter": 1.0,
    "parcel": 1.2,
    "fragile": 1.5,
    "express": 2.0,
}



STATUS_KEYS = ["registered", "in_transit", "delivered", "cancelled"]



TICKET_STATUS_KEYS = ["open", "answered", "closed"]



DARK_BLUE = "#0b2545"
MAIN_BLUE = "#2563eb"
LIGHT_BLUE = "#e8eefc"
BACKGROUND_GRAY = "#eef2f7"
WHITE = "#ffffff"
TEXT_COLOR = "#0f172a"
GRAY_TEXT = "#64748b"
GREEN = "#15803d"
RED = "#b91c1c"
BORDER_GRAY = "#d7e0ea"



TITLE_FONT = ("Tahoma", 24, "bold")
NORMAL_FONT = ("Tahoma", 13)
BOLD_FONT = ("Tahoma", 13, "bold")
SMALL_FONT = ("Tahoma", 11)
NUMBER_FONT = ("Tahoma", 20, "bold")



MAP_WIDTH = 520
MAP_HEIGHT = 480

MAP_MIN_LATITUDE = 25.0
MAP_MAX_LATITUDE = 40.0
MAP_MIN_LONGITUDE = 44.0
MAP_MAX_LONGITUDE = 64.0



CITY_LIST = [
    {"name": "tehran", "latitude": 35.69, "longitude": 51.39},
    {"name": "mashhad", "latitude": 36.26, "longitude": 59.61},
    {"name": "shiraz", "latitude": 29.59, "longitude": 52.58},
    {"name": "tabriz", "latitude": 38.08, "longitude": 46.29},
    {"name": "isfahan", "latitude": 32.65, "longitude": 51.67},
    {"name": "ahvaz", "latitude": 31.32, "longitude": 48.67},
    {"name": "rasht", "latitude": 37.28, "longitude": 49.59},
    {"name": "kerman", "latitude": 30.28, "longitude": 57.08},
]



current_language = "fa"



TEXTS = {
    "fa": {
        "app_name": "سامانهٔ پستی",
        "tagline": "ثبت و رهگیری مرسولهٔ پستی",
        "role_admin": "مدیر",
        "role_customer": "مشتری",
        "back": "برگشت",
        "send": "ارسال",
        "user": "کاربر",
        "toman_unit": "تومان",
        "dollar_unit": "دلار",
        "km_unit": "کیلومتر",
        "weight_unit": "کیلوگرم",

        "login_title": "ورود به سامانه",
        "username": "نام کاربری",
        "password": "رمز عبور",
        "username_placeholder": "نام کاربری خود را بنویسید",
        "password_placeholder": "رمز عبور",
        "login_button": "ورود",
        "no_account": "حساب ندارید؟ ثبت‌نام کنید",
        "admin_hint": "حساب مدیر: admin / admin123",
        "wrong_login": "نام کاربری یا رمز عبور اشتباه است.",
        "signup_title": "ساخت حساب جدید",
        "username_short_placeholder": "حداقل ۳ حرف",
        "password_short_placeholder": "حداقل ۴ حرف",
        "repeat_password": "تکرار رمز عبور",
        "repeat_placeholder": "رمز را دوباره بنویسید",
        "phone": "شمارهٔ تماس (اختیاری)",
        "phone_placeholder": "مثلاً 09120000000",
        "signup_button": "ساخت حساب",
        "back_to_login": "برگشت به ورود",
        "signup_done": "حساب شما ساخته شد. حالا وارد شوید.",
        "username_short_err": "نام کاربری باید حداقل ۳ حرف باشد.",
        "password_short_err": "رمز عبور باید حداقل ۴ حرف باشد.",
        "password_mismatch_err": "رمز عبور و تکرار آن یکسان نیستند.",
        "username_taken_err": "این نام کاربری قبلاً ثبت شده است.",
        "error_title": "خطا",
        "done_title": "انجام شد",

        "rate_label": "نرخ دلار",
        "rate_internet": "اینترنت",
        "rate_saved": "ذخیره‌شده",
        "rate_default": "پیش‌فرض",
        "logout": "خروج",
        "change_language": "English",

        "menu_customer": "منوی مشتری",
        "new_order": "ثبت سفارش",
        "my_orders": "مرسوله‌های من",
        "tracking": "رهگیری",
        "tickets": "تیکت‌ها",
        "chatbot": "چت‌بات",

        "order_title": "ثبت مرسولهٔ جدید",
        "map_title": "نقشهٔ ایران",
        "origin": "مبدأ",
        "destination": "مقصد",
        "pick_hint": "با کلیک روی نقشه، نقطهٔ انتخاب‌شده را مشخص کنید.",
        "weight": "وزن (کیلوگرم)",
        "weight_placeholder": "مثلاً 3.5",
        "type": "نوع مرسوله",
        "receiver": "نام گیرنده",
        "receiver_placeholder": "نام گیرنده",
        "phone_field": "شمارهٔ گیرنده",
        "notes": "توضیحات",
        "submit": "ثبت مرسوله",
        "cost_hint": "برای دیدن هزینه، مبدأ و مقصد را انتخاب کنید.",
        "distance_prefix": "مسافت",
        "not_selected": "هنوز انتخاب نشده",
        "cost_prefix": "هزینه",
        "weight_enter_err": "وزن را وارد کنید",
        "weight_positive_err": "وزن باید بیشتر از صفر باشد",
        "weight_number_err": "وزن مرسوله را به شکل عدد وارد کنید.",
        "order_done": "مرسوله با کد {code} ثبت شد.",
        "need_origin": "لطفاً مبدأ را روی نقشه انتخاب کنید.",
        "need_destination": "لطفاً مقصد را روی نقشه انتخاب کنید.",
        "same_point": "مبدأ و مقصد نمی‌توانند یکی باشند.",

        "my_orders_title": "مرسوله‌های من",
        "empty_orders": "هنوز مرسوله‌ای ثبت نکرده‌اید.",
        "route": "مسیر",
        "weight_kg": "کیلوگرم",
        "created_at": "تاریخ ثبت",

        "track_title": "رهگیری مرسوله",
        "code_placeholder": "مثلاً PP-1001",
        "track_button": "رهگیری",
        "track_empty": "کد رهگیری را وارد کنید.",
        "not_found": "مرسوله‌ای با این کد پیدا نشد.",
        "not_yours": "این مرسوله مربوط به حساب شما نیست.",
        "current_status": "وضعیت فعلی",
        "history_title": "تاریخچهٔ وضعیت",

        "tickets_title": "تیکت‌های پشتیبانی",
        "new_ticket": "تیکت جدید",
        "subject": "موضوع",
        "subject_placeholder": "موضوع تیکت",
        "message": "متن پیام",
        "create_ticket": "ثبت تیکت",
        "empty_tickets": "هنوز تیکتی ثبت نکرده‌اید.",
        "ticket_status": "وضعیت",
        "ticket_done": "تیکت شما با شماره {number} ثبت شد.",
        "ticket_subject_err": "موضوع تیکت را بنویسید.",
        "ticket_message_err": "متن پیام را بنویسید.",
        "sender_customer": "مشتری",
        "sender_admin": "ادمین",

        "chatbot_title": "چت‌بات پشتیبانی",
        "chatbot_placeholder": "سؤال خود را بنویسید...",
        "bot_name": "ربات",
        "you_name": "شما",
        "bot_welcome": "سلام! من دستیار پشتیبانی هستم. سوالتان را بنویسید.",

        "menu_admin": "منوی مدیر",
        "all_orders": "همهٔ مرسوله‌ها",
        "admin_tickets": "تیکت‌ها",
        "stats": "آمار",
        "users": "کاربران",

        "all_orders_title": "همهٔ مرسوله‌ها",
        "empty_orders_admin": "هنوز هیچ مرسوله‌ای ثبت نشده است.",
        "save_status": "ذخیره وضعیت",
        "status_updated": "وضعیت مرسوله {code} به «{status}» تغییر کرد.",
        "tickets_title_admin": "تیکت‌های مشتریان",
        "empty_tickets_admin": "هنوز تیکتی ثبت نشده است.",

        "stats_title": "آمار سامانه",
        "stat_customers": "تعداد مشتریان",
        "stat_orders": "تعداد مرسوله‌ها",
        "stat_tickets": "تعداد تیکت‌ها",
        "stat_revenue": "درآمد کل",
        "by_status": "توزیع وضعیت مرسوله‌ها",
        "orders_unit": "مرسوله",

        "users_title": "مدیریت کاربران",
        "change_role": "تغییر نقش",
        "save_role": "ذخیره نقش",
        "role_changed": "نقش کاربر {name} به «{role}» تغییر کرد.",
        "cant_change_self": "نمی‌توانید نقش خودتان را عوض کنید.",
        "cant_remove_last_admin": "نمی‌توانید آخرین مدیر را حذف کنید.",

        "status_registered": "ثبت شده",
        "status_in_transit": "در حال ارسال",
        "status_delivered": "تحویل شده",
        "status_cancelled": "لغو شده",

        "ticket_status_open": "باز",
        "ticket_status_answered": "پاسخ داده شده",
        "ticket_status_closed": "بسته",

        "parcel_letter": "نامه",
        "parcel_parcel": "بسته",
        "parcel_fragile": "شکستنی",
        "parcel_express": "فوری",

        "city_tehran": "تهران",
        "city_mashhad": "مشهد",
        "city_shiraz": "شیراز",
        "city_tabriz": "تبریز",
        "city_isfahan": "اصفهان",
        "city_ahvaz": "اهواز",
        "city_rasht": "رشت",
        "city_kerman": "کرمان",
        "custom_point": "نقطهٔ نقشه",

        "bot_greeting": "سلام! من دستیار پشتیبانی هستم. می‌توانم دربارهٔ هزینهٔ ارسال، رهگیری مرسوله، زمان تحویل و تغییر وضعیت کمکتان کنم.",
        "bot_price": "تعرفهٔ ما این‌طور است:\n• هزینهٔ ثابت: ۲ دلار\n• وزن: هر کیلوگرم ۱.۵ دلار\n• مسافت: هر ۵ کیلومتر ۱ دلار\n• جمع این‌ها در ضریب نوع مرسوله ضرب می‌شود.",
        "bot_tracking_help": "برای رهگیری، کد مرسوله (مثل PP-1001) را در صفحهٔ «رهگیری» وارد کنید یا همین‌جا کد را بنویسید.",
        "bot_delivery_time": "زمان تحویل: درون‌شهری ۱ تا ۲ روز کاری، بین‌شهری ۲ تا ۴ روز کاری و مرسولهٔ فوری ۲۴ ساعت.",
        "bot_ticket": "از منوی «تیکت‌ها» یک تیکت جدید ثبت کنید؛ مدیر در همان صفحه پاسخ می‌دهد.",
        "bot_cancel": "برای لغو مرسوله، از صفحهٔ «تیکت‌ها» تیکت بزنید و کد مرسوله را بنویسید تا مدیر آن را لغو کند.",
        "bot_thanks": "خواهش می‌کنم! اگر سؤال دیگری داشتید در خدمتم.",
        "bot_fallback": "سؤالتان را متوجه نشدم. می‌توانید دربارهٔ هزینهٔ ارسال، رهگیری مرسوله یا زمان تحویل بپرسید.",
        "bot_code_not_found": "مرسوله‌ای با کد «{code}» پیدا نشد. کد را بررسی کنید.",
        "bot_code_found": "مرسولهٔ {code}:\n• وضعیت: {status}\n• مسیر: {origin} به {destination}\n• هزینه: {cost}",
    },

    "en": {
        "app_name": "Postal System",
        "tagline": "Register and track parcels",
        "role_admin": "Admin",
        "role_customer": "Customer",
        "back": "Back",
        "send": "Send",
        "user": "User",
        "toman_unit": "Toman",
        "dollar_unit": "USD",
        "km_unit": "km",
        "weight_unit": "kg",

        "login_title": "Sign in",
        "username": "Username",
        "password": "Password",
        "username_placeholder": "Type your username",
        "password_placeholder": "Password",
        "login_button": "Sign in",
        "no_account": "No account? Sign up",
        "admin_hint": "Admin account: admin / admin123",
        "wrong_login": "Wrong username or password.",
        "signup_title": "Create an account",
        "username_short_placeholder": "at least 3 letters",
        "password_short_placeholder": "at least 4 letters",
        "repeat_password": "Repeat password",
        "repeat_placeholder": "Type it again",
        "phone": "Phone (optional)",
        "phone_placeholder": "e.g. 09120000000",
        "signup_button": "Create account",
        "back_to_login": "Back to sign in",
        "signup_done": "Your account was created. Now sign in.",
        "username_short_err": "Username must be at least 3 letters.",
        "password_short_err": "Password must be at least 4 letters.",
        "password_mismatch_err": "The passwords do not match.",
        "username_taken_err": "This username is already taken.",
        "error_title": "Error",
        "done_title": "Done",

        "rate_label": "USD rate",
        "rate_internet": "online",
        "rate_saved": "saved",
        "rate_default": "default",
        "logout": "Sign out",
        "change_language": "فارسی",

        "menu_customer": "Customer menu",
        "new_order": "New order",
        "my_orders": "My parcels",
        "tracking": "Tracking",
        "tickets": "Tickets",
        "chatbot": "Chatbot",

        "order_title": "New parcel",
        "map_title": "Map of Iran",
        "origin": "Origin",
        "destination": "Destination",
        "pick_hint": "Click on the map to choose the point.",
        "weight": "Weight (kg)",
        "weight_placeholder": "e.g. 3.5",
        "type": "Parcel type",
        "receiver": "Receiver name",
        "receiver_placeholder": "Receiver name",
        "phone_field": "Receiver phone",
        "notes": "Notes",
        "submit": "Register parcel",
        "cost_hint": "Pick origin and destination to see the price.",
        "distance_prefix": "Distance",
        "not_selected": "not selected yet",
        "cost_prefix": "Cost",
        "weight_enter_err": "Enter the weight",
        "weight_positive_err": "Weight must be more than zero",
        "weight_number_err": "Enter the weight as a number.",
        "order_done": "Parcel registered with code {code}.",
        "need_origin": "Please pick the origin on the map.",
        "need_destination": "Please pick the destination on the map.",
        "same_point": "Origin and destination cannot be the same.",

        "my_orders_title": "My parcels",
        "empty_orders": "You have no parcels yet.",
        "route": "Route",
        "weight_kg": "kg",
        "created_at": "Registered at",

        "track_title": "Track a parcel",
        "code_placeholder": "e.g. PP-1001",
        "track_button": "Track",
        "track_empty": "Enter a tracking code.",
        "not_found": "No parcel found with this code.",
        "not_yours": "This parcel is not on your account.",
        "current_status": "Current status",
        "history_title": "Status history",

        "tickets_title": "Support tickets",
        "new_ticket": "New ticket",
        "subject": "Subject",
        "subject_placeholder": "Ticket subject",
        "message": "Message",
        "create_ticket": "Create ticket",
        "empty_tickets": "You have no tickets yet.",
        "ticket_status": "Status",
        "ticket_done": "Your ticket #{number} was created.",
        "ticket_subject_err": "Write the ticket subject.",
        "ticket_message_err": "Write the message.",
        "sender_customer": "Customer",
        "sender_admin": "Admin",

        "chatbot_title": "Support chatbot",
        "chatbot_placeholder": "Type your question...",
        "bot_name": "Bot",
        "you_name": "You",
        "bot_welcome": "Hello! I am the support assistant. Write your question.",

        "menu_admin": "Admin menu",
        "all_orders": "All parcels",
        "admin_tickets": "Tickets",
        "stats": "Statistics",
        "users": "Users",

        "all_orders_title": "All parcels",
        "empty_orders_admin": "No parcels registered yet.",
        "save_status": "Save status",
        "status_updated": "Parcel {code} is now \"{status}\".",
        "tickets_title_admin": "Customer tickets",
        "empty_tickets_admin": "No tickets yet.",

        "stats_title": "System statistics",
        "stat_customers": "Customers",
        "stat_orders": "Parcels",
        "stat_tickets": "Tickets",
        "stat_revenue": "Total revenue",
        "by_status": "Status distribution",
        "orders_unit": "parcels",

        "users_title": "Manage users",
        "change_role": "Change role",
        "save_role": "Save role",
        "role_changed": "User {name} is now \"{role}\".",
        "cant_change_self": "You cannot change your own role.",
        "cant_remove_last_admin": "You cannot remove the last admin.",

        "status_registered": "Registered",
        "status_in_transit": "In transit",
        "status_delivered": "Delivered",
        "status_cancelled": "Cancelled",

        "ticket_status_open": "Open",
        "ticket_status_answered": "Answered",
        "ticket_status_closed": "Closed",

        "parcel_letter": "Letter",
        "parcel_parcel": "Parcel",
        "parcel_fragile": "Fragile",
        "parcel_express": "Express",

        "city_tehran": "Tehran",
        "city_mashhad": "Mashhad",
        "city_shiraz": "Shiraz",
        "city_tabriz": "Tabriz",
        "city_isfahan": "Isfahan",
        "city_ahvaz": "Ahvaz",
        "city_rasht": "Rasht",
        "city_kerman": "Kerman",
        "custom_point": "Map point",

        "bot_greeting": "Hello! I am the support assistant. I can help with shipping prices, tracking, delivery time and status changes.",
        "bot_price": "Our tariff:\n• Base fee: $2\n• Weight: $1.5 per kg\n• Distance: $1 per 5 km\n• The sum is multiplied by the parcel-type factor.",
        "bot_tracking_help": "To track, enter the parcel code (e.g. PP-1001) on the \"Tracking\" page, or write the code here.",
        "bot_delivery_time": "Delivery time: in-city 1-2 business days, inter-city 2-4 business days, express 24 hours.",
        "bot_ticket": "Open a new ticket from the \"Tickets\" menu; the admin replies there.",
        "bot_cancel": "To cancel a parcel, open a ticket and write the parcel code so the admin can cancel it.",
        "bot_thanks": "You're welcome! Ask me anything else.",
        "bot_fallback": "I didn't understand. You can ask about shipping cost, tracking, or delivery time.",
        "bot_code_not_found": "No parcel with code \"{code}\" was found. Check the code.",
        "bot_code_found": "Parcel {code}:\n• Status: {status}\n• Route: {origin} to {destination}\n• Cost: {cost}",
    },
}



def t(key):
    texts = TEXTS.get(current_language, TEXTS["fa"])
    return texts.get(key, TEXTS["fa"].get(key, key))


def set_language(language):
    global current_language
    if language in ("fa", "en"):
        current_language = language


def status_text(status_key):
    return t("status_" + status_key)


def parcel_type_text(parcel_key):
    return t("parcel_" + parcel_key)


def ticket_status_text(status_key):
    return t("ticket_status_" + status_key)


def city_text(city_key):
    return t("city_" + city_key)
