import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_nickname = { 'chicago': 'the Windy City',
              'new york city': 'the Big Apple',
              'washington': 'the Evergreen State' }

def get_filters():
    """ Asks user to select data from 3 cities and add options to filter data by month and/or day.

  INPUTS:
  city: str. Choice of one of three cities.
  month_input: int. Number ranges from 0 to 6.
  day: str. Abbreviation of the weekdays.

  OUTPUTS:
  city: City to gather data from.
  month_input: Number of the month to filter data by with the option of no filteration, index to retrive month from months_list
  day: Abbreviation of the day to filter by, key of weekdays_dict to return weekday and a small tribute to Avicii.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Currently our data include the cities of Chicago, New York City and Washington, Please choose one:\n')
    # While loop to ensure input is from predetermined choices and handles case sensitive and int/float entries
    while city.lower() not in city_nickname:
        print('\nInvalid input')
        city = input('Please enter one of the 3 cities mentioned and check spelling: ')

    print('\nYou\'ve choosen {}, {}!\n'.format(city.title(), city_nickname[city.lower()]))

    # while loop to deal with various errors
    while True:
        # try and except block to make sure the script doesn't crash by either invalid values or keyboard interrupt errors
        try:
            print('Our data are limited to the first half of the year: 1[Jan] to 6[Jun]')
            month_input = int(input('\nEnter a month number to filter data by or "0" for no filtration: '))
            months_list = ['All', 'January', 'February', 'March', 'April','May', 'June']
            # while loop to limit the range of entries and return index of months_list
            while month_input not in list(range(0,7)):
                month_input = int(input('Please make sure you enter a number in range of 0 to 6: '))

            # if statement to give the user a more interactive experince
            if month_input == 0:
                print('You\'ve decided not to filter data by a month.')
                break
            elif month_input == 1:
                print('You\'ve choosen the {}st month of the year, {}'.format(month_input,months_list[month_input]))
                break
            elif month_input == 2:
                print('You\'ve choosen the {}nd month of the year, {}.'.format(month_input,months_list[month_input]))
                break
            elif month_input == 3:
                print('You\'ve choosen the {}rd month of the year, {}.'.format(month_input,months_list[month_input]))
                break
            else:
                print('You\'ve choosen the {}th month of the year, {}.'.format(month_input,months_list[month_input]))
                break
        except ValueError:
            print('Please make sure you enter a number [eg: 0 = All, 5 = May]')
        except KeyboardInterrupt:
            print('Interrupted.')
            break
    month = months_list[month_input]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays_dict ={'ALL': ('All','♪♪ All I want for Christmas is you ♪♪'), 'MON': ('Monday','♪♪ Monday left me broken ♪♪'), 'TUE': ('Tuesday','♪♪ Tuesday, I was through with hoping ♪♪'),
    'WED': ('Wednesday','♪♪ Wednesday, my empty arms were open ♪♪') ,'THU': ('Thursday','♪♪ Thursday, waiting for love, waiting for love ♪♪'),
    'FRI': ('Friday','♪♪ Thank God it\'s Friday ♪♪'), 'SAT': ('Saturday','♪♪ I\'m burning like a fire gone wild on Saturday ♪♪'),
    'SUN': ('Sunday','♪♪ Guess I won\'t be coming to church on Sunday ♪♪')}
    day = input('\nFinally, enter the first 3 letters of a weekday to filter data by or "all" for no filtration: ')
    # while loop to take input and use it as a key for weekdays_dict to return weekday with a touch of humor
    while day.upper() not in weekdays_dict:
        print('\nInvalid input')
        day = input('Please enter the first 3 letters of a day or "All" [eg: Sun = Sunday, All = ALL ]: ')
    if day.upper() == 'ALL':
        print('\n{}, ahm sorry I got carried away.\nYou\'ve decided not to filter data by days.'.format(weekdays_dict[day.upper()][1]))
    else:
        print('\n{}, ahm sorry I got carried away.\nYour choice is: {}.'.format(weekdays_dict[day.upper()][1], weekdays_dict[day.upper()][0]))

    day = weekdays_dict[day.upper()][0]
    print('\nYou\'ve entered {} - {} - {}'.format(city.title(), month.title(), day.title()))

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    ARGUMENTS:
    city: City to gather data from.
    month: Month to filer by if applicable.
    day: Weekday to filer by if applicable.

    OUTPUTS:
        df - Pandas DataFrame containing city data filtered by month and day.
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hout from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    #if statement to filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # create the new dataframe filtered by month
        df = df[df['month'] == month]

    # if statement to filter by day of week if applicable
    if day.lower() != 'all':
        # create the new dataframe filtered by day of week
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # utilize the mode function to display the most common month
    print('\nMost common month: {}'.format(df['month'].mode()[0]))

    # utilize the mode function to display the most common day of week
    print('\nMost common weekday: {}'.format(df['day_of_week'].mode()[0]))

    # utilize the mode function to display the most common start hour
    print('\nMost common start hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # utilize the mode function to display most commonly used start station
    print('\nMost common start station: {}'.format(df['Start Station'].mode()[0]))

    # utilize the mode function to display most commonly used end station
    print('\nMost common end station: {}'.format(df['End Station'].mode()[0]))


    # utilize the groupby and size functions to combine start and end stations columns
    # utilize idxmax function to return most frequent values
    start, end = df.groupby(['Start Station','End Station']).size().idxmax()
    print('\nMost frequent combination of start station and end station trip: {} ---> {}'.format(start, end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # pd.to_timedelta function with the optionl unit arg to convert 'Trip Duration' into (D H:M:S) form
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')
    # utilize sum function display total travel time
    print('\nTotal travel time: {}'.format(df['Trip Duration'].sum()))

    # utilize mean function display mean travel time
    print('\nMean travel time: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # utilize value_counts function to count unique values of user types
    # utilize to_string function to get rid off dtype: object line because it was bothering me
    print('\nCounts of user type: \n{}'.format(df['User Type'].value_counts().to_string()))

    # if statement to exclude Washington for not having gender & birth year columns
    if city.lower() in ['chicago', 'new york city']:
        print('\nCounts of gender: \n{}'.format(df['Gender'].value_counts().to_string()))

    # display earliest, most recent, and most common year of birth
        print('\nMost common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
        print('\nEarliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('\nMost recent year of birth: {}'.format(int(df['Birth Year'].max())))
    else:
        print('\nData for user gender or date of birth aren\'t available in Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    ''' One function to run them all '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # I added 'city' as argument to exclude Washington
        user_stats(df, city)
        # prompt the user if they want to see 5 lines of raw data wirh IASIP reference
        raw  = input('\nCan I offer you raw data in this tryin\' time ? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print('\nI don\'t want you overwhelmed, so I will show 5 lines at a time.\n')
            print(df.head())
            # while loop to show 5 lines of data, delete them and then show the 5 lines after
            while True:
                more = input('\nWould you like to see more ? Enter yes or no.\n')
                if more.lower() != 'yes':
                    break
                else:
                    n = 5
                    df.drop(df.index[0:n], inplace = True)
                    print(df.head())
                    n +=5
        # asks the user if he wants to restart and change entries
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
""" if main block to ensure modules aren't being run as executable statements in another script """
