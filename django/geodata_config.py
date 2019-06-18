import os

MAPZEN_S3_URL = "https://s3.amazonaws.com/osm-polygons.mapzen.com/"
GEOJSON_TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp/')
SELECTED_FILE_LIST = [
    # NEW ONES
    "albania_geojson.tgz",
    "algeria_geojson.tgz",
    "argentina_geojson.tgz",
    "armenia_geojson.tgz",
    "azerbaijan_geojson.tgz",
    "bolivia_geojson.tgz",
    "burundi_geojson.tgz",
    "c-te-d-ivoire_geojson.tgz",
    "djibouti_geojson.tgz",
    "egypt_geojson.tgz",
    "guatemala_geojson.tgz",
    "jamaica_geojson.tgz",
    "mauritania_geojson.tgz",
    "turkey_geojson.tgz",
    "uruguay_geojson.tgz",
    "belarus_geojson.tgz",
    "bhutan_geojson.tgz",
    "cape-verde_geojson.tgz",
    "china_geojson.tgz",
    "israel_geojson.tgz",
    "maldives_geojson.tgz",
    "united-states-of-america_geojson.tgz",
    "turkmenistan_geojson.tgz",
    "ukraine_geojson.tgz",
    "uzbekistan_geojson.tgz",
    "venezuela_geojson.tgz",
    "yemen_geojson.tgz",

    # NOT WORKING:
    # "senegal_geojson.tgz",

    # "paraguay_geojson.tgz",               # no geodata whatsoever
    # "thailand_geojson.tgz",               # doesnt draw all of them somehow
    # "trinidad-and-tobago_geojson.tgz"     # no geodata whatsoever

    # "canada_geojson.tgz",                 # malformed json
    # "eritrea_geojson.tgz",                # no geodata whatsoever

    # OLDER ONES:
    "afghanistan_geojson.tgz",
    "angola_geojson.tgz",
    "bangladesh_geojson.tgz",
    "benin_geojson.tgz",
    "botswana_geojson.tgz",
    "brazil_geojson.tgz",
    "burkina-faso_geojson.tgz",
    "cameroon_geojson.tgz",
    "central-african-republic_geojson.tgz",
    "chad_geojson.tgz",
    "congo-brazzaville_geojson.tgz",
    "congo-kinshasa_geojson.tgz",
    "costa-rica_geojson.tgz",
    "ethiopia_geojson.tgz",
    "gabon_geojson.tgz",
    "ghana_geojson.tgz",
    "guinea-bissau_geojson.tgz",
    "guinea_geojson.tgz",
    "haiti_geojson.tgz",
    "honduras_geojson.tgz",
    "india_geojson.tgz",
    "indonesia_geojson.tgz",
    "kenya_geojson.tgz",
    "liberia_geojson.tgz",
    "madagascar_geojson.tgz",
    "malawi_geojson.tgz",
    "malaysia_geojson.tgz",
    "mali_geojson.tgz",
    "mexico_geojson.tgz",
    "morocco_geojson.tgz",
    "mozambique_geojson.tgz",
    "myanmar_geojson.tgz",
    "namibia_geojson.tgz",
    "nepal_geojson.tgz",
    "nicaragua_geojson.tgz",
    "niger_geojson.tgz",
    "nigeria_geojson.tgz",
    "pakistan_geojson.tgz",
    "peru_geojson.tgz",
    "philippines_geojson.tgz",
    "rwanda_geojson.tgz",
    "sierra-leone_geojson.tgz",
    "south-africa_geojson.tgz",
    "south-sudan_geojson.tgz",
    "sri-lanka_geojson.tgz",
    "sudan_geojson.tgz",
    "swaziland_geojson.tgz",
    "tanzania_geojson.tgz",
    "the-gambia_geojson.tgz",
    "togo_geojson.tgz",
    "tunisia_geojson.tgz",
    "uganda_geojson.tgz",
    "vietnam_geojson.tgz",
    "zambia_geojson.tgz",
    "zimbabwe_geojson.tgz"
]

# SELECTED_FILE_LIST_DEV = SELECTED_FILE_LIST
SELECTED_FILE_LIST_DEV = ["sierra-leone_geojson.tgz", "rwanda_geojson.tgz", "uganda_geojson.tgz", "india_geojson.tgz"]

ADMIN_LEVELS_TO_IMPORT = [
    "admin_level_2.geojson", "admin_level_3.geojson", "admin_level_4.geojson", "admin_level_5.geojson",
    "admin_level_6.geojson"
]
