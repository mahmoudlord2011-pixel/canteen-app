import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Smart Canteen - Bright Vision", layout="wide", page_icon="🍔")

# تنسيقات واجهة المظهر والتصميم
st.markdown("""
<style>
    .stButton>button { width: 100%; font-size: 16px; border-radius: 8px; }
    .demo-card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; }
    .price-tag { color: #2e7d32; font-weight: bold; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# إدارة حالة الجلسة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'is_demo' not in st.session_state:
    st.session_state['is_demo'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

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
            st.session_state['user_role'] = 'admin'
            st.rerun()

    # العمود الثاني: تسجيل الدخول الفعلي
    with col2:
        st.subheader("تسجيل دخول الإدارة والمشرفين")
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم:")
            password = st.text_input("كلمة المرور:", type="password")
            submit_login = st.form_submit_button("دخول كمسؤول (تعديل وحفظ فعلي)")

            if submit_login:
                if username == "admin" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'admin'
                    st.rerun()
                elif username == "canteen" and password == "canteen123":
                    st.session_state['logged_in'] = True
                    st.session_state['is_demo'] = False
                    st.session_state['user_role'] = 'canteen'
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

# ---- الشاشة الثانية: واجهة التطبيق الرئيسية بعد الدخول ----
else:
    # شريط علوي موضح نوع الجلسة
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        if st.session_state['is_demo']:
            st.warning("⚠️ أنت الآن في **وضع التجربة (Demo Mode)** - التغييرات لن تحفظ في البيانات الأساسية.")
        else:
            st.success("🟢 تم تسجيل الدخول الفعلي كـ مسؤول النظام.")
    with top_col2:
        if st.button("خروج 🚪"):
            st.session_state['logged_in'] = False
            st.session_state['is_demo'] = False
            st.session_state['user_role'] = None
            st.rerun()

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
