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
        'DiDi_App': ['Pop-up Banner', 'Push Notification', 'Home Carousel'],
        'YouTube': ['Pre-roll Ad', 'Mid-roll Ad', 'YouTube Shorts'],
        'Snapchat': ['Snap Ad', 'Story Ad', 'AR Lens Filter'],
        'Meta Ads': ['Facebook Feed', 'Messenger', 'Audience Network'],
        'Quoll Email': ['Weekly Newsletter', 'Dormant User Blast', 'VIP Dedicated']
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
    'Instagram': ['Story', 'Post', 'Reels'],
    'TikTok': ['In-Feed Video', 'TopView', 'Spark Ad'],
    'DiDi_App': ['Pop-up Banner', 'Push Notification', 'Home Carousel'],
    'YouTube': ['Pre-roll Ad', 'Mid-roll Ad', 'YouTube Shorts'],
    'Snapchat': ['Snap Ad', 'Story Ad', 'AR Lens Filter'],
    'Meta Ads': ['Facebook Feed', 'Messenger', 'Audience Network'],
    'Quoll Email': ['Weekly Newsletter', 'Dormant User Blast', 'VIP Dedicated']
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
        in_plat = st.selectbox("Platform", ['Instagram', 'TikTok', 'DiDi_App', 'YouTube', 'Snapchat', 'Meta Ads', 'Quoll Email', 'Other'])
        
        if in_plat == 'Other':
            final_plat = st.text_input("Please specify the custom Platform", value="Local Forum")
            in_area = st.text_input("Please specify the Placement Area", value="General Post")
        else:
            final_plat = in_plat
            in_area = st.selectbox("Placement Area", placement_mapping[in_plat])
            
    with col2:
        in_type = st.radio("Campaign Type", ['Official Ad', 'Influencer / KOL'], horizontal=True)
        in_tier = st.selectbox("Voucher Tier", ['10% Off', '20% Off', '30% Off', '50% Off'])
        in_code = st.text_input("Promo Code Name (e.g., KOL_NAME_20)", value="DIDI_PROMO_2026")
        
    with col3:
        in_clicks = st.number_input("Total Clicks / Impressions", min_value=0, value=1000)
        in_red = st.number_input("Vouchers Redeemed (Claimed)", min_value=0, value=450)
        in_trips = st.number_input("Actual Trips (Vouchers Successfully Used)", min_value=0, value=300)
        in_new_cust = st.number_input("New Customers Generated", min_value=0, value=120)
        
    if st.button("Submit Data", type="primary"):
        new_row = pd.DataFrame([{
            'Date': pd.to_datetime(in_date),
            'Platform': final_plat,
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
        st.success(f"✅ Data for Code **{in_code.upper()}** on {final_plat} ({in_area}) added successfully!")
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
        # Get unique platforms dynamically to include any "Other" platforms added by the user
        all_platforms = st.session_state.db['Platform'].unique().tolist()
        filter_plat = st.multiselect("Filter Platform", all_platforms, default=all_platforms)
        
    search_code = st.text_input("Search Promo Code / Influencer Name", value="")
    
    # Filter DataFrame (Keep original index for accurate deletion)
    df_mgt = st.session_state.db.copy()
    mask = (
        (df_mgt['Date'] >= pd.to_datetime(search_start)) & 
        (df_mgt['Date'] <= pd.to_datetime(search_end)) & 
        (df_mgt['Platform'].isin(filter_plat))
    )
    if search_code:
        mask = mask & (df_mgt['Promo_Code'].str.contains(search_code.upper(), na=False))
        
    filtered_mgt_df = df_mgt[mask].sort_values(by='Date', ascending=False)
    
    st.write(f"Displaying **{len(filtered_mgt_df)}** matching records:")
    
    # Multi-select for Batch Delete
    filtered_mgt_df['Delete'] = False
    edited_df = st.data_editor(
        filtered_mgt_df,
        column_config={"Delete": st.column_config.CheckboxColumn("Select to Delete", default=False)},
        disabled=[c for c in filtered_mgt_df.columns if c != "Delete"],
        use_container_width=True
    )
    
    rows_to_delete = edited_df[edited_df['Delete'] == True]
    
    if len(rows_to_delete) > 0:
        st.warning(f"⚠️ You have selected {len(rows_to_delete)} records to delete.")
        if st.button(f"🗑️ Confirm Delete Selected Records"):
            # Remove selected rows from st.session_state.db using the index
            st.session_state.db = st.session_state.db.drop(rows_to_delete.index).reset_index(drop=True)
            st.success("✅ Selected data has been successfully deleted!")
            st.rerun()

# ------------------------------------------
# TAB 3: REPORT GENERATOR
# ------------------------------------------
with tab3:
    st.subheader("Generate Automated Analytics Reports")
    
    # 1. Date Range & Time Scale Selection
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        report_type = st.radio("Select Time Scale", [
            "Daily (Yesterday)", 
            "Weekly (Last 7 Days)", 
            "Monthly (Last 30 Days)", 
            "Yearly (Last 365 Days)", 
            "All-Time (Up to Now - May take longer)", 
            "Custom Date Range"
        ], key="rep_scale")
        
    with col_r2:
        # Calculate dynamic start and end dates based on selection
        today = date.today()
        if report_type == "Daily (Yesterday)":
            s_date = today - timedelta(days=1)
            e_date = today
        elif report_type == "Weekly (Last 7 Days)":
            s_date = today - timedelta(days=7)
            e_date = today
        elif report_type == "Monthly (Last 30 Days)":
            s_date = today - timedelta(days=30)
            e_date = today
        elif report_type == "Yearly (Last 365 Days)":
            s_date = today - timedelta(days=365)
            e_date = today
        elif report_type == "All-Time (Up to Now - May take longer)":
            s_date = st.session_state.db['Date'].min().date() if not st.session_state.db.empty else today
            e_date = today
        else: # Custom Date Range
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                s_date = st.date_input("Start Date (for Custom)", today - timedelta(days=30), key="rep_start")
            with col_c2:
                e_date = st.date_input("End Date (for Custom)", today, key="rep_end")
                
        st.info(f"📅 **Current Report Range:** {s_date} to {e_date}")

    # 2. Diagram Customization
    st.markdown("##### 🎨 Customize Report Diagrams")
    col_type1, col_type2 = st.columns(2)
    with col_type1:
        chart_1_type = st.selectbox("Chart 1 Type (Time Trend)", ["Line Chart", "Area Chart", "Bar Chart"])
    with col_type2:
        chart_2_type = st.selectbox("Chart 2 Type (Platform Breakdown)", ["Bar Chart", "Line Chart", "Area Chart"])

    # 3. Generate Report Action
    if st.button("📊 Generate Report", type="primary", key="btn_rep"):
        df = st.session_state.db.copy()
        
        # Filter the dataframe by the calculated date range
        df_filtered = df[(df['Date'] >= pd.to_datetime(s_date)) & (df['Date'] <= pd.to_datetime(e_date))]
            
        if df_filtered.empty:
            st.warning("⚠️ No data available for this specific period. Try adjusting your date range.")
        else:
            # Format time period for X-axis based on data range size
            days_diff = (e_date - s_date).days
            if days_diff <= 90:
                df_filtered['Time_Period'] = df_filtered['Date'].dt.date.astype(str)
            else:
                # Group by Month-Year if range is large (Yearly / All-Time) to keep chart clean
                df_filtered['Time_Period'] = df_filtered['Date'].dt.strftime('%Y-%m')

            # Aggregate data for KPIs
            agg_time = df_filtered.groupby('Time_Period')[['Clicks', 'Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
            agg_time = agg_time.sort_values('Time_Period')
            
            # KPI Metrics (Now completely dynamic based on filtered date!)
            total_red = agg_time['Redeemed_Vouchers'].sum()
            total_trp = agg_time['Actual_Trips'].sum()
            total_new = agg_time['New_Customers'].sum()
            conv_rate = (total_trp / total_red * 100) if total_red > 0 else 0
            
            st.markdown("### 📈 Key Performance Indicators (KPIs)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Vouchers Redeemed", f"{total_red:,}")
            m2.metric("Actual Trips (Vouchers Used)", f"{total_trp:,}")
            m3.metric("New Customers Acquired", f"{total_new:,}")
            m4.metric("Trip Conversion Rate", f"{conv_rate:.1f}%")
            
            st.markdown("---")
            
            # Helper function for rendering Plotly charts dynamically
            def render_chart(chart_type, data, x_col, y_cols, title, is_barmode_group=False):
                colors = ["#999999", "#FF5A00", "#00A86B"]
                if chart_type == "Line Chart":
                    return px.line(data, x=x_col, y=y_cols, markers=True, title=title, color_discrete_sequence=colors)
                elif chart_type == "Area Chart":
                    return px.area(data, x=x_col, y=y_cols, title=title, color_discrete_sequence=colors)
                elif chart_type == "Bar Chart":
                    if is_barmode_group:
                        return px.bar(data, x=x_col, y=y_cols, barmode='group', title=title, color_discrete_sequence=colors)
                    else:
                        return px.bar(data, x=x_col, y=y_cols, title=title, color_discrete_sequence=colors)

            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_trend = render_chart(chart_1_type, agg_time, 'Time_Period', ['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'], "Performance & Acquisition Trend")
                fig_trend.update_layout(template="plotly_white", xaxis_title="Time Period", yaxis_title="Count")
                st.plotly_chart(fig_trend, use_container_width=True)
                
            with col_chart2:
                agg_plat = df_filtered.groupby('Platform')[['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
                fig_plat = render_chart(chart_2_type, agg_plat, 'Platform', ['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'], "Platform & Channel Breakdown", is_barmode_group=True)
                fig_plat.update_layout(template="plotly_white", yaxis_title="Count")
                st.plotly_chart(fig_plat, use_container_width=True)
            
            # Export Report Feature
            st.markdown("### 📥 Export Options")
            csv_data = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Report as CSV (Open in Excel)",
                data=csv_data,
                file_name=f"DiDi_Marketing_Report_{s_date}_to_{e_date}.csv",
                mime='text/csv',
                type="primary"
            )
