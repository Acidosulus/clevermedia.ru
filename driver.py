import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup as BS
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid
import rich

class WD:
	site_url = 'https://www.clever-media.ru'
	data = None
	pages  = []
		
	def __init__(self):
		# self.init()
		if False:
			firefox_options = webdriver.FirefoxOptions()
			firefox_options.add_argument('--disable-gpu')
			firefox_options.add_argument("--disable-notifications")
			self.driver = webdriver.Firefox(options=firefox_options)
			self.driver.maximize_window()
			# chrome_options = webdriver.ChromeOptions()
			# chrome_prefs = {}
			# chrome_options.experimental_options["prefs"] = chrome_prefs
			# chrome_options.add_argument('--disable-gpu')
			# chrome_options.add_argument("--disable-notifications")
			# self.driver = webdriver.Chrome(options=chrome_options)
			# self.driver.maximize_window()

	# def __del__(self):
		# try:
		# 	self.driver.quit()
		# except: pass

	def Get_HTML(self, curl):
		if True:
			print(f"==========================================={curl}===============================================")
			# source = requests.get(curl).text
			# self.driver.get(curl)
			r = requests.get(curl, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
			self.page_source = r.text
			file = open("rq.html", "w", encoding='utf-8')
			file.write(r.text)
			file.close()
			if 'data-product-json=' in r.text:
				json_text = sx(r.text, 'data-product-json="','"')
				import html
				json_text = html.unescape(json_text)
				import rich
				self.data = json.loads(json_text)
				rich.print(self.data)

			return r.text
		else:
			#r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
			r = requests.get(curl)
			self.page_source = r.text.replace('pagination__item','page-item')
			print('*********replaced*********')
			#str_to_file(file_path="response.html", st = self.page_source)
			#self.driver.get(curl)
			#self.page_source = self.driver.page_source
			#return self.page_source
		return self.page_source

	def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link:str) -> list:
		echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
		ll_catalog_items = []
		ll_catalog_pages_list = self.Get_List_of_Catalog_Pages(pc_link)
		for catalog_page in ll_catalog_pages_list:
			echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white') + '    ' + style('Страница: ', fg='bright_cyan') +style(catalog_page, fg='bright_green'))
			self.Get_HTML(catalog_page)
			soup = BS(self.page_source, features='html5lib')
			# elements = soup.find_all('a',{'class':'js-item'})
			grid = soup.find('div', {'class':'catalog-list'})
			elements = grid.find_all('a', itemprop='url')
			for ln_counter, element in enumerate(elements):
				if self.site_url + element['href'] not in ll_catalog_items:
					print(f"{ln_counter}  {self.site_url}{element['href']}")
				append_if_not_exists(self.site_url + element['href'], ll_catalog_items)
		print(len(ll_catalog_items))
		return ll_catalog_items


	def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
		self.Get_HTML(pc_href)
		self.pages  = []
		soup = BS(self.page_source, 'html5lib')
		# links = self.driver.find_elements(By.CLASS_NAME,'pagination-link')
		links = soup.find_all('a', {'class' : 'pagination-link'})
		rich.print(dir(links))
		max_number = 0
		for link in links:
			rich.print(link)
			rich.print(type(link))
			rich.print(dir(link))
			rich.print(link.attrs)
			lnk = link.attrs['href']
			import re
			page_number = re.search(r'\d+$', lnk).group()
			max_number = int(page_number)
		for i in range(max_number):
			self.pages.append(f'https://www.clever-media.ru/collection/trendbooks?page={i+1}')
		rich.print(self.pages)
		return self.pages

		

	def Get_link_on_the_next_catalog_page(self, lc_link:str) -> str:
		if lc_link == '':
			return
		self.Get_HTML(lc_link)
		self.Write_To_File('tsource.html')
		#soup = BS(self.page_source, features='html5lib')
		soup = BS(self.page_source, features='html5lib')
		link = soup.find('a',{'class':'pagination-next'})
		if link != None:
			link_on_next = link['href']

			print(link_on_next)

			if len(link_on_next)>0:
				link_on_next = self.site_url + link_on_next
				append_if_not_exists(link_on_next, self.list_pages_of_catalog)
				print(link_on_next.count('http'))
				if link_on_next.count('http')==1:
					self.Get_link_on_the_next_catalog_page(link_on_next)
		return
		"""
		if page source contented text 'icon-arrow-page-next' it have the next page, in other cases it's the last catalog page
		"""
		#if self.page_source.count('pagination__nav pagination__nav--next')==0: # page without link on the next page
		#	return ''
		#else: # the page have link on next page
		print(range(self.page_source.count('<li class="page-item">')))
		for i in range(self.page_source.count('<li class="page-item">')):
			lc_link_section = sx(self.page_source, '<li class="page-item">','</li>',i+1)
			lc_link = sx(lc_link_section, 'href="','"')
			lc_link = (self.site_url if len(lc_link)>0 else '') + lc_link
			print('++++++++++++++++>', lc_link)
			if 'icon-arrow-page-next' in lc_link_section:
				link_on_next = lc_link
			append_if_not_exists(lc_link, self.list_pages_of_catalog)

		return lc_link
		soup = BS(self.page_source, features='html5lib')
		try:
			link_on_next = soup.find('a',{'class':'pagination__nav pagination__nav--next'})['href']
		except:	return ''
		links = soup.find_all('a',{'class':'page-link'})
		for l in links:
			print('=======>',l)
		for ln_index, link in enumerate(links):
			print(1)
			lc_link = (self.site_url if len(link['href'])>0 else '') + link['href']
			append_if_not_exists(lc_link, self.list_pages_of_catalog)
		return (self.site_url if len(link_on_next)>0 else '') + link_on_next
		
	

		
	def Write_To_File(self, cfilename):
		file = open(cfilename, "w", encoding='utf-8')
		file.write(self.page_source)
		file.close()


def Login():
	return WD()


#colorama.init()

# wd = Login()

#print( wd.Get_List_Of_Links_On_Goods_From_Catalog( 'https://www.clever-media.ru/books/filter/collections-is-gigantskie-plakaty/apply/' ))
#print( wd.Get_List_Of_Links_On_Goods_From_Catalog( 'https://www.clever-media.ru/books/?PAGEN_1=1' ))



