import streamlit as st
import pandas as pd
from datetime import datetime

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Smart Canteen - Bright Vision", layout="wide", page_icon="👑")

# إدارة حالة الجلسة والإيقاف الطارئ للنظام (Kill Switch)
if 'system_disabled' not in st.session_state:
    st.session_state['system_disabled'] = False

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'is_demo' not in st.session_state:
    st.session_state['is_demo'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

# تنسيقات واجهة المظهر والتصميم
st.markdown("""
<style>
    .stButton>button { width: 100%; font-size: 16px; border-radius: 8px; }
    .sovereign-card { background-color: #3b0764; border: 2px solid #a855f7; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .status-disabled { background-color: #7f1d1d; color: #fca5a5; padding: 20px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ---- في حالة إيقاف النظام بالكامل من قبل Oody ----
if st.session_state['system_disabled'] and st.session_state.get('user_role') != 'sovereign':
    st.markdown("""
        <div class="status-disabled">
            <h1>⛔ النظام معطل حالياً ⛔</h1>
            <h3>تم إيقاف تشغيل نظام الكانتين بقرار من المالك الأعلى للنظام (OODY_SOVEREIGN).</h3>
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
                    st.success("تم إعادة تفعيل النظام بنجاح!")
                    st.rerun()
                else:
                    st.error("بيانات غير صحيحة!")
    st.stop()

# ---- الشاشة الأولى: تسجيل الدخول ووضع التجربة (Demo) ----
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center;'>🔐 تسجيل الدخول - نظام الكانتين الذكي</h1>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    # العمود الأول: وضع العرض والتجربة Demo Mode
    with col1:
        st.subheader("وضع العرض والتجربة (Demo)")
        st.info("يمكنك تجربة النظام بالكامل، استعراض المنيو، وتسجيل الطلبات التجريبية والتقارير دون التأثير على البيانات الحقيقية للكانتين.")
        
        if st.button("🚀 بدء جلسة تجريبية (Demo Mode)", type="primary"):
            st.session_state['logged_in'] = True
            st.session_state['is_demo'] = True
            st.session_state['user_role'] = 'demo'
            st.rerun()

    # العمود الثاني: تسجيل دخول الحسابات (إدارة / كانتين / المالك / طلاب)
    with col2:
        st.subheader("تسجيل دخول الإدارة والمشرفين")
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم:")
            password = st.text_input("كلمة المرور:", type="password")
            submit_login = st.form_submit_button("دخول للنظام")

            if submit_login:
                # 👑 الحساب الفخم الخاص بـ Oody
                if username == "oody" and password == "Mahmoud@2011":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'sovereign'
                    st.rerun()
                # ⚙️ حساب الأدمن (د. رجب)
                elif username == "admin" and password == "Dr.RagabBV842":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'admin'
                    st.rerun()
                # 🍔 حساب الكانتين
                elif username == "canteen" and password == "canteen 842":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'canteen'
                    st.rerun()
                # 🎓 حساب الطلاب
                elif username == "student" and password == "student123":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'student'
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

# ---- الشاشة الثانية: واجهة التطبيق الرئيسية بعد الدخول ----
else:
    # شريط علوي موضح نوع الجلسة
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        if st.session_state['user_role'] == 'sovereign':
            st.markdown("### 👑 مرحباً بك يا **OODY SOVEREIGN** | المالك الأعلى للنظام")
        elif st.session_state['is_demo']:
            st.warning("⚠️ أنت الآن في **وضع التجربة (Demo Mode)** - التغييرات لن تحفظ في البيانات الأساسية.")
        else:
            st.success(f"🟢 تم تسجيل الدخول بصلاحية: **{st.session_state['user_role'].upper()}**")
            
    with top_col2:
        if st.button("خروج 🚪"):
            st.session_state['logged_in'] = False
            st.session_state['is_demo'] = False
            st.session_state['user_role'] = None
            st.rerun()

    # 🔴 لوحة التحكم الخاصة بالمالك (Oody) لتعطيل/تفعيل النظام بضغطة زر
    if st.session_state['user_role'] == 'sovereign':
        st.markdown("""<div class="sovereign-card">""", unsafe_allow_html=True)
        st.subheader("⚡ لوحة التحكم المطلقة (Sovereign Control)")
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
    
    # قائمة التنقل بالأقسام
    tab1, tab2, tab3 = st.tabs(["🛒 قائمة الطلبات (المنيو)", "📊 لوحة التحكم والمبيعات", "⚙️ إدارة المنتجات"])

    with tab1:
        st.header("تسجيل طلب جديد")
        st.write("اختر الوجبات والمشروبات المطلوبة:")
        col_item1, col_item2, col_item3 = st.columns(3)
        with col_item1:
            st.subheader("🥪 ساندوتشات")
            st.checkbox("ساندوتش جبنة - 15 ج.م")
            st.checkbox("ساندوتش بانييه - 35 ج.م")
        with col_item2:
            st.subheader("🥤 مشروبات")
            st.checkbox("عصير فريش - 20 ج.م")
            st.checkbox("زجاجة مياه - 7 ج.م")
        with col_item3:
            st.subheader("🍿 سناكس")
            st.checkbox("شيبسي - 10 ج.م")
            st.checkbox("بسكويت - 8 ج.م")
        
        if st.button("إتمام الطلب 💳"):
            st.balloons()
            st.success("تم تسجيل الطلب بنجاح!")

    with tab2:
        st.header("📊 إحصائيات مبيعات اليوم")
        st.metric(label="إجمالي مبيعات اليوم", value="1,450 ج.م", delta="+12%")
        st.metric(label="عدد الطلبات المكتملة", value="48 طلب", delta="+5")

    with tab3:
        st.header("⚙️ إضافة/تعديل المنتجات")
        st.text_input("اسم المنتج الجديد:")
        st.number_input("السعر (ج.م):", min_value=1, value=10)
        if st.button("حفظ المنتج"):
            st.success("تمت إضافة المنتج بنجاح إلى المنيو!")
