import streamlit as st
from datetime import datetime
import pandas as pd
import os
import json

st.set_page_config(page_title="Smart Canteen - Bright Vision", layout="wide")

# تنسيقات الواجهة
st.markdown("""
    <style>
    div[data-testid="stButton"] button[kind="primary"] { background-color: #28a745 !important; color: white !important; border: none !important; }
    div[data-testid="stButton"] button[kind="secondary"] { background-color: #dc3545 !important; color: white !important; border: none !important; }
    .price-tag { color: #2e7d32; font-weight: bold; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# ----------------- 📁 إدارة قاعدة البيانات والداتا الدائمة -----------------
ORDERS_FILE = "pending_orders.json"
SALES_FILE = "daily_sales.csv"
STATUS_FILE = "system_status.json"

# 1. تحميل الطلبات المعلقة المحفوظة
def load_pending_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# 2. حفظ الطلبات المعلقة
def save_pending_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

# 3. تحميل المبيعات المكتملة والسجل التاريخي
def load_completed_sales():
    if os.path.exists(SALES_FILE):
        try:
            return pd.read_csv(SALES_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# 4. حفظ أمر بيع جديد في السجل الدائم
def save_completed_sale(order_data):
    df_new = pd.DataFrame([order_data])
    if not os.path.isfile(SALES_FILE):
        df_new.to_csv(SALES_FILE, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(SALES_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

# 5. إدارة حالة الموقع (شغال / مقفول)
def get_system_status():
    if not os.path.exists(STATUS_FILE):
        return True
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f).get("is_active", True)
    except:
        return True

def set_system_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump({"is_active": status}, f)

# ----------------- تهيئة الجلسة والداتا في الذاكرة -----------------
if "cart" not in st.session_state: st.session_state.cart = []
if "total_price" not in st.session_state: st.session_state.total_price = 0
if "play_bell" not in st.session_state: st.session_state.play_bell = False

# بيانات الحسابات والصلاحيات (3 حسابات)
USERS = {
    "student": {"password": "123", "role": "student", "name": "حساب الفصل/الطلاب"},
    "canteen": {"password": "admin", "role": "canteen", "name": "إدارة الكانتين والمطبخ"},
    "owner": {"password": "supersecret", "role": "owner", "name": "مالك النظام (أنت)"}
}

# قراءة الحساب المحفوظ تلقائياً
query_params = st.query_params
if "saved_role" in query_params and query_params["saved_role"] in USERS:
    st.session_state.logged_in = True
    st.session_state.user_role = USERS[query_params["saved_role"]]["role"]
else:
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "user_role" not in st.session_state: st.session_state.user_role = None

# ----------------- 🔑 1. شاشة تسجيل الدخول -----------------
if not st.session_state.logged_in:
    st.title("🏫 نظام الكانتين الذكي - تسجيل الدخول")
    
    with st.form("login_form"):
        username_input = st.text_input("اسم المستخدم (Username):")
        password_input = st.text_input("كلمة المرور (Password):", type="password")
        remember_me = st.checkbox("تذكرني على هذا الجهاز 📌", value=True)
        
        submit_button = st.form_submit_button("تسجيل الدخول 🔓")
        
        if submit_button:
            if username_input in USERS and USERS[username_input]["password"] == password_input:
                role = USERS[username_input]["role"]
                st.session_state.logged_in = True
                st.session_state.user_role = role
                
                if remember_me:
                    st.query_params["saved_role"] = username_input
                    
                st.success(f"أهلاً بك! تم تسجيل الدخول بصفة: {USERS[username_input]['name']}")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")
    st.stop()

# ----------------- زر تسجيل الخروج -----------------
top_col1, top_col2 = st.columns([4, 1])
with top_col1:
    st.title("🏫 نظام الكانتين الذكي - مدرسة برايت فيجن")
with top_col2:
    if st.button("تسجيل الخروج 🚪"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.query_params.clear()
        st.rerun()

# ----------------- 🔒 التحقق من حالة اشتراك الخدمة -----------------
is_system_active = get_system_status()

if not is_system_active and st.session_state.user_role != "owner":
    st.error("⛔ تم إيقاف الخدمة مؤقتاً لانتهاء فترة الاشتراك الشهرية.")
    st.warning("يرجى التواصل مع مدير النظام لتجديد الاشتراك وإعادة التفعيل.")
    st.stop()

# ----------------- 👑 2. لوحة تحكم المالك (Super Admin) -----------------
if st.session_state.user_role == "owner":
    st.header("⚙️ لوحة تحكم المالك (Owner Dashboard)")
    st.subheader("إدارة اشتراك المدرسة والتحكم في الخدمة")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**حالة النظام الحالية:** {'🟢 نشط وشغال' if is_system_active else '🔴 متوقف (مقفول)'}")
    
    with c2:
        if is_system_active:
            if st.button("🔴 إيقاف الخدمة عن المدرسة (قفل الموقع)", type="secondary"):
                set_system_status(False)
                st.warning("تم قفل الموقع عن الطلاب والكانتين!")
                st.rerun()
        else:
            if st.button("🟢 تفعيل الخدمة (فتح الموقع بعد استلام الفلوس)", type="primary"):
                set_system_status(True)
                st.success("تم إعادة فتح الموقع بنجاح!")
                st.rerun()

    st.divider()
    st.subheader("📂 البيانات الدائمة المحفوظة:")
    df_sales = load_completed_sales()
    if not df_sales.empty:
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")

# ----------------- 📱 3. واجهة الطلاب -----------------
elif st.session_state.user_role == "student":
    st.header("📱 تابلت الفصل - طلب الأكل")
    student_name = st.text_input("اسم الطالب:")
    student_class = st.text_input("الفصل (مثال: 10-A):")
    search_query = st.text_input("🔍 ابحث عن صنف في المنيو:")
    
    st.subheader("📋 المنيو:")
    menu = {
        "🥔 قائمة البطاطس": [{"name": "سندوتش بطاطس", "price": 20, "image": "https://i.postimg.cc/qvB2RrSL/631278072773975479.jpg"}],
        "🧃 العصائر": [{"name": "عصير تفاح جهينة", "price": 15, "image": "https://i.postimg.cc/t4RFTbwB/N40871218A.jpg"}]
    }

    tabs = st.tabs(list(menu.keys()))
    for tab, (category, items) in zip(tabs, menu.items()):
        with tab:
            filtered_items = [item for item in items if search_query.lower() in item['name'].lower()]
            for item in filtered_items:
                c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                c2.write(f"**{item['name']}**")
                c2.markdown(f"<span class='price-tag'>🏷️ {item['price']} ج.م</span>", unsafe_allow_html=True)
                if c3.button("➕ إضافة", key=f"add_{item['name']}", type="primary"):
                    st.session_state.cart.append(f"{item['name']}")
                    st.session_state.total_price += item['price']
                    st.rerun()
                if c4.button("➖ حذف", key=f"del_{item['name']}", type="secondary"):
                    if item['name'] in st.session_state.cart:
                        st.session_state.cart.remove(item['name'])
                        st.session_state.total_price -= item['price']
                        st.rerun()

    st.divider()
    st.subheader("🛒 سلة الطلبات الحالية:")
    for cart_item in st.session_state.cart: st.write(f"• {cart_item}")
    special_notes = st.text_input("📝 ملاحظات خاصة:")
    st.markdown(f"### 💵 الإجمالي: {st.session_state.total_price} ج.م")
    paid_amount = st.number_input("المبلغ المدفوع:", min_value=0, value=0)
    
    if st.button("🚀 إرسال الطلب للكانتين", use_container_width=True, type="primary"):
        if not student_name or not student_class or not st.session_state.cart:
            st.error("تاكد من إدخال كافة البيانات والسلة ليست فارغة!")
        else:
            pending_orders = load_pending_orders()
            pending_orders.append({
                "student_name": student_name, "student_class": student_class,
                "items": "، ".join(st.session_state.cart),
                "items_list": list(st.session_state.cart),
                "notes": special_notes if special_notes else "لا يوجد",
                "total": st.session_state.total_price, "paid": paid_amount,
                "change": paid_amount - st.session_state.total_price,
                "time": datetime.now().strftime("%I:%M %p")
            })
            save_pending_orders(pending_orders)
            st.session_state.cart = []
            st.session_state.total_price = 0
            st.success("✅ تم إرسال الطلب للكانتين وبنفس الوقت تم حفظه بشكل دائم!")
            st.rerun()

# ----------------- 👨‍🍳 4. واجهة الكانتين والمطبخ -----------------
elif st.session_state.user_role == "canteen":
    st.header("👨‍🍳 شاشة المطبخ والطلبات الواردة")
    
    pending_orders = load_pending_orders()
    
    if not pending_orders:
        st.info("لا توجد طلبات معلقة حالياً ☕")
    else:
        for idx, order in enumerate(pending_orders):
            with st.container(border=True):
                st.subheader(f"🔔 طلب جديد: {order['student_name']} ({order['student_class']})")
                st.write(f"**الأصناف:** {order['items']}")
                st.write(f"**📌 ملاحظات:** {order['notes']}")
                st.write(f"**الحساب:** {order['total']} ج.م | **المدفوع:** {order['paid']} ج.م")
                st.success(f"**الباقي للطلب:** {order['change']} ج.م 🪙")
                st.caption(f"⏰ الوقت: {order['time']}")
                
                if st.button("إتمام وتقديم الطلب ✅", key=f"done_{idx}"):
                    completed_order = pending_orders.pop(idx)
                    save_pending_orders(pending_orders) # تحديث قائمة المطبخ
                    save_completed_sale(completed_order) # حفظ المبيعات نهائياً في الداتابيز
                    st.rerun()

    st.divider()
    st.header("📊 إحصائيات المبيعات التراكمية والدائمة")

    df_sales = load_completed_sales()

    if df_sales.empty:
        st.write("_لا توجد مبيعات مكتملة بعد_")
    else:
        m1, m2 = st.columns(2)
        m1.metric("إجمالي الطلبات المكتملة 📦", len(df_sales))
        m2.metric("إجمالي المبيعات (الأرباح) 💰", f"{df_sales['total'].sum()} ج.م")

        st.subheader("📈 الرسوم البيانية التراكمية:")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("🏆 **أكثر الأصناف مبيعاً:**")
            # استخراج قائمة الأصناف من الداتابيز
            all_items = []
            for items_str in df_sales['items']:
                all_items.extend(items_str.split("، "))
            df_items = pd.DataFrame(all_items, columns=["الصنف"]).value_counts().reset_index()
            df_items.columns = ["الصنف", "الكمية المباعة"]
            st.bar_chart(df_items.set_index("الصنف"))
            
        with chart_col2:
            st.write("🏫 **إجمالي المبيعات حسب الفصل:**")
            df_classes = df_sales.groupby("student_class")["total"].sum().reset_index()
            df_classes.columns = ["الفصل", "المبيعات (ج.م)"]
            st.bar_chart(df_classes.set_index("الفصل"))

        st.subheader("📑 السجل الكامل للمبيعات التاريخية:")
        st.dataframe(df_sales[['student_name', 'student_class', 'items', 'notes', 'total', 'time']], use_container_width=True)
