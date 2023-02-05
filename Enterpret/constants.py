from datetime import datetime


class Constants:
    start_date = datetime.strptime("2021-02-20", "%Y-%m-%d").date()
    discourse_source = 'S04'
    playstore_source = 'S03'
    intercom_source = 'S02'
    twitter_source = 'S01'

