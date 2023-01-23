# Udacity "Programming with Python for Data Science" project file
# code format: black

import pandas as pd
import numpy as np
import os.path
import logging
import time
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)

valid_cities = ["chicago", "new york city", "washington"]
valid_months = ["january", "february", "march", "april", "may", "june", "all"]
valid_days = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "all",
]


def check_if_file_exists(file_name: str):
    """
    Simple wrapper for whether a file exists or not
    Parameters
    ==========
    file_name: 'str'
        file whose presence we want to check
    Returns
    =======
    _: 'bool'
        True if file exists
    """

    return os.path.isfile(file_name)


def get_input_city():
    """
    Gets the city name from the user and returns the validated imput
    Parameters
    ==========

    Returns
    =======
    input_city: 'str'
        validated city name in lowercase characters
    """
    print(
        "Enter the city name you want to see the data for. Valid values include 'Chicago,'New York City' and 'Washington'"
    )
    input_city = input("Which city name shall it be: ").lower()
    while input_city not in valid_cities:
        print(
            "Invalid value. Valid values include 'Chicago,'New York City' and 'Washington'"
        )
        input_city = input("Which city name shall it be: ").lower()
    return input_city


def get_input_month():
    """
    Gets the month name OR 'all' from the user and returns the validated imput
    Parameters
    ==========

    Returns
    =======
    input_month: 'str'
        validated month name OR 'all' in lowercase characters
    """
    print(
        "Would you like to apply a filter for the month? Valid values are 'January' to 'June' or 'all' [Enter key]"
    )
    input_month = input("Which month shall it be: ").lower()
    if not input_month:
        input_month = "all"
        print("Disabling 'month' filter")
    while input_month not in valid_months:
        print("Invalid value. Valid values are 'January' to 'June' or 'all'")
        input_month = input("Which month shall it be: ").lower()
    return input_month


def get_input_day():
    """
    Gets the weekday name OR 'all' from the user and returns the validated imput
    Parameters
    ==========

    Returns
    =======
    input_day: 'str'
        validated weekday OR 'all' in lowercase characters
    """
    print(
        "Would you like to apply a filter for the weekday? Valid values are 'Monday' to 'Sunday' or 'all' [Enter key]"
    )
    input_day = input("Which day shall it be: ").lower()
    if not input_day:
        input_day = "all"
        print("Disabling 'day' filter")
    while input_day not in valid_days:
        print("Invalid value. Valid values are 'Monday' to 'Sunday' or 'all'")
        input_day = input("Which day shall it be: ").lower()
    return input_day


def get_input_rerun():
    """
    Checks if the user wants to go for another program run
    Parameters
    ==========

    Returns
    =======
    input_retun: 'bool'
        True if user wants to rerun the program
    """
    input_rerun = input(
        "Would you like to do another calculation yes/no [Enter=yes]: "
    ).lower()
    if not input_rerun:
        input_rerun = "yes"
    while input_rerun not in ["yes", "no", "y", "n"]:
        print("Invalid input; please try again")
        input_rerun = input(
            "Would you like to do another calculation yes/no [Enter=yes]: "
        ).lower()
    print("\n")
    input_rerun = True if input_rerun.startswith("y") else False
    return input_rerun


def get_input_header_preview():
    """
    Checks if the user wants to see the dataframe header
    Parameters
    ==========

    Returns
    =======
    input_header_review: 'bool'
        True if user wants to see the dataframe header
    """

    input_header_preview = input(
        "Display up to 5 next header lines yes/no [Enter=yes]: "
    ).lower()
    if not input_header_preview:
        input_header_preview = "yes"
    while input_header_preview not in ["yes", "no", "y", "n"]:
        print("Invalid input; please try again")
        input_header_preview = input(
            "Display up to 5 next header lines  yes/no [Enter=yes]: "
        ).lower()
    print("\n")
    input_header_preview = True if input_header_preview.startswith("y") else False
    return input_header_preview


def load_my_file(city: str):
    """
    Loads the CSV file from disk and returns a pandas DataFrame object
    Parameters
    ==========
    city: 'str'
        prevalidated city name

    Returns
    =======
    df: 'bool'
        True if user wants to retun the program
    """

    df = None

    # create the target filename
    target_filename = f"{input_city.replace(' ', '_')}.csv"

    # Check if the input file exists
    if not check_if_file_exists(target_filename):
        # file is missing; output error message, check if the user wants to continue and re-initiate loop
        print(
            f"File '{target_filename}' not found; please check your local project installation"
        )
        return None
    else:
        logger.debug(msg="Importing file")
        df = pd.read_csv(target_filename)
        logger.debug(msg="File import successful")
        print(f"Initial file contains {len(df)} records")

    return df


def create_custom_dataframe(dataframe: pd.DataFrame, month: str, weekday: str):
    """
    Adjusts the Pandas dataframe based on the month/weekday parameters
    Parameters
    ==========

    Returns
    =======
    input_retun: 'bool'
        True if user wants to retun the program
    """
    # Check if we use a valid file
    if "Start Time" not in dataframe or "End Time" not in dataframe:
        raise ValueError("Invalid project file structure")

    # Cast both Start Time and End Time columns to a datetime object
    dataframe["Start Time"] = pd.to_datetime(df["Start Time"])
    dataframe["End Time"] = pd.to_datetime(df["End Time"])

    # retrieve and create new columns
    # needed for future calculations
    df["month"] = df["Start Time"].dt.month
    df["weekday"] = df["Start Time"].dt.weekday
    df["hour"] = df["Start Time"].dt.hour

    # Calculate numeric values for month and weekday
    # Weekday: 0 (monday) to 6 (sunday)
    # Month: 1..12 (jan..dec) --> add 1 to index
    target_month_numeric = valid_months.index(month) + 1
    target_weekday_numeric = valid_days.index(weekday)

    # Print current number of records
    logger.debug(msg=f"Filter_START: dataframe contains {len(dataframe)} records")

    # Apply the month filter, if requested
    if month != "all":
        logger.debug(msg="Applying MONTH filter")
        dataframe = dataframe[dataframe["Start Time"].dt.month == target_month_numeric]
        logger.debug(
            msg=f"Dataframe length after 'month' filter application: {len(dataframe)}"
        )

    # Apply the weekday filter, if requested
    if weekday != "all":
        logger.debug(msg="Applying WEEKDAY filter")
        dataframe = dataframe[
            dataframe["Start Time"].dt.weekday == target_weekday_numeric
        ]
        logger.debug(
            msg=f"Dataframe length after 'weekday' filter application: {len(dataframe)}"
        )

    # prepopulate potential NaN values with string "not available"
    dataframe.fillna("not available")

    logger.debug(msg=f"Filter_STOP: dataframe contains {len(dataframe)} records")
    logger.debug(msg=f"final dataframe columns: {df.columns}")
    print(f"Post-filter dataframe now contains {len(dataframe)} records")

    return dataframe


def display_dataframe_header(dataframe: pd.DataFrame):
    """
    Displays the dataframe header (5 rows per attempt)
    until the user wants to quit or there are no more
    records left

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our filtered dataframe

    Returns
    =======
    """

    # Display the header if the user wants to see it
    input_header_preview = True
    start_index = 0

    while get_input_header_preview():
        offset = 5  # default offset
        # check if we might exceed the dataframe's max boundaries
        # we might already be outside of its boundaries
        if start_index + 5 >= len(filtered_df):
            offset = len(filtered_df) - start_index
            if offset < 0:
                print("no more records")
                break

        # print up to 5 lines
        print(f"Printing {offset} lines starting from position {start_index}")
        print(filtered_df[start_index : start_index + offset])
        start_index += offset
        if start_index >= len(filtered_df):
            print("no more records to preview")
            break
        else:
            print(f"{len(filtered_df)-start_index} more rows available")


def print_time_elapsed(function_name: str, start_time: float, end_time: float):
    """
    Helper function which prints out the Python function name and the time passed for the calculation

    Parameters
    ==========
    function_name: 'str'
        Python function name
    start_time: 'float'
        start time
    end_time: 'float'
        end time

    Returns
    =======
    """
    time_elapsed = round(end_time - start_time, 5)

    print(f"Calculation for '{function_name}' took {time_elapsed:.5f} seconds")
    print("**")


def create_legible_durations(duration: int):
    """
    Generates a legible duration from a seconds-only input value

    Parameters
    ==========
    duration:  'int'
        Duration in seconds

    Returns
    =======
    days:   'int'
        number of days
    hours:  'int'
        number of hours
    minutes: 'int'
        number of minutes
    seconds: 'int'
        number of seconds

    """
    days = int(duration / 86400)
    remainder = duration - (days * 86400)
    hours = int(remainder / 3600)
    remainder = remainder - (hours * 3600)
    minutes = int(remainder / 60)
    seconds = remainder - (minutes * 60)
    return days, hours, minutes, seconds


def do_the_calculations(dataframe: pd.DataFrame):
    """
    Calls all calculations one by one

    Parameters
    ==========
    dataframe:  'pandas.dataframe'

    Returns
    =======
    """

    logger.debug(msg="Start of the calculation section")

    # section 1
    calculate_most_common_month(dataframe=dataframe)
    calculate_most_common_weekday(dataframe=dataframe)
    calculate_most_common_hour_of_day(dataframe=dataframe)

    # section 2
    calculate_most_common_start_station(dataframe=dataframe)
    calculate_most_common_end_station(dataframe=dataframe)
    calculate_most_common_trip(dataframe=dataframe)

    # section 3
    calculate_total_travel_time(dataframe=dataframe)
    calculate_average_travel_time(dataframe=dataframe)

    # section 4
    calculate_user_type_count(dataframe=dataframe)
    calculate_gender_count(dataframe=dataframe)
    calculate_year_of_birth(dataframe=dataframe)

    logger.debug(msg="End of the calculation section")


def calculate_most_common_month(dataframe: pd.DataFrame):
    """
    Calculates most common month

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    start_time = time.time()
    print(f"start of {sys._getframe().f_code.co_name}")

    # find the most popular hour
    result = df["month"].mode()[0]
    print(f"Most popular month: {result} = {valid_months[result-1]}")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_most_common_weekday(dataframe: pd.DataFrame):
    """
    Calculates most common weekday

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    start_time = time.time()
    print(f"start of {sys._getframe().f_code.co_name}")

    # find the most popular hour
    result = df["weekday"].mode()[0]
    print(f"Most popular weekday: {result} = {valid_days[result]}")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_most_common_hour_of_day(dataframe: pd.DataFrame):
    """
    Calculates most common hour of day

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    start_time = time.time()
    print(f"start of {sys._getframe().f_code.co_name}")

    # find the most popular hour
    result = df["hour"].mode()[0]
    print(f"Most popular start hour: {result}")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_most_common_start_station(dataframe: pd.DataFrame):
    """
    Calculates most common start station

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()

    result = dataframe["Start Station"].mode()[0]
    print(f"Most popular start station: {result}")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_most_common_end_station(dataframe: pd.DataFrame):
    """
    Calculates most common end station

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()

    result = dataframe["End Station"].mode()[0]
    print(f"Most popular end station: {result}")

    pass
    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_most_common_trip(dataframe: pd.DataFrame):
    """
    Calculates most common trip between start and end station

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()

    result = dataframe.groupby(["Start Station", "End Station"]).size().nlargest(1)

    # pretty-print the results. We've only requested one result.
    for index, _ in result.items():
        (start, stop) = index

    print(f"Most popular trip: '{start}' to '{stop}'")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_total_travel_time(dataframe: pd.DataFrame):
    """
    Calculates total travel time

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()
    result = int(dataframe["Trip Duration"].sum())
    days, hours, minutes, seconds = create_legible_durations(duration=result)

    print(
        f"total trip duration: {result} secs aka {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )
    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_average_travel_time(dataframe: pd.DataFrame):
    """
    Calculates mean average total travel time

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()
    result = int(dataframe["Trip Duration"].mean())
    days, hours, minutes, seconds = create_legible_durations(duration=result)

    print(
        f"Average trip duration: {result} secs aka {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )
    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_user_type_count(dataframe: pd.DataFrame):
    """
    Calculates number per user count type

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()

    # Calculate user types
    result = df["User Type"].value_counts()

    # pretty-print the results
    for index, value in result.items():
        print(f"User type '{index}':\t{value}")

    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_gender_count(dataframe: pd.DataFrame):
    """
    Calculates number per gender (whereas present in data set)

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()
    if "Gender" in dataframe:
        result = df["Gender"].value_counts()

        # pretty-print the results
        for index, value in result.items():
            print(f"Gender '{index}':\t{value}")
    else:
        print("This dataset does not provide information on attribute 'Birth Year'")
    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


def calculate_year_of_birth(dataframe: pd.DataFrame):
    """
    Calculates min/max/most common year of birth (whereas present in the data set)

    Parameters
    ==========
    dataframe:  'pandas.dataframe'
        our pre-filtered dataframe

    Returns
    =======
    """
    print(f"start of {sys._getframe().f_code.co_name}")
    start_time = time.time()
    if "Birth Year" in dataframe:
        result = int(df["Birth Year"].min())
        print(f"Minimum birth year:\t\t{result}")

        result = int(df["Birth Year"].max())
        print(f"Maximum birth year:\t\t{result}")

        result = int(df["Birth Year"].mode()[0])
        print(f"Most common birth year:\t{result}")

    else:
        print("This dataset does not provide information on attribute 'Birth Year'")
    print_time_elapsed(
        function_name=sys._getframe().f_code.co_name,
        start_time=start_time,
        end_time=time.time(),
    )


if __name__ == "__main__":

    input_rerun = True
    while input_rerun:
        input_city = get_input_city()
        input_month = get_input_month()
        input_day = get_input_day()
        logger.debug(msg=f"My parameters: {input_city}, {input_month}, {input_day}")

        # load the file with the full dataframe
        df = load_my_file(city=input_city)

        # Apply the month/weekday filter if we received something
        if isinstance(df, pd.DataFrame):
            filtered_df = create_custom_dataframe(
                dataframe=df, month=input_month, weekday=input_day
            )

            # Display the dataframe 5 lines at a time if the user wants to see it
            display_dataframe_header(dataframe=filtered_df)

            # finally, do the calculations as requested through the project requirements
            do_the_calculations(dataframe=filtered_df)
        else:
            raise ValueError("unable to load pandas dataframe")

        # run a quey on whether the user wants to run another query
        input_rerun = get_input_rerun()
    print("Have a nice day!")
