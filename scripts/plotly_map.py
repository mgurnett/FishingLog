from catches.models import Lake, Stock
import plotly.express as px
import pandas as pd

def get_lakes():
    lakes = Lake.objects.all()

    # lakes = Lake.objects.values_list('name', 'other_name', 'district', 'static_tag', 'reg_location', 
    #                                  'ats', 'lat', 'long', 'waterbody_id', 'notes', 'gps_url')
    stocks = Stock.objects.all()

    all_lakes = []

    for lake in lakes:
        stock_for_lake = stocks.filter(lake=lake)
        stock_num = 0
        if stock_for_lake:
            for stock in stock_for_lake:
                if stock.date_stocked.year == 2024:
                    fish = "Walleye" if stock.fish.name == "Walleye" else "Trout"
                    status = "current"
                    stock_num += stock.number
                else:
                    status = "old"
                
                this_lake = {
                    'name': lake.name,
                    'other_name': lake.other_name,
                    'district': lake.district,
                    'reg_location': lake.reg_location,
                    'lat': lake.lat,
                    'long': lake.long,   
                    'fish': fish,
                    'status': status,
                    'stock_num': 5
                }            
                
            all_lakes.append(this_lake)


    df = pd.DataFrame(all_lakes, columns=['name', 'other_name', 'district', 'reg_location', 
                                     'lat', 'long', 'fish', 'status', 'stock_num'])

    return df


def run():
    lakes_df = get_lakes()
    fig = px.scatter_mapbox(
        lakes_df,
        lat="lat",
        lon="long",
        color="status",
        size="stock_num",
        hover_name="name",
        labels={"name": "Lake"}, 
        hover_data=["other_name", "district", 'reg_location', 'fish', 'status'],
        zoom=5,
        height=800,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(showlegend=True)
    fig.show()