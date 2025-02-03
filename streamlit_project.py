import streamlit as st
import pandas as pd
import numpy as np

st.title("Should you stream that pitcher? ")
st.subheader("Enter below and find out!")


st.subheader("First, let's check ERA")
opp_era = st.number_input("Enter your oppenent's ERA")
opp_Ks = st.number_input("Enter your oppenent's total strikeouts")
my_era = st.number_input("Enter your ERA")
my_Ks = st.number_input("Enter your total strikeouts")
my_ip = st.number_input("Enter your innings pitched")

##calc to get earned runs from era
my_er = my_era*my_ip/9
##calc to get K difference
kdiff = opp_Ks - my_Ks

##calc to return
if opp_era != 0:
    final = 9*my_er/opp_era
    finalinnings = final - my_ip
    finalinnine = 9/finalinnings
    finalksinnine = opp_Ks/9
    



##get data for scatter
df = pd.read_csv("SQLdailypitching.csv")


##add calculated columns from SQL
forera = df[["ER", "SO", "IP"]]
forera["K/9"] = 9*(forera["SO"] / forera["IP"]) 
forera["ERA"] = 9*(forera["ER"] / forera["IP"])

# Add the new row using loc (only K/9 and ERA will be filled out). ORDER MATTERS!
forera.loc[len(forera)] = [np.nan, np.nan, np.nan, kdiff, finalinnine]




if finalinnings > 0:   
    st.subheader("Here's how many earned runs you can allow in 9 IP:")
    finalinnine
else: st.subheader("You are already ahead")



st.subheader("Here's a scatterchart for the season and your data point plotted in yellow? Will it happen?")

# Function to apply color based on condition
def color_point(val, column):
    if (column == 'ERA' and val == finalinnine) or (column == 'K/9' and val == kdiff):
        return 'background-color: red'
    return ''



# Getting colors for scatterplot
def color_point(val, column):
    if (column == 'ERA' and val == finalinnine) or (column == 'K/9' and val == kdiff):
        return 'background-color: red'
    return ''

# Apply styling
styled_df = forera.style.applymap(lambda val: color_point(val, 'ERA'), subset=['ERA']) \
                        .applymap(lambda val: color_point(val, 'K/9'), subset=['K/9'])

# Adding colors back as a column
forera['color'] = forera.apply(lambda row: 'red' if (row['ERA'] == finalinnine and row['K/9'] == kdiff) else 'blue', axis=1)
# Adding for different sized circles
forera['frequency'] = forera.groupby(['ERA', 'K/9']).transform('size')



# Display the scatter chart with colors
st.scatter_chart(forera,x = "ERA",y = "K/9", color = "color", size = 'frequency')







