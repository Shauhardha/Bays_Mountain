import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from datetime import date
from utils.feeding_utils import get_mammal_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(initial_sidebar_state="collapsed")

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
            log_list = ["Feeding Log", "Enrichment Log", "Habitat Cleaning Log", "Medical Log", "Injury Log", "Sedation Log"]
        else:
            log_list = ["Feeding Log", "Medical Log", "Daily Care"]

        log_type = st.selectbox("Select Log Type", log_list, key="log_type_key", index=None)

        co1, co2, co3 = st.columns([1, 1, 1])
        with co1:
            from_date = st.date_input("Select From Date", value=date.today())
        with co3:
            to_date = st.date_input("Select To Date", value=date.today())

        st.write("---")

        if "submitted_flag" not in st.session_state:
            st.session_state["submitted_flag"] = False
        if "submitted_data" not in st.session_state:
            st.session_state["submitted_data"] = pd.DataFrame()

        if st.button("Generate Visuals"):
            if not log_type:
                st.error('Please select the log type before generating visuals!')
                return

            if filter_option == "Mammal" and log_type == "Feeding Log":
                df = get_mammal_data(from_date, to_date)

                st.session_state["submitted_data"] = df
                st.session_state["submitted_flag"] = True

        # Check if visuals should be shown
        if st.session_state["submitted_flag"]:
            df = st.session_state["submitted_data"]

            st.download_button(
                label="Download CSV",
                data=df.to_csv().encode("utf-8"),
                file_name=f"{filter_option}_{log_type}_{from_date}_{to_date}.csv",
                mime="text/csv",
                icon=":material/download:",
            )

            food_totals = df[['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables', 'Mazuri Omnivore',
                              'Nebraska Brand', 'OTHER', 'Whole Prey']].sum()
            food_df = food_totals.reset_index()
            food_df.columns = ['Food Type', 'Total Amount Fed (lbs)']

            fig = px.bar(
                food_df,
                x='Food Type',
                y='Total Amount Fed (lbs)',
                title='Total Food Fed by Type',
                labels={'Total Amount Fed (lbs)': 'Total Amount Fed (lbs)'},
                color='Food Type',
                template='plotly_white'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

            # Grouped Stacked Bar Chart
            df_grouped = df.groupby('animal_group')[['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables',
                                                      'Mazuri Omnivore', 'Nebraska Brand', 'OTHER', 'Whole Prey']].sum().reset_index()
            df_melted = df_grouped.melt(id_vars='animal_group', var_name='Food Type', value_name='Amount')

            fig2 = px.bar(df_melted, x='animal_group', y='Amount', color='Food Type',
                          title='Total Food Fed by Animal Type (Stacked)',
                          labels={'animal_group': 'Animal Group', 'Amount': 'Total Amount Fed (lbs)'},
                          text_auto=True)

            fig2.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
            st.plotly_chart(fig2)

            # Heatmap
            heatmap_data = df_melted.pivot(index='animal_group', columns='Food Type', values='Amount')
            fig3 = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='YlGnBu',
                text=heatmap_data.round(2).astype(str),
                texttemplate="%{text}",
                hovertemplate='Food: %{x}<br>Animal: %{y}<br>Amount: %{z:.2f}<extra></extra>',
                showscale=True
            ))
            fig3.update_layout(
                title='Heatmap of Food Types Fed to Each Animal Group',
                xaxis_title='Food Type',
                yaxis_title='Animal Group',
                xaxis=dict(showgrid=True, gridcolor='gray'),
                yaxis=dict(showgrid=True, gridcolor='gray'),
                plot_bgcolor='white'
            )
            st.plotly_chart(fig3)

            # Time Series Line Chart for Specific Selection
            df['Date'] = pd.to_datetime(df['datetime'])

            food_columns = ['Chicken', 'Fish', 'Fresh Fruits', 'Fresh Vegetables', 'Mazuri Omnivore',
                            'Nebraska Brand', 'OTHER', 'Whole Prey']
            animal_options = df['animal_group'].unique().tolist()

            if "selected_animals" not in st.session_state:
                st.session_state["selected_animals"] = [animal_options[0]] if animal_options else []
            if "selected_foods" not in st.session_state:
                st.session_state["selected_foods"] = ["Chicken"]

            selected_animals = st.multiselect(
                "Select Animal Group(s):", animal_options,
                default=st.session_state["selected_animals"],
                key="animal_multiselect"
            )

            selected_foods = st.multiselect(
                "Select Food Column(s):", food_columns,
                default=st.session_state["selected_foods"],
                key="food_multiselect"
            )

            # st.session_state["selected_animals"] = selected_animals
            # st.session_state["selected_foods"] = selected_foods

            if selected_animals and selected_foods:
                filtered_df = df[df['animal_group'].isin(selected_animals)]

                melted_df = filtered_df.melt(
                    id_vars=['Date', 'animal_group'],
                    value_vars=selected_foods,
                    var_name='Food Type',
                    value_name='Amount'
                )
                melted_df = melted_df[melted_df['Amount'] > 0]

                fig = px.line(
                    melted_df,
                    x='Date',
                    y='Amount',
                    color='animal_group',
                    line_dash='Food Type',
                    markers=True,
                    title="Animal Food Intake Over Time"
                )
                fig.update_layout(legend_title="Animal Group / Food Type")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("Please select at least one animal and one food column.")

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
