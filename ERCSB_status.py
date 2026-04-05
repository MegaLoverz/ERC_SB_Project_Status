import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ERC Sandbox Dashboard", layout="wide")
st.title("📊 Dashboard สรุปโครงการ ERC Sandbox")
st.markdown("---")

# 2. ฟังก์ชันโหลดข้อมูล (ใส่ @st.cache_data เพื่อให้เว็บโหลดเร็วขึ้น)
@st.cache_data
def load_data():
    # ตอนแรกลองเทสต์กับไฟล์ CSV ในเครื่องก่อนได้ครับ
    # df = pd.read_csv('Data_for_LookerStudio_SB.csv')
    
    # 🔥 ทริคอัปเดตง่าย: นำลิงก์ Google Sheets ที่ Publish to the web (แบบ CSV) มาใส่ตรงนี้
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSpktBCWEBI1wqdLrJlYUi9acpcbHIKXDimUWswIVTHPGPAzURZnEvcVq9oRByuyMpcDanWiNER8g_w/pub?gid=1294284872&single=true&output=csv"
    df = pd.read_csv(url)
    
    # df = pd.read_csv('Data_for_LookerStudio_SB.csv') # ใช้ไฟล์ที่ผมคลีนให้ไปก่อน
    return df

df = load_data()

# 3. สร้าง Sidebar สำหรับกรองข้อมูล
st.sidebar.header("⚙️ ตัวกรองข้อมูล")
selected_source = st.sidebar.multiselect(
    "เลือกแหล่งที่มาของโครงการ", 
    options=df['Source'].unique(), 
    default=df['Source'].unique()
)

# กรองข้อมูลตามที่ผู้ใช้เลือก
filtered_df = df[df['Source'].isin(selected_source)]

# 4. ออกแบบ Layout กราฟ (แบ่ง 2 คอลัมน์)
col1, col2 = st.columns(2)

with col1:
    # กราฟวงกลม: สถานะโครงการ
    st.subheader("📌 สถานะโครงการทั้งหมด")
    fig_status = px.pie(
        filtered_df, names='สถานะ', 
        hole=0.4, # ทำให้เป็น Donut chart สวยๆ
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_status, use_container_width=True)

    # กราฟแท่ง: รูปแบบการซื้อขาย
    st.subheader("⚡ รูปแบบการซื้อขายไฟฟ้า")
    trade_counts = filtered_df['รูปแบบการซื้อขาย'].value_counts().reset_index()
    trade_counts.columns = ['รูปแบบ', 'จำนวน']
    fig_trade = px.bar(
        trade_counts, x='รูปแบบ', y='จำนวน', 
        text='จำนวน', color='รูปแบบ',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_trade, use_container_width=True)

with col2:
    # กราฟแท่งแนวนอน: ประเภทกิจกรรม
    st.subheader("📋 จำนวนโครงการแยกตามกิจกรรม")
    activity_counts = filtered_df['กิจกรรม'].value_counts().reset_index()
    activity_counts.columns = ['กิจกรรม', 'จำนวน']
    fig_activity = px.bar(
        activity_counts, x='จำนวน', y='กิจกรรม', orientation='h', 
        text='จำนวน', color='กิจกรรม'
    )
    fig_activity.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_activity, use_container_width=True)

    # กราฟแท่งแนวนอน: โครงข่าย
    st.subheader("🔌 โครงข่ายที่เข้าร่วม")
    network_counts = filtered_df['โครงข่าย'].value_counts().reset_index()
    network_counts.columns = ['โครงข่าย', 'จำนวน']
    fig_network = px.bar(
        network_counts, x='จำนวน', y='โครงข่าย', orientation='h', 
        text='จำนวน', color_discrete_sequence=['#9C27B0']
    )
    fig_network.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_network, use_container_width=True)
