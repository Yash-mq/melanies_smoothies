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

# Retrieve fruit options from Snowflake
cur.execute("SELECT FRUIT_NAME, SEARCH_ON FROM smoothies.public.fruit_options")
fruit_options_df = cur.fetch_pandas_all()

# Convert the Snowflake Dataframe to a Pandas Dataframe
pd_df = fruit_options_df

name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=pd_df['FRUIT_NAME'].tolist(), # Display the fruit names in the multiselect
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    # For each fruit in the list, fetch the SEARCH_ON value and display nutritional information
    for fruit_chosen in ingredients_list:
        # Use the LOC function to find the SEARCH_ON value for the chosen fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # API call using the search_on value
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        if fruityvice_response.ok:
            # Process the API response here as needed, e.g., convert to dataframe
            fruit_data = fruityvice_response.json()
            st.subheader(f"{fruit_chosen} Nutrition Information")
            st.json(fruit_data)  # or use st.dataframe() to display it as a table
        else:
            st.error(f"Failed to get nutritional information for {fruit_chosen}")

# Close the cursor and connection to Snowflake
cur.close()
conn.close()
