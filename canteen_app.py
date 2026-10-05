import streamlit as st
import pandas as pd
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
# Supabase Secrets / Config (سحابي / محلي)
# ---------------------------------------------------------
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
except Exception:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # Options: 'master', 'ragab', 'canteen'

if "system_killed" not in st.session_state:
    st.session_state.system_killed = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if "menu_items" not in st.session_state:
    st.session_state.menu_items = [
        {"id": 1, "name": "ساندوتش بطاطس", "price": 20, "cost": 10},
        {"id": 2, "name": "باكت بطاطس", "price": 15, "cost": 8}
    ]

if "kitchen_orders" not in st.session_state:
    st.session_state.kitchen_orders = []

# ---------------------------------------------------------
# Authentication Screen
# ---------------------------------------------------------
if st.session_state.user_role is None:
    st.title("Bright Vision 🍔 - تسجيل الدخول")
    
    role_choice = st.selectbox("اختر نوع الحساب:", ["Master Admin (Oody)", "Dr. Ragab", "كاشير / كانتين"])
    password = st.text_input("كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول"):
        if role_choice == "Master Admin (Oody)" and password == "oody123":
            st.session_state.user_role = "master"
            st.rerun()
        elif role_choice == "Dr. Ragab" and password == "ragab123":
            st.session_state.user_role = "ragab"
            st.rerun()
        elif role_choice == "كاشير / كانتين" and password == "canteen123":
            st.session_state.user_role = "canteen"
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")

else:
    # ---------------------------------------------------------
    # Top Bar & Logout
    # ---------------------------------------------------------
    col_user, col_logout = st.columns([8, 2])
    with col_user:
        if st.session_state.user_role == "master":
            st.markdown("### 👑 **MASTER OODY** (صلاحيات كاملة)")
        elif st.session_state.user_role == "ragab":
            st.markdown("### 👨‍🏫 **Dr. Ragab**")
        else:
            st.markdown("### 🍔 **قسم الكانتين والمطبخ**")

    with col_logout:
        if st.button("تسجيل الخروج 🚪"):
            st.session_state.user_role = None
            st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # 1. Master Control Panel (Kill Switch حصري لك أنت فقط!)
    # ---------------------------------------------------------
    # يظهر فقط إذا كان المستخدم master وليس عند دكتور رجب
    if st.session_state.user_role == "master":
        st.subheader("⚡ لوحة التحكم المطلقة (Master Control)")
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            if st.button("🚨 إيقاف النظام بالكامل (Kill Switch)", use_container_width=True, type="primary"):
                st.session_state.system_killed = True
                st.warning("تم إيقاف النظام بالكامل بواسطة الماستر!")
                
        with col_k2:
            if st.button("🟢 تشغيل النظام بالكامل", use_container_width=True):
                st.session_state.system_killed = False
                st.success("النظام يعمل حالياً بشكل طبيعي.")

        st.divider()

    # فحص حالة Kill Switch
    if st.session_state.system_killed and st.session_state.user_role != "master":
        st.error("⚠️ النظام معطل حالياً من قبل الإدارة العليا (Master Admin).")
    else:
        # ---------------------------------------------------------
        # 2. Bright Vision - نظام الكانتين الذكي (المنيو والطلبات)
        # ---------------------------------------------------------
        st.title("🍔 Bright Vision - نظام الكانتين الذكي")

        tabs = st.tabs(["📝 المنيو وطلب جديد", "🧑‍🍳 شاشة المطبخ والطلبات", "⚙️ إدارة المنتجات والتقارير"])

        # TAB 1: المنيو وطلب جديد
        with tabs[0]:
            st.subheader("📋 قائمة الوجبات والمنتجات")
            
            # عرض المنتجات للطلب
            cols = st.columns(2)
            for idx, item in enumerate(st.session_state.menu_items):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"### {item['name']}")
                        st.markdown(f"🏷️ **{item['price']} ج.م**")
                        if st.button(f"إضافة +", key=f"add_{item['id']}"):
                            st.session_state.cart.append(item)
                            st.success(f"تمت إضافة {item['name']} للسلة")

            st.divider()
            st.subheader("🛒 سلة الطلبات الحالية")
            
            if len(st.session_state.cart) == 0:
                st.info("السلة فارغة حالياً.")
            else:
                total_price = sum(item['price'] for item in st.session_state.cart)
                for c_item in st.session_state.cart:
                    st.write(f"• {c_item['name']} ({c_item['price']} ج.م)")
                
                st.markdown(f"### 🟢 **الإجمالي: {total_price} ج.م**")
                
                student_info = st.text_input("اسم الطالب والصف (مثال: ma 10-a):")
                paid_amount = st.number_input("المبلغ المدفوع (معاك كام؟):", min_value=0.0, value=float(total_price))
                
                remaining = paid_amount - total_price

                if st.button("🚀 إرسال الطلب للكانتين", type="primary", use_container_width=True):
                    if not student_info:
                        st.error("يرجى إدخال اسم الطالب والصف!")
                    else:
                        new_order = {
                            "id": len(st.session_state.kitchen_orders) + 1,
                            "student": student_info,
                            "items": [item['name'] for item in st.session_state.cart],
                            "total": total_price,
                            "paid": paid_amount,
                            "remaining": remaining,
                            "time": datetime.now().strftime("%I:%M %p")
                        }
                        st.session_state.kitchen_orders.append(new_order)
                        st.session_state.cart = []
                        st.success("تم إرسال الطلب بنجاح للمطبخ! 🎉")
                        st.rerun()

        # TAB 2: شاشة المطبخ والطلبات
        with tabs[1]:
            st.subheader("🧑‍🍳 شاشة المطبخ والطلبات")
            
            if len(st.session_state.kitchen_orders) == 0:
                st.info("لا توجد طلبات معلقة حالياً.")
            else:
                for order in st.session_state.kitchen_orders:
                    with st.container(border=True):
                        st.markdown(f"### 📦 طلب: **{order['student']}**")
                        items_str = "، ".join(order['items'])
                        st.write(f"**الأصناف:** {items_str}")
                        st.write(f"**الحساب:** {order['total']} ج.م | **المدفوع:** {order['paid']} ج.م")
                        
                        st.success(f"🟡 **الباقي للطلب: {order['remaining']} ج.م**")
                        st.caption(f"⏰ الوقت: {order['time']}")
                        
                        col_b1, col_b2 = st.columns([2, 1])
                        with col_b1:
                            if st.button("✅ إتمام وتقديم الطلب", key=f"done_{order['id']}"):
                                st.session_state.kitchen_orders = [o for o in st.session_state.kitchen_orders if o['id'] != order['id']]
                                st.success("تم إتمام الطلب!")
                                st.rerun()
                        with col_b2:
                            if st.button("🗑️ حذف", key=f"del_{order['id']}"):
                                st.session_state.kitchen_orders = [o for o in st.session_state.kitchen_orders if o['id'] != order['id']]
                                st.rerun()

        # TAB 3: إدارة المنتجات والتقارير
        with tabs[2]:
            st.subheader("⚙️ إضافة منتج جديد للمنيو")
            new_name = st.text_input("اسم المنتج:")
            new_cost = st.number_input("سعر التكلفة (ج.م):", min_value=0.0, value=10.0)
            new_price = st.number_input("سعر البيع (ج.م):", min_value=0.0, value=20.0)
            
            if st.button("➕ إضافة للمنيو"):
                if new_name:
                    st.session_state.menu_items.append({
                        "id": len(st.session_state.menu_items) + 1,
                        "name": new_name,
                        "price": new_price,
                        "cost": new_cost
                    })
                    st.success(f"تمت إضافة {new_name} للمنيو بنجاح!")
                    st.rerun()
