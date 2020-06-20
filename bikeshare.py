# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:10:50 2020
Created and tested in Anaconda's Jupyter 5.7.6 running Python 3.6.5 and in Anaconda's Spyder (Python 3.6)

@author: Jabik Broersma
@verion date: 22-04-2020
@version: 1.1
@version history: def print_df added which enables the user to see the raw dataframe

@version date 22-04-2020
@version 1.2: module Datetime added to enable the function 'strftime' on more versions of Python
"""

import time
import datetime as dt
import calendar as cal
import pandas as pd
import math
import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=""
    while city not in ('chicago', 'new york city', 'washington'):
        city = input('Would you like to explore the data of Chicago, New York City or Washington? \n')
        city=city.lower()

    # get user input for month (all, january, february, ... , june)
    month=""
    while month.lower() not in ('january', 'february', 'march','april', 'may', 'june', 'all'):
        month = input('Please choose which month (from January up to June) you would like to '
                      'explore (enter "all" for all available months: \n')
        month=month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=""
    while day not in ('sunday', 'monday','tuesday','wednesday', 'thursday', 'friday','saturday', 'all'):
        day = input('Please choose which day (monday till sunday) you would like to '
                    'explore (enter "all" for all days of the week: \n')
        day=day.lower()

    print('='*60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    """
    Reference to local file path
    When not referenced in PATH, or when different file path applicable, change here
    file_path="c:/users/HP/downloads/bikeshare/"
    """
    file_path=""

    df=pd.read_csv(str(file_path)+'{}'.format(CITY_DATA[city]))

    if month != "all":
        df = df[pd.to_datetime(df['Start Time']).dt.strftime('%B')==month.capitalize()]

    if day != "all":
        df = df[pd.to_datetime(df['Start Time']).dt.strftime('%A')==day.capitalize()]

    print('\nYour city of choice is {}'.format(city.upper()))
    print('You have chosen to explore {} as month of the year'.format(month.upper()))
    print('Your day of the week is {}'.format(day.upper()))

    return df

def print_df(df):
    """
    @v1.1
    Enables the user to see the raw data from the dataframe 5 rows consecutively

    """

    key="yes"
    row=0
    key=input('\nDo you want to see the raw data (yes/no)?')
    while key.lower() == "yes":
        print(df[row:row+5])
        key=input('\nDo you want more raw data (yes/no)?')
        row=row+5
        if key.lower() != 'yes':
            break

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    month_mode=df['month'].mode()
    print('\n*  The most common travel month is: {}'.format(cal.month_name[math.floor(month_mode)].upper()))

    # display the most common day of week
    df['weekday'] = pd.DatetimeIndex(df['Start Time']).weekday
    weekday_mode=df['weekday'].mode()
    print('*  The most common travel day of the week is: {}'.format(cal.day_name[math.floor(weekday_mode)].upper()))

    # display the most common start hour
    df['starthour']=pd.DatetimeIndex(df['Start Time']).hour
    hour_mode=df['starthour'].mode()
    print('*  The most common travel hour of the day is: {} \'o clock'.format(int(hour_mode)))

   '''
   Refactoring the overall distribution:
   speeding up the refresh rate
   '''

    # plots the overall distribution of travel hours during the chosen period
    df['starthour'].plot(kind='hist',bins=24,histtype='stepfilled',facecolor='b')
    plt.xlabel('Hour of the day')
    plt.ylabel('nr. of bicycle rentals')
    plt.title('Overall bicycle rentals per hour of the day during the chosen period')
    plt.xlim(0, 25)
    plt.grid(True)
    plt.show()

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    StartStation_mode=df['Start Station'].mode()
    print ('\n*  The most common used start station is: {}'.format(StartStation_mode[0].upper()))

    # display most commonly used end station
    EndStation_mode=df['End Station'].mode()
    print ('*  The most common used end station is: {}'.format(EndStation_mode[0].upper()))


    # display most frequent combination of start station and end station trip
    route=df.groupby(['Start Station','End Station']).size().nlargest(1).reset_index()
    print('*  The most frequent combination of start station and end station trip is: {} from/to {}.'
          .format(route['Start Station'][0].upper(), route['End Station'][0].upper()))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    df['StartTime']=pd.to_datetime(df['Start Time'])
    df['EndTime']=pd.to_datetime(df['End Time'])
    df['DiffTime']=df['EndTime']-df['StartTime']

    # display total travel time
    TotalTravelTime=df['DiffTime'].sum()

    print ("The total travel time is {} days, {} hours, {} minutes and {} seconds.".format(TotalTravelTime.days,
           int(TotalTravelTime.seconds / 3600),int((TotalTravelTime.seconds % 3600)/60 ),
           TotalTravelTime.seconds % 60))

    # display mean travel time
    MeanTravelTime=df['DiffTime'].mean()
    print ("The mean travel time is {} days, {} hours, {} minutes and {} seconds.".format(MeanTravelTime.days,
           int(MeanTravelTime.seconds / 3600),int((MeanTravelTime.seconds % 3600)/60 ),
           MeanTravelTime.seconds % 60))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #calculate total number of rides
    df_ride=df.shape
    print('\n*  The total number of rides is: {}\n'.format(df_ride[0]))

    # Display counts of user types
    if 'User Type' in df.columns:
        total_users=0
        df_unknown_user = df['User Type'].isnull().sum()
        df_user = df['User Type'].value_counts()

        for x in range(df_user.shape[0]):
            print('*  The number of {} is: {}'.format(df_user.index[x-1], df_user[x-1]))
            total_users+=df_user[x-1]

        print('*  The number of unknown users is: {}'.format(df_unknown_user))
        print('**  Crosscheck: Total users + Unknown users = {}'.format(total_users+df_unknown_user))
    else:
        print ('*  No User Type data available!!')


    # Display counts of gender
    if 'Gender' in df.columns:
        total_gender=0
        df_unknown_gender=df['Gender'].isnull().sum()
        df_gender = df['Gender'].value_counts()

        for x in range(df_gender.shape[0]):
            print('*  The number of {} persons is: {}'.format(df_gender.index[x-1], df_gender[x-1]))
            total_gender+=df_gender[x-1]

        print('*  The number of unknown gender is: {}'.format(df_unknown_gender))
        print('**  Crosscheck: Total persons + Unknown = {}'.format(total_gender+df_unknown_gender))
    else:
        print ('\n*** No Gender data available!!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print ('\n*  The earliest year of birth is: {}'.format(int(df['Birth Year'].min())))
        print ('*  The most recent year of birth is: {}'.format(int(df['Birth Year'].max())))
        print ('*  The most common year of birth is: {}'.format(int(df['Birth Year'].mode())))
    else:
        print('\n*** No Birth Year data available!!')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print_df(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
