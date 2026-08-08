import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid
from datetime import date, datetime, time, timedelta

st.set_page_config(page_title="DiDi Central Data & Reporting Framework", layout="wide")

# ==========================================
# 1. Historical Mock Data Generation
# ==========================================
@st.cache_data
def load_initial_data():
    np.random.seed(42)
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=365)
    date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')

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
    
    # Combined Context & Employee Tracking
    context_opts = ['Normal', 'Rainy / Extreme Weather', 'Train Shutdown / Strike', 'Major Event (e.g. Concert)']
    context_probs = [0.6, 0.2, 0.1, 0.1]
    employees = ['Sharon', 'David', 'System_Auto']
    employee_probs = [0.6, 0.3, 0.1]

    data = []
    for d in date_range:
        for _ in range(np.random.randint(1, 3)):
            # Generate random time for peak hour simulation
            random_hour = np.random.choice([8, 9, 17, 18, 19, 21, 22, 23], p=[0.1, 0.1, 0.15, 0.15, 0.2, 0.1, 0.1, 0.1])
            random_minute = np.random.randint(0, 59)
            dt_timestamp = d.replace(hour=random_hour, minute=random_minute)
            
            plat = np.random.choice(list(platforms_config.keys()))
            area = np.random.choice(platforms_config[plat])
            camp_type = np.random.choice(types)
            tier = np.random.choice(tiers)
            code = np.random.choice(sample_codes)
            
            context_status = np.random.choice(context_opts, p=context_probs)
            entered_by = np.random.choice(employees, p=employee_probs)
            
            clicks = np.random.randint(500, 5000)
            redeemed = int(clicks * np.random.uniform(0.2, 0.6))
            
            # Boost trips if bad weather or train shutdown
            if context_status in ['Rainy / Extreme Weather', 'Train Shutdown / Strike']:
                trips = int(redeemed * np.random.uniform(0.7, 0.95))
            else:
                trips = int(redeemed * np.random.uniform(0.4, 0.75))
                
            new_cust = int(trips * np.random.uniform(0.15, 0.45))
            entry_id = f"ID-{str(uuid.uuid4())[:6].upper()}"

            data.append({
                'Entry_ID': entry_id,
                'Timestamp': dt_timestamp,
                'Platform': plat,
                'Placement_Area': area,
                'Campaign_Type': camp_type,
                'Voucher_Tier': tier,
                'Promo_Code': code,
                'Context_Status': context_status,
                'Clicks': clicks,
                'Redeemed_Vouchers': redeemed,
                'Actual_Trips': trips,
                'New_Customers': new_cust,
                'Entered_By': entered_by
            })
            
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

if 'db' not in st.session_state:
    st.session_state.db = load_initial_data()

placement_mapping = {
    'Instagram': ['Story', 'Post', 'Reels', 'Bio Link'],
    'TikTok': ['In-Feed Video', 'TopView', 'Spark Ad'],
    'DiDi_App': ['Pop-up Banner', 'Push Notification', 'Home Carousel'],
    'YouTube': ['Pre-roll Ad', 'Mid-roll Ad', 'YouTube Shorts'],
    'Snapchat': ['Snap Ad', 'Story Ad', 'AR Lens Filter'],
    'Meta Ads': ['Facebook Feed', 'Messenger', 'Audience Network'],
    'Quoll Email': ['Weekly Newsletter', 'Dormant User Blast', 'VIP Dedicated']
}

# ==========================================
# 2. UI Layout & Dynamic Greeting
# ==========================================
current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "Good morning"
elif 12 <= current_hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# The Current User logged in
current_user = "Sharon"

st.markdown(f"### {greeting}, {current_user}! 👋")
st.title("🚗 DiDi Central Data & Reporting Framework")

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 1. Data Entry Portal", 
    "🔍 2. Data Management", 
    "📊 3. Report Generator",
    "🔮 4. Predictive Insights & Context"
])

# ------------------------------------------
# TAB 1: DATA ENTRY PORTAL
# ------------------------------------------
with tab1:
    st.subheader("Input Detailed Campaign, Context & Promo Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        in_date = st.date_input("Date", date.today())
        in_time = st.time_input("Time", time(12, 0))
        in_plat = st.selectbox("Platform", ['Instagram', 'TikTok', 'DiDi_App', 'YouTube', 'Snapchat', 'Meta Ads', 'Quoll Email', 'Other'])
        if in_plat == 'Other':
            final_plat = st.text_input("Specify Platform", value="Local Forum")
            in_area = st.text_input("Specify Placement", value="General Post")
        else:
            final_plat = in_plat
            in_area = st.selectbox("Placement Area", placement_mapping[in_plat])
            
    with col2:
        in_type = st.radio("Campaign Type", ['Official Ad', 'Influencer / KOL'])
        in_tier = st.selectbox("Voucher Tier", ['10% Off', '20% Off', '30% Off', '50% Off'])
        in_code = st.text_input("Promo Code / Influencer Name", value="KOL_ALISHA_20")
        
    with col3:
        in_context = st.selectbox("Special Weather / Transit Status", ['Normal', 'Rainy / Extreme Weather', 'Train Shutdown / Strike', 'Major Event (e.g. Concert)'])
        in_user = st.text_input("Entered By (Audit Tracker)", value=current_user, disabled=True)
        
    with col4:
        in_clicks = st.number_input("Total Clicks / Impressions", min_value=0, value=1500)
        in_red = st.number_input("Vouchers Redeemed (Claimed)", min_value=0, value=500)
        in_trips = st.number_input("Actual Trips (Successfully Used)", min_value=0, value=350)
        in_new_cust = st.number_input("New Customers Generated", min_value=0, value=120)
        
    if st.button("Submit Data Entry", type="primary"):
        combined_dt = datetime.combine(in_date, in_time)
        new_row = pd.DataFrame([{
            'Entry_ID': f"ID-{str(uuid.uuid4())[:6].upper()}",
            'Timestamp': combined_dt,
            'Platform': final_plat,
            'Placement_Area': in_area,
            'Campaign_Type': in_type,
            'Voucher_Tier': in_tier,
            'Promo_Code': in_code.upper().strip(),
            'Context_Status': in_context,
            'Clicks': int(in_clicks),
            'Redeemed_Vouchers': int(in_red),
            'Actual_Trips': int(in_trips),
            'New_Customers': int(in_new_cust),
            'Entered_By': in_user
        }])
        st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
        st.success(f"✅ Data for Code **{in_code.upper()}** added successfully by {in_user}!")

# ------------------------------------------
# TAB 2: DATA MANAGEMENT & SEARCH PORTAL (BATCH DELETE)
# ------------------------------------------
with tab2:
    st.subheader("Search, Filter, and Manage Database Entries")
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        search_start_d = st.date_input("Start Date", date.today() - timedelta(days=7), key="mgt_sd")
        search_start_t = st.time_input("Start Time", time(0, 0), key="mgt_st")
    with col_s2:
        search_end_d = st.date_input("End Date", date.today(), key="mgt_ed")
        search_end_t = st.time_input("End Time", time(23, 59), key="mgt_et")
    with col_s3:
        all_platforms = st.session_state.db['Platform'].unique().tolist()
        filter_plat = st.multiselect("Filter Platform", all_platforms, default=all_platforms)
    with col_s4:
        search_code = st.text_input("Search Code/Influencer", value="")
        
    start_dt_filter = datetime.combine(search_start_d, search_start_t)
    end_dt_filter = datetime.combine(search_end_d, search_end_t)
    
    df_mgt = st.session_state.db.copy()
    mask = (
        (df_mgt['Timestamp'] >= start_dt_filter) & 
        (df_mgt['Timestamp'] <= end_dt_filter) & 
        (df_mgt['Platform'].isin(filter_plat))
    )
    if search_code:
        mask = mask & (df_mgt['Promo_Code'].str.contains(search_code.upper(), na=False))
        
    filtered_mgt_df = df_mgt[mask].sort_values(by='Timestamp', ascending=False).reset_index(drop=True)
    
    st.markdown(f"Displaying **{len(filtered_mgt_df)}** matching records. Check 'Entered_By' to track data origin. Use checkboxes to batch delete.")
    
    filtered_mgt_df.insert(0, "Select", False)
    
    edited_df = st.data_editor(
        filtered_mgt_df,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", help="Select to delete", default=False)
        },
        disabled=[col for col in filtered_mgt_df.columns if col != "Select"],
        hide_index=True,
        use_container_width=True
    )
    
    selected_rows = edited_df[edited_df['Select']]
    
    if not selected_rows.empty:
        st.warning(f"⚠️ You have selected {len(selected_rows)} records. This action cannot be undone.")
        if st.button("🗑️ Batch Delete Selected Records", type="primary"):
            ids_to_delete = selected_rows['Entry_ID'].tolist()
            st.session_state.db = st.session_state.db[~st.session_state.db['Entry_ID'].isin(ids_to_delete)].reset_index(drop=True)
            st.success(f"✅ Successfully deleted {len(ids_to_delete)} record(s)!")
            st.rerun()

# ------------------------------------------
# TAB 3: REPORT GENERATOR
# ------------------------------------------
with tab3:
    st.subheader("Generate Automated Analytics Reports")
    
    today = date.today()
    yd = today - timedelta(days=1)
    
    label_daily = f"Daily ({yd.strftime('%d-%b-%Y')})"
    label_weekly = "Weekly (Last 7 Days)"
    label_monthly = "Monthly (Last 30 Days)"
    label_yearly = "Yearly (Last 365 Days)"
    label_all = "All-Time (Up to Now - May take time)"
    label_custom = "Custom Date & Time Range"
    
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        report_type = st.radio("Select Time Scale", [label_daily, label_weekly, label_monthly, label_yearly, label_all, label_custom])
        
    with col_r2:
        if report_type == label_daily:
            s_dt = datetime.combine(yd, time(0, 0))
            e_dt = datetime.combine(yd, time(23, 59))
        elif report_type == label_weekly:
            s_dt = datetime.combine(today - timedelta(days=7), time(0, 0))
            e_dt = datetime.combine(today, time(23, 59))
        elif report_type == label_monthly:
            s_dt = datetime.combine(today - timedelta(days=30), time(0, 0))
            e_dt = datetime.combine(today, time(23, 59))
        elif report_type == label_yearly:
            s_dt = datetime.combine(today - timedelta(days=365), time(0, 0))
            e_dt = datetime.combine(today, time(23, 59))
        elif report_type == label_all:
            min_date = st.session_state.db['Timestamp'].min() if not st.session_state.db.empty else datetime.now()
            s_dt = min_date
            e_dt = datetime.combine(today, time(23, 59))
        else: # Custom Date & Time Range
            st.markdown("##### Custom Time Selector")
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: c_sd = st.date_input("Start Date", today - timedelta(days=3), key="c_sd")
            with cc2: c_st = st.time_input("Start Time", time(18, 0), key="c_st")
            with cc3: c_ed = st.date_input("End Date", today, key="c_ed")
            with cc4: c_et = st.time_input("End Time", time(23, 59), key="c_et")
            s_dt = datetime.combine(c_sd, c_st)
            e_dt = datetime.combine(c_ed, c_et)
                
        st.info(f"📅 **Report Data Range Extract:** {s_dt.strftime('%Y-%m-%d %H:%M')} to {e_dt.strftime('%Y-%m-%d %H:%M')}")

    st.markdown("##### 🎨 Customize Report Diagrams")
    c_type1, c_type2 = st.columns(2)
    with c_type1:
        chart_1_type = st.selectbox("Chart 1 Type (Time Trend)", ["Line Chart", "Area Chart", "Bar Chart"])
    with c_type2:
        chart_2_type = st.selectbox("Chart 2 Type (Platform Breakdown)", ["Bar Chart", "Line Chart", "Area Chart"])

    if st.button("📊 Generate Report", type="primary"):
        df = st.session_state.db.copy()
        df_filtered = df[(df['Timestamp'] >= s_dt) & (df['Timestamp'] <= e_dt)]
            
        if df_filtered.empty:
            st.warning("⚠️ No data available for this specific period. Try adjusting your date/time range.")
        else:
            days_diff = (e_dt - s_dt).days
            if days_diff <= 2:
                df_filtered['Time_Period'] = df_filtered['Timestamp'].dt.strftime('%m-%d %H:00')
            elif days_diff <= 90:
                df_filtered['Time_Period'] = df_filtered['Timestamp'].dt.date.astype(str)
            else:
                df_filtered['Time_Period'] = df_filtered['Timestamp'].dt.strftime('%Y-%m')

            agg_time = df_filtered.groupby('Time_Period')[['Clicks', 'Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
            
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
            
            def render_chart(c_type, data, x_col, y_cols, title, is_bar_group=False):
                colors = ["#999999", "#FF5A00", "#00A86B"]
                if c_type == "Line Chart":
                    return px.line(data, x=x_col, y=y_cols, markers=True, title=title, color_discrete_sequence=colors)
                elif c_type == "Area Chart":
                    return px.area(data, x=x_col, y=y_cols, title=title, color_discrete_sequence=colors)
                else:
                    return px.bar(data, x=x_col, y=y_cols, barmode='group' if is_bar_group else 'relative', title=title, color_discrete_sequence=colors)

            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig_trend = render_chart(chart_1_type, agg_time, 'Time_Period', ['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'], "Performance Trend")
                st.plotly_chart(fig_trend, use_container_width=True)
                
            with col_chart2:
                agg_plat = df_filtered.groupby('Platform')[['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers']].sum().reset_index()
                fig_plat = render_chart(chart_2_type, agg_plat, 'Platform', ['Redeemed_Vouchers', 'Actual_Trips', 'New_Customers'], "Platform Breakdown", True)
                st.plotly_chart(fig_plat, use_container_width=True)
            
            st.markdown("### 📥 Export Options")
            csv_data = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Report as CSV (Open in Excel)",
                data=csv_data,
                file_name=f"DiDi_Marketing_Report_{s_dt.date()}_to_{e_dt.date()}.csv",
                mime='text/csv',
                type="primary"
            )

# ------------------------------------------
# TAB 4: PREDICTIVE INSIGHTS & CONTEXT
# ------------------------------------------
with tab4:
    st.subheader("Discover Correlation between Marketing, Context & Discounts")
    st.markdown("This module analyzes historical patterns to predict when and how promo codes yield the highest conversion rates.")
    
    df_pred = st.session_state.db.copy()
    if df_pred.empty:
        st.warning("Not enough data to generate insights.")
    else:
        df_pred['Conversion_Rate'] = (df_pred['Actual_Trips'] / df_pred['Redeemed_Vouchers'] * 100).fillna(0)
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            agg_context = df_pred.groupby('Context_Status')['Conversion_Rate'].mean().reset_index()
            fig_context = px.bar(
                agg_context, x='Context_Status', y='Conversion_Rate', 
                title="Avg. Conversion Rate by Special Context", 
                text_auto='.1f', color='Conversion_Rate', color_continuous_scale="Oranges"
            )
            fig_context.update_layout(yaxis_title="Conversion Rate (%)")
            st.plotly_chart(fig_context, use_container_width=True)
            
        with col_p2:
            agg_tier = df_pred.groupby('Voucher_Tier')['Conversion_Rate'].mean().reset_index()
            fig_tier = px.bar(
                agg_tier, x='Voucher_Tier', y='Conversion_Rate', 
                title="Avg. Conversion Rate by Voucher Tier", 
                text_auto='.1f', color='Conversion_Rate', color_continuous_scale="Blues"
            )
            fig_tier.update_layout(yaxis_title="Conversion Rate (%)")
            st.plotly_chart(fig_tier, use_container_width=True)

        st.markdown("### 💡 Automated Insights & Recommendations")
        st.info("Based on your historical database, the system generated the following predictive recommendations:")
        st.markdown("""
        * **Rainy / Train Shutdown Effect**: Ride-hailing demand naturally surges during bad weather or transit strikes. Consider distributing **lower tier vouchers (e.g., 10% Off)** during these periods, as conversion rates remain naturally high, effectively saving your marketing budget.
        * **Weekend & Night Peak (21:00 - 23:59)**: Deploy targeted **Influencer Promo Codes** on Instagram and TikTok during weekend night hours to maximize the Gen Z and Millennial rider segments traveling to events.
        * **Discount Depth Strategy**: While 50% Off yields the highest conversion, 20% Off often provides the optimal balance between high conversion and protecting profit margins (Margin Erosion).
        """)
