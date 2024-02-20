import pandas as pd
from rapidfuzz import process
import streamlit as st

# Function to perform auto-coding
def auto_code(df, brand_list):
    # Define your get_matches function
    def get_matches(query, choices, min_similarity=80):
        if pd.isnull(query):
            return ""
        else:
            query = str(query).strip().lower().capitalize()  # Convert to string before applying string operations
            results = process.extractOne(query, choices)
            if results and results[1] >= min_similarity:
                # If result is 2 or 3 characters long, fully capitalize it
                if len(results[0]) in [2, 3]:
                    return results[0].upper()
                # Otherwise, return result in sentence case
                return results[0].capitalize()
            return "Other"
    
    # Get columns that start with "QO"
    qo_columns = [col for col in df.columns if col.startswith("QO")]
    
    # Loop through QO columns and auto-code them
    for col in qo_columns:
        df[col + "_auto_coded"] = df[col].apply(get_matches, args=(brand_list,))
    
    return df

# Main Streamlit app
def main():
    st.title("Auto-Coding App")
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the uploaded DataFrame
        st.write("Original DataFrame:")
        st.write(df)
        
        # Perform auto-coding
        brand_list_path = "C:/Users/VivekThaker/MaMs 2023/Brandlist.csv"  # Local file path
        brand_list = pd.read_csv(brand_list_path)['Brands_list'].str.capitalize().tolist()
        df_auto_coded = auto_code(df, brand_list)
        
        # Display the auto-coded DataFrame
        st.write("Auto-coded DataFrame:")
        st.write(df_auto_coded)
        
        # Download the auto-coded DataFrame as CSV
        csv_download_link = df_auto_coded.to_csv(index=False)
        st.download_button("Download Auto-coded CSV", data=csv_download_link, file_name="auto_coded_output.csv", mime="text/csv")
    
    # Add another tab for managing the brand list
    with st.sidebar:
        st.title("Manage Brand List")
        st.write("This is where you can view and modify the brand list.")
        
        # Load and display the brand list
        brand_list_path = "C:/Users/VivekThaker/MaMs 2023/Brandlist.csv"  # Local file path
        brand_list = pd.read_csv(brand_list_path)
        st.write("Brand List:")
        st.write(brand_list)

# Run the app
if __name__ == "__main__":
    main()
