import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bright Vision - نظام الكانتين الذكي",
    page_icon="🍔",
    layout="wide"
)

# ---------------------------------------------------------
# Supabase REST API Configuration
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
# Session Memory Initialization
# ---------------------------------------------------------
if "demo_products" not in st.session_state:
    st.session_state.demo_products = pd.DataFrame([
        {"id": 1, "name": "ساندوتش جبنة", "category": "ساندوتشات", "cost_price": 10.0, "selling_price": 15.0, "stock": 20},
        {"id": 2, "name": "ساندوتش كفتة", "category": "ساندوتشات", "cost_price": 25.0, "selling_price": 35.0, "stock": 15},
        {"id": 3, "name": "ساندوتش بانييه", "category": "ساندوتشات", "cost_price": 25.0, "selling_price": 35.0, "stock": 10},
        {"id": 4, "name": "عصير فريش", "category": "مشروبات", "cost_price": 12.0, "selling_price": 20.0, "stock": 25},
        {"id": 5, "name": "زجاجة مياه", "category": "مشروبات", "cost_price": 4.0, "selling_price": 7.5, "stock": 50}
    ])

if "demo_sales" not in st.session_state:
    st.session_state.demo_sales = pd.DataFrame([
        {"id": 1, "product_name": "ساندوتش كفتة", "quantity": 2, "unit_price": 35.0, "total_price": 70.0, "profit": 20.0, "buyer_name": "طالب عام", "created_at": "2026-10-05 10:00"},
        {"id": 2, "product_name": "عصير فريش", "quantity": 1, "unit_price": 20.0, "total_price": 20.0, "profit": 8.0, "buyer_name": "طالب عام", "created_at": "2026-10-05 10:15"}
    ])

if "system_locked" not in st.session_state:
    st.session_state.system_locked = False

# Helper Functions
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
    "oody": {"pass": "Mahmoud@2011", "role": "master", "name": "الملك الأعلى للنظام | MASTER OODY مرحباً بك يا 👑"},
    "admin": {"pass": "Dr.RagabBV842", "role": "admin", "name": "مدير النظام | Dr. Ragab"},
    "canteen": {"pass": "canteen 842", "role": "canteen", "name": "حساب الكانتين والمطبخ 🍔"},
    "student": {"pass": "student123", "role": "student", "name": "حساب الطلاب والزوار 🎓"}
}

GUEST_DEMO_ACCOUNT = {
    "role": "student",
    "name": "زائر الديمو التجريبي 🎓"
}

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------------------------------------------------
# 1. Login Screen
# ---------------------------------------------------------
if st.session_state.current_user is None:
    st.title("🍔 نظام الكانتين الذكي - تسجيل الدخول")
    st.divider()
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        u_name = st.text_input("اسم المستخدم (Username):")
        u_pass = st.text_input("كلمة المرور (Password):", type="password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔑 تسجيل الدخول", type="primary", use_container_width=True):
                if u_name in ACCOUNTS and ACCOUNTS[u_name]["pass"] == u_pass:
                    st.session_state.current_user = ACCOUNTS[u_name]
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")
        with col_btn2:
            if st.button("🚀 دخول سريع بنظام الديمو (Guest Demo)", use_container_width=True):
                st.session_state.current_user = GUEST_DEMO_ACCOUNT
                st.rerun()
                
    st.stop()

# ---------------------------------------------------------
# Header & Master Control Dashboard Info
# ---------------------------------------------------------
user = st.session_state.current_user
user_role = user["role"]

col_header, col_logout = st.columns([5, 1])
with col_header:
    st.markdown(f"## {user['name']}")
with col_logout:
    if st.button("تسجيل الخروج 🚪", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()

# --- Master / Admin Control Panel ---
if user_role in ["master", "admin"]:
    st.markdown("### ⚡ لوحة التحكم المطلقة (Master Control)")
    c_status, c_switch = st.columns([2, 2])
    
    is_locked = check_system_lock()
    
    with c_status:
        if is_locked:
            st.error("حالة النظام الحالية: النظام متوقف بالكامل 🔴")
        else:
            st.success("حالة النظام الحالية: يعمل بالكامل 🟢")
            
    with c_switch:
        if is_locked:
            if st.button("🔓 إيقاف قفل النظام (تشغيل)", type="primary", use_container_width=True):
                toggle_system_lock(False)
                st.rerun()
        else:
            if st.button("🚨 (Kill Switch) إيقاف النظام بالكامل", type="primary", use_container_width=True):
                toggle_system_lock(True)
                st.rerun()

st.divider()
st.title("🍔 Bright Vision - نظام الكانتين الذكي")

# Enforce Emergency System Lock
if check_system_lock() and user_role not in ["master", "admin"]:
    st.error("🔒 النظام مغلق حالياً بقرار من إدارة المدرسة.")
    st.warning("الرجاء التواصل مع الإدارة لإعادة التفعيل.")
    st.stop()

# ---------------------------------------------------------
# Main Navigation Tabs Layout (Matching Video)
# ---------------------------------------------------------
if user_role in ["master", "admin"]:
    tabs = st.tabs(["تسجيل طلب جديد 🛒", "إدارة المنتجات ⚙️", "المبيعات والتقارير 📊"])
    tab_sales, tab_products, tab_reports = tabs[0], tabs[1], tabs[2]
elif user_role == "canteen":
    tabs = st.tabs(["تسجيل طلب جديد 🛒", "إدارة المنتجات ⚙️"])
    tab_sales, tab_products = tabs[0], tabs[1]
    tab_reports = None
else:  # Student / Guest
    tabs = st.tabs(["قائمة الطلبات المتاحة 🛒"])
    tab_sales = tabs[0]
    tab_products, tab_reports = None, None

# --- TAB 1: SALES & POS ---
with tab_sales:
    st.subheader("🛒 تسجيل طلب جديد")
    prods = get_products()
    
    if prods.empty or "stock" not in prods.columns:
        st.info("لا توجد منتجات مسجلة حالياً.")
    else:
        avail_prods = prods[prods["stock"] > 0]
        if avail_prods.empty:
            st.warning("جميع المنتجات نفدت من المخزن حالياً!")
        else:
            # Display products visually grouped
            categories = avail_prods["category"].unique() if "category" in avail_prods.columns else ["عام"]
            
            for cat in categories:
                st.markdown(f"#### 🥪 {cat}")
                cat_items = avail_prods[avail_prods["category"] == cat] if "category" in avail_prods.columns else avail_prods
                
                cols = st.columns(len(cat_items) if len(cat_items) <= 4 else 4)
                for idx, (_, item) in enumerate(cat_items.iterrows()):
                    with cols[idx % 4]:
                        st.checkbox(
                            f"{item['name']} - {item['selling_price']} ج.م (المتاح: {item['stock']})",
                            key=f"item_{item['name']}"
                        )
            
            st.divider()
            col_sel, col_qty = st.columns(2)
            with col_sel:
                selected_prod = st.selectbox("اختر المنتج لتأكيد الطلب:", avail_prods["name"].tolist())
            with col_qty:
                sel_row = avail_prods[avail_prods["name"] == selected_prod].iloc[0]
                qty = st.number_input("الكمية المطلوبة:", min_value=1, max_value=int(sel_row["stock"]), value=1)
                
            tot_price = float(sel_row["selling_price"]) * qty
            profit_val = (float(sel_row["selling_price"]) - float(sel_row["cost_price"])) * qty
            
            st.metric("الإجمالي الحسابي:", f"{tot_price:.2f} ج.م")
            
            if st.button("✅ تأكيد وتنفيذ الطلب", type="primary", use_container_width=True):
                new_stk = int(sel_row["stock"]) - qty
                db_update("products", "name", selected_prod, {"stock": new_stk})
                st.session_state.demo_products.loc[st.session_state.demo_products["name"] == selected_prod, "stock"] = new_stk
                
                sale_record = {
                    "product_name": selected_prod,
                    "quantity": qty,
                    "unit_price": float(sel_row["selling_price"]),
                    "total_price": tot_price,
                    "profit": profit_val,
                    "buyer_name": "طالب",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                db_insert("sales", sale_record)
                st.session_state.demo_sales = pd.concat([st.session_state.demo_sales, pd.DataFrame([sale_record])], ignore_index=True)
                
                st.success("تم تسجيل الطلب وخصمه من المخزون بنجاح!")
                st.rerun()

# --- TAB 2: PRODUCTS MANAGEMENT ---
if tab_products is not None:
    with tab_products:
        st.subheader("⚙️ إضافة منتج جديد للمنيو")
        with st.form("add_product_form"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                prod_name = st.text_input("اسم المنتج:")
                prod_cat = st.selectbox("القسم:", ["ساندوتشات", "مشروبات", "مخبوزات", "وجبات", "أخرى"])
            with col_p2:
                cost_p = st.number_input("سعر التكلفة (ج.م):", min_value=0.0, value=10.0, step=1.0)
                sell_p = st.number_input("سعر البيع (ج.م):", min_value=0.0, value=15.0, step=1.0)
                stock_q = st.number_input("الكمية الأولية بالمخزن:", min_value=1, value=20, step=1)
                
            if st.form_submit_button("➕ إضافة المنتج", use_container_width=True):
                if prod_name:
                    new_item = {
                        "name": prod_name,
                        "category": prod_cat,
                        "cost_price": cost_p,
                        "selling_price": sell_p,
                        "stock": stock_q
                    }
                    db_insert("products", new_item)
                    st.session_state.demo_products = pd.concat([st.session_state.demo_products, pd.DataFrame([new_item])], ignore_index=True)
                    st.success(f"تمت إضافة ({prod_name}) بنجاح إلى المنيو!")
                    st.rerun()

        st.divider()
        st.subheader("📋 قائمة المنتجات والمخزون الحالي")
        st.dataframe(get_products(), use_container_width=True)

# --- TAB 3: REPORTS & ANALYTICS ---
if tab_reports is not None:
    with tab_reports:
        st.subheader("📊 إحصائيات وتقارير المبيعات المحفوظة")
        sales_df = get_sales()
        
        if sales_df.empty:
            st.info("لا توجد مبيعات مسجلة حتى الآن.")
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("إجمالي المبيعات", f"{sales_df['total_price'].sum():.2f} ج.م")
            m2.metric("إجمالي الأرباح", f"{sales_df['profit'].sum():.2f} ج.م")
            m3.metric("عدد العمليات", f"{len(sales_df)}")
            
            st.divider()
            fig = px.bar(sales_df, x="product_name", y="total_price", color="product_name", title="📈 توزيع المبيعات حسب المنتج")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📜 سجل العمليات التفصيلي")
            st.dataframe(sales_df, use_container_width=True)
