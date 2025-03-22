# Data Analysis of the Bike Share data in different cities
import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please enter a valid city.")

    while True:
        filter = input("Would you like to filter the data by month, day, both, or not at all? Enter 'none' for no filter. ").lower()
        if filter in ['month', 'day', 'both', 'none']:
            break
        else:
            print("Invalid filter. Please enter a valid filter.")

    # get user input for month (all, january, february, ... , june)
    month = 'all'
    if filter == 'month' or filter == 'both':
        while True:
            month = input("Which month - January, February, March, April, May, or June? ").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("Invalid month. Please enter a valid month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'all'
    if filter == 'day' or filter == 'both':
        while True:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("Invalid day. Please enter a valid day.")

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[df['month'].mode()[0] - 1]
    print('Most Common Month:', month)

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', day)

    # display the most common start hour
    hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end_station = df['Start_End_Station'].mode()[0]
    print('Most Common Start and End Station Combination:', common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:')
    print(user_types)

    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:')
        print(gender_counts)

        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year'].min()
        print('Earliest Birth Year:', birth_year)

        most_recent_birth_year = df['Birth Year'].max()
        print('Most Recent Birth Year:', most_recent_birth_year)

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """Displays raw data on bikeshare users."""

    # ask if user wants to display raw data
    display_raw_data = input('\nWould you like to display raw data? Enter yes or no. ').lower()
    if display_raw_data.lower() != 'yes':
        return
    
    start_row = 0
    num_rows = 5

    df = pd.read_csv(CITY_DATA[city])

    print('\nDisplaying Raw Data...\n')

    while True:
        end_row = min(start_row + num_rows, len(df))

        # display 5 rows of raw data
        for index, row in df.iloc[start_row:end_row].iterrows():
            print("Row", index)
            print('-'*40)
            print(row)
            print()


        # ask if user wants to display more rows
        if end_row >= len(df):
            print('No more rows to display.')
            break

        display_more_rows = input('\nWould you like to display more rows? Enter no to stop. ').lower()
        if display_more_rows.lower() == 'no':
            break

        start_row = end_row


    print('-'*40)

def main():
    while True:
        # Ask for data filters
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Print user stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask to print out the data
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
