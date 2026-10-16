import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="PEWS Calculator", page_icon="🏥", layout="centered"
)

st.title("🏥 ระบบประมวลผลคะแนน PEWS")
st.write("กรอกข้อมูลสัญญาณชีพด้านล่างเพื่อประเมินคะแนนตามเกณฑ์อายุและแสดงผลลัพธ์")
st.divider()

# ฟังก์ชันสำหรับรีเซ็ตค่าใน session_state
def reset_form():
    st.session_state.age_group = "น้อยกว่า 4 เดือน"
    st.session_state.bt_val = None
    st.session_state.hr_val = None
    st.session_state.rr_val = None
    st.session_state.crt_val = None

# กำหนดค่าเริ่มต้นใน session_state
if 'age_group' not in st.session_state:
    st.session_state.age_group = "น้อยกว่า 4 เดือน"
if 'bt_val' not in st.session_state:
    st.session_state.bt_val = None
if 'hr_val' not in st.session_state:
    st.session_state.hr_val = None
if 'rr_val' not in st.session_state:
    st.session_state.rr_val = None
if 'crt_val' not in st.session_state:
    st.session_state.crt_val = None

# 1. เลือกช่วงอายุ
age_group = st.selectbox(
    "เลือกช่วงอายุ:",
    [
        "น้อยกว่า 4 เดือน",
        "4 เดือน - 2 ปี",
        "2 ปี - 5 ปี",
        "5 ปี - 12 ปี",
        "มากกว่า 12 ปี",
    ],
    key='age_group'
)

# ช่องกรอกข้อมูลสัญญาณชีพ (ค่าเริ่มต้นเป็นช่องว่าง/None)
col1, col2 = st.columns(2)
with col1:
    bt = st.number_input("อุณหภูมิร่างกาย (BT - °C)", value=st.session_state.bt_val, step=0.1, placeholder="กรอกค่า BT...", key='bt_val')
    hr = st.number_input("อัตราการเต้นของหัวใจ (HR - ครั้ง/นาที)", value=st.session_state.hr_val, step=1, placeholder="กรอกค่า HR...", key='hr_val')
with col2:
    rr = st.number_input("อัตราการหายใจ (RR - ครั้ง/นาที)", value=st.session_state.rr_val, step=1, placeholder="กรอกค่า RR...", key='rr_val')
    crt = st.number_input("Capillary Refill Time (CRT - วินาที)", value=st.session_state.crt_val, step=0.1, placeholder="กรอกค่า CRT...", key='crt_val')


# ฟังก์ชันแสดงผลป้ายกำกับสีสำหรับแต่ละหัวข้อ
def get_badge(score):
    if score == 0:
        return '<span style="background-color: #28a745; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold;">0 (สีเขียว)</span>'
    elif score == 1:
        return '<span style="background-color: #ffc107; color: black; padding: 4px 10px; border-radius: 4px; font-weight: bold;">1 (สีเหลือง)</span>'
    else:
        return '<span style="background-color: #dc3545; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold;">3 (สีแดง)</span>'


# เงื่อนไข BT (ทุกช่วงอายุใช้เกณฑ์เดียวกัน)
def calc_bt(val):
    if val is None: return 0
    if val < 35.5: return 3
    elif 35.5 <= val <= 35.9: return 1
    elif 35.9 < val <= 37.9: return 0
    elif 38.5 <= val <= 39.0: return 1
    elif val > 39.0: return 3
    return 0


# เงื่อนไข HR ตามช่วงอายุ
def calc_hr(age, val):
    if val is None: return 0
    if age == "น้อยกว่า 4 เดือน":
        if val < 80: return 3
        elif 80 <= val <= 109: return 1
        elif 110 <= val <= 159: return 0
        elif 160 <= val <= 190: return 1
        else: return 3
    elif age == "4 เดือน - 2 ปี":
        if val < 80: return 3
        elif 80 <= val <= 99: return 1
        elif 100 <= val <= 149: return 0
        elif 150 <= val <= 180: return 1
        else: return 3
    elif age == "2 ปี - 5 ปี":
        if val < 60: return 3
        elif 60 <= val <= 79: return 1
        elif 80 <= val <= 119: return 0
        elif 120 <= val <= 150: return 1
        else: return 3
    elif age == "5 ปี - 12 ปี":
        if val < 60: return 3
        elif 60 <= val <= 69: return 1
        elif 70 <= val <= 119: return 0
        elif 120 <= val <= 150: return 1
        else: return 3
    else:  # มากกว่า 12 ปี
        if val < 60: return 3
        elif 60 <= val <= 69: return 1
        elif 70 <= val <= 99: return 0
        elif 100 <= val <= 150: return 1
        else: return 3


# เงื่อนไข RR ตามช่วงอายุ
def calc_rr(age, val):
    if val is None: return 0
    if age == "น้อยกว่า 4 เดือน":
        if val < 20: return 3
        elif 20 <= val <= 29: return 1
        elif 30 <= val <= 39: return 0
        elif 40 <= val <= 54: return 1
        else: return 3
    elif age == "4 เดือน - 2 ปี":
        if val < 15: return 3
        elif 15 <= val <= 24: return 1
        elif 25 <= val <= 34: return 0
        elif 35 <= val <= 55: return 1
        else: return 3
    elif age == "2 ปี - 5 ปี" or age == "5 ปี - 12 ปี":
        if val < 10: return 3
        elif 10 <= val <= 19: return 1
        elif 20 <= val <= 29: return 0
        elif 30 <= val <= 45: return 1
        else: return 3
    else:  # มากกว่า 12 ปี
        if val < 10: return 3
        elif 10 <= val <= 15: return 1
        elif 15 <= val <= 25: return 0
        elif 25 <= val <= 45: return 1
        else: return 3


# เงื่อนไข CRT (รับค่าเป็นตัวเลขวินาที)
def calc_crt(val):
    if val is None: return 0
    if val <= 2: return 0
    elif val <= 3.9: return 1
    else: return 3


# ปุ่มกดประมวลผล และ ปุ่ม Reset
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    process_clicked = st.button("ประมวลผลคะแนน", type="primary", use_container_width=True)
with btn_col2:
    st.button("Reset (ล้างค่า)", on_click=reset_form, use_container_width=True)

if process_clicked:
    score_bt = calc_bt(bt)
    score_hr = calc_hr(age_group, hr)
    score_rr = calc_rr(age_group, rr)
    score_crt = calc_crt(crt)

    total_score = score_bt + score_hr + score_rr + score_crt

    st.subheader("📊 ผลการประมวลผลรายหัวข้อ")
    st.markdown(f"""
    - **อุณหภูมิร่างกาย (BT):** {bt if bt is not None else '-'} °C $\rightarrow$ {get_badge(score_bt)}
    - **อัตราการเต้นของหัวใจ (HR):** {hr if hr is not None else '-'} ครั้ง/นาที $\rightarrow$ {get_badge(score_hr)}
    - **อัตราการหายใจ (RR):** {rr if rr is not None else '-'} ครั้ง/นาที $\rightarrow$ {get_badge(score_rr)}
    - **Capillary Refill Time (CRT):** {crt if crt is not None else '-'} วินาที $\rightarrow$ {get_badge(score_crt)}
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### 🎯 คะแนนรวมทั้งหมด: **{total_score} คะแนน**")

    # แสดงผลสรุปตามคะแนนรวม
    if total_score >= 7:
        st.markdown(
            '<div style="background-color: #dc3545; color: white; padding: 15px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold;">🚨 แถบสีแดง: แจ้งเตือนและประเมินใน 15 นาที</div>',
            unsafe_allow_html=True
        )
    elif total_score <= 4:
        st.markdown(
            '<div style="background-color: #28a745; color: white; padding: 15px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold;">🟢 แถบสีเขียว: เฝ้าระวังและติดตามตามปกติ</div>',
            unsafe_allow_html=True
        )
    else:  # คะแนนอยู่ช่วง 5 - 6 (เทียบตามเกณฑ์ <= 6)
        st.markdown(
            '<div style="background-color: #ffc107; color: black; padding: 15px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold;">🟡 แถบสีเหลือง: แจ้งเตือนและประเมินใน 30 นาที</div>',
            unsafe_allow_html=True
        )