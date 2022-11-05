from queue import Empty
from my_library import *
from driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style

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

		ol.Get_HTML(pc_good_link)
		ol.Write_To_File('gsource.html')
		soup = BS(ol.page_source, features='html5lib')


		self.article = sx(ol.page_source, "'isbn':'","'")

		self.name = soup.find('h1').text.strip()
		try:
			fg = soup.find('div',{'class':'block product-card-description'}).find_all('div', {'class':'form-group'})
			try:
				for f in fg:
					self.description = self.description + ' ' +reduce(f.text.replace(chr(10),' ').replace(chr(9),' ').strip())
			except: pass
		except:
			self.description = soup.find('div',{'class':'about__description'}).text
			self.description = reduce(self.description.replace(chr(10),' ').replace(chr(9),' ').strip())
		
		for picture in soup.find_all('img',{'class':'fancybox'}):
			append_if_not_exists(ol.site_url + picture['href'], self.pictures)
		
		if len(self.pictures)==0:
			for picture in soup.find_all('img',{'alt':'Слайд4'}):
				append_if_not_exists(ol.site_url + picture['src'], self.pictures)


		try:
			self.price = soup.find('div',{'class':'price-new'}).text.replace('рублей','').replace(' ','')
		except:
			self.price = soup.find('div',{'class':'item__actual-price'}).text.replace('рублей','').replace(' ','')
		self.price = self.price.replace('руб.','')


		try:
			self.description += ' ' + reduce(soup.find('div',{'class':'tab-pane fade show active'}).text.replace(chr(10),' ').replace(chr(9),' '))
		except: pass

		return
		
		for i in range(ol.page_source.count('data-large_image="')):
			append_if_not_exists(sx(ol.page_source,'data-large_image="','"',i+1), self.pictures)
		
		self.price = soup.find('p',{'class':'price'}).text.replace(',00 ₽','').strip()
	
		#for i in range(ol.page_source.count('<option value="')):
		#	lc_size = sx(ol.page_source, '<option value="', '"', i+1)
		#	if len(lc_size)>0:
		#		append_if_not_exists(lc_size, self.sizes)

		
		sizes = soup.find('select',{'id':'pa_rost'})
		if sizes!=None:
			sizes=sizes.find_all('option')
			for size in sizes:
				lc_size = size.text
				if lc_size!='Выбрать опцию':
					append_if_not_exists(lc_size, self.sizes)
		else:
			self.sizes=['*']

		colors = soup.find('select',{'id':'pa_color'})
		if colors!=None:
			colors = colors.find_all('option')
			for color in colors:
				lc_color = color.text
				if lc_color!='Выбрать опцию':
					append_if_not_exists(lc_color, self.colors)

		self.description = soup.find('div',{'class':'woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab'}).text.strip()

		if not '–' in self.price:
			for size in self.sizes:
				self.prices.append(self.price)
		else:
			print()
			print()
			self.sizes=[]
			lc_description_source = self.description.replace('\nРасцветки в ассортименте','').replace(' — ','-').replace(' по ','-').replace('руб\n','руб.\n')
			if 'Расцветки:' in lc_description_source:
				lc_description_source = lc_description_source[0:lc_description_source.find('Расцветки:')]
			if 'Цвет:' in lc_description_source:
				lc_description_source = lc_description_source[0:lc_description_source.find('Цвет:')]
			print(f'Источник размеров:{lc_description_source}')
			print()
			lc = sx(lc_description_source+'|', 'Размеры:','|')
			lc = lc.replace('Размеры:','').strip()
			ll_source = lc.split('\n')
			print(f'll_source:{ll_source}')
			print()
			
			for lc in ll_source:
				print()
				print()
				print()
				print(f'lc:{lc}')
				ll_r_str = ''.join(reversed(lc))
				lc_price = ''.join(reversed(sx(ll_r_str, '.бур ', '-')))
				lc = lc.replace(f'-{lc_price} руб.','')
				print(f'lc: {lc}    => price: {lc_price}')
				for size in lc.split(','):
					if len(size)>0 and len(lc_price)>0:
						self.sizes.append(size)
						self.prices.append(lc_price)
			if len(self.sizes)==0:
				self.sizes=['*']
			print()
			print()


