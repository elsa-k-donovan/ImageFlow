from datetime import datetime as dt
from dateutil.parser import parse



def is_date_and_check(from_, to_, fuzzy=False):
    """
    Return whether both strings can be interpreted as a date.

    Also checks if from date is before the to date

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    
    try: 
        from_tmp = dt.strptime(from_,"%Y-%m-%d")
        to_tmp = dt.strptime(to_,"%Y-%m-%d")
        parse(from_, fuzzy=fuzzy)
        parse(to_, fuzzy=fuzzy)
    except ValueError:
        return 2

    if from_tmp <= to_tmp:
        return True
    else:
        return 3


    # except ValueError:
    #     return False
check = is_date_and_check("2020-01-07", "2020-01-08")
if check == 2:
    print("Your date(s) are typed/formatted incorrectly")
elif check == 3:
    print("From date is greater then To date")
else:
    print("TRUE")