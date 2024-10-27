from queue import Empty
from my_library import *
from driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style
from bs4 import BeautifulSoup

def poiskpers(url):
	geourl = '{0}'.format(quote(url))
	return geourl

class Good:
	def __init__(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.colors = []
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = ''
		self.brand = ''
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
		print(f'------------------------------------{pc_good_link}-----------------------------------------')


	def get_good(self, ol:WD, pc_good_link, pc_price:str):
		ol.Get_HTML(pc_good_link)
		if ol.data == None:
			return

		from rich import print


		self.article = ol.data['variants'][0]['sku']
		if self.article:
			if len(self.article)>0:
				self.article = BeautifulSoup(
					self.article,
					"html.parser"
				).get_text()
		
		try:
			self.price = ol.data['variants'][0]['price']
		except:
			try:
				self.price = ol.data['variants'][0]['base_price']
			except:
				self.price = ol.data['variants'][0]['old_price']

		self.description = ol.data['short_description']
		if self.description:
			if len(self.description)>0:
				self.description = BeautifulSoup(
					ol.data['short_description'],
					"html.parser"
				).get_text()

		self.name = ol.data['title']
		append_if_not_exists(ol.data['first_image']['original_url'], self.pictures)
		for section in ol.data['images']:
			append_if_not_exists(section['original_url'], self.pictures)
