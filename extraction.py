#coding: utf-8
import re


def get_facebook(ocr_text):
	facebook_url = re.findall("(?i)\b((?:https?://|www\d{0,3}[.]|['facebook'|fb]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", ocr_text)
	return facebook_url

def get_website_url(ocr_text):
	website_url = re.findall("?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", ocr_text)

def get_contacts(ocr_text):
	numbers = re.findall('.*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', ocr_text)
	#contact = numbers[0] + numbers[1] + numbers[2] + numbers[3]
	return numbers

def get_hashtags(ocr_text):
	hashtags = re.findall('#(\w+)', ocr_text)
	return hashtags
