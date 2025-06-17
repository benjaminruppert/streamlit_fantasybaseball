import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Pitching Ratio Stat Calculator") 


st.markdown("""
This will help you determine how you far away you are from winning ERA and WHIP as it currently stands.

            
            
Also, if you are already ahead, and perhaps want to chase K's, it is useful to know how "loose" you can be with your streamers,
so we also calculate how many runs and walks + hits your streamers can allow.
            
Good luck.

---------------------------------------------------------------------------------                  
""")


with st.sidebar:
    st.header("⚾ Enter Your Stats⚾")
    innings_options = [f"{i} {frac}".strip() for i in range(251) for frac in ["", "1/3", "2/3"]]
    selected_ip = st.selectbox("Innings Pitched", innings_options)
    my_ip = eval(selected_ip.replace(" 1/3", "+1/3").replace(" 2/3", "+2/3"))
    my_era = st.number_input("ERA", min_value=0.0, step=0.01)
    my_whip = st.number_input("WHIP", min_value=0.0, step=0.01)

    st.header("⚾Enter Opponent Stats⚾")
    opp_era = st.number_input("Opp. ERA", min_value=0.0, step=0.01)
    opp_whip = st.number_input("Opp. WHIP", min_value=0.0, step=0.01)

def check_stats(my_era, opp_era, my_whip, opp_whip, my_ip):
    results = {}
    
    if my_era < opp_era:
        results['ERA'] = "You're winning already"
    else:
        results['ERA'] = compute_era_scenario(my_era, opp_era, my_ip)
    
    if my_whip < opp_whip:
        results['WHIP'] = "You're winning already"
    else:
        results['WHIP'] = compute_whip_scenario(my_whip, opp_whip)
    
    results['ERAahead'] = compute_era_ahead_scenario(opp_era, my_ip)
    results['WHIPahead'] = compute_whip_ahead_scenario(opp_era, my_ip, my_whip)



    return results

def compute_era_scenario(my_era, opp_era, my_ip):
    if opp_era == 0:
        return "N/A"
    
    my_er = my_era * my_ip / 9  # Calculate earned runs
    finalinnings = 9 * my_er / opp_era
    er_freeinnings = finalinnings - my_ip
    
    return er_freeinnings

def compute_whip_scenario(my_whip, opp_whip):

    mywalkshits = my_whip * my_ip
    finalinnings = (mywalkshits + opp_whip) - my_ip
    
    return finalinnings

def compute_era_ahead_scenario(opp_era, my_ip):
    my_er = my_era * my_ip / 9
    er_allowable = ((opp_era*my_ip)-9*(my_er))/9
    
    return er_allowable

def compute_whip_ahead_scenario(opp_era, my_ip, my_whip):
    mywalkshits = my_whip * my_ip
    walks_hits_allowable = (opp_whip*my_ip) - mywalkshits
    
    return walks_hits_allowable


# Perform computation
finaloutput = check_stats(my_era, opp_era, my_whip, opp_whip, my_ip)


#st.subheader("Shutout Innings Needed:")
#st.metric(label="ERA ----> ", value=finaloutput['ERA'])
#st.metric(label="WHIP ----> ", value=finaloutput['WHIP'])


# Create a layout with columns
col1, col2, col3 = st.columns([1.5, 1, 1])


with col1:
    st.subheader("Are You Losing? Shutout Innings Needed for Victory:")

with col2:
    era = finaloutput["ERA"]
    st.metric(label="ERA →", value=f"{float(era):.2f}" if my_era > opp_era and era not in ("N/A", None, "") else "N/A")

with col3:
    whip = finaloutput["WHIP"]
    st.metric(label="WHIP →", value=f"{float(whip):.2f}" if my_whip > opp_whip and whip not in ("N/A", None, "") else "N/A")


# Create a layout with columns
col4, col5, col6 = st.columns([1.5, 1, 1])

with col4:
    st.subheader("Already Winning? Allowable Earned Runs and Walks + Hits:")

with col5:
    era_ahead = finaloutput["ERAahead"]
    st.metric(label="ERA →", value=f"{float(era_ahead):.2f}" if my_era < opp_era and era_ahead not in ("N/A", None, "") else "N/A")

with col6:
    whip_ahead = finaloutput["WHIPahead"]
    st.metric(label="WHIP →", value=f"{float(whip_ahead):.2f}" if my_whip < opp_whip and whip_ahead not in ("N/A", None, "") else "N/A")

############ UNCOMMENT BELOW TO SHOW RANDOM ANALYSIS SECTION
#st.markdown("----------------------------------------------    --------------------------")

# Load DataFrame
#df = pd.read_csv("SQLdailypitching.csv")

# Streamlit App
#st.title("2025 Individual and Team Daily Pitching Stats")



# Dropdown for filtering
#selected_category = st.selectbox("Select Team: ", ["All"] + sorted(df['Table_ID'].dropna().unique()))

# Text input for searching
#search_text = st.text_input('Search Player by Name or Team Daily Totals:')

# Apply filters
#filtered_df = df.copy()
#if selected_category != "All":
#    filtered_df = filtered_df[filtered_df['Table_ID'] == selected_category]
#if search_text:
#    filtered_df = filtered_df[filtered_df['Pitching'].str.contains(search_text, case=False, na=False)]

# Show filtered DataFrame
#st.dataframe(filtered_df)


########### PLOTTTING ####################

#filtered_df_forplot = df.copy()
#filtered_df_forplot = filtered_df_forplot[filtered_df_forplot['Pitching'] == 'Team Totals']

#st.title('Inherited Runners vs Inherited Runners Scored')
#"""
#st.markdown(

#    """
    
#    This chart plots the relationship between inherited runners and inherited runs scored.
#    There is a positive relationship between the two, but instances of teams that have 
#    low inherited runs scored relative to their inherited runners may point to good relief
#    system.
    
#    This uses the Team Totals from the data above.
    
#    """

#)
#"""
#filtered_df_forplot = filtered_df_forplot.groupby("Table_ID")[["IR", "InS"]].sum().reset_index()


#st.scatter_chart(
#    data = filtered_df_forplot,
#    x='IR',
#    y='InS',
#    color='Table_ID',
#    x_label="Inherited Runners",
#    y_label="Inherited Runs Scored"
#)
        
#"""


st.markdown("""
            




            
Any recommendations, question, or just want to chat baseball and/or coding, send me an email!  benjamin.ruppert13@gmail.com             
""")
