import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError


streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas  
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)




streamlit.header("Fruityvice Fruit Advice!")

try:
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
fruit_choice = streamlit.text_input('What fruit would you like information about?')
if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
else:
  streamlit.write('The user entered ', fruit_choice)
  #import requests
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
  #streamlit.text(fruityvice_response.json())
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  streamlit.write('The user entered ', fruit_choice)
  # normalise the json response
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  #streamlit.text(fruityvice_normalized) 
  # this will show the data in table form
  streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()


streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("select * from fruit_load_list")
my_display=my_cur.fetchall()
streamlit.text("The fruit load list contains :")
streamlit.dataframe(my_display)


input=streamlit.text_input("What fruit you would like to add?","kiwi")
streamlit.text("thanks for adding " + input )

my_cur.execute("insert into fruit_load_list values('from stream_lit')")
