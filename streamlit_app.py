# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie"""
)
name_on_order = st.text_input("Name of Smootie")
st.write(name_on_order)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect("Ingredient",my_dataframe,max_selections = 5)


#option = st.selectbox(
#    "Which fruits you want?",
#    ("Banana", "Stawberries", "Peaches"),  
#)
if ingredients_list: 
    st.write("You favourite fruit is:", ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button("Submit")
    if time_to_insert:
        st.write(my_insert_stmt)
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
