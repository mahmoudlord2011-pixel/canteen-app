import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BV Canteen Management System",
    page_icon="👑",
    layout="wide"
)

# ---------------------------------------------------------
# Supabase REST API Setup
# ---------------------------------------------------------
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def db_get(table):
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/{table}?select=*", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
    except Exception:
        pass
    return pd.DataFrame()

def db_insert(table, data):
    try:
        res = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS, json=data, timeout=5)
        return res.status_code in [200, 201]
    except Exception:
        return False

def db_update(table, match_col, match_val, data):
    try:
        res = requests.patch(f"{SUPABASE_URL}/rest/v1/{table}?{match_col}=eq.{match_val}", headers=HEADERS, json=data, timeout=5)
        return res.status_code in [200, 204]
    except Exception:
        return False

# ---------------------------------------------------------
# Local Demo Memory Initialization
# ---------------------------------------------------------
if "demo_products" not in st.session_state:
    st.session_state.demo_products = pd.DataFrame([
        {"id": 1, "name": "ساندوتش شاورما", "cost_price": 25.0, "selling_price": 40.0, "stock": 15},
        {"id": 2, "name": "عصير برتقال فرش", "cost_price": 10.0, "selling_price": 20.0, "stock": 30},
        {"id": 3, "name": "ماء معدني", "cost_price": 3.0, "selling_price": 7.0, "stock": 50},
        {"id": 4, "name": "كرواسون شوكولاتة", "cost_price": 12.0, "selling_price": 25.0, "stock": 8}
    ])

if "demo_sales" not in st.session_state:
    st.session_state.demo_sales = pd.DataFrame([
        {"id": 1, "product_name": "ساندوتش شاورما", "quantity": 2, "unit_price": 40.0, "total_price": 80.0, "profit": 30.0, "buyer_name": "أحمد محمود", "created_at": "2026-10-04 10:00"},
        {"id": 2, "product_name": "عصير برتقال فرش", "quantity": 1, "unit_price": 20.0, "total_price": 20.0, "profit": 10.0, "buyer_name": "عمر خالد", "created_at": "2026-10-04 10:15"}
    ])

if "system_locked" not in st.session_state:
    st.session_state.system_locked = False

# ---------------------------------------------------------
# Unified Data Helpers (Supabase with Demo Fallback)
# ---------------------------------------------------------
def get_products():
    df = db_get("products")
    if not df.empty and "stock" in df.columns:
        return df
    return st.session_state.demo_products

def get_sales():
    df = db_get("sales")
    if not df.empty and "total_price" in df.columns:
        return df
    return st.session_state.demo_sales

def check_system_lock():
    df = db_get("system_config")
    if not df.empty and "key" in df.columns and "value" in df.columns:
        row = df[df["key"] == "is_locked"]
        if not row.empty:
            return str(row.iloc[0]["value"]).lower() == "true"
    return st.session_state.system_locked

def toggle_system_lock(locked_state: bool):
    st.session_state.system_locked = locked_state
    db_update("system_config", "key", "is_locked", {"value": "true" if locked_state else "false"})

# ---------------------------------------------------------
# User Accounts Definition
# ---------------------------------------------------------
ACCOUNTS = {
    "oody": {"pass": "Mahmoud@2011", "role": "master", "name": "👑 Master Oody (حساب المالك الأعظم)", "badge": "🥇 Master Owner"},
    "admin": {"pass": "Dr.RagabBV842", "role": "admin", "name": "⚙️ د. رجب (Admin)", "badge": "👑 System Admin"},
    "canteen": {"pass": "canteen 842", "role": "canteen", "name": "🍔 حساب الكانتين", "badge": "🏪 Cashier / Canteen"},
    "student": {"pass": "student123", "role": "student", "name": "🎓 حساب الطلاب", "badge": "👤 Student"}
}

GUEST_DEMO_ACCOUNT = {
    "role": "student",
    "name": "🚀 زائر الديمو التجريبي (Demo User)",
    "badge": "🎓 Guest Demo"
}

# ---------------------------------------------------------
# Translations
# ---------------------------------------------------------
TRANSLATIONS = {
    "AR": {
        "title": "🏫 نظام إدارة كانتين المدرسة - Bright Vision",
        "login_title": "🔐 تسجيل الدخول للنظام",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "دخول للنظام",
        "demo_btn": "🚀 دخول سريع بنظام الديمو (Guest Demo)",
        "logout_btn": "تسجيل الخروج",
        "wrong_credentials": "❌ اسم المستخدم أو كلمة المرور غير صحيحة!",
        "system_locked": "🔒 النظام مغلق حالياً بقرار من الإدارة.",
        "kill_switch_active": "الرجاء التواصل مع إدارة المدرسة لفتح السيستم.",
        "nav_menu": "📌 القائمة الرئيسية",
        "sales_page": "🛒 تسجيل المبيعات (POS)",
        "products_page": "📦 إدارة المنتجات والمخزون",
        "dashboard_page": "📊 التقارير والإحصائيات المالية",
        "settings_page": "⚙️ الإعدادات ومفتاح الأمان (Kill Switch)",
        "add_sale": "تسجيل عملية بيع جديدة",
        "select_product": "اختر المنتج",
        "quantity": "الكمية المطلوبة",
        "unit_price": "سعر الوحدة",
        "total_price": "الإجمالي",
        "buyer_name": "اسم الطالب / المشتري (اختياري)",
        "complete_sale": "✅ إتمام عملية البيع",
        "sale_success": "تم تسجيل عملية البيع بنجاح وتحديث المخزون!",
        "out_of_stock": "❌ لا توجد منتجات متاحة حالياً بالمخزون!",
        "add_product": "إضافة / تحديث منتج",
        "product_name": "اسم المنتج",
        "cost_price": "سعر التكلفة (ج.م)",
        "selling_price": "سعر البيع (ج.م)",
        "stock_qty": "الكمية المضافة للمخزون",
        "save_product": "➕ حفظ المنتج",
        "product_added": "تم حفظ المنتج بنجاح!",
        "current_inventory": "📋 قائمة المخزون الحالي",
        "total_sales_val": "إجمالي المبيعات",
        "total_profit_val": "صافي الأرباح",
        "total_transactions": "إجمالي العمليات",
        "recent_sales": "📜 سجل المبيعات والعمليات",
        "sales_chart": "📈 تحليل المبيعات حسب المنتج",
        "kill_switch_title": "🚨 مفتاح الطوارئ والإغلاق السريع (Kill Switch)",
        "lock_system": "🔒 قفل النظام فوراً",
        "unlock_system": "🔓 فتح النظام",
        "status_locked": "الحالة الحالية: النظام مغلق 🔴",
        "status_unlocked": "الحالة الحالية: النظام يعمل بنجاح 🟢",
        "currency": "ج.م"
    },
    "EN": {
        "title": "🏫 Bright Vision Canteen Management System",
        "login_title": "🔐 System Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "demo_btn": "🚀 Instant Demo Access (Guest Demo)",
        "logout_btn": "Logout",
        "wrong_credentials": "❌ Invalid username or password!",
        "system_locked": "🔒 System is currently locked by administration.",
        "kill_switch_active": "Please contact school administration.",
        "nav_menu": "📌 Navigation Menu",
        "sales_page": "🛒 Sales POS",
        "products_page": "📦 Product & Stock Management",
        "dashboard_page": "📊 Financial Analytics",
        "settings_page": "⚙️ Admin Settings (Kill Switch)",
        "add_sale": "Register New Sale",
        "select_product": "Select Product",
        "quantity": "Quantity",
        "unit_price": "Unit Price",
        "total_price": "Total Price",
        "buyer_name": "Buyer Name (Optional)",
        "complete_sale": "✅ Complete Sale",
        "sale_success": "Sale completed and stock updated!",
        "out_of_stock": "❌ Out of stock!",
        "add_product": "Add / Update Product",
        "product_name": "Product Name",
        "cost_price": "Cost Price (EGP)",
        "selling_price": "Selling Price (EGP)",
        "stock_qty": "Initial Stock Quantity",
        "save_product": "➕ Save Product",
        "product_added": "Product saved successfully!",
        "current_inventory": "📋 Current Inventory",
        "total_sales_val": "Total Revenue",
        "total_profit_val": "Net Profit",
        "total_transactions": "Transactions",
        "recent_sales": "📜 Recent Transactions",
        "sales_chart": "📈 Sales Analytics per Product",
        "kill_switch_title": "🚨 Emergency Kill Switch",
        "lock_system": "🔒 Lock System",
        "unlock_system": "🔓 Unlock System",
        "status_locked": "Status: System Locked 🔴",
        "status_unlocked": "Status: System Active 🟢",
        "currency": "EGP"
    }
}

# Session State Setup
if "lang" not in st.session_state:
    st.session_state.lang = "AR"

if "current_user" not in st.session_state:
    st.session_state.current_user = None

t = TRANSLATIONS[st.session_state.lang]

# ---------------------------------------------------------
# Top Bar (Header + Lang Toggle Switcher Button)
# ---------------------------------------------------------
col_head, col_lang = st.columns([5, 1])
with col_head:
    st.title(t["title"])
with col_lang:
    lang_btn_text = "English 🌐" if st.session_state.lang == "AR" else "العربية 🌐"
    if st.button(lang_btn_text, use_container_width=True):
        st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"
        st.rerun()

st.divider()

# ---------------------------------------------------------
# 1. Login Screen
# ---------------------------------------------------------
if st.session_state.current_user is None:
    st.subheader(t["login_title"])
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        u_name = st.text_input(t["username"])
        u_pass = st.text_input(t["password"], type="password")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button(t["login_btn"], type="primary", use_container_width=True):
                if u_name in ACCOUNTS and ACCOUNTS[u_name]["pass"] == u_pass:
                    st.session_state.current_user = ACCOUNTS[u_name]
                    st.rerun()
                else:
                    st.error(t["wrong_credentials"])
        with col_b2:
            if st.button(t["demo_btn"], use_container_width=True):
                st.session_state.current_user = GUEST_DEMO_ACCOUNT
                st.rerun()
                
    st.stop()

# ---------------------------------------------------------
# Sidebar Navigation & User Info
# ---------------------------------------------------------
user = st.session_state.current_user
user_role = user["role"]

with st.sidebar:
    st.markdown(f"### {user['name']}")
    st.caption(f"**الرتبة:** {user['badge']}")
    if st.button(t["logout_btn"], use_container_width=True):
        st.session_state.current_user = None
        st.rerun()
    st.divider()
    
    # Navigation Rules
    if user_role in ["master", "admin"]:
        nav_options = [t["sales_page"], t["products_page"], t["dashboard_page"], t["settings_page"]]
    elif user_role == "canteen":
        nav_options = [t["sales_page"], t["products_page"]]
    else:  # Student / Guest
        nav_options = [t["sales_page"], t["products_page"]]
        
    page = st.radio(t["nav_menu"], nav_options)

# ---------------------------------------------------------
# Emergency System Lock Enforcement
# ---------------------------------------------------------
if check_system_lock() and user_role not in ["master", "admin"]:
    st.error(t["system_locked"])
    st.warning(t["kill_switch_active"])
    st.stop()

# ---------------------------------------------------------
# Pages Content
# ---------------------------------------------------------

# --- 1. SALES PAGE (POS) ---
if page == t["sales_page"]:
    st.subheader(t["add_sale"])
    prods_df = get_products()
    
    if prods_df.empty or "stock" not in prods_df.columns:
        st.warning(t["out_of_stock"])
    else:
        avail_df = prods_df[prods_df["stock"] > 0]
        if avail_df.empty:
            st.warning(t["out_of_stock"])
        else:
            names = avail_df["name"].tolist()
            selected = st.selectbox(t["select_product"], names)
            row = avail_df[avail_df["name"] == selected].iloc[0]
            
            c1, c2 = st.columns(2)
            with c1:
                qty = st.number_input(t["quantity"], min_value=1, max_value=int(row["stock"]), value=1)
                buyer = st.text_input(t["buyer_name"])
            with c2:
                u_p = float(row["selling_price"])
                tot_p = u_p * qty
                prof = (u_p - float(row["cost_price"])) * qty
                st.metric(t["unit_price"], f"{u_p:.2f} {t['currency']}")
                st.metric(t["total_price"], f"{tot_p:.2f} {t['currency']}")
                
            if st.button(t["complete_sale"], type="primary", use_container_width=True):
                new_stk = int(row["stock"]) - qty
                db_update("products", "name", selected, {"stock": new_stk})
                st.session_state.demo_products.loc[st.session_state.demo_products["name"] == selected, "stock"] = new_stk
                
                sale_record = {
                    "product_name": selected,
                    "quantity": qty,
                    "unit_price": u_p,
                    "total_price": tot_p,
                    "profit": prof,
                    "buyer_name": buyer if buyer else "طالب عام",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                db_insert("sales", sale_record)
                st.session_state.demo_sales = pd.concat([st.session_state.demo_sales, pd.DataFrame([sale_record])], ignore_index=True)
                
                st.success(t["sale_success"])
                st.rerun()

# --- 2. PRODUCTS PAGE ---
elif page == t["products_page"]:
    if user_role in ["master", "admin", "canteen"]:
        st.subheader(t["add_product"])
        with st.form("add_prod_form"):
            p_name = st.text_input(t["product_name"])
            c1, c2, c3 = st.columns(3)
            c_cost = c1.number_input(t["cost_price"], min_value=0.0, step=1.0)
            c_sell = c2.number_input(t["selling_price"], min_value=0.0, step=1.0)
            c_stk = c3.number_input(t["stock_qty"], min_value=0, step=1)
            
            if st.form_submit_button(t["save_product"], use_container_width=True):
                if p_name:
                    new_item = {"name": p_name, "cost_price": c_cost, "selling_price": c_sell, "stock": c_stk}
                    db_insert("products", new_item)
                    st.session_state.demo_products = pd.concat([st.session_state.demo_products, pd.DataFrame([new_item])], ignore_index=True)
                    st.success(t["product_added"])
                    st.rerun()
        st.divider()

    st.subheader(t["current_inventory"])
    inv = get_products()
    if not inv.empty:
        if user_role in ["student", "guest"]:
            st.dataframe(inv[["name", "selling_price", "stock"]], use_container_width=True)
        else:
            st.dataframe(inv, use_container_width=True)

# --- 3. DASHBOARD PAGE ---
elif page == t["dashboard_page"]:
    st.subheader(t["dashboard_page"])
    sales_df = get_sales()
    
    if sales_df.empty:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric(t["total_sales_val"], f"{sales_df['total_price'].sum():.2f} {t['currency']}")
        c2.metric(t["total_profit_val"], f"{sales_df['profit'].sum():.2f} {t['currency']}")
        c3.metric(t["total_transactions"], str(len(sales_df)))
        
        st.divider()
        fig = px.bar(sales_df, x="product_name", y="total_price", color="product_name", title=t["sales_chart"])
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(t["recent_sales"])
        st.dataframe(sales_df, use_container_width=True)

# --- 4. SETTINGS PAGE (KILL SWITCH) ---
elif page == t["settings_page"]:
    st.subheader(t["kill_switch_title"])
    
    status_locked = check_system_lock()
    if status_locked:
        st.error(t["status_locked"])
    else:
        st.success(t["status_unlocked"])
        
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t["lock_system"], type="primary", use_container_width=True):
            toggle_system_lock(True)
            st.warning("تم إغلاق النظام بأسره!")
            st.rerun()
    with c2:
        if st.button(t["unlock_system"], type="secondary", use_container_width=True):
            toggle_system_lock(False)
            st.success("تم فتح النظام بنجاح!")
            st.rerun()
