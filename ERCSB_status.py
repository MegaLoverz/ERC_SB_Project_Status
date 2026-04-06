import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเพจและฟอนต์ภาษาไทย (Kanit)
st.set_page_config(page_title="ERC Sandbox Executive Dashboard", layout="wide")

# Custom CSS เพื่อความสวยงาม
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Kanit', sans-serif;
    }
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSpktBCWEBI1wqdLrJlYUi9acpcbHIKXDimUWswIVTHPGPAzURZnEvcVq9oRByuyMpcDanWiNER8g_w/pub?gid=1294284872&single=true&output=csv"
    df = pd.read_csv(url)
    # ล้างข้อมูลช่องว่างที่อาจติดมา
    df['สถานะ'] = df['สถานะ'].str.strip()
    df['Source'] = df['Source'].str.strip()
    return df

df = load_data()

# 3. Sidebar: คอนโทรลหลัก (Source & Status)
st.sidebar.header("🎯 ระบบกรองข้อมูลหลัก")

# คอนโทรล 1: แหล่งที่มา
selected_source = st.sidebar.multiselect(
    "เลือกแหล่งที่มา (Source)", 
    options=sorted(df['Source'].unique()), 
    default=df['Source'].unique()
)

# คอนโทรล 2: สถานะโครงการ (ตามที่คุณต้องการ)
selected_status = st.sidebar.multiselect(
    "เลือกสถานะโครงการ (Status)", 
    options=sorted(df['สถานะ'].unique()), 
    default=df['สถานะ'].unique()
)

# กรองข้อมูลตามที่เลือกทั้งสองเงื่อนไข
mask = (df['Source'].isin(selected_source)) & (df['สถานะ'].isin(selected_status))
filtered_df = df[mask]

# 4. ส่วนหัวและ KPI Metrics
st.title("📊 ERC Sandbox Executive Dashboard")
st.markdown("ระบบติดตามสถานะโครงการ ERC Sandbox ระยะที่ 1 และโครงการเพิ่มเติม")

# สร้างแผ่นป้ายสรุปตัวเลข (Metrics)
m1, m2, m3, m4 = st.columns(4)
m1.metric("จำนวนโครงการทั้งหมด", len(filtered_df))
m2.metric("กำลังดำเนินการ", len(filtered_df[filtered_df['สถานะ'] == 'ดำเนินโครงการต่อ']))
m3.metric("ยกเลิกโครงการ", len(filtered_df[filtered_df['สถานะ'] == 'ยกเลิกโครงการ']))
m4.metric("แหล่งข้อมูล (ชุด)", len(selected_source))

st.markdown("---")

# 5. การแสดงผลกราฟ
c1, c2 = st.columns(2)

with c1:
    # กราฟวงกลม: สถานะ (ใช้ Donut Chart เพื่อความทันสมัย)
    st.subheader("📌 สัดส่วนสถานะโครงการ")
    fig_status = px.pie(
        filtered_df, names='สถานะ', 
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_status.update_layout(template="plotly_white", margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_status, width='stretch')

    # กราฟแท่ง: การซื้อขาย
    st.subheader("⚡ รูปแบบการซื้อขายไฟฟ้า")
    trade_df = filtered_df['รูปแบบการซื้อขาย'].value_counts().reset_index()
    trade_df.columns = ['รูปแบบ', 'จำนวน']
    fig_trade = px.bar(
        trade_df, x='รูปแบบ', y='จำนวน', 
        color='รูปแบบ', text_auto=True,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig_trade.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig_trade, width='stretch')

with c2:
    # กราฟแท่งแนวนอน: กิจกรรม
    st.subheader("📋 กิจกรรมแยกตามประเภท")
    act_df = filtered_df['กิจกรรม'].value_counts().reset_index()
    act_df.columns = ['กิจกรรม', 'จำนวน']
    fig_act = px.bar(
        act_df, x='จำนวน', y='กิจกรรม', orientation='h',
        text_auto=True, color='กิจกรรม',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_act.update_layout(template="plotly_white", showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_act, width='stretch')

    # กราฟแท่งแนวนอน: โครงข่าย
    st.subheader("🔌 โครงข่ายที่เข้าร่วม")
    net_df = filtered_df['โครงข่าย'].value_counts().reset_index()
    net_df.columns = ['โครงข่าย', 'จำนวน']
    fig_net = px.bar(
        net_df, x='จำนวน', y='โครงข่าย', orientation='h',
        text_auto=True, color_discrete_sequence=['#636EFA']
    )
    fig_net.update_layout(template="plotly_white", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_net, width='stretch')

# 6. ตารางข้อมูลดิบ (เผื่ออยากดูรายชื่อโครงการ)
with st.expander("🔍 ดูข้อมูลโครงการทั้งหมดแบบละเอียด"):
    st.dataframe(filtered_df[['เลขที่โครงการ', 'ชื่อโครงการ', 'ผู้ยื่นโครงการ', 'สถานะ', 'Source']], use_container_width=True)
