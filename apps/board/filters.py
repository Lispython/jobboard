# -*- coding: utf-8 -*-

from django.utils.http import  urlencode, urlquote
from pytils.templatetags import pytils_dt, pytils_numeral, pytils_translit


def urlquote_filter(url):
    return urlquote(url)

filters = {
    'distance_of_time': pytils_dt.distance_of_time,
    'ru_strftime': pytils_dt.ru_strftime,
    'ru_strftime_inflected': pytils_dt.ru_strftime_inflected,
    'ru_strftime_preposition': pytils_dt.ru_strftime_preposition,
    'choose_plural': pytils_numeral.choose_plural,
    'get_plural': pytils_numeral.get_plural,
    'rubles': pytils_numeral.rubles,
    'in_words': pytils_numeral.in_words,
    'translify': pytils_translit.translify,
    'detranslify': pytils_translit.detranslify,
    'slugify': pytils_translit.slugify,
    'urlencode': urlencode,
    'urlquote_filter': urlquote_filter}
