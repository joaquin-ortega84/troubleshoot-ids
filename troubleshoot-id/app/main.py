import streamlit as st
import pandas as pd

#### THE JUICE ##### OUR FORMULA CONVERTER!!!
# Formula to Convert SFDC digits from 15 to 18
def convert_15_to_18(sfdc_id):
    if len(sfdc_id) != 15:
        raise ValueError("ID must be 15 characters long")
    
    suffix = ""
    for i in range(0, 15, 5):
        chunk = sfdc_id[i:i+5]
        bits = 0
        for j in range(5):
            char = chunk[j:j+1]
            if char.isupper():
                bits += 2 ** j
        suffix += "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"[bits]
    
    return sfdc_id + suffix

#### THE WEB APP BEGINS HERE ####
st.title('Troubleshoot ID')

st.subheader('Convert 15 to 18 digit ID - SFDC to Einstein ID')

# Single ID Conversion

single_id = st.text_input('Enter 15-digit SFDC ID:')
if single_id:
    try:
        converted_single_id = convert_15_to_18(single_id)
        st.write('18-digit ID:', converted_single_id)
    except ValueError as e:
        st.error(e)

st.write('---')

# Upload CSV files
st.write('### Convert and Compare IDs from CSV files')
st.write('Salesforce (SFDC) IDs are 15 digits long. We must convert them to 18 digits to compare them with Einstein 18-digit IDs.')

st.subheader('Upload SFDC CSV')

# Upload SFDC file
uploaded_file_sfdc = st.file_uploader("Choose a SFDC file", key='sfdc')
if uploaded_file_sfdc is not None:
    sfdc_df = pd.read_csv(uploaded_file_sfdc)
    st.write(sfdc_df)
else:
    sfdc_df = None

st.subheader('Upload Einstein CSV')

# Upload Einstein file
uploaded_file_einstein = st.file_uploader("Choose an Einstein file", key='einstein')
if uploaded_file_einstein is not None:
    ein_df = pd.read_csv(uploaded_file_einstein)
    st.write(ein_df)
else:
    ein_df = None

# Button to trigger the comparison
if st.button("Compare"):
    if sfdc_df is not None and ein_df is not None:
        try:
            # Convert SFDC to 18 digits Contact ID
            sfdc_df['Converted IDs'] = sfdc_df['Contact ID'].apply(convert_15_to_18)

            # Compare the IDs
            sf_ids = set(sfdc_df['Converted IDs'])
            ein_ids = set(ein_df['Lead or Contact ID'])

            # IDs not found in Salesforce
            not_in_sf = ein_ids - sf_ids
            not_in_sf = list(not_in_sf)
            not_in_sf = ', '.join(not_in_sf)

            # IDs not found in Einstein
            not_in_ein = sf_ids - ein_ids
            not_in_ein_list = list(not_in_ein)
            not_in_ein = ', '.join(not_in_ein)

            # Output the results
            st.write('Missing in SFDC:', not_in_sf)
            st.write('Missing in Einstein:', not_in_ein_list)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload both SFDC and Einstein CSV files to compare.")
