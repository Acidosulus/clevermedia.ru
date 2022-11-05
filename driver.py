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

class WD:
	def init(self):
		self.site_url = 'https://www.clever-media.ru'
		config = configparser.ConfigParser()


		
	def __init__(self):
		self.init()
		if False:
			chrome_options = webdriver.ChromeOptions()
			chrome_prefs = {}
			chrome_options.experimental_options["prefs"] = chrome_prefs
			chrome_options.add_argument('--disable-gpu')
			chrome_options.add_argument("--disable-notifications")
			#chrome_options.add_argument('--headless')
			self.driver = webdriver.Chrome(options=chrome_options)
			self.driver.maximize_window()

	def __del__(self):
		try:
			self.driver.quit()
		except: pass

	def Get_HTML(self, curl):
		if False:
			if os.path.isfile('response.html'):
					echo(style('Загружен локальный файл: ', fg='bright_red') + style('response.html', fg='red'))
					self.page_source = file_to_str('response.html')
			else:
				r = requests.get(curl)
				self.page_source = r.text
				str_to_file('response.html', self.page_source)
		else:
			r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
			#r = requests.get(curl)
			self.page_source = r.text.replace('pagination__item','page-item')
			print('*********replaced*********')
			#self.page_source
			#str_to_file(file_path="response.html", st = r.text)
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
			elements = soup.find_all('a',{'class':'js-item'})
			for ln_counter, element in enumerate(elements):
				if self.site_url + element['href'] not in ll_catalog_items:
					print(f"{ln_counter}  {self.site_url}{element['href']}")
				append_if_not_exists(self.site_url + element['href'], ll_catalog_items)
		print(len(ll_catalog_items))
		return ll_catalog_items

	
	def get_link_with_bigger_page_number(self) -> str:
		ln_bigger_number = 0
		lc_link_with_bigger_number= ''
		for link in self.list_pages_of_catalog:
			if '?PAGEN_1=' not in link:
				continue
			ln_number = int(sx(link+"|", '/?PAGEN_1=', '|'))
			if ln_number>ln_bigger_number:
				ln_bigger_number = ln_number
				lc_link_with_bigger_number = link
		return lc_link_with_bigger_number
		


	def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
		self.Get_HTML(pc_href)
		self.list_pages_of_catalog = [pc_href]
		lc_result = pc_href
		ln_stored_lenght = 1
		print("==========FIRST============")
		self.Get_link_on_the_next_catalog_page(pc_href)
		print(f"==={len(self.list_pages_of_catalog)}===={ln_stored_lenght}===")
		if len(self.list_pages_of_catalog)==ln_stored_lenght:
			return self.list_pages_of_catalog 
		
		while len(self.list_pages_of_catalog)>ln_stored_lenght:
			print("==========SECOND============")
			print(f"==={len(self.list_pages_of_catalog)}===={ln_stored_lenght}===")
			ln_stored_lenght = len(self.list_pages_of_catalog)
			self.Get_link_on_the_next_catalog_page(self.get_link_with_bigger_page_number())
		return self.list_pages_of_catalog 

		while len(lc_result)>0:
			echo(style('Список страниц каталога:', fg='bright_yellow') + '  ' + style(lc_result, fg='bright_cyan'))
			lc_result = self.Get_link_on_the_next_catalog_page(lc_result)
		ll = self.list_pages_of_catalog.copy()
		for lnk in ll:
			echo(style('Список страниц каталога:', fg='bright_yellow') + '  ' + style(lnk, fg='bright_cyan') + style(text='   второй проход', fg='bright_red'))
			self.Get_link_on_the_next_catalog_page(lnk)
		return self.list_pages_of_catalog

		

	def Get_link_on_the_next_catalog_page(self, lc_link:str) -> str:
		self.Get_HTML(lc_link)
		self.Write_To_File('tsource.html')
		#soup = BS(self.page_source, features='html5lib')
		lc_link = ''
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

wd = Login()

#print( wd.Get_List_Of_Links_On_Goods_From_Catalog( 'https://www.clever-media.ru/books/filter/collections-is-gigantskie-plakaty/apply/' ))
#print( wd.Get_List_Of_Links_On_Goods_From_Catalog( 'https://www.clever-media.ru/books/?PAGEN_1=1' ))



