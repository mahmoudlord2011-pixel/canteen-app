import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. إعداد قاعدة البيانات الدائمة (SQLite)
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("canteen.db", check_same_thread=False)
    cursor = conn.cursor()
    # جدول المنتجات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            category TEXT,
            price REAL
        )
    """)
    # جدول الطلبات والمبيعات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            items TEXT,
            total_price REAL,
            role TEXT
        )
    """)
    
    # إضافة منتجات افتراضية إذا كانت قاعدة البيانات فارغة
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        default_products = [
            ("ساندوتش جبنة", "🥪 ساندوتشات", 15.0),
            ("ساندوتش بانييه", "🥪 ساندوتشات", 35.0),
            ("عصير فريش", "🥤 مشروبات", 20.0),
            ("زجاجة مياه", "🥤 مشروبات", 7.0),
            ("شيبسي", "🍿 سناكس", 10.0),
            ("بسكويت", "🍿 سناكس", 8.0)
        ]
        cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", default_products)
        conn.commit()
    conn.close()

init_db()

def get_db_connection():
    return sqlite3.connect("canteen.db", check_same_thread=False)

# ---------------------------------------------------------
# 2. ضبط إعدادات الصفحة وحفظ الجلسة في الـ URL
# ---------------------------------------------------------
st.set_page_config(page_title="Smart Canteen - Bright Vision", layout="wide", page_icon="👑")

# استرجاع حالة التسجيل من الـ URL إن وجدت (علشان الدخول التلقائي)
query_params = st.query_params

if 'logged_in' not in st.session_state:
    if 'user' in query_params and 'role' in query_params:
        st.session_state['logged_in'] = True
        st.session_state['user_role'] = query_params['role']
        st.session_state['is_demo'] = (query_params['role'] == 'demo')
    else:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['is_demo'] = False

if 'system_disabled' not in st.session_state:
    st.session_state['system_disabled'] = False

# تنسيقات الواجهة
st.markdown("""
<style>
    .stButton>button { width: 100%; font-size: 16px; border-radius: 8px; }
    .sovereign-card { background-color: #3b0764; border: 2px solid #a855f7; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .status-disabled { background-color: #7f1d1d; color: #fca5a5; padding: 20px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. حالة إيقاف النظام (Kill Switch)
# ---------------------------------------------------------
if st.session_state['system_disabled'] and st.session_state.get('user_role') != 'sovereign':
    st.markdown("""
        <div class="status-disabled">
            <h1>⛔ النظام معطل حالياً ⛔</h1>
            <h3>تم إيقاف تشغيل نظام الكانتين بقرار من المالك الأعظم للنظام (MASTER OODY).</h3>
            <p>يرجى المراجعة مع إدارة النظام لإعادة التشغيل.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")
    with st.expander("🔑 تسجيل دخول المالك لإعادة التفعيل"):
        with st.form("sovereign_unlock"):
            s_user = st.text_input("اسم المالك:")
            s_pass = st.text_input("كلمة السر:", type="password")
            if st.form_submit_button("إلغاء الإيقاف وتفعيل النظام"):
                if s_user == "oody" and s_pass == "Mahmoud@2011":
                    st.session_state['system_disabled'] = False
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = 'sovereign'
                    st.query_params["user"] = "oody"
                    st.query_params["role"] = "sovereign"
                    st.success("تم إعادة تفعيل النظام بنجاح يا ماستر أودي!")
                    st.rerun()
                else:
                    st.error("بيانات غير صحيحة!")
    st.stop()

# ---------------------------------------------------------
# 4. شاشة تسجيل الدخول
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center;'>🔐 تسجيل الدخول - نظام الكانتين الذكي</h1>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("وضع العرض والتجربة (Demo)")
        st.info("تجربة النظام وتسجيل الطلبات دون التغيير في الحسابات الرئيسية.")
        if st.button("🚀 بدء جلسة تجريبية (Demo Mode)", type="primary"):
            st.session_state['logged_in'] = True
            st.session_state['is_demo'] = True
            st.session_state['user_role'] = 'demo'
            st.query_params["user"] = "demo"
            st.query_params["role"] = "demo"
            st.rerun()

    with col2:
        st.subheader("تسجيل دخول الحسابات")
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم:")
            password = st.text_input("كلمة المرور:", type="password")
            submit_login = st.form_submit_button("دخول للنظام")

            if submit_login:
                role = None
                if username == "oody" and password == "Mahmoud@2011":
                    role = 'sovereign'
                elif username == "admin" and password == "Dr.RagabBV842":
                    role = 'admin'
                elif username == "canteen" and password == "canteen 842":
                    role = 'canteen'
                elif username == "student" and password == "student123":
                    role = 'student'
                
                if role:
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = role
                    st.query_params["user"] = username
                    st.query_params["role"] = role
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

# ---------------------------------------------------------
# 5. الواجهة الرئيسية بالتطبيق بعد تسجيل الدخول
# ---------------------------------------------------------
else:
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        if st.session_state['user_role'] == 'sovereign':
            st.markdown("### 👑 مرحباً بك يا **MASTER OODY** | المالك الأعلى للنظام")
        elif st.session_state['is_demo']:
            st.warning("⚠️️ أنت الآن في **وضع التجربة (Demo Mode)**")
        else:
            st.success(f"🟢 تم تسجيل الدخول بصلاحية: **{st.session_state['user_role'].upper()}** (الدخول متذكر تلقائياً 🔓)")
            
    with top_col2:
        if st.button("تسجيل خروج 🚪"):
            st.session_state['logged_in'] = False
            st.session_state['is_demo'] = False
            st.session_state['user_role'] = None
            st.query_params.clear()
            st.rerun()

    # لوحة تحكم المالك (Master Oody)
    if st.session_state['user_role'] == 'sovereign':
        st.markdown("""<div class="sovereign-card">""", unsafe_allow_html=True)
        st.subheader("⚡ لوحة تحكم المالك الأعظم (Master Oody Control)")
        sov_col1, sov_col2 = st.columns(2)
        with sov_col1:
            if not st.session_state['system_disabled']:
                if st.button("🔴 إيقاف النظام بالكامل (Kill Switch)", type="primary"):
                    st.session_state['system_disabled'] = True
                    st.warning("تم إيقاف النظام وحظره عن باقي المستخدمين!")
                    st.rerun()
            else:
                if st.button("🟢 إعادة تفعيل النظام (System Restore)"):
                    st.session_state['system_disabled'] = False
                    st.success("تم تشغيل النظام بنجاح!")
                    st.rerun()
        with sov_col2:
            st.write(f"حالة النظام الحالية: **{'🛑 معطل' if st.session_state['system_disabled'] else '🟢 يعمل بانتظام'}**")
        st.markdown("</div>", unsafe_allow_html=True)

    st.title("🍔 نظام الكانتين الذكي - Bright Vision")
    
    # تحديد التبويبات بناءً على الصلاحيات
    user_role = st.session_state['user_role']
    
    tabs_to_show = ["🛒 قائمة الطلبات (المنيو)"]
    if user_role in ['sovereign', 'canteen', 'admin', 'demo']:
        tabs_to_show.append("📊 المبيعات والتقارير")
    if user_role in ['sovereign', 'canteen', 'demo']:
        tabs_to_show.append("⚙️ إدارة المنتجات")
        
    created_tabs = st.tabs(tabs_to_show)
    conn = get_db_connection()

    # --- TAB 1: شراء المنتجات وتسجيل الطلب ---
    with created_tabs[0]:
        st.header("تسجيل طلب جديد")
        df_prod = pd.read_sql("SELECT * FROM products", conn)
        
        if df_prod.empty:
            st.info("لا توجد منتجات مسجلة في المنيو حتى الآن.")
        else:
            selected_items = []
            categories = df_prod['category'].unique()
            cols = st.columns(len(categories) if len(categories) > 0 else 1)
            
            for idx, cat in enumerate(categories):
                with cols[idx % len(cols)]:
                    st.subheader(cat)
                    cat_items = df_prod[df_prod['category'] == cat]
                    for _, row in cat_items.iterrows():
                        if st.checkbox(f"{row['name']} - {row['price']} ج.م", key=f"p_{row['id']}"):
                            selected_items.append(row)
            
            if selected_items:
                total = sum(item['price'] for item in selected_items)
                items_str = ", ".join([item['name'] for item in selected_items])
                st.write(f"### الإجمالي: **{total} ج.م**")
                
                if st.button("إتمام الطلب وحفظه 💳", type="primary"):
                    cursor = conn.cursor()
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO orders (timestamp, items, total_price, role) VALUES (?, ?, ?, ?)",
                                   (now_str, items_str, total, user_role))
                    conn.commit()
                    st.balloons()
                    st.success("تم تسجيل الطلب وحفظه بنجاح في قاعدة البيانات! 🎉")

    # --- TAB 2: عرض تقارير المبيعات (Master Oody + الكانتين + الأدمن) ---
    if "📊 المبيعات والتقارير" in tabs_to_show:
        tab_idx = tabs_to_show.index("📊 المبيعات والتقارير")
        with created_tabs[tab_idx]:
            st.header("📊 إحصائيات وتقارير المبيعات المحفوظة")
            df_orders = pd.read_sql("SELECT * FROM orders ORDER BY id DESC", conn)
            
            if df_orders.empty:
                st.info("لا توجد مبيعات مسجلة حتى الآن.")
            else:
                total_sales = df_orders['total_price'].sum()
                total_count = len(df_orders)
                
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("إجمالي المبيعات المحفوظة", f"{total_sales:.2f} ج.م")
                m_col2.metric("عدد الطلبات الكلي", f"{total_count} طلب")
                
                st.subheader("سجل الطلبات الأخير:")
                st.dataframe(df_orders, use_container_dict=True)

    # --- TAB 3: إضافة المنتجات (Master Oody + الكانتين فقط) ---
    if "⚙️ إدارة المنتجات" in tabs_to_show:
        tab_idx = tabs_to_show.index("⚙️ إدارة المنتجات")
        with created_tabs[tab_idx]:
            st.header("⚙️ إضافة منتج جديد للمنيو")
            with st.form("add_product_form"):
                p_name = st.text_input("اسم المنتج:")
                p_cat = st.selectbox("القسم:", ["🥪 ساندوتشات", "🥤 مشروبات", "🍿 سناكس", "حلويات 🍫"])
                p_price = st.number_input("السعر (ج.م):", min_value=1.0, value=10.0, step=0.5)
                submit_p = st.form_submit_button("إضافة للمنيو")
                
                if submit_p and p_name:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                                       (p_name, p_cat, p_price))
                        conn.commit()
                        st.success(f"تم إضافة {p_name} بنجاح ولن يتم مسحه!")
                        st.rerun()
                    except Exception as e:
                        st.error("هذا المنتج موجود بالفعل أو حدث خطأ!")

    conn.close()
