import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BV Canteen Management System",
    page_icon="🍔",
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
        res = requests.get(f"{SUPABASE_URL}/rest/v1/{table}?select=*", headers=HEADERS)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
    except Exception as e:
        st.error(f"Error fetching {table}: {e}")
    return pd.DataFrame()

def db_insert(table, data):
    try:
        res = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=HEADERS, json=data)
        return res.status_code in [200, 201]
    except Exception as e:
        st.error(f"Error inserting: {e}")
        return False

def db_update(table, match_col, match_val, data):
    try:
        res = requests.patch(f"{SUPABASE_URL}/rest/v1/{table}?{match_col}=eq.{match_val}", headers=HEADERS, json=data)
        return res.status_code in [200, 204]
    except Exception as e:
        st.error(f"Error updating: {e}")
        return False

# ---------------------------------------------------------
# System Lock Check
# ---------------------------------------------------------
def is_system_locked():
    df = db_get("system_config")
    if not df.empty and "key" in df.columns and "value" in df.columns:
        row = df[df["key"] == "is_locked"]
        if not row.empty:
            return str(row.iloc[0]["value"]).lower() == "true"
    return False

def set_system_lock(locked: bool):
    val = "true" if locked else "false"
    db_update("system_config", "key", "is_locked", {"value": val})

# ---------------------------------------------------------
# Translations
# ---------------------------------------------------------
TRANSLATIONS = {
    "AR": {
        "title": "🏫 نظام إدارة كانتين المدرسة - Bright Vision",
        "switch_lang": "🌐 Language / اللغة",
        "nav_menu": "📌 القائمة الرئيسية",
        "sales_page": "🛒 تسجيل المبيعات (POS)",
        "products_page": "📦 إدارة المنتجات والمخزون",
        "dashboard_page": "📊 التقارير والإحصائيات المالية",
        "settings_page": "⚙️ الإعدادات والأمان (الأدمن)",
        "login_title": "🔐 تسجيل الدخول للنظام",
        "select_role": "اختر نوع الحساب",
        "role_student": "👤 طالب / كاشير",
        "role_admin": "👑 مدير النظام (Admin)",
        "admin_password": "كلمة سر الأدمن",
        "login_btn": "دخول",
        "logout_btn": "تسجيل الخروج",
        "wrong_pass": "❌ كلمة السر غير صحيحة!",
        "system_locked": "🔒 النظام مغلق حالياً بقرار من الإدارة.",
        "kill_switch_active": "الرجاء التواصل مع إدارة المدرسة لفتح السيستم.",
        "add_sale": "تسجيل عملية بيع جديدة",
        "select_product": "اختر المنتج",
        "quantity": "الكمية",
        "unit_price": "سعر الوحدة",
        "total_price": "الإجمالي",
        "buyer_name": "اسم الطالب / المشترِي (اختياري)",
        "complete_sale": "✅ إتمام عملية البيع",
        "sale_success": "تم تسجيل عملية البيع بنجاح!",
        "insufficient_stock": "⚠️ الكمية المتاحة غير كافية!",
        "out_of_stock": "❌ لا توجد منتجات متاحة حالياً!",
        "add_product": "إضافة / تحديث منتج",
        "product_name": "اسم المنتج",
        "cost_price": "سعر التكلفة",
        "selling_price": "سعر البيع",
        "stock_qty": "الكمية المضافة للمخزون",
        "save_product": "➕ حفظ المنتج",
        "product_added": "تم حفظ المنتج بنجاح!",
        "current_inventory": "📋 المخزون الحالي",
        "total_sales_val": "إجمالي المبيعات",
        "total_profit_val": "إجمالي الأرباح الصافية",
        "total_transactions": "عدد العمليات",
        "recent_sales": "📜 سجل المبيعات الأخيرة",
        "sales_chart": "📈 رسم بياني للمبيعات",
        "kill_switch_title": "🚨 مفتاح الإغلاق السريع (Kill Switch)",
        "lock_system": "🔒 قفل النظام فوراً",
        "unlock_system": "🔓 فتح النظام",
        "status_locked": "الحالة الحالية: النظام مغلق 🔴",
        "status_unlocked": "الحالة الحالية: النظام يعمل بنجاح 🟢",
        "currency": "ج.م"
    },
    "EN": {
        "title": "🏫 Bright Vision Canteen Management System",
        "switch_lang": "🌐 Language / اللغة",
        "nav_menu": "📌 Navigation",
        "sales_page": "🛒 Sales POS",
        "products_page": "📦 Product & Stock Management",
        "dashboard_page": "📊 Financial Analytics",
        "settings_page": "⚙️ Admin Settings & Security",
        "login_title": "🔐 System Login",
        "select_role": "Select Account Role",
        "role_student": "👤 Student / Cashier",
        "role_admin": "👑 Administrator",
        "admin_password": "Admin Password",
        "login_btn": "Login",
        "logout_btn": "Logout",
        "wrong_pass": "❌ Incorrect Admin Password!",
        "system_locked": "🔒 System is currently locked by administration.",
        "kill_switch_active": "Please contact school administration.",
        "add_sale": "Register New Sale",
        "select_product": "Select Product",
        "quantity": "Quantity",
        "unit_price": "Unit Price",
        "total_price": "Total Price",
        "buyer_name": "Buyer Name (Optional)",
        "complete_sale": "✅ Complete Sale",
        "sale_success": "Sale registered successfully!",
        "insufficient_stock": "⚠️ Insufficient stock!",
        "out_of_stock": "❌ Out of stock!",
        "add_product": "Add / Update Product",
        "product_name": "Product Name",
        "cost_price": "Cost Price",
        "selling_price": "Selling Price",
        "stock_qty": "Stock Quantity to Add",
        "save_product": "➕ Save Product",
        "product_added": "Product saved successfully!",
        "current_inventory": "📋 Current Inventory",
        "total_sales_val": "Total Revenue",
        "total_profit_val": "Net Profit",
        "total_transactions": "Transactions",
        "recent_sales": "📜 Recent Transactions",
        "sales_chart": "📈 Sales Analytics",
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

if "user_role" not in st.session_state:
    st.session_state.user_role = None

with st.sidebar:
    lang_choice = st.radio(
        TRANSLATIONS[st.session_state.lang]["switch_lang"],
        options=["العربية (AR)", "English (EN)"],
        index=0 if st.session_state.lang == "AR" else 1
    )
    st.session_state.lang = "AR" if "AR" in lang_choice else "EN"

t = TRANSLATIONS[st.session_state.lang]

# ---------------------------------------------------------
# Login Screen Logic
# ---------------------------------------------------------
if st.session_state.user_role is None:
    st.title(t["title"])
    st.subheader(t["login_title"])
    
    col1, col2 = st.columns([1, 2])
    with col1:
        role = st.selectbox(t["select_role"], [t["role_student"], t["role_admin"]])
        
        if role == t["role_admin"]:
            pwd = st.text_input(t["admin_password"], type="password")
            if st.button(t["login_btn"], type="primary"):
                if pwd == "admin123":  # كلمة سر الأدمن
                    st.session_state.user_role = "admin"
                    st.rerun()
                else:
                    st.error(t["wrong_pass"])
        else:
            if st.button(t["login_btn"], type="primary"):
                st.session_state.user_role = "student"
                st.rerun()
    st.stop()

# Header & Sidebar Navigation
st.title(t["title"])

with st.sidebar:
    st.write(f"**الحساب الحالي:** {t['role_admin'] if st.session_state.user_role == 'admin' else t['role_student']}")
    if st.button(t["logout_btn"]):
        st.session_state.user_role = None
        st.rerun()
    st.divider()
    
    menu_options = [t["sales_page"]]
    if st.session_state.user_role == "admin":
        menu_options.extend([t["products_page"], t["dashboard_page"], t["settings_page"]])
    else:
        menu_options.append(t["products_page"]) # الطالب يشاهد المخزون بدون تعديل
        
    page = st.radio(t["nav_menu"], menu_options)

# ---------------------------------------------------------
# Check System Lock Status
# ---------------------------------------------------------
locked = is_system_locked()
if locked and st.session_state.user_role != "admin":
    st.error(t["system_locked"])
    st.info(t["kill_switch_active"])
    st.stop()

# ---------------------------------------------------------
# Page Logic
# ---------------------------------------------------------

# --- 1. SALES PAGE ---
if page == t["sales_page"]:
    st.subheader(t["add_sale"])
    products_df = db_get("products")
    
    if products_df.empty or "stock" not in products_df.columns:
        st.warning(t["out_of_stock"])
    else:
        available_prods = products_df[products_df["stock"] > 0]
        if available_prods.empty:
            st.warning(t["out_of_stock"])
        else:
            prod_names = available_prods["name"].tolist()
            selected_name = st.selectbox(t["select_product"], prod_names)
            prod_row = available_prods[available_prods["name"] == selected_name].iloc[0]
            
            c1, c2 = st.columns(2)
            with c1:
                qty = st.number_input(t["quantity"], min_value=1, max_value=int(prod_row["stock"]), value=1)
                buyer = st.text_input(t["buyer_name"])
            with c2:
                u_price = float(prod_row["selling_price"])
                t_price = u_price * qty
                profit = (u_price - float(prod_row["cost_price"])) * qty
                st.metric(t["unit_price"], f"{u_price:.2f} {t['currency']}")
                st.metric(t["total_price"], f"{t_price:.2f} {t['currency']}")
                
            if st.button(t["complete_sale"], type="primary"):
                new_stock = int(prod_row["stock"]) - qty
                if db_update("products", "name", selected_name, {"stock": new_stock}):
                    db_insert("sales", {
                        "product_name": selected_name,
                        "quantity": qty,
                        "unit_price": u_price,
                        "total_price": t_price,
                        "profit": profit,
                        "buyer_name": buyer if buyer else "Anonymous"
                    })
                    st.success(t["sale_success"])
                    st.rerun()

# --- 2. PRODUCTS PAGE ---
elif page == t["products_page"]:
    if st.session_state.user_role == "admin":
        st.subheader(t["add_product"])
        with st.form("add_p"):
            p_name = st.text_input(t["product_name"])
            c1, c2, c3 = st.columns(3)
            cost = c1.number_input(t["cost_price"], min_value=0.0)
            price = c2.number_input(t["selling_price"], min_value=0.0)
            stock = c3.number_input(t["stock_qty"], min_value=0, step=1)
            
            if st.form_submit_button(t["save_product"]):
                if p_name:
                    db_insert("products", {"name": p_name, "cost_price": cost, "selling_price": price, "stock": stock})
                    st.success(t["product_added"])
                    st.rerun()
        st.divider()

    st.subheader(t["current_inventory"])
    inv = db_get("products")
    if not inv.empty:
        if st.session_state.user_role != "admin":
            display_inv = inv[["name", "selling_price", "stock"]].copy()
            st.dataframe(display_inv, use_container_width=True)
        else:
            st.dataframe(inv, use_container_width=True)

# --- 3. DASHBOARD PAGE (ADMIN ONLY) ---
elif page == t["dashboard_page"]:
    st.subheader(t["dashboard_page"])
    sales = db_get("sales")
    if sales.empty:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric(t["total_sales_val"], f"{sales['total_price'].sum():.2f} {t['currency']}")
        c2.metric(t["total_profit_val"], f"{sales['profit'].sum():.2f} {t['currency']}")
        c3.metric(t["total_transactions"], str(len(sales)))
        
        st.divider()
        fig = px.bar(sales, x="product_name", y="total_price", color="product_name", title=t["sales_chart"])
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(t["recent_sales"])
        st.dataframe(sales, use_container_width=True)

# --- 4. SETTINGS & KILL SWITCH (ADMIN ONLY) ---
elif page == t["settings_page"]:
    st.subheader(t["kill_switch_title"])
    
    current_status = is_system_locked()
    if current_status:
        st.error(t["status_locked"])
    else:
        st.success(t["status_unlocked"])
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["lock_system"], type="primary", use_container_width=True):
            set_system_lock(True)
            st.warning("تم إغلاق النظام!")
            st.rerun()
    with col2:
        if st.button(t["unlock_system"], type="secondary", use_container_width=True):
            set_system_lock(False)
            st.success("تم فتح النظام!")
            st.rerun()
