# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write(
    """
    "Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smooethie will be: ', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Join the list with commas

    # Prepare the SQL statement with named parameters
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
    VALUES (:1, :2)
    """

    # Display the SQL for debugging. Comment this out in production.
    # st.write("DEBUG SQL:", my_insert_stmt, ingredients_string, name_on_order)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Execute the SQL statement with parameters
        session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()
        
        st.success('Order Submitted')
    # The st.stop() is commented out for debugging. Uncomment it when the flow is confirmed to work.
    # st.stop()
