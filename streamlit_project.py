import streamlit as st
import pandas as pd

st.title("Pitching Ratio Stat Caclulator") 

st.markdown("""
This will help you determine how you far away your are from winning ERA and WHIP as it currently stands.
If you are already ahead, then flip entries in columns below to see how safe you are.

""")







#opp_era = st.number_input("Enter your opponent's ERA")
#opp_whip = st.number_input("Enter your opponent's WHIP")
#my_era = st.number_input("Enter your ERA")
#my_whip = st.number_input("Enter your WHIP")
#my_ip = st.number_input("Enter your innings pitched")

# Create two columns
col1, col2 = st.columns(2)

# User's stats
with col1:
    st.subheader("Your Stats")
    innings_options = [f"{i} {frac}".strip() for i in range(251) for frac in ["", "1/3", "2/3"]]

# User input for innings pitched
    selected_ip = st.selectbox("Innings Pitched", innings_options)

# Convert to float
    my_ip = eval(selected_ip.replace(" 1/3", "+1/3").replace(" 2/3", "+2/3"))
    my_era = st.number_input("ERA", min_value=0.0, step=0.01)
    my_whip = st.number_input("WHIP", min_value=0.0, step=0.01)

# Opponent's stats
with col2:
    st.subheader("Opponent Stats")
    opp_era = st.number_input("Opponent ERA", min_value=0.0, step=0.01)
    opp_whip = st.number_input("Opponent WHIP", min_value=0.0, step=0.01)


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
        return "N/A"
    
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


#st.subheader("Shutout Innings Needed:")
#st.metric(label="ERA ----> ", value=finaloutput['ERA'])
#st.metric(label="WHIP ----> ", value=finaloutput['WHIP'])


# Create a layout with columns
col1, col2, col3 = st.columns([1.5, 1, 1])  # Adjust width ratios as needed

with col1:
    st.subheader("Shutout Innings Needed:")

with col2:
    st.metric(label="ERA →", value=finaloutput["ERA"])

with col3:
    st.metric(label="WHIP →", value=finaloutput["WHIP"])




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

