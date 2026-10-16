
import streamlit as st

st.set_page_config(page_title="PEWS Calculator", page_icon="🏥", layout="centered")

st.title("🏥 ระบบประมวลผลคะแนน PEWS")
st.write("กรอกข้อมูลสัญญาณชีพด้านล่างเพื่อประเมินคะแนนตามเกณฑ์อายุและแสดงแถบสี")
st.divider()

age_group = st.selectbox(
    "เลือกช่วงอายุ:",
    [
        "น้อยกว่า 4 เดือน",
        "4 เดือน - 2 ปี",
        "2 ปี - 5 ปี",
        "5 ปี - 12 ปี",
        "มากกว่า 12 ปี",
    ],
)

col1, col2 = st.columns(2)
with col1:
    bt = st.number_input("อุณหภูมิร่างกาย (BT - °C)", value=37.0, step=0.1)
    hr = st.number_input("อัตราการเต้นของหัวใจ (HR - ครั้ง/นาที)", value=100, step=1)
with col2:
    rr = st.number_input("อัตราการหายใจ (RR -ครั้ง/นาที)", value=25, step=1)
    crt = st.selectbox("Capillary Refill Time (CRT)", ["< 2 วินาที", "3 - 4 วินาที", "> 4 วินาที"])

def get_badge(score):
    if score == 0:
        return '<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">0 - สีเขียว</span>'
    elif score == 1:
        return '<span style="background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 5px; font-weight: bold;">1 - สีเหลือง</span>'
    else:
        return '<span style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">3 - สีแดง</span>'

def calc_bt(val):
    if val < 35.5: return 3
    elif 35.5 <= val <= 35.9: return 1
    elif 35.9 < val <= 37.9: return 0
    elif 38.5 <= val <= 39.0: return 1
    elif val > 39.0: return 3
    return 0

def calc_hr(age, val):
    if age == "น้อยกว่า 4 เดือน":
        if val < 80: return 3
        elif val <= 109: return 1
        elif val <= 159: return 0
        elif val <= 190: return 1
        return 3
    elif age == "4 เดือน - 2 ปี":
        if val < 80: return 3
        elif val <= 99: return 1
        elif val <= 149: return 0
        elif val <= 180: return 1
        return 3
    elif age == "2 ปี - 5 ปี":
        if val < 60: return 3
        elif val <= 79: return 1
        elif val <= 119: return 0
        elif val <= 150: return 1
        return 3
    elif age == "5 ปี - 12 ปี":
        if val < 60: return 3
        elif val <= 69: return 1
        elif val <= 119: return 0
        elif val <= 150: return 1
        return 3
    else:
        if val < 60: return 3
        elif val <= 69: return 1
        elif val <= 99: return 0
        elif val <= 150: return 1
        return 3

def calc_rr(age, val):
    if age == "น้อยกว่า 4 เดือน":
        if val < 20: return 3
        elif val <= 29: return 1
        elif val <= 39: return 0
        elif val <= 54: return 1
        return 3
    elif age == "4 เดือน - 2 ปี":
        if val < 15: return 3
        elif val <= 24: return 1
        elif val <= 34: return 0
        elif val <= 55: return 1
        return 3
    elif age == "2 ปี - 5 ปี" or age == "5 ปี - 12 ปี":
        if val < 10: return 3
        elif val <= 19: return 1
        elif val <= 29: return 0
        elif val <= 45: return 1
        return 3
    else:
        if val < 10: return 3
        elif val <= 15: return 1
        elif val <= 25: return 0
        elif val <= 45: return 1
        return 3

def calc_crt(val):
    if val == "< 2 วินาที": return 0
    elif val == "3 - 4 วินาที": return 1
    return 3

if st.button("ประมวลผลคะแนน", type="primary"):
    score_bt = calc_bt(bt)
    score_hr = calc_hr(age_group, hr)
    score_rr = calc_rr(age_group, rr)
    score_crt = calc_crt(crt)
    total_score = score_bt + score_hr + score_rr + score_crt

    st.subheader("📊 ผลการประมวลผล")
    st.markdown(f"""
    - **อุณหภูมิร่างกาย (BT):** {bt} °C $\rightarrow$ {get_badge(score_bt)}
    - **อัตราการเต้นของหัวใจ (HR):** {hr} ครั้ง/นาที $\rightarrow$ {get_badge(score_hr)}
    - **อัตราการหายใจ (RR):** {rr} ครั้ง/นาที $\rightarrow$ {get_badge(score_rr)}
    - **CRT:** {crt} $\rightarrow$ {get_badge(score_crt)}
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### 🎯 คะแนนรวมทั้งหมด: **{total_score} คะแนน**", unsafe_allow_html=True)