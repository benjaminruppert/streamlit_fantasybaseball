import streamlit as st
import pandas as pd

st.title("Need help with ratio stats?")

st.markdown("""
This will help you determine how you far away your are from winning ERA and WHIP as it currently stands.








Enter matchup stats below:









""")







opp_era = st.number_input("Enter your opponent's ERA")
opp_whip = st.number_input("Enter your opponent's WHIP")
my_era = st.number_input("Enter your ERA")
my_whip = st.number_input("Enter your WHIP")
my_ip = st.number_input("Enter your innings pitched")

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
    
    return results

def compute_era_scenario(my_era, opp_era, my_ip):
    if opp_era == 0:
        return "Opponent's ERA is zero, computation not possible."
    
    my_er = my_era * my_ip / 9  # Calculate earned runs
    finalinnings = 9 * my_er / opp_era
    er_freeinnings = finalinnings - my_ip
    
    return er_freeinnings

def compute_whip_scenario(my_whip, opp_whip):

    mywalkshits = my_whip * my_ip
    finalinnings = (mywalkshits + opp_whip) - my_ip
    
    return finalinnings

# Perform computation
finaloutput = check_stats(my_era, opp_era, my_whip, opp_whip, my_ip)


st.subheader("Shutout Innings Needed:")


# Display results
if not finaloutput:
    st.write("Please enter the stats, numbers will appear here")
else:
    st.write(finaloutput)


# Load DataFrame
df = pd.read_csv("SQLdailypitching.csv")

# Streamlit App
st.title("2024 Individual and Team Daily Pitching Stats")

# Dropdown for filtering
selected_category = st.selectbox("Select Team: ", ["All"] + sorted(df['Table_ID'].dropna().unique()))

# Text input for searching
search_text = st.text_input('Search Player by Name or Team Daily Totals:')

# Apply filters
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Table_ID'] == selected_category]
if search_text:
    filtered_df = filtered_df[filtered_df['Pitching'].str.contains(search_text, case=False, na=False)]

# Show filtered DataFrame
st.dataframe(filtered_df)

