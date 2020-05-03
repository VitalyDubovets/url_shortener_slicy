import random
import string


def make_short_url(k=8):
    all_symbols = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(all_symbols, k=k))
    return short_url
