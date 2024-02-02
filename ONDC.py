import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime
import warnings
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
# import locale

warnings.filterwarnings('ignore')

def ONDC_dash():
    # locale.setlocale(locale.LC_ALL, 'en_IN')

    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Apply the custom style
    st.markdown('<p class="big-font">ONDC Dashboard</p>', unsafe_allow_html=True)
    # @st.cache_data
    def load_data():
        df = pd.read_csv(r"C:\Users\vijay39.kumar\Desktop\Ploytly and Streamlit dashboard\dashboard_dummy_data.csv")
        df[['soi_created_at', 'soi_eta', 'sof_shipped_at', 'sof_delivered_at']] = df[
            ['soi_created_at', 'soi_eta', 'sof_shipped_at', 'sof_delivered_at']
        ].apply(pd.to_datetime)
        df['Date'] = df['soi_created_at'].dt.date
        # df = df[df['Date'] >= pd.to_datetime('2024-01-01')]
        # df['Net_order_value'] = df[['net_shipping_charges', 'net_order_value_inc_pf_exc_sc']].sum(axis=1)
        # df.drop(['net_shipping_charges', 'net_order_value_inc_pf_exc_sc'], axis=1, inplace=True)
        # df['soi_cust_id'] = df['soi_cust_id'].astype('str').str.strip()
        # df['Gross_order_value'] = df[['gross_shipping_charges', 'gross_order_value_inc_pf_exc_sc']].sum(axis=1)
        # df.drop(['gross_shipping_charges', 'gross_order_value_inc_pf_exc_sc'], axis=1, inplace=True)
        return df

    df = load_data()
    
    min_date = df['Date'].min()
    max_date = df['Date'].max()

    # #Date filter
    # date_selector = st.date_input('Date', 
    #                                       value=(min_date, max_date), 
    #                                       min_value=min_date, 
    #                                       max_value=max_date)

    # if isinstance(date_selector, tuple):  
    #     start_date, end_date = date_selector
    #     df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    # else:  
    #     df = df[df['Date'] == date_selector]

    # #L1 Category filter
    # l1_cn_options = ['All'] + list(df['l1_cn'].unique())
    # l1_cn_selector = st.multiselect('Category', options=l1_cn_options, default='All')

    # if 'All' not in l1_cn_selector:
    #     df = df[df['l1_cn'].isin(l1_cn_selector)]


    #marchant name filter
    # merchant_name_options = ['All'] + list(df['merchant_name'].sort_values().unique())
    # merchant_name_selector = st.multiselect('Merchant Name', options=merchant_name_options, default='All')

    # if 'All' not in merchant_name_selector:
    #     df = df[df['merchant_name'].isin(merchant_name_selector)]


    # #customer city filter
    # cust_city_options = ['All'] + list(df['cust_city'].sort_values().unique())
    # cust_city_selector = st.multiselect('Customer City', options=cust_city_options, default='All')

    # if 'All' not in cust_city_selector:
    #     df = df[df['cust_city'].isin(cust_city_selector)]
        
        
    #item name filter
    # soi_sku_name_options = ['All'] + list(df['soi_sku_name'].sort_values().unique())
    # soi_sku_name_options_selector = st.multiselect('Item', options=soi_sku_name_options, default='All')

    # if 'All' not in soi_sku_name_options_selector:
    #     df = df[df['soi_sku_name'].isin(soi_sku_name_options_selector)]


    #marchant ID filter
    # search_term_merchant = st.text_input('Merchant ID')
    # soi_merchant_id_options = ['All'] + list(df['soi_merchant_id'].unique())
    # filtered_merchant_options = [option for option in soi_merchant_id_options if search_term_merchant.lower() in str(option).lower()]
        
    # if 'All' not in filtered_merchant_options:
    #     df = df[df['soi_merchant_id'].isin(filtered_merchant_options)]
            
    #cust ID filter
    # search_term_cust = st.text_input('Customer ID')
    # soi_cust_id_options = ['All'] + list(df['soi_cust_id'].unique())
    # filtered_cust_options = [option for option in soi_cust_id_options if search_term_cust.lower() in str(option).lower()]

    # if 'All' not in filtered_cust_options:
    #     df = df[df['soi_cust_id'].isin(filtered_cust_options)]
        
    def category_wise_count(a):    
        category_wise_orders = a.groupby('l1_cn').agg({'network_order_id':'nunique',
                                                        'Gross_order_value':'sum',
                                                        'Net_order_value':'sum'}).reset_index().rename(columns={'network_order_id':'Total orders',
                                                                                                                'Gross_order_value':'GOV',
                                                                                                                'Net_order_value':'NOV',
                                                                                                                'l1_cn':'Category'})
        # with st.expander("Data Preview"):
        st.dataframe(category_wise_orders, use_container_width=True)

    def barchart(a, chart_width=700, chart_height=450):
        # Grouping the data
        l1_cn_grouped = a.groupby('l1_cn')['Net_order_value'].sum().reset_index()

        # Creating a bar chart
        bar_fig = px.bar(
            l1_cn_grouped, 
            x='l1_cn',
            y='Net_order_value',
            title='Category wise orders - Bar Chart',
            color='l1_cn',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            width=chart_width,
            height=chart_height
        )
        # Updating legend position
        bar_fig.update_layout(showlegend=False,title_x=0.36)
        bar_fig.update_xaxes(title=None)
        bar_fig.update_yaxes(title=None)

        # Displaying the charts in Streamlit
        st.plotly_chart(bar_fig)

    def barchart(a, chart_width=700, chart_height=450):
        # Grouping the data
        l1_cn_grouped = a.groupby('l1_cn')['Net_order_value'].sum().reset_index()
        
        max_value = l1_cn_grouped['Net_order_value'].max()
        l1_cn_grouped['color'] = l1_cn_grouped['Net_order_value'] / max_value
        
        # Defining a custom color scale that doesn't go to white
        # Replace 'lightblue' with the desired lightest color you want to use
        custom_color_scale = [
            [0, 'lightblue'],  # or any light but clearly visible color of your choice
            [1, 'navy']  # or any dark blue color of your choice
        ]
        
        # custom_color_scale = [
        # [0.0, 'lightblue'],   # Lightest blue for the lowest values
        # [0.2, 'skyblue'],     # Light sky blue for low values
        # [0.4, 'deepskyblue'], # Deeper sky blue for medium-low values
        # [0.6, 'dodgerblue'],  # Bright dodger blue for medium values
        # [0.8, 'blue'],        # Regular blue for medium-high values
        # [1.0, 'navy']         # Darkest navy blue for the highest values
        # ]
        
        # Creating a bar chart
        bar_fig = px.bar(
            l1_cn_grouped, 
            x='l1_cn',
            y='Net_order_value',
            title='Category wise orders - Bar Chart',
            color='Net_order_value',
            color_continuous_scale=custom_color_scale,
            width=chart_width,
            height=chart_height
        )
        # Updating legend position
        bar_fig.update_layout(showlegend=False,coloraxis_showscale=False,title_x=0.36)
        bar_fig.update_xaxes(title=None)
        bar_fig.update_yaxes(title=None)

        # Displaying the charts in Streamlit
        st.plotly_chart(bar_fig)

    def horizontal_barchart(a, chart_width=700, chart_height=450):
        # Grouping the data
        l1_cn_grouped = a.groupby('l1_cn')['network_order_id'].nunique().reset_index()
            
        max_value = l1_cn_grouped['network_order_id'].max()
        l1_cn_grouped['color'] = l1_cn_grouped['network_order_id'] / max_value
        
        # Defining a custom color scale that doesn't go to white
        # Replace 'lightblue' with the desired lightest color you want to use
        custom_color_scale = [
            [0, 'lightblue'],  # or any light but clearly visible color of your choice
            [1, 'navy']  # or any dark blue color of your choice
        ]
        # Creating a horizontal bar chart
        horizontal_bar_fig = px.bar(
            l1_cn_grouped, 
            x='network_order_id',  # Swap x and y for horizontal bars
            y='l1_cn',            # Swap x and y for horizontal bars
            title='Category wise orders - Horizontal Bar Chart',
            color='network_order_id',
            color_continuous_scale=custom_color_scale,
            orientation='h',       # Set the orientation to horizontal
            width=chart_width,
            height=chart_height
        )
        # Updating legend position
        horizontal_bar_fig.update_layout(showlegend=False,coloraxis_showscale=False, title_x=0.36)
        horizontal_bar_fig.update_xaxes(title=None)
        horizontal_bar_fig.update_yaxes(title=None)

        # Displaying the horizontal bar chart in Streamlit
        st.plotly_chart(horizontal_bar_fig)
        
            
    def linechart(a, chart_width=700, chart_height=450):
        # Grouping the data
        l1_cn_grouped = a.groupby('Date')['Net_order_value'].sum().reset_index()

        # Creating a line chart
        line_fig = px.line(
            l1_cn_grouped, 
            x='Date',
            y='Net_order_value',
            title='Order value trend line',
            width=chart_width,
            height=chart_height
        )
        
        for i, row in l1_cn_grouped.iterrows():
            formatted_value = round(row['Net_order_value'])
            line_fig.add_annotation(
                x=row['Date'],
                y=row['Net_order_value'],
                text=formatted_value,
                showarrow=False,
                font=dict(size=13, color='black'),
                bgcolor='rgba(173, 216, 230, 0.5)'
            )
            
        # Updating legend position
        line_fig.update_layout(showlegend=False, title_x=0.36)
        line_fig.update_xaxes(title=None)  # Rotate x-axis labels by 45 degrees
        line_fig.update_yaxes(title=None)

        # Displaying the line chart in Streamlit
        st.plotly_chart(line_fig)
        
    def sunburst_plot():
            
        data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

        fig = px.sunburst(
            data,
            names='character',
            parents='parent',
            values='value',
        )
        
        st.plotly_chart(fig)


    def total_orders(a):
        a = a['network_order_id'].nunique()
        return a


    def Net_Order_Value(a):
        a=round(a['Net_order_value'].sum())
        return a

        
    def GOV(a):
        a = round(a['Gross_order_value'].nunique())
        return a

    def Gross_AOV(a):
        a = round(a['Gross_order_value'].mean(),2)
        return a

    def Net_AOV(a):
        return round(a['Net_order_value'].mean(),2)
            

    def Merchants(a):
        a = round(df['soi_merchant_id'].nunique(),2)
        return a


    def Customers(a):
        a = round(df['soi_cust_id'].nunique(),2)
        return a

    def gauge(a):

        fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = round(a['Net_order_value'].sum()),
            mode = "gauge+number+delta",
            title = {'text': "Total order value"},
            delta = {'reference': round(a['Net_order_value'].sum()) * .080, 'increasing': {'color': "skyblue"}},
            gauge = {'axis': {'range': [None, round(a['Net_order_value'].sum()) * 1.3]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 250], 'color': "lightgray"},
                        {'range': [250, 400], 'color': "gray"}],
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': round(a['Net_order_value'].sum()) * 1.2}}))

        # Displaying the line chart in Streamlit
        st.plotly_chart(fig)


    def custom_metric(label, value, font_size="18px"):
        st.markdown(f"""
            <style>
            @media screen and (max-width: 768px) {{
                .metric-label {{
                    font-size: calc({font_size} * 0.8);
                }}
                .metric-value {{
                    font-size: calc({font_size} * 1);
                }}
            }}
            @media screen and (max-width: 480px) {{
                .metric-label {{
                    font-size: calc({font_size} * 0.4);
                }}
                .metric-value {{
                    font-size: calc({font_size} * 1);
                }}
            }}
            .metric-container {{
                text-align: center;
                margin: 10px 0;
            }}
            .metric-label {{
                font-size: {font_size};
                font-weight: bold;
                display: block;
                margin-bottom: 5px;
            }}
            .metric-value {{
                font-size: calc({font_size} * 1.1);            
                display: block;
            }}
            </style>
            <div class="metric-container">
                <span class="metric-label">{label}</span>
                <span class="metric-value">{value}</span>
            </div>
        """, unsafe_allow_html=True)


    col_widths = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
    
    slicer_1, slicer_2, slicer_3, slicer_4, slicer_5   = st.columns(5) 
    
    slicer_6, slicer_7   = st.columns(2)

    col_1, col_2, col_3, col_4, col_5, col_6, col_7   = st.columns(col_widths) 

    with slicer_1:
        
        date_selector = st.date_input('Date', 
                                          value=(min_date, max_date), 
                                          min_value=min_date, 
                                          max_value=max_date)

        if isinstance(date_selector, tuple):  
            start_date, end_date = date_selector
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        else:  
            df = df[df['Date'] == date_selector]
        
    with slicer_2:
        l1_cn_options = ['All'] + list(df['l1_cn'].unique())
        l1_cn_selector = st.multiselect('Category', options=l1_cn_options, default='All')

        if 'All' not in l1_cn_selector:
            df = df[df['l1_cn'].isin(l1_cn_selector)]

    with slicer_3:
        merchant_name_options = ['All'] + list(df['merchant_name'].sort_values().unique())
        merchant_name_selector = st.multiselect('Merchant Name', options=merchant_name_options, default='All')

        if 'All' not in merchant_name_selector:
            df = df[df['merchant_name'].isin(merchant_name_selector)]   

    with slicer_4:
        cust_city_options = ['All'] + list(df['cust_city'].sort_values().unique())
        cust_city_selector = st.multiselect('Customer City', options=cust_city_options, default='All')

        if 'All' not in cust_city_selector:
            df = df[df['cust_city'].isin(cust_city_selector)] 
                
    with slicer_5:
        soi_sku_name_options = ['All'] + list(df['soi_sku_name'].sort_values().unique())
        soi_sku_name_options_selector = st.multiselect('Item', options=soi_sku_name_options, default='All')

        if 'All' not in soi_sku_name_options_selector:
            df = df[df['soi_sku_name'].isin(soi_sku_name_options_selector)]     
        
    with slicer_6:
        search_term_merchant = st.text_input('Merchant ID')
        soi_merchant_id_options = ['All'] + list(df['soi_merchant_id'].unique())
        filtered_merchant_options = [option for option in soi_merchant_id_options if search_term_merchant.lower() in str(option).lower()]
            
        if 'All' not in filtered_merchant_options:
            df = df[df['soi_merchant_id'].isin(filtered_merchant_options)]
        

    with slicer_7:
        search_term_cust = st.text_input('Customer ID')
        soi_cust_id_options = ['All'] + list(df['soi_cust_id'].unique())
        filtered_cust_options = [option for option in soi_cust_id_options if search_term_cust.lower() in str(option).lower()]

        if 'All' not in filtered_cust_options:
            df = df[df['soi_cust_id'].isin(filtered_cust_options)] 
        
    with col_1:
        
        net_order_value = GOV(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("Net Order Value", formatted_net_order_value)
        
    with col_2:
        net_order_value = Net_Order_Value(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("Net Order Value", formatted_net_order_value)

    with col_3:
        net_order_value = total_orders(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("total_orders", formatted_net_order_value)    

    with col_4:
        net_order_value = Gross_AOV(df)
        formatted_net_order_value = f"₹{net_order_value:,.2f}"
        custom_metric("Gross_AOV", formatted_net_order_value) 
                
    with col_5:
        net_order_value = Net_AOV(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("Net_AOV", formatted_net_order_value)     
        
    with col_6:
        net_order_value = Merchants(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("Merchants", formatted_net_order_value)    

    with col_7:
        net_order_value = Customers(df)
        formatted_net_order_value = f"₹{net_order_value:,.0f}"
        custom_metric("Customers", formatted_net_order_value)    

    chart_col, bar_col = st.columns(2)

    with chart_col:
        barchart(df)

    with bar_col:
        horizontal_barchart(df)

    category_wise_count_col, gauge_col = st.columns(2)

    with category_wise_count_col:
        linechart(df)

    with gauge_col:
        gauge(df)

    category_wise_count(df)
    sunburst_plot()

    # st.write(df)

    # with tabs[1]:
    #     st.header("Second Tab")
