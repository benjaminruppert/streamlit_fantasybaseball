import streamlit as st
import pandas as pd
import numpy as np


finalinnine = 0
finalinnings = 0

##need to remove this
opp_Ks = 10
my_Ks = 5


st.title("Should you stream that pitcher? ")
st.subheader("Enter below and find out!")


st.subheader("First, let's check to see if your ERA and WHIP goals are in reach")
opp_era = st.number_input("Enter your oppenent's ERA")
opp_whip = st.number_input("Enter your oppenent's WHIP")
my_era = st.number_input("Enter your ERA")
my_whip = st.number_input("Enter your WHIP")
my_ip = st.number_input("Enter your innings pitched")

## make this into a function!
if opp_era > my_era:
    st.subheader("You are already ahead in ERA")
if opp_whip > my_whip:
    st.subheader("You are already ahead in WHIP")
    

##calc to get earned runs from era
my_er = my_era*my_ip/9
##calc to get additional walks+hits for whip
addwalkshits = opp_whip*(my_ip + 9)
##calc to get K difference
kdiff = opp_Ks - my_Ks

##calc to return for era
if opp_era != 0:
    #final = 9*my_er/opp_era
    finalinnings = (9*my_er-opp_era*my_ip)/opp_era
    finalinnine = (9*my_er)/(my_ip + finalinnings)
    finalksinnine = opp_Ks/9

##ERA again...
#if opp_era != 0:
    #finalinnine = finalinnings/9



##calc to return for whip
finalwhip = addwalkshits/(my_ip + 9)


    



##get data for scatter
df = pd.read_csv("SQLdailypitching.csv")


##add calculated columns from SQL
forera = df[["ER", "SO", "IP"]]
forera["K/9"] = 9*(forera["SO"] / forera["IP"]) 
forera["ERA"] = 9*(forera["ER"] / forera["IP"])

# Add the new row using loc (only K/9 and ERA will be filled out). ORDER MATTERS!
forera.loc[len(forera)] = [np.nan, np.nan, np.nan, kdiff, finalinnine]


# Output
st.subheader("Here's how many run free innings you need")
finalinnine
finalinnings
st.subheader("Here's the WHIP you need from your streamers (scaled to 9IP)")
finalwhip




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







