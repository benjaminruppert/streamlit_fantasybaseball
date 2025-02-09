import streamlit as st

st.title("Should you stream that pitcher?")
st.subheader("Enter below and find out!")

st.subheader("First, let's check ERA and WHIP categories:")

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
st.write(finaloutput)
