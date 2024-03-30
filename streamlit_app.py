import streamlit as st
import snowflake.connector
import requests

# Access Snowflake credentials from Streamlit secrets
snowflake_secrets = st.secrets["snowflake"]

# Establish a connection to Snowflake
conn_params = {
    "account": snowflake_secrets["account"],
    "user": snowflake_secrets["user"],
    "password": snowflake_secrets["password"],
    "warehouse": snowflake_secrets["warehouse"],
    "database": snowflake_secrets["database"],
    "schema": snowflake_secrets["schema"],
}

# If using Snowflake connector directly
conn = snowflake.connector.connect(**conn_params)
cur = conn.cursor()

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('The name on your Smoothie will be:', name_on_order)

# Retrieve fruit options from Snowflake and display in multiselect
try:
    cur.execute("SELECT Fruit_name FROM smoothies.public.fruit_options")
    fruit_options = cur.fetchall()
    fruit_names = [fruit[0] for fruit in fruit_options]

    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_names,
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list)

        if st.button('Submit Order'):
            # Insert order into Snowflake
            insert_query = f"""
                INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                VALUES ('{ingredients_string}', '{name_on_order}')
            """
            cur.execute(insert_query)
            st.success('Order Submitted')

            # After submitting the order, display nutritional information about a fruit
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

finally:
    cur.close()
    conn.close()
