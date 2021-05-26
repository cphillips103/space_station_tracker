# -*- coding: utf-8 -*-
"""
Created on Wed May 26 12:43:06 2021

International Space Station position tracker (ISS)

Uses open-notify API for ISS latitudinal and Longitudinal position data
in JSON file format.

Final result ploted using Plotly Geo based scatter plot.

@author: Christopher Phillips
credits: open-notify.org for ISS position API


"""
# load necessary libraries
import datetime as dt
import pandas as pd
import time
import plotly.express as px


# ISS position polling function
def Iss_polling():
    # open notify API url address for ISS position information
    # data is message status, time stamp, latitude and longitude
    # retreival message lets us know if data retreival is a success.
    
    # URL for open-notify data
    url = 'http://api.open-notify.org/iss-now.json'

    #read json file into dataframe
    polling = pd.read_json(url)
    
    #rename column names for ease of use
    polling['latitude'] = polling.loc['latitude','iss_position']
    polling['longitude'] = polling.loc['longitude','iss_position']
    #re-index data to better format for adding to our dataframe for plotting.
    polling.reset_index(inplace=True)
    
    #drop unneeded columns
    polling = polling.drop(['index','iss_position'], axis = 1)

    return polling #return cleaned up dataframe
    
# Dataframe for storring retreived position data   
df = pd.DataFrame(columns = ['message', 'timestamp', 'latitude','longitude'])



# time retreival to build plot
for i in range(15): # currenlty pulling 90 data points.
    time.sleep(60) #pausing 60 seconds between retreivals
    poll = Iss_polling() #polling ISS position

    df = df.append(poll.iloc[-1:]) # add new position to plotting dataframe

print (df) #print dataframe to see if all messages are successful.

#timestamp to show on plot time when data was made.

stamp = pd.to_datetime("today").strftime("%d/%m/%Y %I:%M:%S")


# create title with timestamp for chart
our_title = ("International Space Station Position. Time: {}" \
   .format(stamp))


#simple plotting of the ISS position.
fig = px.scatter_geo(df, lat = 'latitude', lon='longitude',
                    labels={
                     "ISS Latitude",
                     "ISS Longitude"},
                title = our_title)
# plot figure
fig.show()
