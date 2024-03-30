import streamlit as st
from snowflake.snowpark.functions import col

# Title of your Streamlit app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input field for name on order
name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('The name on your Smoothie will be:', name_on_order)

# Initialize connection to Snowflake
cnx = st.connection(type="snowflake", **st.secrets["snowflake"])

# Start a new session using the connection
with cnx as session:
    # Retrieve fruit options from the table
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name')).collect()
    fruit_names = [row['Fruit_name'] for row in my_dataframe]

    # Multi-select widget for choosing ingredients
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_names,
        max_selections=5
    )

    # Button to submit the order
    if st.button('Submit Order') and ingredients_list:
        ingredients_string = ', '.join(ingredients_list)  # Join the list with commas

        # SQL statement to insert the order
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
        # Execute the SQL statement
        session.sql(my_insert_stmt).collect()
        
        # Success message
        st.success('Order Submitted')

# This line is not necessary but included for completeness
st.stop()
