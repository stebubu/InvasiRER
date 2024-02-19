import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import pymcdm
from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata

# Assuming your computational code is in a separate file named 'computational_code.py'
# and there is a function called 'run_computation' that takes two lists (weights and values)
# along with a DataFrame and returns some result. You need to adjust this according to your actual code.
# from computational_code import run_computation



def run_computation(weight_list, value_list, df):
    weights_geco=np.array(weight_list)
    types=np.array(value_list)
    alts = df[df.columns[1:]].to_numpy()

    # Define list with several weighting methods
    weighting_methods = [
    w.equal_weights,
    w.entropy_weights,
    w.standard_deviation_weights,
    w.gini_weights
    ]

    # To use the COMET method, we need to define characteristic values.
    # It could be achieved using `make_cvalues` static method of a COMET object.
    # Alternatively, characteristic values should be provided by an expert.
    c = COMET.make_cvalues(alts)


    # COMET method also uses a rate function to rate characteristic objects.
    # To automatize the process, `topsis_rate_function` could be used.
    #rate_function = COMET.topsis_rate_function(weights, types)

    # A similar thing should be done for the SPOTIS method. For this method decision
    # bounds should be provided. Bounds could be defined by a decision maker or
    # calculated automatically from the data.
    bounds = SPOTIS.make_bounds(alts)
    prefs = []
    ranks = []
    #geco pesi
    method= TOPSIS()
    pref = method(alts, weights_geco, types, bounds=bounds)
    rank = method.rank(pref)
    
    prefs.append(pref)
    ranks.append(rank)
    a = [f'$A_{{{i+1}}}$' for i in range(len(prefs[0]))]

    results=pd.DataFrame(zip(*prefs), columns=['Score'], index=a).round(3)
    return results


def main():

    # Assuming 'logo.png' is the logo image file in the same directory as your Streamlit app
    #logo_path = "logo.png"  # Or use a URL to an image: "https://example.com/logo.png"
    #st.image(logo_path, width=100)  # Adjust the width as necessary

    st.title("Analisi MCA per raking di idoneità alla laminazione invasi - RER")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("CSV File Content:")
        st.dataframe(df)

        weights = st.text_input("Enter 9 weight values separated by comma ex. 0.46,0.13,0.11,0.13,0.02,0.02,0.015,0.02,0.1", "")
        try:
            weight_list = [float(x.strip()) for x in weights.split(",") if x]
            if len(weight_list) != 9:
                st.error("Please enter exactly 9 weight values.")
            else:
                values = st.text_input("Enter 9 suitability [1=suitable] [-1=non suitable] values separated by comma ex. 1, 1, 1, 1, -1, -1, 1, -1, 1", "")
                value_list = [float(x.strip()) for x in values.split(",") if x]
                if len(value_list) != 9:
                    st.error("Please enter exactly 9 values.")
                else:
                    if st.button("Run Computation"):
                        # Simulate running your computation and generating a DataFrame with a 'score' column
                        df_result = run_computation(weight_list, value_list, df)
                       

                        # Sorting the DataFrame by 'score' in descending order
                        df_sorted = df_result.sort_values(by="Score", ascending=False)
                        
                        # Renaming index for visualization
                        df_sorted.index.name = "Alternative"
                        df_sorted.reset_index(inplace=True)
                        
                        #df_sorted=df_result
                        st.write("Results (sorted by score):")
                        st.dataframe(df_sorted)

                        # Plotting a bar plot with 'Alternative' as X and 'score' as Y
                        fig, ax = plt.subplots()
                        df_sorted.plot(kind='bar', x='Alternative', y='Score', ax=ax, legend=False)
                        ax.set_title('Score by Alternative')
                        ax.set_xlabel('Alternative')
                        ax.set_ylabel('Score')
                        st.pyplot(fig)
                        
                        

        except ValueError:
            st.error("Please enter valid numbers.")

if __name__ == "__main__":
    main()
