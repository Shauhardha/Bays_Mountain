import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from datetime import date
from utils.feeding_utils import get_mammal_data
from utils.medical_utils import get_meds_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

def main():

    if "logged_in" not in st.session_state:
        if cookie_controller.get("logged_in") == True:
            st.session_state["user_id"] = cookie_controller.get("user_id")
            st.session_state["username"] = cookie_controller.get("username")
            st.session_state["role"] = cookie_controller.get("role")
            st.session_state.logged_in = True
        else:
            st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        navbar()
        with st.sidebar:
            if st.button("Logout", key="logout_button"):                
                st.session_state.logged_in = False
                clear_cookies()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.write(
                    """
                    <meta http-equiv="refresh" content="0; url=/" />
                    """,
                    unsafe_allow_html=True
                )
                st.stop()

        if 'form_clear' in st.session_state and st.session_state.form_clear:
            st.session_state.log_type_key = None
            st.session_state.form_clear = False
            st.rerun()

        st.title("BaysTrack Data Visualization")

        filter_option = st.radio("Log Type", ("Mammal", "Watershed", "Herpetarium"), horizontal=True)

        if filter_option == "Mammal":
            log_list = ["Feeding Log", "Medical Log", "Habitat Cleaning Log", "Enrichment Log", "Injury Log", "Sedation Log"]
        else:
            log_list = ["Feeding Log", "Medical Log", "Daily Care"]

        log_type = st.selectbox("Select Log Type", log_list, key="log_type_key", index=None)

        co1, co2, co3 = st.columns([1, 1, 1])
        with co1:
            from_date = st.date_input("Select From Date", value=date.today())
        with co3:
            to_date = st.date_input("Select To Date", value=date.today())

        st.session_state["log_type"] = log_type
        st.session_state["filter_option"] = filter_option

        st.write("---")

        if "submitted_flag" not in st.session_state:
            st.session_state["submitted_flag"] = False
        #st.session_state["submitted_flag"] = False
        if "submitted_data" not in st.session_state:
            st.session_state["submitted_data"] = pd.DataFrame()

        # Reset submitted_flag if log_type or filter_option changed
        if (
            "prev_log_type" not in st.session_state or
            "prev_filter_option" not in st.session_state or
            st.session_state["prev_log_type"] != log_type or
            st.session_state["prev_filter_option"] != filter_option
        ):
            st.session_state["submitted_flag"] = False

        # Update previous values
        st.session_state["prev_log_type"] = log_type
        st.session_state["prev_filter_option"] = filter_option

        if st.button("Generate Visuals"):
            if not log_type:
                st.error('Please select the log type before generating visuals!')
                return

            if filter_option == "Mammal" and log_type == "Feeding Log":
                df = get_mammal_data(from_date, to_date)
            elif filter_option == "Mammal" and log_type == "Medical Log":
                df = get_meds_data(from_date, to_date)

            st.session_state["submitted_data"] = df
            st.session_state["submitted_flag"] = True

        
        if st.session_state["submitted_flag"]:
            if filter_option == "Mammal" and log_type == "Feeding Log":
            #Feeding Log ------------------------------------------------------------------
                df = st.session_state["submitted_data"]    

                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{filter_option}_{log_type}_{from_date}_{to_date}.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

                st.write("---")

                #columns_for_food = ['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables', 'Mazuri Omnivore','Nebraska Brand', 'OTHER', 'Whole Prey']

                food_totals = df[['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables', 'Mazuri Omnivore',
                                'Nebraska Brand', 'OTHER', 'Whole Prey']].sum()
                food_df = food_totals.reset_index()
                food_df.columns = ['Food Type', 'Total Amount Fed (lbs)']
            

                chart = alt.Chart(food_df).mark_bar().encode(
                    x=alt.X('Food Type:N', title='Food Type', axis=alt.Axis(labelAngle=-45, labelColor='white', titleColor='white')),  # Rotate x-axis labels
                    y=alt.Y('Total Amount Fed (lbs):Q', title='Total Amount Fed (lbs)', axis=alt.Axis(labelColor='white', titleColor='white')),
                    color='Food Type:N',  # Different colors for each Food Type
                    tooltip=['Food Type', 'Total Amount Fed (lbs)']  # Show tooltip with food type and amount fed
                ).properties(
                    title='Total Food Fed by Type',
                    width=600,
                    height=400
                ).configure_title(
                    fontSize=18
                ).configure_axis(
                    labelColor='black',  # Color for axis labels
                    titleColor='black'   # Color for axis titles
                ).interactive()

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                # Grouped Stacked Bar Chart
                df_grouped = df.groupby('animal_group')[['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables',
                                                        'Mazuri Omnivore', 'Nebraska Brand', 'OTHER', 'Whole Prey']].sum().reset_index()
                df_melted = df_grouped.melt(id_vars='animal_group', var_name='Food Type', value_name='Amount')


                # Altair stacked bar chart
                chart = alt.Chart(df_melted).mark_bar().encode(
                    x=alt.X('animal_group:N', title='Animal Group', axis=alt.Axis(labelAngle=-45, labelColor='white')),  # Rotate x-axis labels and make them white
                    y=alt.Y('Amount:Q', title='Total Amount Fed (lbs)', axis=alt.Axis(labelColor='white')),  # Make y-axis labels white
                    color='Food Type:N',  # Color by Food Type
                    tooltip=['animal_group', 'Food Type', 'Amount'],  # Tooltip with details
                    order=alt.Order('Food Type:N', sort='ascending')  # Stack the bars
                ).properties(
                    title='Total Food Fed by Animal Type (Stacked)',
                    width=600,
                    height=400
                ).configure_title(
                    fontSize=18,
                    color='white'  # Set title color to white
                ).configure_axis(
                    labelColor='white',  # Set axis labels to white
                    titleColor='white'   # Set axis titles to white
                ).interactive()  # Make the chart interactive

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                # Heatmap
                # heatmap_data = df_melted.pivot(index='animal_group', columns='Food Type', values='Amount')
                # fig3 = go.Figure(data=go.Heatmap(
                #     z=heatmap_data.values,
                #     x=heatmap_data.columns,
                #     y=heatmap_data.index,
                #     colorscale='YlGnBu',
                #     text=heatmap_data.round(2).astype(str),
                #     texttemplate="%{text}",
                #     hovertemplate='Food: %{x}<br>Animal: %{y}<br>Amount: %{z:.2f}<extra></extra>',
                #     showscale=True
                # ))
                # fig3.update_layout(
                #     title='Heatmap of Food Types Fed to Each Animal Group',
                #     xaxis_title='Food Type',
                #     yaxis_title='Animal Group',
                #     xaxis=dict(showgrid=True, gridcolor='gray'),
                #     yaxis=dict(showgrid=True, gridcolor='gray'),
                #     plot_bgcolor='white'
                # )
                # st.plotly_chart(fig3)
                # st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                # Time Series Line Chart for Specific Selection
                df['Date'] = pd.to_datetime(df['datetime'])
                df['Month_Year'] = df['Date'].dt.to_period('M')
                df['Month_Year'] = df['Month_Year'].dt.to_timestamp()

                # Perform the melt operation beforehand
                melted_df = df.melt(
                    id_vars=['Date', 'Month_Year', 'animal_group'],
                    value_vars=['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables', 'Mazuri Omnivore',
                                'Nebraska Brand', 'OTHER', 'Whole Prey'],
                    var_name='Food Type',
                    value_name='Amount'
                )

                # Filter out rows where the Amount is 0 or NaN
                melted_df = melted_df.loc[melted_df['Amount'] > 0]

                # Extract unique animal groups and food types
                animal_options = melted_df['animal_group'].unique().tolist()

                if "selected_animals" not in st.session_state:
                    st.session_state["selected_animals"] = [animal_options[0]] if animal_options else []

                selected_animal = st.selectbox(
                    "Select Animal Group:", animal_options,
                    index=animal_options.index(st.session_state["selected_animals"][0]) if st.session_state["selected_animals"] else 0,
                    key="animal_selectbox"
                )

                # Filter the melted dataset based on the selected animal to dynamically update food options
                filtered_food_df = melted_df[melted_df['animal_group'] == selected_animal] if selected_animal else melted_df
                food_columns = filtered_food_df['Food Type'].unique().tolist()

                # Ensure the default value for selected_foods exists in the food_columns list
                if "selected_foods" not in st.session_state or not set(st.session_state["selected_foods"]).issubset(set(food_columns)):
                    st.session_state["selected_foods"] = [food_columns[0]] if food_columns else []

                selected_foods = st.multiselect(
                    "Select Food Column(s):", food_columns,
                    default=st.session_state["selected_foods"],
                    key="food_multiselect"
                )

                if selected_animal and selected_foods:
                    # Filter the melted dataset based on selected animals and foods
                    filtered_df = melted_df[
                        (melted_df['animal_group'] == selected_animal) &
                        (melted_df['Food Type'].isin(selected_foods))
                    ]

                    # Sort by Date to ensure proper line plotting
                    filtered_df = filtered_df.sort_values(by='Date')

                    test_group = filtered_df.groupby(['Month_Year','animal_group','Food Type'])['Amount'].sum().reset_index(name="Food_Amount")
                    test_group = test_group.sort_values(by='Month_Year')

                    fig = px.line(
                        test_group,
                        x='Month_Year',
                        y='Food_Amount',
                        color='Food Type',
                        line_dash='animal_group',
                        markers=True,
                        title="Animal Food Intake Over Time"
                    )
                    fig.update_layout(legend_title="Animal Group / Food Type")
                    config = {'scrollZoom': True}
                    st.plotly_chart(fig, use_container_width=True, config=config)

                    # st.download_button(
                    #     label="Download CSV ",
                    #     data=melted_df.to_csv(index=False).encode("utf-8"),
                    #     file_name=f"{filter_option}_{log_type}_{from_date}_{to_date}_melted.csv",
                    #     mime="text/csv",
                    #     icon=":material/download:",
                    # )
                else:
                    st.warning("Please select at least one animal and one food column.")

#----------------------------------------------------------------------------------
            #Medical Log ------------------------------------------------------------------

            elif filter_option == "Mammal" and log_type == "Medical Log":
                med_df = st.session_state["submitted_data"]    

                st.download_button(
                    label="Download CSV",
                    data=med_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{filter_option}_{log_type}_{from_date}_{to_date}.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

                top_medication = med_df[['Meloxicam','Cephalexin','Gabapentin','Bravecto','Intercepter']].sum()

                # Convert to DataFrame for Plotly
                top_med_df = top_medication.reset_index()
                top_med_df.columns = ['Medication', 'Count']

                # Base bar chart
                bars = alt.Chart(top_med_df).mark_bar().encode(
                    x=alt.X('Medication:N', sort='-y', axis=alt.Axis(labelAngle=0)),
                    y='Count:Q',
                    tooltip=['Medication', 'Count'],
                    color=alt.Color('Medication:N', legend=None)  # No legend
                )

                # Text labels on top of bars
                text = alt.Chart(top_med_df).mark_text(
                    dy=-5,
                    color='white'
                ).encode(
                    x=alt.X('Medication:N', sort='-y'),
                    y='Count:Q',
                    text='Count:Q'
                )

                # Combine both charts
                chart = (bars + text).properties(
                    width=600,
                    height=400,
                    title='Medication Type Count'
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)               


                # Get value counts and reset for plotting
                animal_counts = med_df['Animal'].value_counts().reset_index()
                animal_counts.columns = ['Animal', 'Count']

                bars = alt.Chart(animal_counts).mark_bar().encode(
                    x=alt.X('Animal:N', sort='-y', axis=alt.Axis(labelAngle=45)),
                    y='Count:Q',
                    tooltip=['Animal', 'Count'],
                    color=alt.Color('Animal:N', legend=None)
                )

                # Text labels above bars
                text = alt.Chart(animal_counts).mark_text(
                    dy=-5,  # move text above the bar
                    color='white'  # change to black if background is light
                ).encode(
                    x=alt.X('Animal:N', sort='-y'),
                    y='Count:Q',
                    text='Count:Q'
                )

                # Combine bar and text charts
                chart = (bars + text).properties(
                    width=600,
                    height=400,
                    title='Medication Giver per Animal'
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)


                # Aggregate medication counts by animal
                medication_counts = med_df.groupby('Animal')[['Gabapentin', 'Bravecto', 'Meloxicam', 'Intercepter', 'Cephalexin']].sum()

                # Prepare the data
                med_long = medication_counts.reset_index().melt(id_vars='Animal', var_name='Medication', value_name='Count')

                # Define color palette
                color_scale = alt.Scale(range=['#00FFFF', '#FFFF00', '#FF00FF', '#FF4500', '#32CD32'])  # Custom vivid colors

                chart = alt.Chart(med_long).mark_bar().encode(
                    x=alt.X('Animal:N', axis=alt.Axis(labelAngle=45, labelColor='white', titleColor='white')),
                    y=alt.Y('Count:Q', axis=alt.Axis(labelColor='white', titleColor='white')),
                    color=alt.Color(
                        'Medication:N',
                        scale=color_scale,
                        legend=alt.Legend(
                            titleColor='white',
                            labelColor='white',
                            labelFontSize=10,    # Smaller legend labels
                            titleFontSize=12     # Smaller legend title
                        )
                    ),
                    tooltip=['Animal', 'Medication', 'Count']
                ).properties(
                    width=1200,  # Larger figure width
                    height=500, # Larger figure height
                    title=alt.TitleParams(text='Medication Types per Animal', color='white')
                ).configure_view(
                    stroke=None,
                    fill='black'
                ).configure_axis(
                    grid=False
                ).configure_title(
                    fontSize=18,
                    color='white'
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                # Get counts
                success_counts = med_df['meds_taken'].value_counts().reset_index()
                success_counts.columns = ['Response', 'Count']

                # Create pie chart
                fig = px.pie(
                    success_counts,
                    names='Response',
                    values='Count',
                    title='Medication Success Rate',
                    hole=0,  # Use hole=0.4 for donut chart
                )

                # Optional: Add percentage labels inside the chart
                fig.update_traces(textinfo='percent+label')

                fig.update_layout(
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                

                med_df['Timestamp'] = pd.to_datetime(med_df['datetime'])
                med_df['Month_Year'] = med_df['datetime'].dt.to_period('M')
                med_col = ['Meloxicam', 'Cephalexin', 'Gabapentin', 'Bravecto', 'Intercepter']
                time_series = med_df.groupby('Month_Year')[med_col].sum()
                time_series.index = time_series.index.to_timestamp()
                time_series = time_series.reset_index()

                # Melt the DataFrame to long format for Plotly
                long_df = time_series.melt(id_vars='Month_Year', var_name='Medication', value_name='Count')

                # Plot with Plotly Express
                fig = px.line(
                    long_df,
                    x='Month_Year',
                    y='Count',
                    color='Medication',
                    markers=True,
                    title='Medication Administration Over Time'
                )
                fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Count',
                    hovermode='x unified',
                    template='plotly_dark'  # optional for dark theme
                )
                st.plotly_chart(fig, use_container_width=True)


                # Convert datetime and create Month_Year column
                # med_df['Timestamp'] = pd.to_datetime(med_df['datetime'])
                # med_df['Month_Year'] = med_df['Timestamp'].dt.to_period('M')
                # med_col = ['Meloxicam', 'Cephalexin', 'Gabapentin', 'Bravecto', 'Intercepter']

                # Prepare the time series data
                # time_series = med_df.groupby(['Month_Year','Animal'])[med_col].sum()
                # time_series['Month_Year'] = time_series['Month_Year'].dt.to_timestamp()
                # time_series = time_series.reset_index()

                # Melt the DataFrame to long format for Plotly
                # long_df = med_df.melt(id_vars=['Month_Year','Animal'], value_vars=med_col, var_name='Medication', value_name='Count')

                # # Filter out rows where Count is 0 or NaN (optional)
                # long_df = long_df.loc[long_df['Count'] > 0]

                # # Extract unique animals and medications for selection
                # animal_options = long_df['Animal'].unique().tolist()
                # medication_options = long_df['Medication'].unique().tolist()

                # # Initialize session state if not present
                # if "selected_animals" not in st.session_state:
                #     st.session_state["selected_animals"] = [animal_options[0]] if animal_options else []

                # if "selected_meds" not in st.session_state:
                #     st.session_state["selected_meds"] = [medication_options[0]] if medication_options else []

                # # Select animal(s) for filtering
                # selected_animal = st.selectbox(
                #     "Select Animal:", animal_options,
                #     index=animal_options.index(st.session_state["selected_animals"][0]) if st.session_state["selected_animals"] else 0,
                #     key="animal_selectbox"
                # )

                # # Select medication(s) for filtering
                # selected_meds = st.multiselect(
                #     "Select Medication(s):", medication_options,
                #     default=st.session_state["selected_meds"],
                #     key="medication_multiselect"
                # )

                # # Filter the DataFrame based on selected animal and medications
                # filtered_df = long_df[long_df['Medication'].isin(selected_meds)]

                # # If a specific animal is selected, filter by animal too
                # if selected_animal:
                #     filtered_df = filtered_df[med_df['Animal'] == selected_animal]

                # # Check if any filtered data is available
                # if not filtered_df.empty:
                #     # Sort the data by Month_Year for proper line plotting
                #     filtered_df = filtered_df.sort_values(by='Month_Year')

                #     # Group by Month_Year and Medication and sum the counts
                #     filtered_group = filtered_df.groupby(['Month_Year', 'Medication'])['Count'].sum().reset_index(name="Medication_Count")
                #     filtered_group = filtered_group.sort_values(by='Month_Year')

                #     # Create line plot using Plotly Express
                #     fig = px.line(
                #         filtered_group,
                #         x='Month_Year',
                #         y='Medication_Count',
                #         color='Medication',
                #         markers=True,
                #         title='Medication Administration Over Time'
                #     )
                #     fig.update_layout(
                #         xaxis_title='Date',
                #         yaxis_title='Count',
                #         hovermode='x unified',
                #         template='plotly_dark'  # optional for dark theme
                #     )
                #     # Display the plot in Streamlit
                #     st.plotly_chart(fig, use_container_width=True)
                # else:
                #     st.warning("No data available for the selected filters.")


            if st.button("Clear Filters"):
                
                st.session_state["submitted_data"] = pd.DataFrame()
                st.session_state["submitted_flag"] = False
                df = pd.DataFrame()
                st.session_state["from_date"] = date.today()
                st.session_state["to_date"] = date.today()
                # st.session_state["selected_animals"] = []
                # st.session_state["selected_foods"] = []
                del st.session_state["selected_animals"]
                del st.session_state["selected_foods"]
                del st.session_state.log_type_key
                st.session_state.form_clear = True
                st.rerun()


if __name__ == "__main__":
    main()
