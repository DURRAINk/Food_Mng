import streamlit as st
import plotly.express as px
import pandas as pd
from Database import * #search_food, prov_names, locations, food_types,engine, sql_queries, prov_city, get_table_data, update_query,tables

queries=["1. How many food providers and receivers are there in each city?",
    "2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?",
    "3. What is the contact information of food providers in a specific city?", "4. Which receivers have claimed the most food?",
    "5.  What is the total quantity of food available from all providers?","6. Which city has the highest number of food listings?",
    "7. What are the most commonly available food types?","8. How many food claims have been made for each food item?", 
    "9. Which provider has had the highest number of successful food claims?","10. What percentage of food claims are completed vs. pending vs. canceled?",
    "11. What is the average quantity of food claimed per receiver?","12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?",
    "13. What is the total quantity of food donated by each provider?","14. Claim date and expiry date of each food item",
    "15. Which type of Receiver has received the highest quantity of food?"]

# Set the page configuration
st.set_page_config(
    page_title="Food Management System", page_icon="🍽️", layout="wide",)

# Custom CSS for background image
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://tse3.mm.bing.net/th/id/OIP.e6KJKrrsWOTUw00Nt2ABogHaFL?w=2000&h=1397&rs=1&pid=ImgDetMain&o=7&rm=3");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Food Management System")

sidebar=st.sidebar
sidebar.title("Navigation")
menu=sidebar.radio("Go to", ["Search","CRUD Operations", "Analysis", "Contact Providers/Receivers","About Us"])

# Search-------------------------------------------------------------------------------------------
if menu == "Search":
    def on_search():
        if opts['location'] == "'all'":
            opts['location'] = 'fl.Location'
        if opts['provider'] == "'all'":
            opts['provider'] = 'pd.Name'
        if opts['food_type'] == "'all'":
            opts['food_type'] = 'fl.Food_Type'
        return opts
    st.header("Search Food Listings")
    st.write("Search for food listings based on provider, location, and food type.")
    opts={'location': 'all', 'provider': 'all', 'food_type': 'all'}
    col_1,col_2,col_3 = st.columns(3)
    opts['location']="'"+ col_2.selectbox("Select Location", ['all']+locations)+"'"
    opts['provider']="'"+ col_1.selectbox("Select Provider Type", ['all']+prov_names)+"'"
    opts['food_type']="'"+ col_3.selectbox("Select Food Type", ['all']+food_types)+"'"
    search_button=st.button("Search")
    if search_button:
        result=on_search()
        df=search_food(result)
        if not df.empty:
            st.subheader("Search Results")
            st.dataframe(df)
        else:
            st.warning("No results found for the selected criteria.")

#Crud Operations------------------------------------------------------------------------------------------
elif menu == "CRUD Operations":
    st.header("CRUD Operations")
    st.write("Create, Read, Update, or Delete records from here.")

    # --- Initialize session state flags ---
    if 'select_Dataset' not in st.session_state:
        st.session_state['select_Dataset'] = None
    if 'select_Operation' not in st.session_state:
        st.session_state['select_Operation'] = None
    if 'operation_triggered' not in st.session_state:
        st.session_state['operation_triggered'] = False

    # --- Dataset and Operation Selection ---
    col1, col2 = st.columns(2)
    table_name = col1.selectbox("Select Dataset", ["Claims Data", "Food Listings Data", "Providers Data", "Receivers Data"])
    operation = col2.selectbox("Select Operation", ["Read", "Create", "Update", "Delete"])

    # --- Submit Button ---
    if st.button("Submit"):
        st.session_state['select_Dataset'] = table_name
        st.session_state['select_Operation'] = operation
        st.session_state['operation_triggered'] = True

    # --- Perform Operation ---
    if st.session_state['operation_triggered']:
        selected_table = st.session_state['select_Dataset']
        selected_operation = st.session_state['select_Operation']

        # --- Read Operation ---
        if selected_operation == "Read":
            data = get_table_data(selected_table)
            st.dataframe(data)

        # --- Create Operation ---
        elif selected_operation == "Create":
            data = get_table_data(selected_table)
            lst = data.columns.tolist()

            st.subheader("Create New Record")

            # Divide columns into two rows
            half = len(lst) // 2 + len(lst) % 2
            row1_cols = st.columns(half)
            row2_cols = st.columns(len(lst) - half)

            new_record = {}

            new_record[lst[0]]=row1_cols[0].text_input(f"The {lst[0]}",
                                                       value=data.at[data.index[-1], lst[0]] + 1 if not data.empty else 1, disabled=True)
           
            # First row inputs
            for i, col in enumerate(lst[1:half]):
                
                i+=1
                if data[col].dtype == 'int64':
                    new_record[col] = row1_cols[i].number_input(f"Enter {col}", value=0, step=1)
               
                else:
                    new_record[col] = row1_cols[i].text_input(f"Enter {col}")
                   

            # Second row inputs
            for i, col in enumerate(lst[half:]):
                
                if data[col].dtype == 'int64':
                    new_record[col] = row2_cols[i].number_input(f"Enter {col}", value=0, step=1)
                
                else:
                    new_record[col] = row2_cols[i].text_input(f"Enter {col}")
                    
            # Confirm creation
            if st.button("Add Record"):
                st.success("✅ New record added successfully!")
                st.dataframe(insert_table(tables[selected_table], new_record))
                
        #---Update Operation-----
        elif selected_operation == "Update":
            data = get_table_data(selected_table)
            lst = data.columns.tolist()

            st.subheader("Update Record")

            # Select row to update
            id = st.number_input(f"Enter {lst[0]} ", min_value=data[lst[0]].min(), max_value=data[lst[0]].max(), step=1)

            # Pre-fill current values
            idx = data.index[data[lst[0]] == id].tolist()[0]
            current_values = data.iloc[idx]

            # Divide columns into two rows
            attrs=lst[1:]
            half = len(attrs) // 2 #+ len(attrs) % 2
            row1_cols = st.columns(half)
            row2_cols = st.columns( len(attrs) -half)

            updated_record = {}

            # First row inputs
            for i, col in enumerate(attrs[:half]):
                if data[col].dtype == 'int64':
                    updated_record[col] = row1_cols[i].number_input(f"Update {col}", value=int(current_values[col]), step=1)
                
                else:
                    updated_record[col] = row1_cols[i].text_input(f"Update {col}", value=str(current_values[col]))

            # Second row inputs
            for i, col in enumerate(attrs[half:]):
                if data[col].dtype == 'int64':
                    updated_record[col] = row2_cols[i].number_input(f"Update {col}", value=int(current_values[col]), step=1)
               
                else:
                    updated_record[col] = row2_cols[i].text_input(f"Update {col}", value=str(current_values[col]))

            # Confirm update
            if st.button("Update Record"):
                st.success("✅ Record updated successfully!")
                st.dataframe(update_table(tables[selected_table], updated_record, lst, id))

        #---Delete Operation-----
        elif selected_operation == "Delete":
           
            data = get_table_data(selected_table)
            lst = data.columns.tolist()

            st.subheader("Delete Record")

            # Select the primary key value to delete
            id = st.number_input(
                f"Select {lst[0]} to delete",
                min_value=int(data[lst[0]].min()),
                key="delete_id")

            # Show the selected record for confirmation
            if id in data[lst[0]].values:
                idx = data.index[data[lst[0]] == id][0]
                st.write("Record to be deleted:")
                st.dataframe(data.loc[[idx]])

                # Confirm deletion
                if st.button("Confirm Delete"):
                    delete_record(tables[selected_table], id, lst)
                    st.success(f"✅ Record with {lst[0]} = {id} deleted successfully!")
            else:
                st.warning(f"No record found with {lst[0]} = {id}")

        # Invalid operation
        else:
            st.error("Invalid operation selected. Please choose a valid operation.")


#Data Analysis--------------------------------------------------------------------
elif menu == "Analysis":        
    st.header("Analysis")
    st.write("Get insights from the data by applying differrent Queries.")
    index=queries.index(st.selectbox("Select Query", queries))+1
    if index == 3:
        prov_loc= st.selectbox("Select Location", prov_city)
        query = sql_queries[index].format(prov_loc)
        df_3rd=pd.read_sql(query, engine)
    run_query=st.button("Run Query")
    if run_query:
        if index ==1:
            df1= pd.read_sql(sql_queries[0], engine)
            df2= pd.read_sql(sql_queries[1], engine)
            col1, col2 = st.columns(2)
            col1.subheader("Total Providers from each city")
            col1.dataframe(df1)
            col2.subheader("Total Receivers from each city")
            col2.dataframe(df2)
        elif index == 3:
            st.dataframe(df_3rd)
        else:
            data=pd.read_sql(sql_queries[index], engine)
            st.dataframe(data)
            if data.empty:
                st.warning("No data found for the selected query.")
            elif data.shape[1] == 2 and data.shape[0]< 10:
                st.subheader("Bar Chart")
                st.bar_chart(data,x=data.columns[0], y=data.columns[1],horizontal=True)
                
        
#Contact Providers and Receivers----------------------------------------
elif menu == "Contact Providers/Receivers":
    st.header("Contact Providers and Receivers")
    st.divider()
    prov, rece = st.columns(2)
    prov.subheader("Providers Phone Book")
    prov.dataframe(contact_providers())

    rece.subheader("Receivers Phone Book")
    rece.dataframe(contact_receivers())

# About Us-------------------------------------------------------------
elif menu == "About Us":
    st.header("About Us")
    st.divider()
    st.write("developed by")
    st.header('Durrain Khan')
    st.write("Data Science, Machine Learning snd AI enthusiast.")
    st.subheader("Links")
    c1,c2,c3 = st.columns(3)
    c1.link_button("LinkedIn Profile", "https://www.linkedin.com/in/durrain-khan-pathan-728762304")
    c2.link_button("GitHub Profile", "https://github.com/DURRAINk")
    c3.write("durrainpathan123@gmail.com")
    st.divider()
    st.write("Rate this app")
    stars=st.feedback("stars")
    if stars == None:
        stars = -1
    
    if stars > -1 and stars <= 3:
        
        st.write(f"Thank you for your feedback! You rated this app {stars+1} stars.")
    elif stars >3:
            st.success(f"Thank you for your positive feedback! You rated this app {stars+1} stars.")
            st.balloons()
