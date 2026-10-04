import pandas as pd

# Count number of Job Codes
def count_jobCode(df):
    jobs = df["Job Code"].count()
    return jobs

# Sum of Callout Hours
def calloutHours(df):
    hours = df["Callout Time"].sum()
    return hours

# Sum of Callout Hours multiplied by volunteers present
def TotalCalloutTime(df):
    totalHours = 0

    for index, value in df["Callout Time"].items():
        if not pd.isnull(value):
            attended = df.loc[index, "Attended By"]
            if not pd.isnull(attended):
                peoplePresent = attended.count(",") + 1
            else:
                peoplePresent = 1

            totalHours += value * peoplePresent
    return totalHours

# Counts number of displaced animals by adding number of animals
def NumbDisplaced(df):
    sum = 0

    for index, value in df["Issue"].items():
        if not pd.isnull(value):
            if "Displaced" in value:
                sum += int(df.loc[index, "No of Animals"])
    return sum

# Total number of animals
def TotalAnimals(df):
    numbAnimals = int(df["No of Animals"].sum())
    return numbAnimals

# Total number of darts used
def TotalDarted(df):
    numbDarts = int(df["Total No of Darts"].sum())
    jobCodes = []
    darters = ["Chris", "Oliver", "Elaine", "Oscar", "Caitlin", "Jason", "Mel A", "Brenden", "Courtney"]

    for index, value in df["Total No of Darts"].items():

        if pd.isnull(value):
            outcome = df.loc[index, "Outcome"]
            darts_column = df.loc[index, "Darter/s"]

            if pd.notnull(outcome) and pd.notnull(darts_column):

                if "Darted" in outcome and any(darter in darts_column for darter in darters):
                    jobCode = df.loc[index, "Job Code"]
                    jobCodes.append(jobCode)
                    numbDarts += 1
                    df.loc[index, "Total No of Darts"] = 1
    return numbDarts, jobCodes

# Total number of sedation drugs used
def TotalSedated(df):
    numbSedated = 0
    sedationDrugs = ["Pamlin", "Butorphanol", "Zol ACP 10. (5ml in a bottle)", "Zoletil alone (5 mls water in bottle).", "Xylazine Zoletil (3 mls in bottle Zoletil) - total 3.5 ml"]

    for index, value in df["Drugs/Meds Used"].items():
        medColumn = df.loc[index, "Drugs/Meds Used"]

        if pd.notnull(value):
            for sedatedMed in sedationDrugs:
                if sedatedMed in medColumn:
                    numbSedated += 1
    return numbSedated

# Number of other drugs
def TotalOtherDrugs(df):
    numbOther = 0
    otherDrug = ["Subcut fluids", "Atipamezole reversal", "Eye drops", "Antibiotics", "IV fluids", "Multivitamins", "Se", "Worming", "Lethabarb", ]

    for index, value in df["Drugs/Meds Used"].items():
        medColumn = df.loc[index, "Drugs/Meds Used"]

        if pd.notnull(value) and any(_otherDrug in medColumn for _otherDrug in otherDrug):
            numbOther += (1 * int(df.loc[index, "No of Animals"]))
    return numbOther

# Calculate the total drug cost
def TotalDrugCost(df):
    cost = (int(TotalDarted(df)[0]) * 75) + (TotalSedated(df) * 40) + (TotalOtherDrugs(df) * 25)
    return round(cost, 2)

# Fuel cost
def FuelCost(kms):
    return 0.91*kms

# Fuel cost with tolls
def TotalFuelCost(df, kms):
    return FuelCost(kms) + 110

# Total Volunteer Field hours
def TotalVolHours(df, prm, kms):
    return TotalCalloutTime(df) + prm + kms/60