"""
Real media, classified by looking at every file rather than by filename.

Only files that exist are listed. Anything the architecture asks for that we
do not have stays a labelled placeholder, so the gap is briefable instead of
silently blank.

U = /wp-content/uploads
"""
U = "/wp-content/uploads"

# Slot -> (path, alt). One slot per job, so a re-shoot is a one-line change.
MEDIA = {
    # video
    "hero_loop":      (U + "/2026/08/dining-loop.mp4", "The dining room through service"),

    # the room
    "room_wide":      (U + "/2025/11/A7404217.jpg", "The dining room, warm light under the canopy"),
    "room_bar":       (U + "/2025/11/A7404218.jpg", "The bar counter and dining room"),
    "room_booths":    (U + "/2025/11/DSC05005.jpg", "Curved booths by the windows"),
    "room_booth_one": (U + "/2025/11/A7404213.jpg", "A curved booth set for two"),
    "room_evening":   (U + "/2025/12/DSC08777.jpg", "The room in the evening, bar behind"),
    "room_lounge":    (U + "/2025/12/DSC08767.jpg", "Warm light across the lounge"),
    "room_private":   (U + "/2025/12/DSC08761.jpg", "The private table under the mirrors"),

    # food
    "pasta_finish":   (U + "/2025/11/DSC04982.jpg", "Pasta finished at the pass"),
    "pasta_truffle":  (U + "/2025/11/italian-food-3.jpg", "Truffle shaved over pasta"),
    "pasta_plated":   (U + "/2025/11/italian-dish.jpg", "Spaghetti plated"),
    "dish_dark":      (U + "/2025/11/DSC04941.jpg", "A plate finished with sauce"),
    "pizza":          (U + "/2025/12/amami-Pizza-scaled.jpeg", "Margherita from the oven"),

    # people and craft
    "server_wine":    (U + "/2025/11/A7404220.jpg", "Wine and cocktails carried to a table"),

    # drinks and table
    "cocktail_smoke": (U + "/2025/11/A7404259.jpg", "A smoked cocktail, lid lifting"),
    "wine_pour":      (U + "/2025/11/A7404231.jpg", "Wine poured at a set table"),
    "wine_table":     (U + "/2025/11/DSC05015.jpg", "A bottle and glasses on the table"),
    "table_setting":  (U + "/2025/11/DSC05009.jpg", "The table, laid"),
}

# Ordered pools for galleries, best first.
# chef_plate and chef_kitchen were removed on 2026-09-03. Both photographs are
# of the previous chef, Gianluca Martinucci, with his name embroidered on the
# jacket, and the site is now Chef Isabella Comello's. The files are still in
# wp-content/uploads; they are simply no longer addressable from the build.
GALLERY = ["room_wide", "room_evening", "pasta_finish", "cocktail_smoke", "room_booths",
           "pizza", "wine_pour", "room_lounge", "pasta_truffle",
           "room_private", "table_setting", "server_wine", "room_bar", "dish_dark",
           "wine_table", "room_booth_one", "pasta_plated"]
