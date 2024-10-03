import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    while True:
        city = input('Select a city to see it data (chicago, new york city, washington) ?').lower()
        if city in CITY_DATA.keys():
            print('done!')
            break
        else:
            print('please enter one of this cities (chicago, new york city, washington)')
            
            
    # get user input for month (all, january, february, ... , june)
    mon = ['all','january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Select a month (all,january,february ,march,april,may,june) ?').lower()
        if month in mon:
            print('done!')
            break
        else:
            print("please enter valid day such as 'january ,february ,march , april,may , june:'")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    week_days =['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while True:
        day = input('Select a day (all, monday, tuesday,Wednesday,Thursday ,Friday ,saturday ,sunday)').lower()
        if day in week_days:
            print('done!')
            break
        else:
            print("please enter valid day such as 'monday, tuesday,Wednesday...:")

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    """" the chunks function i took it from earrlier lessons to, return 5 unique columns at a time"""
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    for chunk in chunks(df, 5):
        user_input = input('Would you like to see raw data (yes|no)..[space]?')
        if user_input.lower() =="yes":
            print(chunk)
            continue
        elif user_input.lower() == "no":
            print("Exiting...")
            break

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
        df = df[df['day'] == day.title()]
        
    return df.head()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    print('The most common month for traveling is..: ', df['month'].mode())

    # display the most common day of week
    print('The most common month for traveling is..: ', df['day'].mode())

    # display the most common start hour
    print('The most common start hour is.. ', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('The most commonly used start station is.. ', df['Start Station'].mode())

    # display most commonly used end station
    print('The most common end station is.. ', df['End Station'].mode())

    # display most frequent combination of start station and end station trip
    most_frequent_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip.. ', most_frequent_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    """sec_to_hours function take the seconds saved in Trip duration column and process it to return it as days, hours,minutes and seconds. but first i define int_trip variable to store the new type assigened to df['Trip Duration']"""
    int_trip = df['Trip Duration'].astype(int)

    def sec_to_hours(seconds):
        days = str(seconds // 86400)
        hours = str((seconds // 3600) % 24)
        minutes = str((seconds % 3600) // 60)
        seconds = str((seconds % 3600) % 60)
        d = [f'{days} days {hours} hrs {minutes} min {seconds} second']
        return d
    # TO DO: display total travel time
    print('The total travel time is...: ', sec_to_hours(int_trip.sum()))

    # display mean travel time
    print('The Average of travel time is...: ', sec_to_hours(int(int_trip.mean())))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('Users types\n', df['User Type'].value_counts())

    # Display counts of gender
    print('Counts of genders\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('The earliest year of birth is.. ', df['Birth Year'].min())
    print('most recent year of birth is ... ', df['Birth Year'].max())
    print('The most common year of birth is.. ', df['Birth Year'].mode())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington':
            user_stats(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
