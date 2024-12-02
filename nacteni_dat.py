import eurostat
import pandas as pd

# vyhladnie datasetov z Eurostat, ktore maju v klucovych slovach "smoking/smoker" - SMOK a ulozenie do slovniku
toc_df = eurostat.get_toc_df()
filtered_df = eurostat.subset_toc_df(toc_df, "smok")
codes_titles_dict = dict(zip(filtered_df["code"], filtered_df["title"])) # slovnik kódov a názvov datasetov

# ulozenie tabulky o datasetoch o fajceni do csv

filtered_df.columns = filtered_df.iloc[0] # definovanie nazvu stlpcov
filtered_df = filtered_df.drop(filtered_df.index[0]).reset_index(drop=True) # posunutie indexovania riadkov od obsahu bez raidku s nazvami stlcpv
filtered_df.to_csv("smoker_smoking_toc.csv", index=False, encoding="utf-8") # ulozenie do csv

'''
kody vybratych datasetov, co chcem pouzivat: HLTH_EHIS_SK1E, HLTH_EHIS_SK1I, SDG_03_30
kody dalsich datasetov pre hladanie spojitosti s tymi zatial vybranymi: HLTH_EHIS_AL1E, UNE_RT_A
'''

codes_to_explore = ["HLTH_EHIS_SK1E", "HLTH_EHIS_SK1I", "SDG_03_30"]
other_codes_to_explore = ["hlth_ehis_al1e", "une_rt_a"]   

# filtracia slovnika dat o fajceni len na vybrate kody
filtered_codes_titles_dict = {}
for code, title in codes_titles_dict.items():
    if code in codes_to_explore:
        filtered_codes_titles_dict[code] = title

# Výpis upraveného slovníka
# for code, title in filtered_codes_titles_dict.items():
#     print(f"Filtered Code: {code}, Title: {title}")

# slovnik pre datasety naviac kvoli moznym spojitostiam v datach (alkohol, nezamestnanost)
filtered_other_df = toc_df[toc_df["code"].str.lower().isin(other_codes_to_explore)]
other_codes_titles_dict = dict(zip(filtered_other_df["code"], filtered_other_df["title"]))

# Výpis slovníka
# for code, title in other_codes_titles_dict.items():
#     print(f"Code: {code}, Title: {title}")

# ulozenie vybranych datasetov o fajceni do csv

for code, title in filtered_codes_titles_dict.items():
    df = pd.DataFrame(eurostat.get_data(code))
    df.columns = df.iloc[0] # prvy riadok tabulky ako nazvy stlpcov
    df = df.drop(df.index[0]).reset_index(drop=True) # resetuje indexovanie od obsahu
    df.rename(columns={"geo\\TIME_PERIOD": "geo"}, inplace=True) # napravi a nahradi eurostat podivnost v ich tabulkach
    df.to_csv(f"{title}.csv", index=False, encoding="utf-8") 

# ulozenie vybranych datasetov o nezamestnanosti a alkohole do csv
for code, title in other_codes_titles_dict.items():
    df = pd.DataFrame(eurostat.get_data(code))
    df.columns = df.iloc[0] 
    df = df.drop(df.index[0]).reset_index(drop=True) 
    df.rename(columns={"geo\\TIME_PERIOD": "geo"}, inplace=True) 
    df.to_csv(f"{title}.csv", index=False, encoding="utf-8")
