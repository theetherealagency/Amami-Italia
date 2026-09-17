"""
Amami Italia — the real menu, transcribed from
Downloads/1787148406161-Amami Menu 2026.pdf (four pages, image-only, so it was
read and transcribed by hand — pdftotext returns nothing).

Prices are as printed. `v` = vegetarian, `gf` = gluten free, matching the
legend on the printed menu.

FOOTER NOTES on every printed page, to be carried onto the menu pages:
  - Automatic gratuity of 18% applied to all parties of 6 guests or more
  - Maximum of 3 separate checks per table, split evenly
"""

LEGEND_NOTES = [
    "Automatic gratuity of 18% applies to parties of six or more.",
    "Maximum of three separate checks per table, split evenly.",
]

# (name, description, price, tags, add-ons)
DINING = [
    ("Antipasti", "Appetizers", [
        ("Arancini", "Rice balls filled with mozzarella, served with house tomato sauce (3)", "18", ["v"], ""),
        ("Melanzane Parmigiana", "Baked layers of eggplant, tomato sauce, mozzarella and parmigiano", "18", ["v"], ""),
        ("Caprese", "Buffalo mozzarella with heirloom tomatoes and basil oil", "28", ["v", "gf"], ""),
        ("Bruschetta", "Toasted artisan bread topped with tomatoes, garlic, olive oil and sea salt (3)", "14", ["v"], ""),
        ("Burrata", "Fresh burrata with sautéed cherry tomatoes, garlic and basil oil", "30", ["v", "gf"], "Add Parma prosciutto 6"),
        ("Frittura di Mare Mista", "Fried calamari, prawns and zucchini with Greek lime yogurt", "38", ["gf"], ""),
    ]),
    ("Primi Piatti", "Pasta", [
        ("Gnocchi al Pesto", "Potato gnocchi tossed in fresh basil pesto and pine nuts, Parmigiano, topped with stracciatella", "38", ["v"], ""),
        ("Ravioli", "Ricotta and spinach ravioli with blush sauce", "38", ["v"], ""),
        ("Risotto allo Zafferano e Asparagi", "Carnaroli risotto finished with saffron", "35", ["v", "gf"], "Add shrimp 8"),
        ("Spaghetti Aglio Olio e Peperoncino", "Garlic, extra virgin olive oil, hot pepper", "30", ["v"], "Add shrimp 8"),
        ("Lasagna", "Beef, spinach, mozzarella and house tomato sauce", "30", [], ""),
        ("Artisanal Penne", "Vodka-infused tomato cream sauce", "28", ["v"], "Add chicken 6 · shrimp 8 · vegetables 6"),
    ]),
    ("Secondi", "Main entrées — all served with grilled seasonal vegetables and fingerling potatoes", [
        ("Salmone al Sambuca", "Sesame-crusted seared salmon with Pernod and Sambuca cream sauce", "52", ["gf"], ""),
        ("Agnello alla Griglia", "Grilled lamb chops marinated with rosemary and lemon", "80", [], ""),
        ("Tomahawk", "Dry-aged 45 days, AAA Canadian", "195/kg", [], ""),
        ("Bistecca alla Fiorentina", "Dry-aged 45 days, AAA Canadian T-bone", "190/kg", [], ""),
        ("Scaloppine al Marsala", "Veal or chicken scaloppine, mushrooms and creamy marsala sauce", "40", [], ""),
        ("Bistecca di Cavolfiore", "Grilled cauliflower steak with chickpea and beet cream sauce", "38", ["v", "gf"], ""),
        ("Ribeye", "12 oz AAA", "80", [], ""),
        ("Petto di Pollo al Limone", "Chicken breast with a light lemon jus", "38", ["gf"], ""),
    ]),
    ("Contorni", "Sides", [
        ("Cavoletti Fritti", "Cajun fried brussels sprouts", "18", ["v", "gf"], ""),
        ("Caesar Salad", "Crisp romaine, croutons and house caesar dressing", "18", ["v", "gf"], ""),
        ("Truffle Fries / Sweet Potato Fries", "", "14", ["v"], ""),
        ("Insalata di Casa", "Seasonal mixed salad with house dressing", "18", ["v", "gf"], ""),
        ("Fagioli al Pomodoro", "Beans in house tomato sauce", "12", ["v", "gf"], ""),
        ("Mandy's Signature Salad", "Roasted red beets, greens, feta, mandarin oranges and house Italian dressing", "21", ["v", "gf"], ""),
    ], "Add chicken 6 · smoked salmon 10 · shrimp 8 to any salad"),
    ("Dolci", "Dessert", [
        ("Cheesecake ai Frutti di Bosco", "Light ricotta and mascarpone cheesecake with fresh berries", "18", ["v"], ""),
        ("Ricotta & Pistachio Cheesecake", "Pistachio and ricotta creams separated by sponge cake, crusted pistachios, powdered sugar", "18", ["v"], ""),
        ("Chocolate Cheesecake", "Creamy cheesecake with rich ganache on a chocolate crumb base", "15", ["v"], ""),
        ("Sorbetto al Limone", "Artisanal lemon sorbet", "18", ["v", "gf"], ""),
        ("Tiramisù", "Savoiardi soaked in espresso and rum essence, layered with mascarpone and cocoa", "22", ["v"], ""),
        ("Affogato", "Vanilla or pistachio ice cream drowned in freshly made espresso", "14", ["v"], ""),
    ]),
]

CAFFE = [
    ("Caffè e Specialità", "", [
        ("Espresso", "Single", "5", [], ""),
        ("Espresso double or macchiato", "", "7", [], ""),
        ("Americano", "", "7", [], ""),
        ("Cappuccino", "", "8", [], ""),
        ("Latte macchiato", "", "8", [], ""),
        ("Tea", "Mighty Leaf", "8", [], ""),
        ("Caffè Corretto", "Espresso corrected with grappa or Sambuca (0.5 oz)", "10", [], ""),
        ("Irish Coffee", "Americano with Bushmills and a hint of vanilla (1.5 oz)", "17", [], ""),
        ("Amami Caffè", "Americano with Frangelico, Galliano and Gran Sasso Amaro (1.5 oz)", "19", [], ""),
        ("Spanish Coffee", "Americano with brandy and Kahlúa (1.5 oz)", "17", [], ""),
    ]),
]

# The printed menu's "Dopo Cena" is after-dinner DRINKS, not small plates.
AFTER_DARK = [
    ("Porto & Dessert Wine", "4 oz", [
        ("Fonseca White Port", "", "13", [], ""),
        ("Taylor Fladgate 20 Year Tawny", "", "19", [], ""),
        ("Castelgrave Vinsanto", "Tuscany", "25", [], "Bottle 60"),
        ("Grotta del Ninfeo Recioto", "Veneto", "45", [], "Bottle 125"),
    ]),
    ("Digestivi", "2 oz", [
        ("Amaro Montenegro", "", "16", [], ""),
        ("Amaro Dli Amis", "", "18", [], ""),
        ("Amaro Nonino", "", "18", [], ""),
        ("Faccia Brutto Centerbe", "", "18", [], ""),
        ("Venti Amaro", "", "19", [], ""),
        ("Paesani Amaro Gran Sasso", "", "19", [], ""),
        ("Amaro Jefferson", "", "22", [], ""),
        ("Amaro Washington", "", "22", [], ""),
        ("Queen Mary Amaro Trittico", "", "22", [], ""),
    ]),
    ("Liquore", "1.5 oz", [
        ("Limoncello", "", "12", [], ""), ("Sambuca", "White or black", "12", [], ""),
        ("Jägermeister", "", "12", [], ""), ("Kahlúa", "", "12", [], ""),
        ("Malibu", "", "12", [], ""), ("Peach Schnapps", "", "12", [], ""),
        ("Goldschläger", "", "12", [], ""), ("St. Germain", "", "12", [], ""),
        ("Baileys", "", "13", [], ""), ("Frangelico", "", "13", [], ""),
        ("Amaretto", "", "13", [], ""), ("Southern Comfort", "", "13", [], ""),
        ("Chambord", "", "15", [], ""), ("Drambuie", "", "15", [], ""),
        ("Cointreau", "", "15", [], ""), ("Grand Marnier", "", "16", [], ""),
    ]),
    ("Grappa", "1.5 oz", [
        ("Montanaro Liquore di Camomilla", "", "14", [], ""),
        ("Grappa Friulano Nonino", "", "15", [], ""),
        ("Po' di Poli Morbida Grappa", "", "17", [], ""),
        ("Bocale Grappa di Sagrantino", "", "20", [], ""),
    ]),
]

# The printed "Dopo Cena" is after-dinner drinks and coffee, so the two sit
# together on one page. Dolci lives on the dining menu, where it is ordered.
MENUS = {
    "/menu/dining/": DINING,
    "/menu/after-dark/": AFTER_DARK + CAFFE,
}
