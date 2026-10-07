import streamlit as st
import pandas as pd
import blank
import computation

st.set_page_config(layout="wide")

st.title("VFC Notion Count Automation")

st.write("Please enter the kms:")
kms = st.number_input("Kms:")

st.write("Please upload the file below")
file = st.file_uploader("Upload CSV", type="csv")

if file is not None:
    df = blank.InitialiseData(file)

    # Data cleaning operations
    missingJobCodes = blank.BlankJobCode(df)
    if len(missingJobCodes) > 0:
        st.write("Missing job codes detected. Please review the notion")

    blankCols = blank.BlanksOtherFields(df)
    if len(blankCols) > 0:
        st.write("Columns & Missing Information")
        st.write(blankCols)
    
    emptydarts = blank.DartCheck(df)
    if len(emptydarts) > 0:
        st.write("Total Number of darts was missing from:")
        st.write(emptydarts)


    # Run Calculations
    jobCode = computation.count_jobCode(df)
    calloutHours = computation.calloutHours(df)
    totalCalloutHours = computation.TotalCalloutTime(df)
    displacedTotal = computation.NumbDisplaced(df)
    totalAnimals = computation.TotalAnimals(df)
    totalDarted = computation.TotalDarted(df)
    totalSedated = computation.TotalSedated(df)
    otherMeds = computation.TotalOtherDrugs(df)
    drugCost = computation.TotalDrugCost(df)
    fuelCost = computation.FuelCost(kms)
    totalFuelCost = computation.TotalFuelCost(df, kms)
    prm = computation.PRMCount(df)
    totalVolHours = computation.TotalVolHours(df, prm, kms)

    st.write(f"PRM Hours: {prm}")

    # Append back out
    new_rows = pd.DataFrame([
    {"Job Code" : jobCode, "Callout Time": calloutHours, "Total Callout Time": totalCalloutHours, "Issue": f"Displaced: {displacedTotal}", "No of Animals": totalAnimals, "Outcome": f"Darted: {totalDarted[0]}", "Entered By": f"Sedated: {totalSedated}", "Darter/s": f"Other: {otherMeds}"},
    {},
    {"Issue": f"${drugCost:.2f}", "Animal Type": "drug costs"},
    {"Issue": kms, "Animal Type": "km"},
    {"Issue": f"${fuelCost:.2f}", "Animal Type": "fuel @ $0.91/km"},
    {"Issue": f"${totalFuelCost:.2f}", "Animal Type": "with tolls"},
    {},
    {"Issue": totalCalloutHours, "Animal Type": "total callout time"},
    {"Issue": prm, "Animal Type": "total hours of PRM team"},
    {"Issue": totalVolHours, "Animal Type": "Volunteer field team hours out for rescue"}
    ])

    df = pd.concat([df, new_rows], ignore_index=True)
    
    #st.dataframe(df)
    
    st.download_button(
        label="Download cleaned CSV",
        data=df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

