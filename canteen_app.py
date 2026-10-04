import streamlit as st
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BV Canteen Management System",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. Translations Dictionary (Arabic & English)
# ---------------------------------------------------------
TRANSLATIONS = {
    "AR": {
        "title": "🏫 نظام إدارة كانتين المدرسة - Bright Vision",
        "switch_lang": "🌐 Language / اللغة",
        "nav_menu": "📌 القائمة الرئيسية",
        "sales_page": "🛒 تسجيل المبيعات",
        "products_page": "📦 إدارة المنتجات",
        "dashboard_page": "📊 التقارير والإحصائيات",
        "settings_page": "⚙️ الإعدادات والأمان",
        "system_locked": "🔒 النظام مغلق حالياً بقرار من الإدارة.",
        "kill_switch_active": "الرجاء التواصل مع المسين لقفل/فتح النظام.",
        "add_sale": "تسجيل عملية بيع جديدة",
        "select_product": "اختر المنتج",
        "quantity": "الكمية",
        "unit_price": "سعر الوحدة",
        "total_price": "الإجمالي",
        "buyer_name": "اسم الطالب / المشترِي (اختياري)",
        "complete_sale": "✅ إتمام عملية البيع",
        "sale_success": "تم تسجيل عملية البيع بنجاح!",
        "insufficient_stock": "⚠️ الكمية المتاحة في المخزون غير كافية!",
        "out_of_stock": "❌ هذا المنتج غير متوفر في المخزون حالياً!",
        "add_product": "إضافة منتج جديد",
        "product_name": "اسم المنتج",
        "cost_price": "سعر التكلفة (الشراء)",
        "selling_price": "سعر البيع",
        "stock_qty": "الكمية الأولية في المخزون",
        "save_product": "➕ حفظ المنتج",
        "product_added": "تمت إضافة المنتج بنجاح!",
        "current_inventory": "📋 المخزون الحالي",
        "total_sales_val": "إجمالي المبيعات",
        "total_profit_val": "إجمالي الأرباح",
        "total_transactions": "عدد العمليات",
        "recent_sales": "📜 سجل المبيعات الأخيرة",
        "sales_chart": "📈 رسم بياني للمبيعات",
        "kill_switch_title": "🚨 مفتاح الإغلاق السريع (Kill Switch)",
        "lock_system": "قفل النظام",
        "unlock_system": "فتح النظام",
        "status_locked": "الحالة: النظام مغلق 🔴",
        "status_unlocked": "الحالة: النظام يعمل بنجاح 🟢",
        "currency": "ج.م"
    },
    "EN": {
        "title": "🏫 Bright Vision Canteen Management System",
        "switch_lang": "🌐 Language / اللغة",
        "nav_menu": "📌 Navigation",
        "sales_page": "🛒 Sales POS",
        "products_page": "📦 Product Management",
        "dashboard_page": "📊 Analytics & Reports",
        "settings_page": "⚙️ Settings & Security",
        "system_locked": "🔒 System is currently locked by administration.",
        "kill_switch_active": "Please contact admin to enable access.",
        "add_sale": "Register New Sale",
        "select_product": "Select Product",
        "quantity": "Quantity",
        "unit_price": "Unit Price",
        "total_price": "Total Price",
        "buyer_name": "Student/Buyer Name (Optional)",
        "complete_sale": "✅ Complete Sale",
        "sale_success": "Sale registered successfully!",
        "insufficient_stock": "⚠️ Insufficient stock available!",
        "out_of_stock": "❌ Out of stock!",
        "add_product": "Add New Product",
        "product_name": "Product Name",
        "cost_price": "Cost Price",
        "selling_price": "Selling Price",
        "stock_qty": "Initial Stock Quantity",
        "save_product": "➕ Save Product",
        "product_added": "Product added successfully!",
        "current_inventory": "📋 Current Inventory",
        "total_sales_val": "Total Sales",
        "total_profit_val": "Total Profit",
        "total_transactions": "Total Transactions",
        "recent_sales": "📜 Recent Sales History",
        "sales_chart": "📈 Sales Analytics",
        "kill_switch_title": "🚨 Emergency Kill Switch",
        "lock_system": "Lock System",
        "unlock_system": "Unlock System",
        "status_locked": "Status: System Locked 🔴",
        "status_unlocked": "Status: System Active 🟢",
        "currency": "EGP"
    }
}

# ---------------------------------------------------------
# 3. Language Selector Session State
# ---------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "AR"

with st.sidebar:
    lang_choice = st.radio(
        TRANSLATIONS[st.session_state.lang]["switch_lang"],
        options=["العربية (AR)", "English (EN)"],
        index=0 if st.session_state.lang == "AR" else 1
    )
    st.session_state.lang = "AR" if "AR" in lang_choice else "EN"

t = TRANSLATIONS[st.session_state.lang]

# ---------------------------------------------------------
# 4. Database Connection (Supabase / Postgres)
# ---------------------------------------------------------
@st.cache_resource
def get_db_engine():
    try:
        db_url = st.secrets["postgres"]["url"]
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

engine = get_db_engine()

# Initialize Tables
def init_db():
    if engine is None:
        return
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                cost_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                stock INT NOT NULL
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INT NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                profit REAL NOT NULL,
                buyer_name TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS system_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """))
        # Default Kill Switch State
        conn.execute(text("""
            INSERT INTO system_config (key, value)
            VALUES ('is_locked', 'false')
            ON CONFLICT (key) DO NOTHING;
        """))

init_db()

# Helpers
def is_system_locked():
    if engine is None:
        return False
    with engine.connect() as conn:
        res = conn.execute(text("SELECT value FROM system_config WHERE key = 'is_locked'")).fetchone()
        return res[0] == "true" if res else False

def set_system_lock(locked: bool):
    val = "true" if locked else "false"
    with engine.begin() as conn:
        conn.execute(text("UPDATE system_config SET value = :v WHERE key = 'is_locked'"), {"v": val})

# ---------------------------------------------------------
# 5. Header & Navigation
# ---------------------------------------------------------
st.title(t["title"])

locked = is_system_locked()

with st.sidebar:
    st.divider()
    page = st.radio(
        t["nav_menu"],
        [t["sales_page"], t["products_page"], t["dashboard_page"], t["settings_page"]]
    )

# ---------------------------------------------------------
# 6. Page Logic
# ---------------------------------------------------------

# --- SYSTEM LOCKED CHECK ---
if locked and page != t["settings_page"]:
    st.error(t["system_locked"])
    st.info(t["kill_switch_active"])
    st.stop()

# --- 1. SALES POS PAGE ---
if page == t["sales_page"]:
    st.subheader(t["add_sale"])
    
    with engine.connect() as conn:
        products_df = pd.read_sql("SELECT * FROM products WHERE stock > 0 ORDER BY name ASC", conn)
    
    if products_df.empty:
        st.warning(t["out_of_stock"])
    else:
        product_list = products_df["name"].tolist()
        selected_prod_name = st.selectbox(t["select_product"], product_list)
        
        prod_data = products_df[products_df["name"] == selected_prod_name].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            qty = st.number_input(t["quantity"], min_value=1, max_value=int(prod_data["stock"]), value=1, step=1)
            buyer = st.text_input(t["buyer_name"])
        
        with col2:
            unit_price = prod_data["selling_price"]
            total_price = unit_price * qty
            profit = (unit_price - prod_data["cost_price"]) * qty
            
            st.metric(t["unit_price"], f"{unit_price:.2f} {t['currency']}")
            st.metric(t["total_price"], f"{total_price:.2f} {t['currency']}")
        
        if st.button(t["complete_sale"], type="primary"):
            if qty > prod_data["stock"]:
                st.error(t["insufficient_stock"])
            else:
                with engine.begin() as conn:
                    # Deduct stock
                    conn.execute(
                        text("UPDATE products SET stock = stock - :qty WHERE name = :name"),
                        {"qty": qty, "name": selected_prod_name}
                    )
                    # Insert sale
                    conn.execute(
                        text("""
                            INSERT INTO sales (product_name, quantity, unit_price, total_price, profit, buyer_name)
                            VALUES (:pname, :qty, :uprice, :tprice, :profit, :buyer)
                        """),
                        {
                            "pname": selected_prod_name,
                            "qty": qty,
                            "uprice": unit_price,
                            "tprice": total_price,
                            "profit": profit,
                            "buyer": buyer if buyer else "Anonymous"
                        }
                    )
                st.success(t["sale_success"])
                st.rerun()

# --- 2. PRODUCT MANAGEMENT PAGE ---
elif page == t["products_page"]:
    st.subheader(t["add_product"])
    
    with st.form("add_prod_form", clear_on_submit=True):
        p_name = st.text_input(t["product_name"])
        c1, c2, c3 = st.columns(3)
        with c1:
            cost = st.number_input(t["cost_price"], min_value=0.0, step=0.5)
        with c2:
            price = st.number_input(t["selling_price"], min_value=0.0, step=0.5)
        with c3:
            stock = st.number_input(t["stock_qty"], min_value=0, step=1)
            
        submitted = st.form_submit_button(t["save_product"])
        if submitted:
            if p_name and price >= 0 and stock >= 0:
                try:
                    with engine.begin() as conn:
                        conn.execute(
                            text("""
                                INSERT INTO products (name, cost_price, selling_price, stock)
                                VALUES (:name, :cost, :price, :stock)
                                ON CONFLICT (name) DO UPDATE SET
                                cost_price = EXCLUDED.cost_price,
                                selling_price = EXCLUDED.selling_price,
                                stock = products.stock + EXCLUDED.stock;
                            """),
                            {"name": p_name, "cost": cost, "price": price, "stock": stock}
                        )
                    st.success(t["product_added"])
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving product: {e}")

    st.divider()
    st.subheader(t["current_inventory"])
    with engine.connect() as conn:
        inv_df = pd.read_sql("SELECT name, cost_price, selling_price, stock FROM products ORDER BY name ASC", conn)
    st.dataframe(inv_df, use_container_width=True)

# --- 3. ANALYTICS & DASHBOARD PAGE ---
elif page == t["dashboard_page"]:
    st.subheader(t["dashboard_page"])
    
    with engine.connect() as conn:
        sales_df = pd.read_sql("SELECT * FROM sales ORDER BY timestamp DESC", conn)
        
    if sales_df.empty:
        st.info("No sales records available yet.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric(t["total_sales_val"], f"{sales_df['total_price'].sum():.2f} {t['currency']}")
        c2.metric(t["total_profit_val"], f"{sales_df['profit'].sum():.2f} {t['currency']}")
        c3.metric(t["total_transactions"], str(len(sales_df)))
        
        st.divider()
        st.subheader(t["sales_chart"])
        
        fig = px.bar(
            sales_df,
            x="product_name",
            y="total_price",
            color="product_name",
            title=t["sales_chart"],
            labels={"product_name": "Product", "total_price": "Revenue"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(t["recent_sales"])
        st.dataframe(sales_df, use_container_width=True)

# --- 4. SETTINGS & KILL SWITCH PAGE ---
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
            st.warning("System Locked!")
            st.rerun()
    with col2:
        if st.button(t["unlock_system"], type="secondary", use_container_width=True):
            set_system_lock(False)
            st.success("System Unlocked!")
            st.rerun()
