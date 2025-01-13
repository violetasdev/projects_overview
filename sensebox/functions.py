import requests
import time
import pandas as pd

import seaborn as sns
sns.set(rc={'figure.figsize':(20,10)})
sns.set_palette("Greys_r")

import matplotlib.pyplot as plt


my_key = ""

# Key obtained from https://developer.nytimes.com/

def obtain_monthly_counts(search_term, start_year, end_year):
    """
    Obtain monthly values for the search term in the NYT archive

    Params:
    string search term: term to look out in the archive
    int start_year: starting year for the time frame
    int end_year: ending year for the time frame
    
    """
  
    params = {"q": search_term,
              "api-key": my_key}

    monthsday=["0131","0228","0331","0430","0531","0630","0731","0831","0930","1031","1130","1231"]
    
    all_counts = []
    counts=pd.DataFrame()
    df_data=pd.DataFrame()
    
    for year in range(start_year, end_year+1):
        
            for month in monthsday:
               
                params["begin_date"] = f"{year}{month[0:2]}01"
                # If we keep the "end" parameter, it is accumulating hits through time, this needs to be corrected.
                # experimental results shows 20200131 is 27 hits, 0228 is 27 hits. 1202 hits for the original script - 27 =1175 which is the next cummulative result
                params["end_date"] = f"{year}{month}"

                r = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json", params=params)
                data = r.json()
                count = data["response"]["meta"]["hits"]

                df_data=pd.concat([df_data, pd.DataFrame(data["response"]["docs"])])

                # Wait 7 seconds between requests to hace some buffer as only 10 requests
                # per minute are allowed
                time.sleep(7)

                all_counts.append(count)
                
    counts['counts'] = pd.DataFrame(all_counts)
    counts['dates'] = pd.date_range(pd.to_datetime(f"{start_year}0101"), periods=(end_year-start_year+1)*12, freq='M')
            
    return counts, df_data


def plot_mentions(plot_data, x_data, y_data, year):
    """
    Creates a Line Plot for the retrieved number of mentions

    Params:
    dataframe plot_data:  dataframe with the data to be plotted
    dataframe column x_data : reference to axis x
    dataframe column y_data: reference to axis y
    string year: period of time for which the title will be doing reference 
    """
    
    sns.set_theme(style="darkgrid")
    sns.lineplot(x=x_data, y=y_data,data=plot_data,palette='Greys', linewidth=3).set(title='Term mentions ('+year+') - New York Times API data')
    plt.xticks(rotation=90)
    plt.xlabel("Dates")
    plt.ylabel("Counts")

    return plt

def plot_mentions_vs(plot_data, x_data, y_data, hue_data):
    """
    Creates a Line Plot for the retrieved number of mentions for a continuos period assigning to each a different color

    Params:
    dataframe plot_data:  dataframe with the data to be plotted
    dataframe column x_data : reference to axis x
    dataframe column y_data: reference to axis y
    string year: period of time for which the title will be doing reference 
    """

    sns.set_theme(style="darkgrid")
    sns.lineplot(x=x_data, y=y_data,data=plot_data, hue=hue_data, style=hue_data, markers=True, palette='Greys', linewidth=3).set(title='Term mentions (2018-2019 vs 2020-2021) - New York Times API data')
    plt.xticks(rotation=90)
    plt.xlabel("Dates")
    plt.ylabel("Counts")

    return plt

