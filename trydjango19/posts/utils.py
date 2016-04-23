import datetime
import re

from django.utils.html import strip_tags


def count_words(html_string):
    """Calculate number of words in the given string
    ommiting HTML tags"""
    no_tags_text = strip_tags(html_string)
    count = len(re.findall(r'\w+', no_tags_text))
    return count


def get_read_time(html_string):
    """Get reading time in minutes of the provided HTML marked up string,
    assuming that the average reading rate is about
    200 words per minute for the English languge
    """
    word_count = count_words(html_string)
    reading_time_in_minutes = word_count / 200.0
    reading_time_in_seconds = reading_time_in_minutes * 60
    reading_time = str(datetime.timedelta(seconds=reading_time_in_seconds))
    return reading_time
