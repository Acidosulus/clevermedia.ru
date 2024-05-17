from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from driver import *
from good import *
import colorama
from colorama import Fore, Back, Style
from click import echo, style
import asyncio

async def limited_task_sem(sem, wd, link, cat, price):
    async with sem:
        return await unload_one_good( wd, link, cat, price)

async def unload_one_good(dw:WD, lc_link_on_good: str, pc_price:str, price:Price):
    lo_good = Good(dw, lc_link_on_good, pc_price)
    print(f'{Fore.YELLOW}Название: {Fore.LIGHTGREEN_EX}{lo_good.name}{Fore.RESET}')
    print(f'{Fore.YELLOW}Артикул: {Fore.LIGHTCYAN_EX}{lo_good.article}{Fore.RESET}')
    print(f'{Fore.YELLOW}Цена: {Fore.LIGHTGREEN_EX}{lo_good.price}{Fore.RESET}')
    print(f'{Fore.YELLOW}Описание: {Fore.LIGHTGREEN_EX}{lo_good.description}{Fore.RESET}')
    print(f'{Fore.YELLOW}Картинки: {Fore.LIGHTCYAN_EX}{lo_good.pictures}{Fore.RESET}')
    lc_name = lo_good.name if lo_good.name.count(lo_good.article) != 0 else lo_good.article + ' ' + lo_good.name
    # if 'Под заказ' in lo_good.description or 'Под заказ' in lo_good.page_source:
    #     echo(style('Под заказ', fg='bright_red'))
    #     continue
    # else: print('Не под заказ')
    # print(type(lo_good.price), len(lo_good.price))
    if lo_good.price != '':
        price.add_good('',
                                prepare_str(lc_name),
                                prepare_str(lo_good.description),
                                prepare_str( str(round(float(lo_good.price)*float(sys.argv[4]), 2))),
                                '15',
                                prepare_str(lc_link_on_good),
                                prepare_for_csv_non_list(lo_good.pictures))
        price.write_to_csv(sys.argv[3])
    



async def unload_catalog():
    if sys.argv[1] == 'catalog':
        wd = Login()
        wd.Get_List_of_Catalog_Pages(sys.argv[2])
        links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
        print('Список товаров:', links_list)
        ln_total = len(links_list)
        ln_counter = 0
        price = Price(sys.argv[3])
        sem = asyncio.Semaphore(10)
        tasks = []
        for link in links_list:
            # lo_good = unload_one_good(wd, link, sys.argv[3])
            task = limited_task_sem(sem, wd, link, sys.argv[3], price)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

########################################################################################################################
########################################################################################################################
colorama.init()
########################################################################################################################
########################################################################################################################

if sys.argv[1] == 'good':
    wd = Login()
    print(sys.argv[1], sys.argv[2])
    price = Price(sys.argv[3])
    for link in [sys.argv[2]]:
        lo_good = unload_one_good(wd, link, sys.argv[3], price)
        lc_name = lo_good.name if lo_good.name.count(lo_good.article) != 0 else lo_good.article + ' ' + lo_good.name
        # if 'Под заказ' in lo_good.description or 'Под заказ' in lo_good.page_source:
        #     echo(style('Под заказ', fg='bright_red'))
        #     continue
        # else: print('Не под заказ')
        price.add_good('',
                                prepare_str(lc_name),
                                prepare_str(lo_good.description),
                                prepare_str( str(round(float(lo_good.price)*float(sys.argv[4]), 2))),
                                '15',
                                prepare_str(link),
                                prepare_for_csv_non_list(lo_good.pictures))
        price.write_to_csv(sys.argv[3])

if sys.argv[1] == 'catalog':
    asyncio.run(unload_catalog())


if sys.argv[1] == 'reverse':
    reverse_csv_price(sys.argv[2])

if sys.argv[1] == 'ansi':
    convert_file_to_ansi(sys.argv[2] + '_reversed.csv')

    # try: wd.driver.quit()
    # except: pass