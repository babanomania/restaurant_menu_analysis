from scrapper.soup_utils import *
import pandas as pd

def get_all_page_links( base_url ):
    soup = get_soup( base_url )

    all_page_links = soup.find_all( 'a', attrs={'href': re.compile(r".*?page=.*")} )
    all_pages = []

    for each_page in all_page_links:
        all_pages.append( 'https://swiggy.com' + each_page['href'] )

    return all_pages

def get_restaurants_for_page( page_url ):
    df = pd.DataFrame()
    soup = get_soup( page_url )

    qv_spans = soup.find_all( 'span', attrs={'aria-label': 'Open'} )
    for qv_span in qv_spans:
        parent = qv_span.parent.parent.parent.parent

        link = 'https://swiggy.com' + parent.find( 'a' )['href']
        name = parent.find( 'img' )['alt']
        category = parent.find( 'div', attrs={ 'title': re.compile(r".*") } )['title']
        rating = parent.find( 'span', attrs={ 'class', re.compile(r"icon-star .*") } ).findNext('span').text
        price_fortwo = parent.find('div', text=re.compile(r".* FOR TWO")).text.replace( ' FOR TWO', '' ).replace('₹','')

        data = pd.DataFrame( data=[[name, category, rating, price_fortwo, link ]], columns=["name", "category", "rating", "price_fortwo", "link" ])
        df = df.append( data, ignore_index=True )

    return df

def get_restaurant_for_location( location_url ):
    all_pages = get_all_page_links( location_url )
    region_data = pd.DataFrame()

    for each_page in all_pages:
        page_data = get_restaurants_for_page( each_page )
        region_data = region_data.append( page_data, ignore_index=True )

    region_data.index.name = 'index'
    return region_data