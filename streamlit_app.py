import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🫐🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬🥬Kale,Spinach and Rocket Smoothie')
streamlit.text('🥚Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
#IMPORT PANDAS
streamlit.header('🍌🍓Build your own Fruit Smoothie🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create the repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
          fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
          fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
          streamlit.dataframe(fruityvice_normalized)
#IMPORT REQUESTS
streamlit.header("Fruityvice Fruit Advice!")
try:
         fruit_choice=streamlit.text_input('what fruit would you like information about?')
         if not fruit_choice:
                  streamlit.error("please select a fruit to get information.")
         else:
          back_from_function=get_fruityvice_data(fruit_choice)
          streamlit.dataframe(back_from_function)

except URLError as e:
      streamlit.error();
#streamlit.write('The user entered ', fruit_choice)

streamlit.header("the fruit load list contains:")
#snowflake-related functions
def get_fruit_load_list():
          with my_cnx.cursor() as my_cur: 
               my_cur.execute("SELECT * FROM fruit_load_list")
               return my_cur.fetchall()

#add button to load a fruit
if streamlit.button('get the fruit load list'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
          my_data_rows = get_fruit_load_list()
          streamlit.dataframe(my_data_rows)

#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
          with my_cnx.cursor() as my_cur:
                    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
                    return "thanks for adding"+new_fruit
          
 add_my_fruit=streamlit.text_input('what fruit whould you like to add?')
 if streamlit.button('add a fruit to the list'):
                my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          back_from_function=insert_row_snowflake(add_my_fruit)
          streamlit.text(back_from_function)




#DONT RUN ANY THING PAST HERE WHILE WE TROUBLESHOOT
#STREAMLIT.STOP()





#streamlit.header("The fruit load list contains:")


#allow the end user to add a fruit to the list
#add_my_fruit=streamlit.text_input('what fruit would you like to add?')
#streamlit.write('Thanks for adding'+ add_my_fruit)

#THIS WILL NOT WORK CORRECTLY,BUT JUST GO WITH IT FOR NOW
#MY_CUR.EXECUTE("insert into fruit_load_list('from sreamlit')")
