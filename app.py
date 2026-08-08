import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="DiDi Central Data & Reporting Framework", layout="wide")

# ==========================================
# 1. Historical Mock Data Generation
# ==========================================
@st.cache_data
def load_initial_data():
    np.random.seed(42)
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    platforms_config = {
        'Instagram': ['Story', 'Post', 'Reels'],
        'TikTok': ['In-Feed Video', 'TopView', 'Spark Ad'],
        'App': ['Pop-up Banner', 'Notification', 'Home Banner'],
        'Email': ['Weekly Newsletter', 'Dormant User Blast', 'VIP Dedicated'],
        'Other': ['General / Partner']
    }
    
    tiers = ['10% Off', '20% Off', '30% Off', '50% Off']
    types = ['Official Ad', 'Influencer / KOL']
    sample_codes = ['MELB20', 'DIDI_KOL_01', 'SUMMER30', 'APP_POP_10', 'TIKTOK_FUN']

    data = []
    for d in date_range:
        for _ in range(np.random.randint(1, 3)):
            plat = np.random.choice(list(platforms_config.keys()))
            area = np.random.choice(platforms_config[plat])
            camp_type = np.random.choice(types)
            tier = np.random.choice(tiers)
            code = np.random.choice(sample_codes)
            
            clicks = np.random.randint(500, 5000)
            redeemed = int(clicks * np.random.uniform(0.2, 0.6))
            trips = int(redeemed * np.random.uniform(0.4, 0.85))
            new_cust = int(trips * np.random.uniform(0.15, 0.45))

            data.append({
                'Date': d,
                'Platform': plat,
                'Placement_Area': area,
                'Campaign_Type': camp_type,
                'Voucher_Tier': tier,
                'Promo_Code': code,
                'Clicks': clicks,
                'Redeemed_Vouchers': redeemed,
                'Actual_Trips': trips,
                'New_Customers': new_cust
            })
            
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

if 'db' not in st.session_state:
    st.session_state.db = load_initial_data()

# Dynamic options for placements based on Platform
placement_mapping = {
    'Instagram': ['Story', 'Post', 'Reels', 'Bio Link'],
    'TikTok': ['In-Feed Video', 'TopView', 'Spark Ad'],
    'App': ['Pop-up Banner', 'Push Notification', 'Home Carousel'],
    'Email': ['Weekly Newsletter', 'Dormant User Blast', 'VIP Dedicated'],
    'Other': ['Offline Flyer', 'Partner Promotion', 'General']
}

# ==========================================
# 2. UI Layout
# ==========================================
st.title("🚗 DiDi Central Data & Reporting Framework")

tab1, tab2, tab3 = st.tabs([
    "📝 1. Data Entry Portal", 
    "🔍 2. Data Management Portal", 
    "📊 3. Report Generator"
])

# ------------------------------------------
# TAB 1: DATA ENTRY PORTAL
# ------------------------------------------
with tab1:
    st.subheader("Input Detailed Campaign & Promo Code Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        in_date = st.date_input("Date", date.today())
        in_plat = st.selectbox("Platform", ['Instagram', 'TikTok', 'App', 'Email', 'Other'])
        in_area = st.selectbox("Placement Area", placement_mapping[in_plat])
        
    with col2:
        in_type = st.radio("Campaign Type", ['Official Ad', 'Influencer / KOL'], horizontal=True)
        in_tier = st.selectbox("Voucher Tier", ['10% Off', '20% Off', '30% Off', '50% Off'])
        in_code = st.text_input("Promo Code Name", value="DIDI_PROMO_2026")
        
    with col3:
        in_clicks = st.number_input("Total Clicks / Opens", min_value=0, value=1000)
        in_red = st.number_input("Vouchers Redeemed", min_value=0, value=450)
        in_trips = st.number_input("Actual Trips Completed", min_value=0, value=300)
        in_new_cust = st.number_input("New Customers Generated", min_value=0, value=120)
        
    if st.button("Submit Data", type="primary"):
        new_row = pd.DataFrame([{
            'Date': pd.to_datetime(in_date),
            'Platform': in_plat,
            'Placement_Area': in_area,
            'Campaign_Type': in_type,
            'Voucher_Tier': in_tier,
            'Promo_Code': in_code.upper().strip(),
            'Clicks': int(in_clicks),
            'Redeemed_Vouchers': int(in_red),
            'Actual_Trips': int(in_trips),
            'New_Customers': int(in_new_cust)
        }])
        st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
        st.success(f"✅ Data for Code **{in_code.upper()}** on {in_plat} ({in_area}) added successfully!")
        st.dataframe(st.session_state.db.tail(5))

# ------------------------------------------
# TAB 2: DATA MANAGEMENT & SEARCH PORTAL
# ------------------------------------------
with tab2:
    st.subheader("Search, Filter, and Manage Database Entries")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        search_start = st.date_input("Start Date", date.today() - timedelta(days=30), key="mgt_start")
    with col_s2:
        search_end = st.date_input("End Date", date.today(), key="mgt_end")
    with col_s3:
        filter_plat = st.multiselect("Filter Platform", ['Instagram', 'TikTok', 'App', 'Email', 'Other'], default=['Instagram', 'TikTok', 'App', 'Email', 'Other'])
        
    search_code = st.text_input("Search Promo Code / Influencer Name", value="")
    
    # Filter DataFrame
    df_mgt = st.session_state.db.copy()
    mask = (
        (df_mgt['Date'] >= pd.to_datetime(search_start)) & 
        (df_mgt['Date'] <= pd.to_datetime(search_end)) & 
        (df_mgt['Platform'].isin(filter_plat))
    )
    if search_code:
        mask = mask & (df_mgt['Promo_Code'].str.contains(search_code.upper(), na=False))
        
    filtered_mgt_df = df_mgt[mask].sort_values(by='Date', ascending=False).reset_index(drop=True)
    
    st.write(f"顯示 **{len(filtered_mgt_df)}** 條符合條件的記錄：")
    
    # Multi-select for Batch Delete
    filtered_mgt_df['Delete'] = False
    edited_df = st.data_editor(
        filtered_mgt_df,
        column_config={"Delete": st.column_config.CheckboxColumn("Select to Delete", default=False)},
        disabled=[c for c in filtered_mgt_df.columns if c != "Delete"],
        hide_index=True,
        use_container_width=True
    )
    
    rows_to_delete = edited_df[edited_df['Delete'] == True]
    
    if len(rows_to_delete) > 0:
        if st.button(f"🗑️ 批量刪除選中的 {len(rows_to_delete)} 條數據", type="primary"):
            # Remove selected rows from st.session_state.db
            cond = st.session_state.db.index.isin(rows_to_delete.index)
            st.session_state.db = st.session_state.db[~cond].reset_index(drop=True)
            st.success("✅ 選中數據已順利刪除！")
            st.rerun()

# ------------------------------------------
# TAB 3: REPORT GENERATOR
# ------------------------------------------
with tab3:
    st.subheader("Generate Automated Analytics Reports")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        report_type = st.radio("Select Time Scale", ["Daily", "Weekly", "Monthly", "Yearly", "Custom Date Range"], key="rep_scale")
    with col_r2:
        custom_start = st.date_input("Start Date (for Custom)", date.today() - timedelta(days=30), key="rep_start")
    with col_r3:
        custom_end = st.date_input("End Date (for Custom)", date.today(), key="rep_end")
        
    if st.button("Generate Report", type="primary", key="btn_rep"):
        df = st.session_state.db.copy()
        
        if report_type == "Custom Date Range":
            df = df[(df['Date'] >= pd.to_datetime(custom_start)) & (df['Date'] <= pd.to_datetime(custom_end))]
            
        if df.empty:
            st.warning("⚠️ No data available for this period. Try adjusting your date range.")
        else:
            if report_type == "Daily":
                df['Time_Period'] = df['Date'].dt.date.astype(str)
            elif report_type == "Weekly":
                df['Time_Period'] = df['Date'].dt.strftime('%Y-W%V')
            elif report_type == "Monthly":
                df['Time_Period'] = df['Date'].dt.strftime('%Y-%m')
            elif report_type == "Yearly":
                df['Time_Period'] = df['Date'].dt.year.astype(str)
            else:
                df['Time_Period'] = df['Date'].dt.date.astype(str)

            agg_time = df.groupby('Time_Period')[['Clicks', 'Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
            agg_time = agg_time.sort_values('Time_Period')
            
            total_red = agg_time['Redeemed_Vouchers'].sum()
            total_trp = agg_time['Actual_Trips'].sum()
            total_new = agg_time['New_Customers'].sum()
            conv_rate = (total_trp / total_red * 100) if total_red > 0 else 0
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Vouchers Redeemed", f"{total_red:,}")
            m2.metric("Total Actual Trips", f"{total_trp:,}")
            m3.metric("New Customers Acquired", f"{total_new:,}")
            m4.metric("Trip Conversion Rate", f"{conv_rate:.1f}%")
            
            st.markdown("---")
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_trend = px.line(
                    agg_time, x='Time_Period', y=['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'],
                    markers=True, title="Performance & Acquisition Trend",
                    color_discrete_sequence=["#999999", "#FF5A00", "#00A86B"]
                )
                fig_trend.update_layout(template="plotly_white", xaxis_title="Time Period", yaxis_title="Count")
                st.plotly_chart(fig_trend, use_container_width=True)
                
            with col_chart2:
                agg_plat = df.groupby('Platform')[['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
                fig_plat = px.bar(
                    agg_plat, x='Platform', y=['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'],
                    barmode='group', title="Platform & Channel Breakdown",
                    color_discrete_sequence=["#CCCCCC", "#FF5A00", "#00A86B"]
                )
                fig_plat.update_layout(template="plotly_white", yaxis_title="Count")
                st.plotly_chart(fig_plat, use_container_width=True)
