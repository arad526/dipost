
import os
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter

import config
import data



app_window = None
page_container = None
current_page_function = None
rate_label_widget = None

map_start_point = None
map_end_point = None
active_map_point_variable = None
map_canvas = None

order_weight_entry = None
order_parcel_type_menu = None
order_distance_label = None
order_cost_dollar_label = None
order_cost_toman_label = None

chat_messages = []



def change_page(page_function):
    global current_page_function
    current_page_function = page_function

    for child_widget in page_container.winfo_children():
        child_widget.destroy()

    page_function(page_container)


def clear_window():
    for child_widget in app_window.winfo_children():
        child_widget.destroy()



def create_card(parent_frame, width=None, height=None):
    card = customtkinter.CTkFrame(parent_frame, fg_color=config.WHITE, corner_radius=12)
    if width is not None:
        card.configure(width=width)
    if height is not None:
        card.configure(height=height)
    return card


def create_title_label(parent_frame, text):
    return customtkinter.CTkLabel(parent_frame, text=text, font=config.TITLE_FONT,
                                  text_color=config.TEXT_COLOR, anchor="e", justify="right")


def create_normal_label(parent_frame, text):
    return customtkinter.CTkLabel(parent_frame, text=text, font=config.NORMAL_FONT,
                                  text_color=config.TEXT_COLOR, anchor="e", justify="right")


def create_small_label(parent_frame, text):
    return customtkinter.CTkLabel(parent_frame, text=text, font=config.SMALL_FONT,
                                  text_color=config.GRAY_TEXT, anchor="e", justify="right")


def create_field_label(parent_frame, text):
    return customtkinter.CTkLabel(parent_frame, text=text, font=config.SMALL_FONT,
                                  text_color=config.GRAY_TEXT, anchor="e")


def create_text_entry(parent_frame, placeholder_text="", width=240):
    return customtkinter.CTkEntry(parent_frame, placeholder_text=placeholder_text,
                                  font=config.NORMAL_FONT, height=36, width=width,
                                  justify="right")



def get_map_image_path():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, config.MAP_IMAGE_FILE_NAME)


def load_map_background_image():
    try:
        from PIL import Image, ImageTk

        image = Image.open(get_map_image_path())
        image = image.convert("RGB")
        image = image.resize((config.MAP_WIDTH, config.MAP_HEIGHT))
        photo = ImageTk.PhotoImage(image)
        print("عکس نقشه بارگذاری شد.")
        return photo
    except Exception as error:
        print("عکس نقشه بارگذاری نشد؛ از شبکهٔ ساده استفاده می‌شود:", error)
        return None


def longitude_to_x(longitude):
    how_much_from_left = longitude - config.MAP_MIN_LONGITUDE
    total_range = config.MAP_MAX_LONGITUDE - config.MAP_MIN_LONGITUDE
    return int(how_much_from_left / total_range * config.MAP_WIDTH)


def latitude_to_y(latitude):
    how_much_from_top = config.MAP_MAX_LATITUDE - latitude
    total_range = config.MAP_MAX_LATITUDE - config.MAP_MIN_LATITUDE
    return int(how_much_from_top / total_range * config.MAP_HEIGHT)


def x_to_longitude(x_position):
    total_range = config.MAP_MAX_LONGITUDE - config.MAP_MIN_LONGITUDE
    longitude = config.MAP_MIN_LONGITUDE + (x_position / config.MAP_WIDTH) * total_range
    return round(longitude, 2)


def y_to_latitude(y_position):
    total_range = config.MAP_MAX_LATITUDE - config.MAP_MIN_LATITUDE
    latitude = config.MAP_MAX_LATITUDE - (y_position / config.MAP_HEIGHT) * total_range
    return round(latitude, 2)


def draw_map_grid():
    latitude = config.MAP_MIN_LATITUDE
    while latitude <= config.MAP_MAX_LATITUDE:
        y = latitude_to_y(latitude)
        map_canvas.create_line(0, y, config.MAP_WIDTH, y, fill=config.BORDER_GRAY, dash=(2, 5))
        latitude = latitude + 5

    longitude = config.MAP_MIN_LONGITUDE
    while longitude <= config.MAP_MAX_LONGITUDE:
        x = longitude_to_x(longitude)
        map_canvas.create_line(x, 0, x, config.MAP_HEIGHT, fill=config.BORDER_GRAY, dash=(2, 5))
        longitude = longitude + 5


def draw_map_cities():
    for city in config.CITY_LIST:
        x = longitude_to_x(city["longitude"])
        y = latitude_to_y(city["latitude"])
        city_name = config.city_text(city["name"])
        map_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=config.GRAY_TEXT, outline="")
        map_canvas.create_text(x + 7, y, text=city_name, anchor="w",
                               fill=config.DARK_BLUE, font=("Tahoma", 8, "bold"))


def draw_map_points():
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0

    if map_start_point is not None:
        start_x = longitude_to_x(map_start_point["longitude"])
        start_y = latitude_to_y(map_start_point["latitude"])
        map_canvas.create_oval(start_x - 7, start_y - 7, start_x + 7, start_y + 7,
                               fill=config.MAIN_BLUE, outline=config.WHITE, width=2)
        map_canvas.create_text(start_x, start_y - 16, text=config.t("origin"),
                               fill=config.MAIN_BLUE, font=("Tahoma", 10, "bold"))

    if map_end_point is not None:
        end_x = longitude_to_x(map_end_point["longitude"])
        end_y = latitude_to_y(map_end_point["latitude"])
        map_canvas.create_oval(end_x - 7, end_y - 7, end_x + 7, end_y + 7,
                               fill=config.GREEN, outline=config.WHITE, width=2)
        map_canvas.create_text(end_x, end_y - 16, text=config.t("destination"),
                               fill=config.GREEN, font=("Tahoma", 10, "bold"))

    if map_start_point is not None and map_end_point is not None:
        map_canvas.create_line(start_x, start_y, end_x, end_y,
                               fill=config.MAIN_BLUE, width=2, dash=(6, 4))


def draw_map():
    if map_canvas is None:
        return

    map_canvas.delete("all")

    background_photo = load_map_background_image()
    if background_photo is not None:
        map_canvas.background_photo = background_photo
        map_canvas.create_image(0, 0, image=background_photo, anchor="nw")
    else:
        draw_map_grid()

    draw_map_cities()
    draw_map_points()


def handle_map_click(event):
    global map_start_point, map_end_point

    clicked_longitude = x_to_longitude(event.x)
    clicked_latitude = y_to_latitude(event.y)
    clicked_point = {"latitude": clicked_latitude, "longitude": clicked_longitude}

    chosen_type = active_map_point_variable.get()

    if chosen_type == "start":
        map_start_point = clicked_point
        print("مبدأ انتخاب شد:", clicked_point)
    else:
        map_end_point = clicked_point
        print("مقصد انتخاب شد:", clicked_point)

    draw_map()
    refresh_cost_preview()


def clear_map_points():
    global map_start_point, map_end_point
    map_start_point = None
    map_end_point = None
    draw_map()
    refresh_cost_preview()



def get_parcel_key_from_menu(menu):
    for key in config.PARCEL_TYPE_KEYS:
        if menu.get() == config.parcel_type_text(key):
            return key
    return config.PARCEL_TYPE_KEYS[0]


def get_status_key_from_menu(menu):
    for key in config.STATUS_KEYS:
        if menu.get() == config.status_text(key):
            return key
    return config.STATUS_KEYS[0]


def refresh_cost_preview():
    if order_distance_label is None:
        return

    if map_start_point is None or map_end_point is None:
        order_distance_label.configure(
            text=config.t("distance_prefix") + ": " + config.t("not_selected"))
        order_cost_dollar_label.configure(text=config.t("cost_hint"))
        order_cost_toman_label.configure(text="")
        return

    distance = data.calculate_distance_in_km(
        map_start_point["latitude"], map_start_point["longitude"],
        map_end_point["latitude"], map_end_point["longitude"],
    )
    order_distance_label.configure(
        text=config.t("distance_prefix") + ": " + data.format_distance(distance))

    weight_text = order_weight_entry.get().strip()
    try:
        weight_in_kg = float(weight_text)
    except ValueError:
        order_cost_dollar_label.configure(text=config.t("weight_enter_err"))
        order_cost_toman_label.configure(text="")
        return

    if weight_in_kg <= 0:
        order_cost_dollar_label.configure(text=config.t("weight_positive_err"))
        order_cost_toman_label.configure(text="")
        return

    parcel_key = get_parcel_key_from_menu(order_parcel_type_menu)
    cost = data.calculate_cost(distance, weight_in_kg, parcel_key)

    order_cost_dollar_label.configure(
        text=config.t("cost_prefix") + ": " + data.format_dollar(cost["total_dollar"]))
    order_cost_toman_label.configure(text=data.format_toman(cost["total_toman"]))



def create_top_bar():
    top_bar = customtkinter.CTkFrame(app_window, fg_color=config.DARK_BLUE,
                                     corner_radius=0, height=64)
    top_bar.pack(fill="x")

    app_name_label = customtkinter.CTkLabel(top_bar, text=config.t("app_name"),
                                            font=("Tahoma", 18, "bold"), text_color=config.WHITE)
    app_name_label.pack(side="right", padx=18)

    global rate_label_widget
    rate_text = build_rate_text()
    rate_label_widget = customtkinter.CTkLabel(top_bar, text=rate_text,
                                               font=config.SMALL_FONT, text_color="#93a8c0")
    rate_label_widget.pack(side="left", padx=10)

    user_text = data.current_user["username"] + " - " + config.t("role_" + data.current_user["role"])
    user_label = customtkinter.CTkLabel(top_bar, text=user_text,
                                        font=config.SMALL_FONT, text_color=config.WHITE)
    user_label.pack(side="left", padx=10)

    language_button = customtkinter.CTkButton(top_bar, text=config.t("change_language"),
                                              width=80, height=32, fg_color="#173a63",
                                              hover_color="#22518a", font=config.SMALL_FONT,
                                              command=switch_language)
    language_button.pack(side="left", padx=8)

    logout_button = customtkinter.CTkButton(top_bar, text=config.t("logout"), width=70,
                                            height=32, fg_color="#173a63",
                                            hover_color="#22518a", font=config.SMALL_FONT,
                                            command=logout_and_show_login)
    logout_button.pack(side="left", padx=10)

    return top_bar


def build_rate_text():
    rate = f"{data.dollar_rate_toman:,} " + config.t("toman_unit")
    return config.t("rate_label") + ": " + rate + " (" + data.rate_source_text + ")"


def show_rate_on_top_bar():
    if rate_label_widget is None:
        return
    if rate_label_widget.winfo_exists():
        rate_label_widget.configure(text=build_rate_text())


def logout_and_show_login():
    print("کاربر خارج شد:", data.current_user["username"])
    data.current_user = {}
    show_login_page()


def switch_language():
    if config.current_language == "fa":
        config.set_language("en")
    else:
        config.set_language("fa")

    if data.current_user.get("username") is not None:
        data.current_user["language"] = config.current_language
        data.save_all_data()

    print("زبان برنامه به", config.current_language, "تغییر کرد.")

    page_that_was_open = current_page_function
    if data.current_user.get("role") == "admin":
        show_admin_panel()
    else:
        show_customer_panel()

    if page_that_was_open is not None:
        change_page(page_that_was_open)



def show_login_page():
    print("نمایش صفحهٔ ورود")
    clear_window()
    app_window.title(config.t("app_name") + " - " + config.t("login_title"))

    background = customtkinter.CTkFrame(app_window, fg_color=config.BACKGROUND_GRAY)
    background.pack(fill="both", expand=True)

    login_card = create_card(background)
    login_card.pack(expand=True)

    title = customtkinter.CTkLabel(login_card, text=config.t("app_name"),
                                   font=config.TITLE_FONT, text_color=config.DARK_BLUE)
    title.pack(pady=(30, 4), padx=30)

    subtitle = create_small_label(login_card, config.t("tagline"))
    subtitle.pack(pady=(0, 22), padx=30)

    user_name_label = create_field_label(login_card, config.t("username"))
    user_name_label.pack(fill="x", padx=30)
    user_name_entry = create_text_entry(login_card, config.t("username_placeholder"), width=300)
    user_name_entry.pack(fill="x", padx=30, pady=(4, 12))

    password_label = create_field_label(login_card, config.t("password"))
    password_label.pack(fill="x", padx=30)
    password_entry = customtkinter.CTkEntry(login_card, show="*", font=config.NORMAL_FONT,
                                            height=36, width=300, justify="right",
                                            placeholder_text=config.t("password_placeholder"))
    password_entry.pack(fill="x", padx=30, pady=(4, 18))

    error_label = customtkinter.CTkLabel(login_card, text="", font=config.SMALL_FONT,
                                         text_color=config.RED)
    error_label.pack(pady=(0, 6))

    def handle_login_click():
        entered_name = user_name_entry.get()
        entered_password = password_entry.get()
        user = data.check_login(entered_name, entered_password)

        if user is None:
            error_label.configure(text=config.t("wrong_login"))
            print("ورود ناموفق برای:", entered_name)
            return

        print("ورود موفق:", user["username"])
        open_panel_for_user(user)

    login_button = customtkinter.CTkButton(login_card, text=config.t("login_button"),
                                           height=42, font=config.BOLD_FONT,
                                           fg_color=config.MAIN_BLUE, hover_color="#1e40af",
                                           command=handle_login_click)
    login_button.pack(fill="x", padx=30, pady=(0, 10))

    sign_up_button = customtkinter.CTkButton(login_card, text=config.t("no_account"),
                                             height=34, fg_color="transparent",
                                             text_color=config.MAIN_BLUE, font=config.SMALL_FONT,
                                             hover_color=config.LIGHT_BLUE,
                                             command=show_sign_up_page)
    sign_up_button.pack(fill="x", padx=30, pady=(0, 8))

    hint_label = create_small_label(login_card, config.t("admin_hint"))
    hint_label.pack(pady=(0, 24), padx=30)

    user_name_entry.bind("<Return>", lambda event: handle_login_click())
    password_entry.bind("<Return>", lambda event: handle_login_click())



def show_sign_up_page():
    print("نمایش صفحهٔ ثبت‌نام")
    clear_window()
    app_window.title(config.t("app_name") + " - " + config.t("signup_title"))

    background = customtkinter.CTkFrame(app_window, fg_color=config.BACKGROUND_GRAY)
    background.pack(fill="both", expand=True)

    sign_up_card = create_card(background)
    sign_up_card.pack(expand=True)

    title = customtkinter.CTkLabel(sign_up_card, text=config.t("signup_title"),
                                   font=config.TITLE_FONT, text_color=config.DARK_BLUE)
    title.pack(pady=(26, 16), padx=30)

    user_name_label = create_field_label(sign_up_card, config.t("username"))
    user_name_label.pack(fill="x", padx=30)
    user_name_entry = create_text_entry(sign_up_card, config.t("username_short_placeholder"), width=300)
    user_name_entry.pack(fill="x", padx=30, pady=(4, 10))

    password_label = create_field_label(sign_up_card, config.t("password"))
    password_label.pack(fill="x", padx=30)
    password_entry = customtkinter.CTkEntry(sign_up_card, show="*", font=config.NORMAL_FONT,
                                            height=36, width=300, justify="right",
                                            placeholder_text=config.t("password_short_placeholder"))
    password_entry.pack(fill="x", padx=30, pady=(4, 10))

    repeat_label = create_field_label(sign_up_card, config.t("repeat_password"))
    repeat_label.pack(fill="x", padx=30)
    repeat_entry = customtkinter.CTkEntry(sign_up_card, show="*", font=config.NORMAL_FONT,
                                          height=36, width=300, justify="right",
                                          placeholder_text=config.t("repeat_placeholder"))
    repeat_entry.pack(fill="x", padx=30, pady=(4, 10))

    phone_label = create_field_label(sign_up_card, config.t("phone"))
    phone_label.pack(fill="x", padx=30)
    phone_entry = create_text_entry(sign_up_card, config.t("phone_placeholder"), width=300)
    phone_entry.pack(fill="x", padx=30, pady=(4, 12))

    error_label = customtkinter.CTkLabel(sign_up_card, text="", font=config.SMALL_FONT,
                                         text_color=config.RED)
    error_label.pack(pady=(0, 6))

    def handle_sign_up_click():
        is_done, error_key = data.sign_up_user(
            user_name_entry.get(),
            password_entry.get(),
            repeat_entry.get(),
            phone_entry.get(),
        )

        if not is_done:
            error_label.configure(text=config.t(error_key))
            return

        messagebox.showinfo(config.t("done_title"), config.t("signup_done"))
        show_login_page()

    sign_up_button = customtkinter.CTkButton(sign_up_card, text=config.t("signup_button"),
                                             height=42, font=config.BOLD_FONT,
                                             fg_color=config.MAIN_BLUE, hover_color="#1e40af",
                                             command=handle_sign_up_click)
    sign_up_button.pack(fill="x", padx=30, pady=(0, 8))

    back_button = customtkinter.CTkButton(sign_up_card, text=config.t("back_to_login"),
                                          height=32, fg_color="transparent",
                                          text_color=config.MAIN_BLUE, font=config.SMALL_FONT,
                                          hover_color=config.LIGHT_BLUE,
                                          command=show_login_page)
    back_button.pack(fill="x", padx=30, pady=(0, 20))



def open_panel_for_user(user):
    global map_start_point, map_end_point

    data.current_user = user
    config.set_language(user.get("language", "fa"))

    map_start_point = None
    map_end_point = None
    chat_messages.clear()

    if user["role"] == "admin":
        show_admin_panel()
    else:
        show_customer_panel()



def show_customer_panel():
    print("نمایش پنل مشتری")
    clear_window()
    app_window.title(config.t("app_name") + " - " + config.t("role_customer"))

    create_top_bar()

    body = customtkinter.CTkFrame(app_window, fg_color=config.BACKGROUND_GRAY)
    body.pack(fill="both", expand=True)

    menu_frame = create_card(body, width=180)
    menu_frame.pack(side="right", fill="y", padx=(12, 6), pady=12)
    menu_frame.pack_propagate(False)

    menu_title = customtkinter.CTkLabel(menu_frame, text=config.t("menu_customer"),
                                        font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    menu_title.pack(pady=(16, 10))

    new_order_button = customtkinter.CTkButton(menu_frame, text=config.t("new_order"), height=38,
                                               font=config.NORMAL_FONT, fg_color=config.MAIN_BLUE,
                                               hover_color="#1e40af",
                                               command=lambda: change_page(show_new_order_page))
    new_order_button.pack(fill="x", padx=12, pady=4)

    my_orders_button = customtkinter.CTkButton(menu_frame, text=config.t("my_orders"), height=38,
                                               font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                               text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                               command=lambda: change_page(show_my_orders_page))
    my_orders_button.pack(fill="x", padx=12, pady=4)

    tracking_button = customtkinter.CTkButton(menu_frame, text=config.t("tracking"), height=38,
                                              font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                              text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                              command=lambda: change_page(show_tracking_page))
    tracking_button.pack(fill="x", padx=12, pady=4)

    tickets_button = customtkinter.CTkButton(menu_frame, text=config.t("tickets"), height=38,
                                             font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                             text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                             command=lambda: change_page(show_tickets_page))
    tickets_button.pack(fill="x", padx=12, pady=4)

    chat_button = customtkinter.CTkButton(menu_frame, text=config.t("chatbot"), height=38,
                                          font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                          text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                          command=lambda: change_page(show_chatbot_page))
    chat_button.pack(fill="x", padx=12, pady=4)

    global page_container
    page_container = customtkinter.CTkFrame(body, fg_color=config.BACKGROUND_GRAY)
    page_container.pack(side="right", fill="both", expand=True, padx=(0, 12), pady=12)

    change_page(show_new_order_page)



def show_new_order_page(parent_frame):
    global order_weight_entry, order_parcel_type_menu
    global order_distance_label, order_cost_dollar_label, order_cost_toman_label
    global map_canvas, active_map_point_variable

    title = create_title_label(parent_frame, config.t("order_title"))
    title.pack(anchor="e", pady=(0, 8))

    columns = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
    columns.pack(fill="both", expand=True)

    map_card = create_card(columns)
    map_card.pack(side="right", fill="both", expand=True, padx=(0, 6))

    map_title = customtkinter.CTkLabel(map_card, text=config.t("map_title"),
                                       font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    map_title.pack(anchor="e", padx=14, pady=(12, 4))

    map_hint = create_small_label(map_card, config.t("pick_hint"))
    map_hint.pack(anchor="e", padx=14)

    active_map_point_variable = tk.StringVar(value="start")
    radio_frame = customtkinter.CTkFrame(map_card, fg_color="transparent")
    radio_frame.pack(anchor="e", padx=14, pady=6)

    start_radio = customtkinter.CTkRadioButton(radio_frame, text=config.t("origin"),
                                               variable=active_map_point_variable,
                                               value="start", font=config.SMALL_FONT)
    start_radio.pack(side="right", padx=6)

    end_radio = customtkinter.CTkRadioButton(radio_frame, text=config.t("destination"),
                                             variable=active_map_point_variable,
                                             value="end", font=config.SMALL_FONT)
    end_radio.pack(side="right", padx=6)

    map_canvas = tk.Canvas(map_card, width=config.MAP_WIDTH, height=config.MAP_HEIGHT,
                           bg=config.WHITE, highlightthickness=0)
    map_canvas.pack(padx=12, pady=6)
    map_canvas.bind("<Button-1>", handle_map_click)

    distance_label = customtkinter.CTkLabel(
        map_card, text=config.t("distance_prefix") + ": " + config.t("not_selected"),
        font=config.BOLD_FONT, text_color=config.MAIN_BLUE)
    distance_label.pack(anchor="e", padx=14, pady=(0, 10))
    order_distance_label = distance_label

    form_card = create_card(columns)
    form_card.pack(side="right", fill="y", padx=(6, 0))

    weight_label = create_field_label(form_card, config.t("weight"))
    weight_label.pack(fill="x", padx=16, pady=(14, 2))
    order_weight_entry = customtkinter.CTkEntry(form_card, font=config.NORMAL_FONT,
                                                height=34, width=240, justify="right",
                                                placeholder_text=config.t("weight_placeholder"))
    order_weight_entry.pack(fill="x", padx=16)
    order_weight_entry.bind("<KeyRelease>", lambda event: refresh_cost_preview())

    type_label = create_field_label(form_card, config.t("type"))
    type_label.pack(fill="x", padx=16, pady=(10, 2))
    type_values = []
    for key in config.PARCEL_TYPE_KEYS:
        type_values.append(config.parcel_type_text(key))
    order_parcel_type_menu = customtkinter.CTkOptionMenu(
        form_card, values=type_values, font=config.SMALL_FONT, height=34, width=240,
        command=lambda chosen_value: refresh_cost_preview())
    order_parcel_type_menu.pack(fill="x", padx=16)

    receiver_label = create_field_label(form_card, config.t("receiver"))
    receiver_label.pack(fill="x", padx=16, pady=(10, 2))
    receiver_entry = create_text_entry(form_card, config.t("receiver_placeholder"))
    receiver_entry.pack(fill="x", padx=16)

    phone_label = create_field_label(form_card, config.t("phone_field"))
    phone_label.pack(fill="x", padx=16, pady=(10, 2))
    phone_entry = create_text_entry(form_card, "09xxxxxxxxx")
    phone_entry.pack(fill="x", padx=16)

    notes_label = create_field_label(form_card, config.t("notes"))
    notes_label.pack(fill="x", padx=16, pady=(10, 2))
    notes_box = customtkinter.CTkTextbox(form_card, height=60, width=240, font=config.SMALL_FONT)
    notes_box.pack(fill="x", padx=16)

    cost_card = customtkinter.CTkFrame(form_card, fg_color=config.LIGHT_BLUE, corner_radius=10)
    cost_card.pack(fill="x", padx=16, pady=12)

    order_cost_dollar_label = customtkinter.CTkLabel(cost_card, text=config.t("cost_hint"),
                                                     font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    order_cost_dollar_label.pack(anchor="e", padx=12, pady=(10, 2))

    order_cost_toman_label = customtkinter.CTkLabel(cost_card, text="",
                                                    font=("Tahoma", 15, "bold"),
                                                    text_color=config.MAIN_BLUE)
    order_cost_toman_label.pack(anchor="e", padx=12, pady=(0, 10))

    def handle_submit_click():
        weight_text_value = order_weight_entry.get().strip()

        try:
            weight_in_kg = float(weight_text_value)
        except ValueError:
            messagebox.showerror(config.t("error_title"), config.t("weight_number_err"))
            return

        parcel_key = get_parcel_key_from_menu(order_parcel_type_menu)
        order_code, error_key = data.create_new_order(
            map_start_point, map_end_point, weight_in_kg, parcel_key,
            receiver_entry.get().strip(), phone_entry.get().strip(),
            notes_box.get("1.0", "end").strip(),
        )

        if order_code is None:
            messagebox.showerror(config.t("error_title"), config.t(error_key))
            return

        messagebox.showinfo(config.t("done_title"),
                            config.t("order_done").replace("{code}", order_code))
        clear_map_points()
        order_weight_entry.delete(0, "end")
        notes_box.delete("1.0", "end")

    submit_button = customtkinter.CTkButton(form_card, text=config.t("submit"), height=42,
                                            font=config.BOLD_FONT, fg_color=config.MAIN_BLUE,
                                            hover_color="#1e40af",
                                            command=handle_submit_click)
    submit_button.pack(fill="x", padx=16, pady=(0, 14))

    draw_map()
    refresh_cost_preview()



def show_my_orders_page(parent_frame):
    print("نمایش صفحهٔ مرسوله‌های من")

    title = create_title_label(parent_frame, config.t("my_orders_title"))
    title.pack(anchor="e", pady=(0, 8))

    my_orders = []
    for order in data.all_data["orders"]:
        if order["username"] == data.current_user["username"]:
            my_orders.append(order)

    if len(my_orders) == 0:
        empty_label = create_normal_label(parent_frame, config.t("empty_orders"))
        empty_label.pack(anchor="e", pady=20)
        return

    list_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True)

    for order in my_orders:
        create_order_card(list_frame, order, show_admin_buttons=False)


def create_order_card(parent_frame, order, show_admin_buttons):
    card = create_card(parent_frame)
    card.pack(fill="x", pady=6, padx=4)

    first_line = order["code"] + "   |   " + config.status_text(order["status"])
    first_label = customtkinter.CTkLabel(card, text=first_line, font=config.BOLD_FONT,
                                         text_color=config.DARK_BLUE, anchor="e")
    first_label.pack(anchor="e", padx=14, pady=(10, 2))

    route_text = config.t("route") + ": " + config.city_text(order["origin_name"]) + " → " \
        + config.city_text(order["destination_name"])
    route_label = create_normal_label(card, route_text)
    route_label.pack(anchor="e", padx=14)

    detail_text = (
        data.format_distance(order["distance_km"])
        + "   |   " + data.format_weight(order["weight_kg"])
        + "   |   " + config.parcel_type_text(order["parcel_type"])
    )
    detail_label = customtkinter.CTkLabel(card, text=detail_text, font=config.SMALL_FONT,
                                          text_color=config.GRAY_TEXT, anchor="e")
    detail_label.pack(anchor="e", padx=14)

    price_text = data.format_dollar(order["cost_dollar"]) + "  /  " + data.format_toman(order["cost_toman"])
    price_label = customtkinter.CTkLabel(card, text=price_text, font=config.BOLD_FONT,
                                         text_color=config.MAIN_BLUE, anchor="e")
    price_label.pack(anchor="e", padx=14)

    date_label = create_small_label(card, config.t("created_at") + ": " + order["created_at"])
    date_label.pack(anchor="e", padx=14, pady=(0, 10))

    if show_admin_buttons:
        buttons_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(anchor="e", padx=14, pady=(0, 12))

        status_values = []
        for key in config.STATUS_KEYS:
            status_values.append(config.status_text(key))
        status_menu = customtkinter.CTkOptionMenu(buttons_frame, values=status_values,
                                                  width=130, height=30, font=config.SMALL_FONT)
        status_menu.set(config.status_text(order["status"]))
        status_menu.pack(side="right", padx=4)

        save_button = customtkinter.CTkButton(
            buttons_frame, text=config.t("save_status"), width=110, height=30,
            font=config.SMALL_FONT, fg_color=config.MAIN_BLUE, hover_color="#1e40af",
            command=lambda order_to_change=order, menu_widget=status_menu:
                save_new_status(order_to_change, menu_widget))
        save_button.pack(side="right", padx=4)


def save_new_status(order, status_menu):
    new_status = get_status_key_from_menu(status_menu)
    if order["status"] == new_status:
        return

    data.add_status_to_history(order, new_status)
    messagebox.showinfo(config.t("done_title"),
                        config.t("status_updated")
                        .replace("{code}", order["code"])
                        .replace("{status}", config.status_text(new_status)))
    change_page(show_all_orders_page)



def show_tracking_page(parent_frame):
    print("نمایش صفحهٔ رهگیری")

    title = create_title_label(parent_frame, config.t("track_title"))
    title.pack(anchor="e", pady=(0, 8))

    search_card = create_card(parent_frame)
    search_card.pack(fill="x", pady=(0, 10))

    search_row = customtkinter.CTkFrame(search_card, fg_color="transparent")
    search_row.pack(fill="x", padx=14, pady=12)

    code_entry = customtkinter.CTkEntry(search_row, font=config.NORMAL_FONT, height=36,
                                        width=200, justify="right",
                                        placeholder_text=config.t("code_placeholder"))
    code_entry.pack(side="right", padx=(0, 8))

    result_card = create_card(parent_frame)
    result_card.pack(fill="both", expand=True)

    result_label = customtkinter.CTkLabel(result_card, text=config.t("track_empty"),
                                          font=config.NORMAL_FONT, text_color=config.GRAY_TEXT,
                                          anchor="e", justify="right")
    result_label.pack(anchor="e", padx=16, pady=16)

    def handle_track_click():
        order = data.find_order_by_code(code_entry.get())

        if order is None:
            result_label.configure(text=config.t("not_found"), text_color=config.RED)
            return

        if order["username"] != data.current_user["username"]:
            result_label.configure(text=config.t("not_yours"), text_color=config.RED)
            return

        text_lines = []
        text_lines.append(order["code"])
        text_lines.append(config.t("current_status") + ": " + config.status_text(order["status"]))
        text_lines.append(config.t("route") + ": " + config.city_text(order["origin_name"])
                          + " → " + config.city_text(order["destination_name"]))
        text_lines.append(data.format_distance(order["distance_km"]))
        text_lines.append(config.t("receiver") + ": " + order["receiver_name"])
        text_lines.append(data.format_toman(order["cost_toman"]))
        text_lines.append("")
        text_lines.append(config.t("history_title") + ":")

        for history_item in order["history"]:
            text_lines.append("• " + config.status_text(history_item["status"])
                              + " - " + history_item["date"])

        full_text = ""
        for line in text_lines:
            full_text = full_text + line + "\n"

        result_label.configure(text=full_text, text_color=config.TEXT_COLOR)

    track_button = customtkinter.CTkButton(search_row, text=config.t("track_button"), width=100,
                                           height=36, font=config.BOLD_FONT,
                                           fg_color=config.MAIN_BLUE, hover_color="#1e40af",
                                           command=handle_track_click)
    track_button.pack(side="right")



def show_tickets_page(parent_frame):
    print("نمایش صفحهٔ تیکت‌ها")

    title = create_title_label(parent_frame, config.t("tickets_title"))
    title.pack(anchor="e", pady=(0, 8))

    new_ticket_card = create_card(parent_frame)
    new_ticket_card.pack(fill="x", pady=(0, 10))

    form_title = customtkinter.CTkLabel(new_ticket_card, text=config.t("new_ticket"),
                                        font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    form_title.pack(anchor="e", padx=14, pady=(12, 4))

    subject_label = create_field_label(new_ticket_card, config.t("subject"))
    subject_label.pack(fill="x", padx=14)
    subject_entry = create_text_entry(new_ticket_card, config.t("subject_placeholder"))
    subject_entry.pack(fill="x", padx=14, pady=(2, 8))

    message_label = create_field_label(new_ticket_card, config.t("message"))
    message_label.pack(fill="x", padx=14)
    message_box = customtkinter.CTkTextbox(new_ticket_card, height=60, font=config.SMALL_FONT)
    message_box.pack(fill="x", padx=14, pady=(2, 8))

    def handle_create_ticket_click():
        subject_text = subject_entry.get().strip()
        message_text = message_box.get("1.0", "end").strip()

        if subject_text == "":
            messagebox.showerror(config.t("error_title"), config.t("ticket_subject_err"))
            return
        if message_text == "":
            messagebox.showerror(config.t("error_title"), config.t("ticket_message_err"))
            return

        ticket_number = data.make_new_ticket_number()
        new_ticket = {
            "number": ticket_number,
            "username": data.current_user["username"],
            "subject": subject_text,
            "status": "open",
            "created_at": data.get_now_text(),
            "messages": [
                {"sender": "customer", "text": message_text, "date": data.get_now_text()},
            ],
        }
        data.all_data["tickets"].append(new_ticket)
        data.save_all_data()
        print("تیکت جدید ثبت شد:", ticket_number)

        messagebox.showinfo(config.t("done_title"),
                            config.t("ticket_done").replace("{number}", str(ticket_number)))
        change_page(show_tickets_page)

    create_ticket_button = customtkinter.CTkButton(new_ticket_card, text=config.t("create_ticket"),
                                                   height=36, font=config.BOLD_FONT,
                                                   fg_color=config.MAIN_BLUE,
                                                   hover_color="#1e40af",
                                                   command=handle_create_ticket_click)
    create_ticket_button.pack(fill="x", padx=14, pady=(0, 12))

    my_tickets = []
    for ticket in data.all_data["tickets"]:
        if ticket["username"] == data.current_user["username"]:
            my_tickets.append(ticket)

    if len(my_tickets) == 0:
        empty_label = create_normal_label(parent_frame, config.t("empty_tickets"))
        empty_label.pack(anchor="e", pady=10)
        return

    list_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True)

    for ticket in my_tickets:
        ticket_text = ("#" + str(ticket["number"]) + "   " + ticket["subject"]
                       + "   (" + config.ticket_status_text(ticket["status"]) + ")")
        ticket_button = customtkinter.CTkButton(
            list_frame, text=ticket_text, height=40, font=config.NORMAL_FONT,
            fg_color=config.WHITE, text_color=config.DARK_BLUE, hover_color=config.LIGHT_BLUE,
            anchor="e", command=lambda number=ticket["number"]: open_ticket_conversation(number))
        ticket_button.pack(fill="x", pady=4, padx=4)


def open_ticket_conversation(ticket_number):
    ticket = data.find_ticket_by_number(ticket_number)
    if ticket is None:
        messagebox.showerror(config.t("error_title"), config.t("not_found"))
        return

    print("باز کردن تیکت شماره", ticket_number)

    clear_window()
    create_top_bar()

    body = customtkinter.CTkFrame(app_window, fg_color=config.BACKGROUND_GRAY)
    body.pack(fill="both", expand=True, padx=14, pady=14)

    header = customtkinter.CTkFrame(body, fg_color="transparent")
    header.pack(fill="x")

    title_text = "#" + str(ticket["number"]) + " - " + ticket["subject"]
    title_label = customtkinter.CTkLabel(header, text=title_text, font=config.BOLD_FONT,
                                         text_color=config.DARK_BLUE)
    title_label.pack(side="right")

    back_button = customtkinter.CTkButton(header, text=config.t("back"), width=80, height=30,
                                          font=config.SMALL_FONT, fg_color=config.LIGHT_BLUE,
                                          text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                          command=go_back_to_ticket_list)
    back_button.pack(side="left")

    status_label = customtkinter.CTkLabel(header, text=config.t("ticket_status") + ": "
                                          + config.ticket_status_text(ticket["status"]),
                                          font=config.SMALL_FONT, text_color=config.GRAY_TEXT)
    status_label.pack(side="left", padx=10)

    messages_frame = customtkinter.CTkScrollableFrame(body, fg_color=config.WHITE, corner_radius=12)
    messages_frame.pack(fill="both", expand=True, pady=10)

    for message in ticket["messages"]:
        create_message_bubble(messages_frame, message["sender"], message["text"], message["date"])

    send_frame = customtkinter.CTkFrame(body, fg_color="transparent")
    send_frame.pack(fill="x")

    reply_box = customtkinter.CTkTextbox(send_frame, height=60, font=config.SMALL_FONT)
    reply_box.pack(side="right", fill="x", expand=True, padx=(0, 8))

    def handle_send_click():
        reply_text = reply_box.get("1.0", "end").strip()
        if reply_text == "":
            return

        ticket["messages"].append({
            "sender": data.current_user["role"],
            "text": reply_text,
            "date": data.get_now_text(),
        })

        if data.current_user["role"] == "admin":
            ticket["status"] = "answered"
        else:
            ticket["status"] = "open"

        data.save_all_data()
        print("پیام جدید در تیکت", ticket["number"], "ثبت شد.")
        open_ticket_conversation(ticket["number"])

    send_button = customtkinter.CTkButton(send_frame, text=config.t("send"), width=90, height=60,
                                          font=config.BOLD_FONT, fg_color=config.MAIN_BLUE,
                                          hover_color="#1e40af", command=handle_send_click)
    send_button.pack(side="left")


def create_message_bubble(parent_frame, sender_key, message_text, message_date):
    if sender_key == "admin":
        bubble_color = config.LIGHT_BLUE
    else:
        bubble_color = config.BACKGROUND_GRAY

    bubble = customtkinter.CTkFrame(parent_frame, fg_color=bubble_color, corner_radius=10)
    bubble.pack(fill="x", pady=5, padx=6)

    if sender_key == "bot":
        sender_name = config.t("bot_name")
    elif sender_key == "admin":
        sender_name = config.t("sender_admin")
    else:
        sender_name = config.t("sender_customer")

    if message_date == "":
        sender_text = sender_name
    else:
        sender_text = sender_name + " - " + message_date

    sender_label = customtkinter.CTkLabel(bubble, text=sender_text,
                                          font=("Tahoma", 9), text_color=config.GRAY_TEXT,
                                          anchor="e")
    sender_label.pack(anchor="e", padx=10, pady=(6, 0))

    text_label = customtkinter.CTkLabel(bubble, text=message_text, font=config.NORMAL_FONT,
                                        text_color=config.TEXT_COLOR, anchor="e",
                                        justify="right", wraplength=520)
    text_label.pack(anchor="e", padx=10, pady=(0, 8))


def go_back_to_ticket_list():
    if data.current_user["role"] == "admin":
        show_admin_panel()
        change_page(show_all_tickets_page)
    else:
        show_customer_panel()
        change_page(show_tickets_page)



def show_chatbot_page(parent_frame):
    print("نمایش صفحهٔ چت‌بات")

    title = create_title_label(parent_frame, config.t("chatbot_title"))
    title.pack(anchor="e", pady=(0, 8))

    chat_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color=config.WHITE,
                                                  corner_radius=12)
    chat_frame.pack(fill="both", expand=True, pady=(0, 10))

    if len(chat_messages) == 0:
        chat_messages.append(("bot", config.t("bot_welcome")))

    for sender, text in chat_messages:
        create_message_bubble(chat_frame, sender, text, "")

    input_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.pack(fill="x")

    question_entry = customtkinter.CTkEntry(input_frame, font=config.NORMAL_FONT, height=38,
                                            justify="right",
                                            placeholder_text=config.t("chatbot_placeholder"))
    question_entry.pack(side="right", fill="x", expand=True, padx=(0, 8))

    def handle_send_question():
        question_text = question_entry.get().strip()
        if question_text == "":
            return

        print("سؤال کاربر:", question_text)
        answer_text = data.get_bot_answer(question_text)

        chat_messages.append(("customer", question_text))
        chat_messages.append(("bot", answer_text))

        change_page(show_chatbot_page)

    send_button = customtkinter.CTkButton(input_frame, text=config.t("send"), width=90, height=38,
                                          font=config.BOLD_FONT, fg_color=config.MAIN_BLUE,
                                          hover_color="#1e40af", command=handle_send_question)
    send_button.pack(side="left")



def show_admin_panel():
    print("نمایش پنل مدیر")
    clear_window()
    app_window.title(config.t("app_name") + " - " + config.t("role_admin"))

    create_top_bar()

    body = customtkinter.CTkFrame(app_window, fg_color=config.BACKGROUND_GRAY)
    body.pack(fill="both", expand=True)

    menu_frame = create_card(body, width=180)
    menu_frame.pack(side="right", fill="y", padx=(12, 6), pady=12)
    menu_frame.pack_propagate(False)

    menu_title = customtkinter.CTkLabel(menu_frame, text=config.t("menu_admin"),
                                        font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    menu_title.pack(pady=(16, 10))

    orders_button = customtkinter.CTkButton(menu_frame, text=config.t("all_orders"), height=38,
                                            font=config.NORMAL_FONT, fg_color=config.MAIN_BLUE,
                                            hover_color="#1e40af",
                                            command=lambda: change_page(show_all_orders_page))
    orders_button.pack(fill="x", padx=12, pady=4)

    tickets_button = customtkinter.CTkButton(menu_frame, text=config.t("admin_tickets"), height=38,
                                             font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                             text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                             command=lambda: change_page(show_all_tickets_page))
    tickets_button.pack(fill="x", padx=12, pady=4)

    stats_button = customtkinter.CTkButton(menu_frame, text=config.t("stats"), height=38,
                                           font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                           text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                           command=lambda: change_page(show_statistics_page))
    stats_button.pack(fill="x", padx=12, pady=4)

    users_button = customtkinter.CTkButton(menu_frame, text=config.t("users"), height=38,
                                           font=config.NORMAL_FONT, fg_color=config.LIGHT_BLUE,
                                           text_color=config.DARK_BLUE, hover_color="#d6e2fb",
                                           command=lambda: change_page(show_users_page))
    users_button.pack(fill="x", padx=12, pady=4)

    global page_container
    page_container = customtkinter.CTkFrame(body, fg_color=config.BACKGROUND_GRAY)
    page_container.pack(side="right", fill="both", expand=True, padx=(0, 12), pady=12)

    change_page(show_all_orders_page)


def show_all_orders_page(parent_frame):
    print("نمایش صفحهٔ همهٔ مرسوله‌ها")

    title = create_title_label(parent_frame, config.t("all_orders_title"))
    title.pack(anchor="e", pady=(0, 8))

    if len(data.all_data["orders"]) == 0:
        empty_label = create_normal_label(parent_frame, config.t("empty_orders_admin"))
        empty_label.pack(anchor="e", pady=20)
        return

    list_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True)

    for order in data.all_data["orders"]:
        create_order_card(list_frame, order, show_admin_buttons=True)


def show_all_tickets_page(parent_frame):
    print("نمایش صفحهٔ همهٔ تیکت‌ها")

    title = create_title_label(parent_frame, config.t("tickets_title_admin"))
    title.pack(anchor="e", pady=(0, 8))

    if len(data.all_data["tickets"]) == 0:
        empty_label = create_normal_label(parent_frame, config.t("empty_tickets_admin"))
        empty_label.pack(anchor="e", pady=20)
        return

    list_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True)

    for ticket in data.all_data["tickets"]:
        ticket_text = ("#" + str(ticket["number"]) + "   " + ticket["subject"]
                       + "   (" + config.ticket_status_text(ticket["status"]) + ")   "
                       + config.t("user") + ": " + ticket["username"])
        ticket_button = customtkinter.CTkButton(
            list_frame, text=ticket_text, height=40, font=config.NORMAL_FONT,
            fg_color=config.WHITE, text_color=config.DARK_BLUE, hover_color=config.LIGHT_BLUE,
            anchor="e", command=lambda number=ticket["number"]: open_ticket_conversation(number))
        ticket_button.pack(fill="x", pady=4, padx=4)


def show_statistics_page(parent_frame):
    print("نمایش صفحهٔ آمار")

    title = create_title_label(parent_frame, config.t("stats_title"))
    title.pack(anchor="e", pady=(0, 8))

    customer_count = 0
    for user in data.all_data["users"]:
        if user["role"] == "customer":
            customer_count = customer_count + 1

    order_count = len(data.all_data["orders"])
    ticket_count = len(data.all_data["tickets"])

    money_total_dollar = 0
    for order in data.all_data["orders"]:
        if order["status"] != "cancelled":
            money_total_dollar = money_total_dollar + order["cost_dollar"]

    cards_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
    cards_frame.pack(fill="x", pady=(0, 10))

    create_statistic_card(cards_frame, config.t("stat_customers"), str(customer_count))
    create_statistic_card(cards_frame, config.t("stat_orders"), str(order_count))
    create_statistic_card(cards_frame, config.t("stat_tickets"), str(ticket_count))
    create_statistic_card(cards_frame, config.t("stat_revenue"),
                          data.format_toman(int(money_total_dollar * data.dollar_rate_toman)))

    status_card = create_card(parent_frame)
    status_card.pack(fill="x", pady=6)

    status_title = customtkinter.CTkLabel(status_card, text=config.t("by_status"),
                                          font=config.BOLD_FONT, text_color=config.DARK_BLUE)
    status_title.pack(anchor="e", padx=14, pady=(12, 6))

    for status in config.STATUS_KEYS:
        status_count = 0
        for order in data.all_data["orders"]:
            if order["status"] == status:
                status_count = status_count + 1

        line_text = config.status_text(status) + ": " + str(status_count) + " " + config.t("orders_unit")
        line_label = create_normal_label(status_card, line_text)
        line_label.pack(anchor="e", padx=20, pady=2)

    bottom_space = customtkinter.CTkLabel(status_card, text="", height=8)
    bottom_space.pack()


def create_statistic_card(parent_frame, title_text, value_text):
    card = customtkinter.CTkFrame(parent_frame, fg_color=config.WHITE, corner_radius=12)
    card.pack(side="right", fill="both", expand=True, padx=4, pady=4)

    title_label = customtkinter.CTkLabel(card, text=title_text, font=config.SMALL_FONT,
                                         text_color=config.GRAY_TEXT)
    title_label.pack(anchor="e", padx=12, pady=(12, 2))

    value_label = customtkinter.CTkLabel(card, text=value_text, font=config.NUMBER_FONT,
                                         text_color=config.MAIN_BLUE)
    value_label.pack(anchor="e", padx=12, pady=(0, 12))



def show_users_page(parent_frame):
    print("نمایش صفحهٔ مدیریت کاربران")

    title = create_title_label(parent_frame, config.t("users_title"))
    title.pack(anchor="e", pady=(0, 8))

    list_frame = customtkinter.CTkScrollableFrame(parent_frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True)

    role_values = [config.t("role_admin"), config.t("role_customer")]

    for user in data.all_data["users"]:
        card = create_card(list_frame)
        card.pack(fill="x", pady=6, padx=4)

        info_text = user["username"] + "   |   " + config.t("role_" + user["role"])
        info_label = customtkinter.CTkLabel(card, text=info_text, font=config.BOLD_FONT,
                                            text_color=config.DARK_BLUE, anchor="e")
        info_label.pack(anchor="e", padx=14, pady=(10, 4))

        buttons_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(anchor="e", padx=14, pady=(0, 12))

        role_menu = customtkinter.CTkOptionMenu(buttons_frame, values=role_values,
                                                width=130, height=30, font=config.SMALL_FONT)
        role_menu.set(config.t("role_" + user["role"]))
        role_menu.pack(side="right", padx=4)

        save_button = customtkinter.CTkButton(
            buttons_frame, text=config.t("save_role"), width=110, height=30,
            font=config.SMALL_FONT, fg_color=config.MAIN_BLUE, hover_color="#1e40af",
            command=lambda user_to_change=user, menu_widget=role_menu:
                save_new_role(user_to_change, menu_widget))
        save_button.pack(side="right", padx=4)


def save_new_role(user, role_menu):
    chosen_label = role_menu.get()
    if chosen_label == config.t("role_admin"):
        new_role = "admin"
    else:
        new_role = "customer"

    if user["role"] == new_role:
        return

    is_done, error_key = data.change_user_role(user["username"], new_role)
    if not is_done:
        messagebox.showerror(config.t("error_title"), config.t(error_key))
        return

    messagebox.showinfo(config.t("done_title"),
                        config.t("role_changed")
                        .replace("{name}", user["username"])
                        .replace("{role}", config.t("role_" + new_role)))
    change_page(show_users_page)



def start_loading_dollar_rate():
    background_thread = threading.Thread(target=load_dollar_rate_in_background)
    background_thread.start()


def load_dollar_rate_in_background():
    new_rate = data.fetch_dollar_rate_from_internet()
    app_window.after(0, lambda: apply_new_dollar_rate(new_rate))


def apply_new_dollar_rate(new_rate):
    data.set_dollar_rate(new_rate)
    show_rate_on_top_bar()



def start_app():
    global app_window

    print("برنامه شروع شد.")

    data.all_data = data.load_all_data()

    saved_rate = data.all_data["settings"].get("dollar_rate", config.DEFAULT_DOLLAR_RATE)
    if saved_rate > 0:
        data.dollar_rate_toman = saved_rate
        data.rate_source_text = config.t("rate_saved")

    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")

    app_window = customtkinter.CTk()
    app_window.title(config.t("app_name"))
    app_window.geometry("1120x720")
    app_window.minsize(980, 640)

    data.create_default_admin()

    show_login_page()

    start_loading_dollar_rate()

    print("برنامه آماده است.")
    app_window.mainloop()
    print("برنامه بسته شد.")
