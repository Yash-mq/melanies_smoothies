import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Initialize connection to Snowflake using the secrets
snowflake_secrets = st.secrets["snowflake"]
cnx = st.connection(
    type="snowflake",
    account=snowflake_secrets["account"],
    user=snowflake_secrets["user"],
    password=snowflake_secrets["password"],
    warehouse=snowflake_secrets["warehouse"],
    database=snowflake_secrets["database"],
    schema=snowflake_secrets["schema"]
)

# Start a new session using the connection
with cnx as session:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name')).collect()
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        [row['Fruit_name'] for row in my_dataframe],
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list)  # Join the list with commas

        # Prepare the SQL statement with named parameters
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Button to submit the order
        if st.button('Submit Order'):
            # Execute the SQL statement with parameters
            session.sql(my_insert_stmt).collect()
            
            st.success('Order Submitted')
