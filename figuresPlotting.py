import pandas as pd
import numpy as np
import os
import glob
import sys
import copy
import json
import math
from datetime import date
#import plotly.express as px
#import plotly.graph_objects as go
import matplotlib.pyplot as plt

dir = os.getcwd()

results_path = "/Users/apham/Documents/Projects/REopt_Projects/FY25/URBANopt_REopt/5_building_site"

buildings = 5
itc = 0
rates = ['ONS', 'TOD']
techs = ["BESS", "BESS+PV"]
df = pd.read_csv(os.path.join(results_path, 'all_scenarios_summary_neg.csv'))

# EMISSION:
df_emissions = df
df_emissions["scenario"] = pd.Categorical(df_emissions["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_emissions["Site"] = pd.Categorical(df_emissions["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
emission_pivot = df_emissions.pivot(index='Site', columns='scenario', values='lifecycle CO2 emissions')
emission_pivot = emission_pivot.reset_index()     

# Plotting:
fig, ax = plt.subplots()
ax = emission_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Lifecycle CO2e Emission')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Lifecycle CO2e Emission [tonnes]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path, "figures","emissions.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 

# LCC:
df_lcc = df
df_lcc['lcc_k'] = df_lcc['lcc']/1000
df_lcc["scenario"] = pd.Categorical(df_lcc["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_lcc["Site"] = pd.Categorical(df_lcc["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
lcc_pivot = df_lcc.pivot(index='Site', columns='scenario', values='lcc_k')
lcc_pivot = lcc_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = lcc_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Lifecycle Total Cost')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Lifecycle Total [thousand $]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path, "figures","lcc.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 

# Utility Bill
df_ub = df
df_ub["scenario"] = pd.Categorical(df_ub["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_ub["Site"] = pd.Categorical(df_ub["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
df_ub['lifecycle utility bill k'] = df_ub['lifecycle utility bill']/1000
ub_pivot = df_ub.pivot(index='Site', columns='scenario', values='lifecycle utility bill k')
ub_pivot = ub_pivot.reset_index()           
# Plotting:
fig, ax = plt.subplots()
ax = ub_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Lifecycle Utility Bills')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Lifecycle Utility Bills [thousand $]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","utility.png"),dpi=300, bbox_inches='tight', pad_inches=0.1) 

# GHX Sizing:
df_ghx_size = df
df_ghx_size = df_ghx_size[df_ghx_size['Site']=='GHX']
df_ghx_size["scenario"] = pd.Categorical(df_ghx_size["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_ghx_size['GHX size [thousand ft]'] = df_ghx_size['GHX size [ft]']/1000
ghx_pivot = df_ghx_size.pivot(index='Site', columns='scenario', values='GHX size [thousand ft]')
ghx_pivot = ghx_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = ghx_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='GHX size')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("GHX size [thousand ft]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","ghx_size.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 


# GHP sizing:
df_ghp_size = df
df_ghp_size["scenario"] = pd.Categorical(df_ghp_size["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_ghp_size["Site"] = pd.Categorical(df_ghp_size["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
ghp_pivot = df_ghp_size.pivot(index='Site', columns='scenario', values='GHP size [tons]')
ghp_pivot = ghp_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = ghp_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='GHP size')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("GHP size [tons]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","ghp_size.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 

# Boiler sizing:
df_boiler_size = df
df_boiler_size["scenario"] = pd.Categorical(df_boiler_size["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_boiler_size["Site"] = pd.Categorical(df_boiler_size["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
boiler_pivot = df_boiler_size.pivot(index='Site', columns='scenario', values='Boiler size [mmbtu]')
boiler_pivot = boiler_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = boiler_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Boiler size')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Boiler size [mmbtu-hr]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","boiler_size.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 


# Electric Heater sizing:
df_eh_size = df
df_eh_size["scenario"] = pd.Categorical(df_eh_size["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_eh_size["Site"] = pd.Categorical(df_eh_size["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
eh_pivot = df_eh_size.pivot(index='Site', columns='scenario', values='Electric heater size [mmbtu]')
eh_pivot = eh_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = eh_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Electric Heater size')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Electric Heater size [mmbtu-hr]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","electric_heater_size.png"),dpi=200, bbox_inches='tight', pad_inches=0.1) 

# Capital Cost:
df_lccc = df
df_lccc["scenario"] = pd.Categorical(df_lccc["scenario"], ["BAU", "Standalone GHP", "District GHP"])
df_lccc["Site"] = pd.Categorical(df_lccc["Site"], ['Restaurant', 'Hotel', 'Office', 'Apartment', 'Mall', 'GHX', 'District Total'])
df_lccc['lifecycle capital cost k'] = df_lccc['lifecycle capital cost']/1000
lccc_pivot = df_lccc.pivot(index='Site', columns='scenario', values='lifecycle capital cost k')
lccc_pivot = lccc_pivot.reset_index()           

# Plotting:
fig, ax = plt.subplots()
ax = lccc_pivot.plot(x="Site",kind='bar',stacked=False,
                    color = ['lightpink','skyblue','darkseagreen'], 
                    title='Lifecycle Capital Cost')
plt.xticks(rotation=0)
ax.set_xlabel('')
plt.legend(title='Scenario',loc = "upper left")
plt.ylabel("Lifecycle Capital Cost [thousand $]")
fig = plt.gcf() # get current figure
fig.set_size_inches(7,4)
plt.savefig(os.path.join(results_path,"figures","lccc.png"),dpi=200, bbox_inches='tight', pad_inches=0.1)   

# Utility Bill components
df_ub_bd_org = pd.read_csv(os.path.join(results_path, 'utility_bill_components.csv'))
scenarios = ["BAU", "Standalone GHP", "District GHP"]
for scenario in scenarios:
    df_ub_bd = df_ub_bd_org[df_ub_bd_org["scenario"]==scenario]
    if scenario != 'BAU':
        df_ub_bd = df_ub_bd.drop('lifecycle natural gas bill', axis=1)

    df_ub_bd_T = df_ub_bd.T
    df_ub_bd_T = df_ub_bd_T.iloc[2:]
    df_ub_bd_T = df_ub_bd_T.reset_index()
    if scenario == 'BAU':
        df_ub_bd_T = df_ub_bd_T.rename(columns = {'index':'Cost type', 0:'Value'})
    elif scenario == 'Standalone GHP':
        df_ub_bd_T = df_ub_bd_T.rename(columns = {'index':'Cost type', 1:'Value'})
    else:
        df_ub_bd_T = df_ub_bd_T.rename(columns = {'index':'Cost type', 2:'Value'})
    
    fig, ax = plt.subplots()
    ax = df_ub_bd_T.plot.pie(y='Value', labels=df_ub_bd_T['Cost type'], autopct='%1.1f%%', startangle=90, figsize=(4, 4), 
                        colors=['lightpink','skyblue','darkseagreen'])
    plt.axis('equal')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.get_legend().remove()
    plt.title('Lifecycle Total Cost Components - ' + scenario)
    plt.savefig(os.path.join(results_path,"figures","cost_component_"+scenario+".png"),dpi=200, bbox_inches='tight', pad_inches=0.1)   