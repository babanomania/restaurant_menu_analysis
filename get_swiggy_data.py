from scrapper.restaurant_details import *
from scrapper.restaurant_list import *

def dump_data( location_url, list_file, detail_file ):

    print( "[~] populating for", location_url )
    location_data = get_restaurant_for_location( location_url )
    location_data.to_csv( list_file )

    restaurant_data = pd.DataFrame()
    for index, each_restaurant in location_data.iterrows():
        restaurant_url = each_restaurant['link']
        print( index, " - populating for", restaurant_url )
        restaurant_data = restaurant_data.append( get_restaurant_data(restaurant_url), ignore_index=True )

    restaurant_data.index.name = 'index'
    restaurant_data.to_csv( detail_file )

#howrah region
print( "~{ Howrah Region Data }~" )
location_url = "https://www.swiggy.com/kolkata/howrah-restaurants"
restaurant_list_file = 'data/hwh_restaurant_list.csv'
restaurant_details_file = 'data/hwh_restaurant_details.csv'
dump_data( location_url, restaurant_list_file, restaurant_details_file )

#API url for salt lake
#https://www.swiggy.com/dapi/restaurants/list/v5?lat=22.581706&lng=88.430218
