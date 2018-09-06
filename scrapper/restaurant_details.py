from scrapper.soup_utils import *
import pandas as pd

def get_restaurant_name( page ):
    title_div = page.find( 'h1', {"title" : re.compile(r".*")} )
    return title_div.text.strip()

def get_price( parent_div ):
    price_all = parent_div.find_all( 'span' )
    item_price = -1

    for price in price_all:
        if( price.text != '' ):
            item_price = price.text

    return item_price

def get_restaurant_data( url ):
    df = pd.DataFrame()
    soup = get_soup( url )

    restaurant_name = get_restaurant_name( soup )

    itemname_divsome = soup.find('div', attrs={'itemtype': 'http://schema.org/MenuItem'})
    super_parent = itemname_divsome.parent.parent.parent.parent

    for category_div in super_parent.find_all( 'div', recursive=False ) :
        if( category_div.find('h2') ):

            category_name = category_div.find('h2').text.strip()
            menu_items = category_div.find_all('div', attrs={'itemtype': 'http://schema.org/MenuItem'})

            for each_item in menu_items:
                item_name = each_item.find( 'div', attrs={'itemprop' :'name'} ).text.strip()
                item_price = get_price(each_item)

                data = pd.DataFrame( [[restaurant_name, category_name, item_name, item_price] ], columns=["restaurant", "category", "name", "price" ])
                df = df.append( data, ignore_index=True )

    return df
