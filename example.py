git
import streamlit as st
import plotly_express as px
import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter, defaultdict

# page cofigurations
st.set_page_config(page_title="Penixar.com", page_icon=":tada:", layout="wide")
hide_st_style = """
               <style>
               footer {visibility : hidden;}
               header {visibilty : hidden;}
               <style/>
   """

# extracting data from excel sheet
df = pd.read_csv('C:/Users/user/PycharmProjects/onlinemarket/all_data_2.csv' )


#clean up data
nan_df = df[df.isna().any(axis=1)]
df = df.dropna(how= 'all') #dropping NAN
df = df[df['Order Date']. str[0:2] != 'Or']

#covert columns to correct type
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
df['Price Each'] = pd.to_numeric(df['Price Each'])



# App begins
st.title("Welcome to your Business Dashboard :wave:")
st.write(
            """
            Penixar is a platform that will help you analysis ,visualize and understand your business operations
            .It will answer questions such as:
            - what was the best month for sales? How much was earned that month?
            - At What times do customers usually buy your products?
            - What products are often sold together?
            - what product sold the most? why do you think it sold the most?

            """
)



#what was the best month for sales? How much was earned that month?
st.write("---")
st.subheader("What was the best month for sales? How much was earned that month?")
st.markdown('''
               Below is a bar chart showing different months and the amount of sales made per month. 
                       ''')

#add month column
df['Month'] = df['Order Date'].str[0:2]
df['Month'] = df['Month'].astype('int32')

#add sales column
df['Sales'] = df['Quantity Ordered'] * df['Price Each']


results = ((df.groupby('Month').sum())[["Sales"]])

product = px.bar(
    results,
    x= results.index,
    y= "Sales",
    title="<b> BEST MONTH FOR SALES </b>",
    template="plotly_white"

)

product.update_layout(
    xaxis= dict(title= "Months",tickmode= "linear"),
    plot_bgcolor= "rgba(0,0,0,0)",
    yaxis= (dict(title="Sales",showgrid= False))

)

st.plotly_chart(product)







#What time should we display advertisemnts to maximize likelihood of customers buying product
st.subheader("At what times do customers usually buy your products?")
st.markdown('''
               Below is a line chart showing time variations with the amount of orders made.
                       ''')


df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Hour'] = df['Order Date'].dt.hour
df['Minute'] = df['Order Date'].dt.minute

hours = [hour for hour, df in df.groupby('Hour')]
key2 = df.groupby(['Hour']).count()

orders = []
for value in key2['Quantity Ordered']:
    orders.append(value)


chart = pd.DataFrame(orders,hours)

product5 = px.line(
    chart,
    x= hours,
    y= orders,
    title="<b> ORDERS MADE BASED ON HOURS </b>",
    template="plotly_white",

)

product5.update_layout(
    xaxis= dict(title= "Hours",tickmode= "linear"),
    plot_bgcolor= "rgba(0,0,0,0)",
    yaxis= (dict(title="Order Quantity",showgrid= True))
)

st.plotly_chart(product5)






#what products are often sold together
st.subheader("What products are often sold together?")
st.markdown('''
               Below is a Table showing products and how ofthen this products are sold together. 
                       ''')

daf = df[df['Order ID'].duplicated(keep= False)]
daf['Grouped'] = daf.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
daf = daf[['Order ID', 'Grouped']].drop_duplicates()


count = Counter()

for row in daf['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))

list = []
list2 = []
for key, value in count.most_common(10):
    list.append(key)
    list2.append(value)


chart_data = pd.DataFrame()
chart_data['Items'] = list
chart_data['Orders made this Month'] = list2
st.write(chart_data)






#what product sold the most? why do you think it sold the most
st.subheader("What product sold the most? why do you think it sold the most?")
st.markdown('''
               Below is a bar chart and line chart displaying the product that sold the most. 
                       ''')


product_group = df.groupby('Product')
quantity_ordered = product_group.sum(['Quantity Order'])
quantities = []
for value in quantity_ordered['Quantity Ordered']:
    quantities.append(value)

products = [product for product, df in product_group]

chart3 = pd.DataFrame(quantities, products)

# prices of each product
prices = df.groupby('Product').mean()['Price Each']
st.write(prices)



with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        product1 = px.bar(
            chart3,
            x=products,
            y=quantities,
            title="<b> BEST PERFORMING PRODUCT </b>",
            template="plotly_white"

        )

        product1.update_layout(
            xaxis=dict(title= "Products",tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(title= "Order Quantity",showgrid=False))
        )
        st.plotly_chart(product1)

    with right_column:
        product8 = px.line(
            prices,
            x=prices.index,
            y='Price Each',
            title="<b> PRICES OF PRODUCTS </b>",
            template="plotly_white"

        )

        product8.update_layout(
            xaxis=dict(title="Products",tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(title="Prices (kwacha)",showgrid=True))
        )

        st.plotly_chart(product8)




