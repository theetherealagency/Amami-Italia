# -*- coding: utf-8 -*-
"""English -> Italian, keyed by the exact English string.

The build annotates every matching text node with data-it and the switch swaps
them in the page. A string that is not in here stays English, so a gap shows up
as untranslated copy rather than as an empty element.

Written to be read by an Italian speaker before it goes near a campaign — the
dish descriptions in particular are the restaurant's own words.
"""

IT = {
    # ---- navigation and actions ----
    "Menu": "Menu",
    "Our Story": "Chi siamo",
    "After Dark": "After Dark",
    "Events": "Eventi",
    "Reservations": "Prenotazioni",
    "Home": "Home",
    "Visit": "Dove siamo",
    "Contact": "Contatti",
    "FAQ": "Domande frequenti",
    "Catering": "Catering",
    "Journal": "Giornale",
    "Gift Cards": "Carte regalo",
    "Careers": "Lavora con noi",
    "Press": "Stampa",
    "Reserve a Table": "Prenota un tavolo",
    "Reserve": "Prenota",
    "Call": "Chiama",
    "Directions": "Indicazioni",
    "Get Directions": "Come arrivare",
    "See the Menu": "Guarda il menu",
    "See the list": "Guarda la lista",
    "Read the menu": "Leggi il menu",
    "Event Enquiry": "Richiesta eventi",
    "Catering Enquiry": "Richiesta catering",
    "Buy a Gift Card": "Acquista una carta regalo",
    "Apply": "Candidati",
    "Media Enquiry": "Richieste stampa",
    "Skip to content": "Vai al contenuto",
    "Open menu": "Apri il menu",
    "Close menu": "Chiudi il menu",
    "Language": "Lingua",
    "English": "English",
    "Italiano": "Italiano",
    "Sign up": "Iscriviti",
    "Send": "Invia",
    "Send enquiry": "Invia richiesta",
    "Phone": "Telefono",
    "Address": "Indirizzo",
    "Today": "Oggi",
    "Hours": "Orari",
    "Join the Amami table": "Unisciti alla tavola di Amami",
    "Explore": "Esplora",
    "Connect": "Seguici",
    "Amami — Love Me.": "Amami — Love Me.",
    "Tuscan restaurant, lounge & catering in Brampton.":
        "Ristorante toscano, lounge e catering a Brampton.",

    # ---- legal ----
    "Privacy": "Privacy",
    "Cookies": "Cookie",
    "Accessibility": "Accessibilità",
    "Reservation Terms": "Condizioni di prenotazione",
    "Gift Card Terms": "Condizioni carte regalo",
    "Terms of Use": "Condizioni d'uso",
    "Legal": "Note legali",

    # ---- hours ----
    "Monday": "Lunedì", "Tuesday – Thursday": "Martedì – Giovedì",
    "Friday – Saturday": "Venerdì – Sabato", "Sunday": "Domenica",
    "Closed": "Chiuso",
    "Mon closed &middot; Tue–Thu 12–10pm &middot; Fri–Sat 12–11pm &middot; Sun 12–9pm":
        "Lun chiuso &middot; Mar–Gio 12–22 &middot; Ven–Sab 12–23 &middot; Dom 12–21",

    # ---- home ----
    "It means love me. Tuscan cooking on Mayfield Road.":
        "Significa amami. Cucina toscana su Mayfield Road.",
    "Private Dining": "Sala privata",
    "Enquire": "Richiedi informazioni",

    # ---- menu hub ----
    "Dining": "Sala", "Pizza": "Pizza", "Wine": "Vini", "Cocktails": "Cocktail",
    "Tasting": "Degustazione",
    "Also on the menu": "Anche sul menu",
    "The other five lists": "Le altre cinque liste",
    "These pages are built and named. The kitchen and the bar are still sending the current lists, and they go up as text the day they arrive.":
        "Queste pagine esistono e hanno un nome. La cucina e il bar stanno ancora mandando le liste aggiornate: appena arrivano, le pubblichiamo come testo.",
    "List to come": "Lista in arrivo",
    "Neapolitan, from the oven.": "Napoletana, dal forno.",
    "Tuscany first, then the rest of Italy.": "Prima la Toscana, poi il resto d'Italia.",
    "The aperitivo hour and the bar's own list.": "L'ora dell'aperitivo e la lista del bar.",
    "The chef's sequence, on notice.": "La sequenza dello chef, su prenotazione.",
    "Trays, pasta and mains to take away.": "Vassoi, paste e secondi da portare via.",
    "Book the table first &mdash; the menu will still be here.":
        "Prima prenota il tavolo &mdash; il menu resta qui.",
    "Antipasti through dolci. Gnocchi al pesto, saffron risotto, lamb chops, and the tomahawk and fiorentina, both aged 45 days and cut by the kilo.":
        "Dagli antipasti ai dolci. Gnocchi al pesto, risotto allo zafferano, costolette d'agnello, e la tomahawk e la fiorentina, entrambe frollate 45 giorni e servite al chilo.",
    "What the bar works from once the plates go away. Tawny port, a long row of amari, grappa, and coffee with something in it.":
        "Ciò che il bar serve quando i piatti sono andati via. Porto tawny, una lunga fila di amari, grappe, e caffè corretti.",

    # ---- our story ----
    "Tuscan at heart. Brampton at home.": "Toscana nel cuore. Brampton a casa.",
    "Amami means love me. It is a Tuscan kitchen on Mayfield Road, cooking for Brampton, Caledon and Vaughan.":
        "Amami vuol dire amami. È una cucina toscana su Mayfield Road, che cucina per Brampton, Caledon e Vaughan.",
    "Where it came from": "Da dove viene",
    "Tuscan cooking is plainer than the Italy most people picture — bread, beans, olive oil, a short list of things done properly.":
        "La cucina toscana è più semplice dell'Italia che si immagina di solito: pane, fagioli, olio d'oliva, poche cose fatte bene.",
    "The craft that travelled": "Il mestiere che ha viaggiato",
    "Technique arrives with a person, not from a book. Pasta is rolled here, sauces are built here, and the kitchen is run by someone who learned it where it comes from.":
        "La tecnica arriva con una persona, non da un libro. Qui la pasta si tira a mano, i sughi si costruiscono in casa, e la cucina è guidata da chi l'ha imparata dove è nata.",
    "The room on Mayfield Road": "La sala su Mayfield Road",
    "The room seats a Tuesday dinner for two and a table of twenty on a Saturday. It is warm, it is loud when it should be, and it is ten minutes from Caledon and Vaughan.":
        "La sala accoglie una cena per due il martedì e una tavolata di venti il sabato. È calda, è rumorosa quando deve esserlo, ed è a dieci minuti da Caledon e Vaughan.",

    # ---- after dark ----
    "Raise the": "Alza il", "Bar": "Bancone",
    "From 10pm": "Dalle 22", "The lounge": "Il lounge",
    "Port, amaro, grappa": "Porto, amaro, grappa", "Music": "Musica",
    "The room": "La sala", "doesn&rsquo;t empty": "non si svuota", "at ten": "alle dieci",
    "After dinner, at Amami": "Dopo cena, da Amami",
    "Dinner service turns over and the room stays open. Forty-three pours after the plates go away &mdash; tawny port, a long row of amari, grappa, and coffee with something in it.":
        "Il servizio di cena finisce e la sala resta aperta. Quarantatré etichette al bicchiere dopo i piatti: porto tawny, una lunga fila di amari, grappe, e caffè corretti.",
    "The counter takes twelve. The lounge takes sixty standing, thirty seated. Come for one, stay for the room.":
        "Il bancone tiene dodici persone. Il lounge sessanta in piedi, trenta sedute. Vieni per uno, resta per la sala.",
    "Read the after-dark list": "Leggi la lista after dark",
    "The Lounge": "Il Lounge", "The Bar": "Il Bancone",
    "Cocktails, small plates and music once dinner service turns over.":
        "Cocktail, piccoli piatti e musica quando finisce il servizio di cena.",
    "The aperitivo hour, and where the signatures are made.":
        "L'ora dell'aperitivo, e dove nascono i nostri signature.",
    "Planning a night for a group, or taking the room for the evening? Tell us the date and how many.":
        "Stai organizzando una serata per un gruppo, o vuoi la sala per tutta la sera? Dicci la data e quante persone.",
    "Ask about a private night": "Chiedi per una serata privata",

    # ---- visit / contact / faq ----
    "Vieni a Trovarci": "Vieni a Trovarci",
    "Come and find us. An invitation rather than a directory listing.":
        "Vieni a trovarci. Un invito, non una voce in un elenco.",
    "Parking": "Parcheggio",
    "Free on-site parking. Count and accessible bays to confirm.":
        "Parcheggio gratuito sul posto. Numero di posti e stalli accessibili da confermare.",
    "Step-free entry, accessible washroom. Details to confirm.":
        "Ingresso senza scalini, bagno accessibile. Dettagli da confermare.",
    "Getting here": "Come raggiungerci",
    "Mayfield Road at Brampton's northern edge; minutes from Caledon, Bolton and Vaughan.":
        "Mayfield Road, al limite nord di Brampton; a pochi minuti da Caledon, Bolton e Vaughan.",
    "Scrivici": "Scrivici",
    "Write to us. One form, routed by subject, so nothing lands in the wrong inbox.":
        "Scrivici. Un solo modulo, smistato per argomento, così nulla finisce nella casella sbagliata.",
    "What is it about?": "Di cosa si tratta?",
    "General": "Informazioni generali",
    "Reservation": "Prenotazione",
    "Private dining or events": "Sala privata o eventi",
    "Name": "Nome", "Email": "Email", "Message": "Messaggio",
    "First name": "Nome", "Last name": "Cognome", "Date": "Data", "Guests": "Ospiti",
    "Buono a Sapersi": "Buono a Sapersi",
    "Contact": "Contatti",
}

# ---------------------------------------------------------------------------
# Menu: course labels, notes and the dish descriptions. The dish NAMES are
# already Italian and are left alone in both languages.
# ---------------------------------------------------------------------------
IT.update({
    "Appetizers": "Antipasti",
    "Pasta": "Paste",
    "Main entrées — all served with grilled seasonal vegetables and fingerling potatoes":
        "Secondi — serviti con verdure di stagione alla griglia e patate novelle",
    "Sides": "Contorni",
    "Dessert": "Dolci",
    "Single": "Singolo",
    "White or black": "Bianca o nera",
    "Mighty Leaf": "Mighty Leaf",
    "Tuscany": "Toscana",
    "Veneto": "Veneto",
    "Bottle 60": "Bottiglia 60",
    "Bottle 125": "Bottiglia 125",
    "Add Parma prosciutto 6": "Aggiungi prosciutto di Parma 6",
    "Add shrimp 8": "Aggiungi gamberi 8",
    "Add chicken 6 · shrimp 8 · vegetables 6": "Aggiungi pollo 6 · gamberi 8 · verdure 6",
    "Add chicken 6 · smoked salmon 10 · shrimp 8 to any salad":
        "Aggiungi a ogni insalata pollo 6 · salmone affumicato 10 · gamberi 8",
    "Automatic gratuity of 18% applies to parties of six or more.":
        "Per tavoli da sei persone o più si applica un servizio del 18%.",
    "Maximum of three separate checks per table, split evenly.":
        "Massimo tre conti separati per tavolo, divisi in parti uguali.",
    "Ready to book?": "Pronto a prenotare?",

    "Rice balls filled with mozzarella, served with house tomato sauce (3)":
        "Arancini ripieni di mozzarella, serviti con salsa di pomodoro della casa (3)",
    "Baked layers of eggplant, tomato sauce, mozzarella and parmigiano":
        "Strati di melanzane al forno con salsa di pomodoro, mozzarella e parmigiano",
    "Buffalo mozzarella with heirloom tomatoes and basil oil":
        "Mozzarella di bufala con pomodori antichi e olio al basilico",
    "Toasted artisan bread topped with tomatoes, garlic, olive oil and sea salt (3)":
        "Pane artigianale tostato con pomodoro, aglio, olio d'oliva e sale marino (3)",
    "Fresh burrata with sautéed cherry tomatoes, garlic and basil oil":
        "Burrata fresca con pomodorini saltati, aglio e olio al basilico",
    "Fried calamari, prawns and zucchini with Greek lime yogurt":
        "Frittura di calamari, gamberi e zucchine con yogurt greco al lime",
    "Potato gnocchi tossed in fresh basil pesto and pine nuts, Parmigiano, topped with stracciatella":
        "Gnocchi di patate al pesto di basilico fresco e pinoli, parmigiano, con stracciatella",
    "Ricotta and spinach ravioli with blush sauce":
        "Ravioli di ricotta e spinaci con salsa rosata",
    "Carnaroli risotto finished with saffron": "Riso Carnaroli mantecato allo zafferano",
    "Garlic, extra virgin olive oil, hot pepper": "Aglio, olio extravergine d'oliva, peperoncino",
    "Beef, spinach, mozzarella and house tomato sauce":
        "Manzo, spinaci, mozzarella e salsa di pomodoro della casa",
    "Vodka-infused tomato cream sauce": "Crema di pomodoro alla vodka",
    "Sesame-crusted seared salmon with Pernod and Sambuca cream sauce":
        "Salmone in crosta di sesamo con crema al Pernod e Sambuca",
    "Grilled lamb chops marinated with rosemary and lemon":
        "Costolette d'agnello alla griglia marinate con rosmarino e limone",
    "Dry-aged 45 days, AAA Canadian": "Frollata 45 giorni, AAA canadese",
    "Dry-aged 45 days, AAA Canadian T-bone": "T-bone AAA canadese, frollata 45 giorni",
    "Veal or chicken scaloppine, mushrooms and creamy marsala sauce":
        "Scaloppine di vitello o pollo, funghi e crema al marsala",
    "Grilled cauliflower steak with chickpea and beet cream sauce":
        "Trancio di cavolfiore alla griglia con crema di ceci e barbabietola",
    "12 oz AAA": "340 g AAA",
    "Chicken breast with a light lemon jus": "Petto di pollo con un leggero jus al limone",
    "Cajun fried brussels sprouts": "Cavoletti fritti alla cajun",
    "Crisp romaine, croutons and house caesar dressing":
        "Lattuga romana croccante, crostini e salsa caesar della casa",
    "Seasonal mixed salad with house dressing":
        "Insalata mista di stagione con condimento della casa",
    "Beans in house tomato sauce": "Fagioli in salsa di pomodoro della casa",
    "Roasted red beets, greens, feta, mandarin oranges and house Italian dressing":
        "Barbabietole rosse arrostite, insalata, feta, mandarini e condimento italiano della casa",
    "Light ricotta and mascarpone cheesecake with fresh berries":
        "Cheesecake leggera di ricotta e mascarpone con frutti di bosco freschi",
    "Pistachio and ricotta creams separated by sponge cake, crusted pistachios, powdered sugar":
        "Creme di pistacchio e ricotta separate da pan di Spagna, pistacchi in granella, zucchero a velo",
    "Creamy cheesecake with rich ganache on a chocolate crumb base":
        "Cheesecake cremosa con ganache su base di biscotto al cacao",
    "Artisanal lemon sorbet": "Sorbetto al limone artigianale",
    "Savoiardi soaked in espresso and rum essence, layered with mascarpone and cocoa":
        "Savoiardi inzuppati in espresso ed essenza di rum, con mascarpone e cacao",
    "Vanilla or pistachio ice cream drowned in freshly made espresso":
        "Gelato alla vaniglia o al pistacchio affogato nell'espresso appena fatto",
    "Espresso corrected with grappa or Sambuca (0.5 oz)":
        "Espresso corretto con grappa o Sambuca (15 ml)",
    "Americano with Bushmills and a hint of vanilla (1.5 oz)":
        "Americano con Bushmills e un tocco di vaniglia (45 ml)",
    "Americano with Frangelico, Galliano and Gran Sasso Amaro (1.5 oz)":
        "Americano con Frangelico, Galliano e Amaro Gran Sasso (45 ml)",
    "Americano with brandy and Kahlúa (1.5 oz)": "Americano con brandy e Kahlúa (45 ml)",
    "Wild boar ragù": "Ragù di cinghiale",
    "45-day dry-aged, on the bone.": "Frollata 45 giorni, con l'osso.",
    "The family recipe.": "La ricetta di famiglia.",
})

# ---------------------------------------------------------------------------
# Page copy: headings, ledes, FAQ, and the small print.
# ---------------------------------------------------------------------------
IT.update({
    "Lunch and dinner.": "Pranzo e cena.",
    "After dinner.": "Dopo cena.",
    "From the oven.": "Dal forno.",
    "The cellar.": "La cantina.",
    "Aperitivo, and what to drink before dinner.": "L'aperitivo, e cosa bere prima di cena.",
    "The tasting.": "La degustazione.",
    "Away from home.": "Fuori casa.",
    "A Tavola &mdash; the menu": "A Tavola &mdash; il menu",
    "Vieni a Trovarci &mdash; visit": "Vieni a Trovarci &mdash; dove siamo",
    "View Menus": "Guarda i menu",
    "Capacity |": "Capienza |",
    "Standing 60 · seated 30": "60 in piedi · 30 sedute",
    "12 at the bar": "12 al bancone",
    "32 dishes &middot; 12pm until close": "32 piatti &middot; dalle 12 alla chiusura",
    "43 pours &middot; port, amaro, grappa, caff&egrave;":
        "43 etichette &middot; porto, amaro, grappa, caff&egrave;",

    # chef
    "Le Mani di Gianluca": "Le Mani di Gianluca",
    "Gianluca's hands. Ties the chef directly to the craft.":
        "Le mani di Gianluca. Lo chef legato direttamente al mestiere.",
    "Born in Canada": "Nata in Canada",
    "Born and raised in Canada. She cooks Italian the way she believes it should be cooked: simply, as at home.":
        "Nata e cresciuta in Canada. Cucina l'italiano come crede che si debba cucinare: semplicemente, come a casa.",
    "Working portrait": "Ritratto al lavoro",

    # experiences
    "Tell us what you are planning and we will come back to you with dates, space and a per-head price.":
        "Raccontaci cosa stai organizzando e ti risponderemo con date, spazi e un prezzo a persona.",
    "What are you planning?": "Cosa stai organizzando?",
    "We reply within one business day.": "Rispondiamo entro un giorno lavorativo.",
    "Catering enquiry": "Richiesta catering",
    "Drop-off": "Consegna",
    "Trays and platters delivered, set out by you.":
        "Vassoi e piatti consegnati, che disponi tu.",
    "Full service": "Servizio completo",
    "Our team, on site, start to finish.":
        "Il nostro team, sul posto, dall'inizio alla fine.",
    "Coverage": "Zone servite",
    "Amami Fuori Casa": "Amami Fuori Casa",
    "Amami, away from home.": "Amami, fuori casa.",
    "Regala Amami": "Regala Amami",
    "Give Amami.": "Regala Amami.",
    "Gift card purchase widget": "Modulo di acquisto carta regalo",
    "Provider not yet chosen.": "Fornitore ancora da scegliere.",
    "Il Quaderno": "Il Quaderno",
    "The notebook.": "Il quaderno.",
    "Lavora con Noi": "Lavora con Noi",
    "Work with us.": "Lavora con noi.",
    "Role": "Ruolo",
    "Si Parla di Noi": "Si Parla di Noi",
    "People are talking about us.": "Si parla di noi.",
    "Press kit": "Cartella stampa",
    "Images, bio, fact sheet &mdash; to assemble.":
        "Immagini, biografia, scheda informativa &mdash; da preparare.",
    "Logos and links to add.": "Loghi e link da aggiungere.",
    "Media enquiry": "Richiesta stampa",

    # FAQ
    "Good to know. Publish every fact — these answer guests, local search and AI answer engines at the same time.":
        "Buono a sapersi. Pubblichiamo ogni informazione: serve agli ospiti, alle ricerche locali e ai motori di risposta insieme.",
    "Do you take reservations?": "Accettate prenotazioni?",
    "Yes — OpenTable, and by phone.": "Sì — su OpenTable e per telefono.",
    "Is there parking?": "C'è parcheggio?",
    "Free on-site parking.": "Parcheggio gratuito sul posto.",
    "Can you handle allergies?": "Gestite le allergie?",
    "Yes. Tell us when you book and again at the table.":
        "Sì. Dicci quando prenoti e ricordacelo al tavolo.",
    "Do you have a tasting menu?": "Avete un menu degustazione?",
    "Degustazione, with a notice period — see the menu page.":
        "Degustazione, con preavviso — vedi la pagina del menu.",
    "Is the lounge age-restricted?": "Il lounge ha un limite di età?",
    "Policy to confirm and publish here.": "Regola da confermare e pubblicare qui.",
    "Can we book the whole room?": "Si può prenotare tutta la sala?",
    "Yes — private dining and full buyouts.":
        "Sì — sala privata e affitto esclusivo dell'intero locale.",

    # landing pages
    "Una Sera per Due": "Una Sera per Due",
    "An evening for two.": "Una sera per due.",
    "Romantic dining in Brampton": "Cena romantica a Brampton",
    "What the evening actually looks like, from arrival to the last drink.":
        "Com'è davvero la serata, dall'arrivo all'ultimo bicchiere.",
    "Cene di Lavoro": "Cene di Lavoro",
    "Working dinners.": "Cene di lavoro.",
    "Why Italian food works for corporate events":
        "Perché la cucina italiana funziona per gli eventi aziendali",
    "Capacities, set menus and the notice period, stated plainly.":
        "Capienze, menu fissi e tempi di preavviso, detti chiaramente.",
    "Le Feste": "Le Feste",
    "The celebrations.": "Le feste.",
    "Bring everyone": "Portate tutti",
    "Group sizes, cake policy, timings and what a celebration here includes.":
        "Numero di ospiti, torta, orari e cosa comprende una festa da noi.",
    "Da Caledon": "Da Caledon",
    "From Caledon.": "Da Caledon.",
    "Minutes from Caledon": "A pochi minuti da Caledon",
    "Where we are relative to Caledon, drive time and parking.":
        "Dove siamo rispetto a Caledon, tempi in auto e parcheggio.",
    "Da Bolton": "Da Bolton",
    "From Bolton.": "Da Bolton.",
    "A short drive from Bolton": "A pochi minuti in auto da Bolton",
    "Route, drive time and parking.": "Percorso, tempi in auto e parcheggio.",
    "Da Vaughan": "Da Vaughan",
    "From Vaughan.": "Da Vaughan.",
    "For Vaughan and Woodbridge": "Per Vaughan e Woodbridge",
    "Why the drive is worth it, and how long it takes.":
        "Perché vale il viaggio, e quanto ci vuole.",
    "What makes a luxury Italian restaurant different":
        "Cosa distingue un ristorante italiano di alto livello",
    "A room that can hold a conversation": "Una sala dove si può conversare",
    "Dinner, then the lounge": "Prima la cena, poi il lounge",
    "Tuscan, slow, unfashionable, correct.": "Toscana, lenta, fuori moda, giusta.",
    "What to expect": "Cosa aspettarsi",
    "What it costs": "Quanto costa",
    "How to book": "Come prenotare",

    # legal + utility
    "Privacy policy.": "Informativa sulla privacy.",
    "Cookies policy.": "Informativa sui cookie.",
    "Accessibility policy.": "Dichiarazione di accessibilità.",
    "Reservation Terms policy.": "Condizioni di prenotazione.",
    "Gift Card Terms policy.": "Condizioni delle carte regalo.",
    "Terms of Use policy.": "Condizioni d'uso.",
    "Policies and terms for Amami Italia.": "Informative e condizioni di Amami Italia.",
    "This policy is being finalised. For anything urgent, call or email us and we will answer directly.":
        "Questo documento è in fase di completamento. Per qualsiasi urgenza chiamaci o scrivici: rispondiamo direttamente.",
    "Ti Sei Perso?": "Ti Sei Perso?",
    "Lost? Here are the three places people usually want.":
        "Ti sei perso? Ecco i tre posti che cercano quasi tutti.",
    "Open in Google Maps": "Apri in Google Maps",
    "Call 905-794-3366": "Chiama 905-794-3366",
})

# ---------------------------------------------------------------------------
# The remaining English labels — course names on the menus that are not printed
# yet, and a few stragglers.
# ---------------------------------------------------------------------------
IT.update({
    "Dinner": "Cena",
    "Read": "Leggi",
    "Classics": "Classici",
    "Sparkling": "Bollicine",
    "By the glass": "Al bicchiere",
    "Zero proof": "Senza alcol",
    "Mains": "Secondi",
    "Italy by region": "Italia per regione",
    "Trays & platters": "Vassoi e piatti",
    "Trays &amp; platters": "Vassoi e piatti",
    "The sequence": "La sequenza",
    "Signatures": "Signature",
    "Small plates": "Piccoli piatti",
    "Late bites": "Bocconi di fine serata",
    "Sweet": "Dolce",
    "Aperitivi list": "Lista aperitivi",
    "Bianche list": "Lista bianche",
    "Calzoni list": "Lista calzoni",
    "Classics list": "Lista classici",
    "Dolci list": "Lista dolci",
    "Italy by region list": "Lista Italia per regione",
    "Mains list": "Lista secondi",
    "Pasta list": "Lista paste",
    "Rosse list": "Lista rosse",
    "Signatures list": "Lista signature",
    "Sparkling list": "Lista bollicine",
    "The sequence list": "Lista della sequenza",
    "Toscana list": "Lista Toscana",
    "Trays &amp; platters list": "Lista vassoi e piatti",
    "By the glass list": "Lista al bicchiere",
    "Zero proof list": "Lista senza alcol",
    "Dish names, one-line descriptions and prices as HTML text. Awaiting the current list from the kitchen.":
        "Nomi dei piatti, descrizioni di una riga e prezzi come testo HTML. In attesa della lista aggiornata dalla cucina.",
    "The Room": "La Sala",
    "GF": "SG",
    "Gluten free": "Senza glutine",
    "Vegetarian": "Vegetariano",
    "From Italy to Brampton": "Dall'Italia a Brampton",
})

IT.update({
    "1.5 oz": "45 ml", "2 oz": "60 ml", "4 oz": "120 ml", "0.5 oz": "15 ml",
    "12pm – 10pm": "12 – 22", "12pm – 11pm": "12 – 23", "12pm – 9pm": "12 – 21",
    "Porto & Dessert Wine": "Porto e vini da dessert",
    "Porto &amp; Dessert Wine": "Porto e vini da dessert",
    "Chef Gianluca": "Chef Gianluca",
})

# ---------------------------------------------------------------------------
# Nothing left in English (client, 2026-09-01). The words that had been left
# alone because they read the same in both languages now carry real Italian,
# the build notes are translated because they are visible on the pages that are
# still waiting for content, and every page title has an Italian version for
# the browser tab.
# ---------------------------------------------------------------------------
IT.update({
    "Menu": "Menù",
    "Home": "Inizio",
    "After Dark": "A Notte Fonda",
    "Catering": "Fuori Casa",
    "After": "A Notte", "Dark": "Fonda",
    "Raise the": "Alziamo il", "Bar": "Livello",
    "Dining": "Sala",
    "Journal": "Giornale",
    "Visit": "Dove siamo",
    "Amami After Dark": "Amami a Notte Fonda",
    "Il Salotto": "Il Salotto",

    # build notes — visible on the pages still waiting for photography or lists
    "Asset required": "Materiale da fornire",
    "Shoot 1": "Servizio 1", "Shoot 2": "Servizio 2", "Shoot 3": "Servizio 3",
    "Full-bleed landscape.": "Orizzontale a piena pagina.",
    "Full-bleed landscape, evening light.": "Orizzontale a piena pagina, luce serale.",
    "Landscape.": "Orizzontale.",
    "Vertical.": "Verticale.",
    "Supporting image": "Immagine di supporto",
    "To write.": "Da scrivere.",
    "Publish the range.": "Da pubblicare la fascia di prezzo.",
    "One action, stated plainly.": "Un'azione sola, detta chiaramente.",
    "FAQPage schema to be emitted from this list.":
        "Da questa lista va generato lo schema FAQPage.",
    "Working portrait": "Ritratto al lavoro",
    "Press kit": "Cartella stampa",
    "Date night hero": "Immagine principale cena romantica",
    "Corporate dining hero": "Immagine principale cene aziendali",
    "Celebrations hero": "Immagine principale feste",
    "Caledon hero": "Immagine principale Caledon",
    "Bolton hero": "Immagine principale Bolton",
    "Vaughan &amp; Woodbridge hero": "Immagine principale Vaughan e Woodbridge",
    "Vaughan & Woodbridge": "Vaughan e Woodbridge",
    "Vaughan &amp; Woodbridge": "Vaughan e Woodbridge",
    "OpenTable booking widget": "Modulo di prenotazione OpenTable",
    "Embed the OpenTable reservation widget for restRef 1470808.":
        "Inserire il modulo di prenotazione OpenTable per restRef 1470808.",
    "No file for this slot yet.": "Nessun file per questo spazio.",
    "Room at full service.": "La sala in pieno servizio.",
    "Table setting or a held moment.": "La tavola apparecchiata o un momento sospeso.",

    # browser tab
    "Amami Italia — Tuscan Restaurant & Lounge in Brampton":
        "Amami Italia — Ristorante Toscano e Lounge a Brampton",
    "Menu — Tuscan Restaurant in Brampton | Amami Italia":
        "Menù — Ristorante Toscano a Brampton | Amami Italia",
    "Dining Menu — Italian Restaurant in Brampton | Amami Italia":
        "Menù di Sala — Ristorante Italiano a Brampton | Amami Italia",
    "Pizza Menu — Neapolitan Pizza in Brampton | Amami Italia":
        "Menù Pizza — Pizza Napoletana a Brampton | Amami Italia",
    "After Dark Small Plates — Late Night in Brampton | Amami Italia":
        "Piccoli Piatti a Notte Fonda — Brampton | Amami Italia",
    "Wine List — Italian Wine in Brampton | Amami Italia":
        "Carta dei Vini — Vini Italiani a Brampton | Amami Italia",
    "Cocktails & Aperitivo — Lounge in Brampton | Amami Italia":
        "Cocktail e Aperitivo — Lounge a Brampton | Amami Italia",
    "Chef's Tasting Menu — Brampton | Amami Italia":
        "Menù Degustazione dello Chef — Brampton | Amami Italia",
    "Catering Menu — Italian Catering in Brampton | Amami Italia":
        "Menù Fuori Casa — Catering Italiano a Brampton | Amami Italia",
    "Our Story — Tuscan Restaurant in Brampton | Amami Italia":
        "Chi Siamo — Ristorante Toscano a Brampton | Amami Italia",
    "Chef Gianluca Martinucci — Amami Italia, Brampton":
        "Chef Gianluca Martinucci — Amami Italia, Brampton",
    "Amami After Dark — Late Night Lounge in Brampton":
        "Amami a Notte Fonda — Lounge Notturno a Brampton",
    "Catering & Events in Brampton | Amami Italia":
        "Catering ed Eventi a Brampton | Amami Italia",
    "Italian Catering in Brampton & Caledon | Amami Italia":
        "Catering Italiano a Brampton e Caledon | Amami Italia",
    "Visit — Hours, Location & Parking | Amami Italia Brampton":
        "Dove Siamo — Orari, Indirizzo e Parcheggio | Amami Italia Brampton",
    "FAQ — Amami Italia, Brampton": "Domande Frequenti — Amami Italia, Brampton",
    "Contact — Amami Italia, Brampton": "Contatti — Amami Italia, Brampton",
    "Reserve a Table | Amami Italia": "Prenota un Tavolo | Amami Italia",
    "Gift Cards — Amami Italia, Brampton": "Carte Regalo — Amami Italia, Brampton",
    "Journal — Amami Italia, Brampton": "Giornale — Amami Italia, Brampton",
    "Careers — Work at Amami Italia, Brampton":
        "Lavora con Noi — Amami Italia, Brampton",
    "Press & Recognition — Amami Italia, Brampton":
        "Stampa e Riconoscimenti — Amami Italia, Brampton",
    "Date Night in Brampton — Italian Restaurant | Amami Italia":
        "Cena Romantica a Brampton — Ristorante Italiano | Amami Italia",
    "Corporate Dining in Brampton — Private Rooms | Amami Italia":
        "Cene Aziendali a Brampton — Sale Private | Amami Italia",
    "Birthdays & Celebrations in Brampton | Amami Italia":
        "Compleanni e Feste a Brampton | Amami Italia",
    "Italian Restaurant near Caledon | Amami Italia, Brampton":
        "Ristorante Italiano vicino a Caledon | Amami Italia, Brampton",
    "Italian Restaurant near Bolton | Amami Italia, Brampton":
        "Ristorante Italiano vicino a Bolton | Amami Italia, Brampton",
    "Italian Restaurant near Vaughan & Woodbridge | Amami Italia":
        "Ristorante Italiano vicino a Vaughan e Woodbridge | Amami Italia",
    "Page not found | Amami Italia": "Pagina non trovata | Amami Italia",
    "Legal | Amami Italia": "Note Legali | Amami Italia",
    "Book a table at Amami Italia": "Prenota un tavolo da Amami Italia",
})

IT.update({
    # nav labels on the local landing pages, and the legal page titles
    "Tasting Menu": "Menù Degustazione",
    "Celebrations": "Feste",
    "Corporate dining": "Cene aziendali",
    "Date night": "Cena romantica",
    "Privacy | Amami Italia": "Privacy | Amami Italia",
    "Cookies | Amami Italia": "Cookie | Amami Italia",
    "Accessibility | Amami Italia": "Accessibilità | Amami Italia",
    "Reservation Terms | Amami Italia": "Condizioni di prenotazione | Amami Italia",
    "Gift Card Terms | Amami Italia": "Condizioni carte regalo | Amami Italia",
    "Terms of Use | Amami Italia": "Condizioni d'uso | Amami Italia",
    "Chef&#x27;s Tasting Menu — Brampton | Amami Italia":
        "Menù Degustazione dello Chef — Brampton | Amami Italia",
    "Chef's Tasting Menu — Brampton | Amami Italia":
        "Menù Degustazione dello Chef — Brampton | Amami Italia",
    # the address stays as written — it is how the post arrives
})

# ---------------------------------------------------------------------------
# The English loanwords go too, using the Italian names the site already uses
# for itself: the lounge is Il Salotto, catering is Fuori Casa. "Miscelati" is
# what an Italian list calls cocktails, and a signature cocktail is "d'autore".
# ---------------------------------------------------------------------------
IT.update({
    "Tuscan restaurant, lounge & catering in Brampton.":
        "Ristorante toscano, salotto e cucina fuori casa a Brampton.",
    "The Lounge": "Il Salotto",
    "The lounge": "Il salotto",
    "Is the lounge age-restricted?": "Il salotto ha un limite di età?",
    "Dinner, then the lounge": "Prima la cena, poi il salotto",
    "The counter takes twelve. The lounge takes sixty standing, thirty seated. Come for one, stay for the room.":
        "Il bancone tiene dodici persone. Il salotto sessanta in piedi, trenta sedute. Vieni per uno, resta per la sala.",
    "Cocktails, small plates and music once dinner service turns over.":
        "Miscelati, piccoli piatti e musica quando finisce il servizio di cena.",
    "Cocktails": "Miscelati",
    "Aperitivi & Cocktails": "Aperitivi e Miscelati",
    "Aperitivi &amp; Cocktails": "Aperitivi e Miscelati",
    "Signatures": "D'autore",
    "Signatures list": "Lista d'autore",
    "The aperitivo hour, and where the signatures are made.":
        "L'ora dell'aperitivo, e dove nascono i nostri d'autore.",
    "Catering Enquiry": "Richiesta Fuori Casa",
    "Catering enquiry": "Richiesta Fuori Casa",
    "Amami After Dark — Late Night Lounge in Brampton":
        "Amami a Notte Fonda — Il Salotto Notturno a Brampton",
    "Catering Menu — Italian Catering in Brampton | Amami Italia":
        "Menù Fuori Casa — Cucina Italiana a Domicilio a Brampton | Amami Italia",
    "Italian Catering in Brampton & Caledon | Amami Italia":
        "Cucina Italiana Fuori Casa a Brampton e Caledon | Amami Italia",
    "Cocktails & Aperitivo — Lounge in Brampton | Amami Italia":
        "Miscelati e Aperitivo — Il Salotto a Brampton | Amami Italia",
    "Visit — Hours, Location & Parking | Amami Italia Brampton":
        "Dove Siamo — Orari, Indirizzo e Parcheggio | Amami Italia Brampton",
    "Catering & Events in Brampton | Amami Italia":
        "Fuori Casa ed Eventi a Brampton | Amami Italia",
    "Amami Italia — Tuscan Restaurant & Lounge in Brampton":
        "Amami Italia — Ristorante Toscano e Salotto a Brampton",
})

# ---------------------------------------------------------------------------
# The two restored pages. Their copy was written before this generator and
# lives in captured HTML, so it never came through the string extractor —
# these are the strings the switch was leaving in English on /events/ and
# /reservation/.
# ---------------------------------------------------------------------------
IT.update({
    # /events/ — the elastic panels
    "Corporate": "Aziendale",
    "Lunches and year end": "Pranzi di lavoro e fine anno",
    "Weddings": "Matrimoni",
    "Showers, rehearsals, the day": "Addii, prove e il giorno stesso",
    "Either room, closed": "Una delle due sale, in esclusiva",
    "At Your Home": "A Casa Tua",
    "The kitchen, moved": "La cucina, spostata",
    "Holidays": "Feste",
    "Christmas, New Year, Easter": "Natale, Capodanno, Pasqua",
    "Either room, or yours": "La nostra sala, o la tua",
    "Catering & events": "Fuori casa ed eventi",
    "What we cater": "Cosa portiamo in tavola",
    "Open a panel.": "Apri un pannello.",
    "Start an enquiry": "Fai una richiesta",
    "See the catering menu": "Guarda il menù fuori casa",
    "How it actually works": "Come funziona davvero",
    "Tell us the shape of it": "Raccontaci com'è fatta",
    "Date. Headcount. Where. A range is enough to start.":
        "Data. Numero di persone. Dove. Per iniziare basta una stima.",
    "We write a menu for it": "Scriviamo un menù su misura",
    "Written for the room and the season. Change whatever you want.":
        "Scritto per la sala e per la stagione. Cambia quello che vuoi.",
    "We cook it and bring it": "Cuciniamo e portiamo",
    "Delivered hot, or set up and served on site. Notice required: [TBC].":
        "Consegnato caldo, oppure allestito e servito sul posto. Preavviso richiesto: [da definire].",
    "Tell us about your event": "Raccontaci del tuo evento",
    "Date, headcount, where.": "Data, numero di persone, dove.",
    "Your name *": "Il tuo nome *",
    "Email *": "Email *",
    "Phone *": "Telefono *",
    "Type of event": "Tipo di evento",
    "Something else": "Altro",
    "Roughly how many people": "Più o meno quante persone",
    "Where is it": "Dove si tiene",
    "Anything else we should know": "Altro che dovremmo sapere",
    "Or call": "Oppure chiama",
    "or email": "oppure scrivi a",
    "View Menu": "Guarda il menù",
    "VALENTINE’S DAY SPECIAL MENU": "MENÙ SPECIALE DI SAN VALENTINO",

    # /reservation/
    "a table": "un tavolo",
    "Reserve": "Prenota",
    "Tell us when.": "Dicci quando.",
    "Book online": "Prenota online",
    "Every step happens here &mdash; find a table, pick a time, add your details. Eight or more is best arranged by phone.":
        "Ogni passaggio avviene qui &mdash; trova un tavolo, scegli l'ora, inserisci i tuoi dati. Da otto persone in su è meglio per telefono.",
    "Prefer to speak to someone?": "Preferisci parlare con qualcuno?",
    "Before you come": "Prima di venire",
    "Dress": "Come vestirsi",
    "Semi formal for evening service. Collared shirts, dress trousers or an elegant dress.":
        "Semi formale per il servizio serale. Camicia con collo, pantaloni eleganti o un abito elegante.",
    "Timing": "Orari",
    "Tables are held [TBC] minutes. Call if you are running late.":
        "Teniamo il tavolo [da definire] minuti. Chiamaci se sei in ritardo.",
    "Larger tables": "Tavoli grandi",
    "Six or more is best arranged by phone. Gratuity on parties of six or more: [TBC].":
        "Da sei persone in su è meglio per telefono. Servizio per tavoli da sei o più: [da definire].",
    "Fortified, dessert, digestivo and coffee. No table wine. Either room can be booked privately.":
        "Vini liquorosi, da dessert, digestivi e caffè. Nessun vino da tavola. Entrambe le sale si possono prenotare in esclusiva.",
    "The table is ready. The light is right. Nobody is waiting at the door.":
        "Il tavolo è pronto. La luce è quella giusta. Nessuno aspetta alla porta.",
})

# ---------------------------------------------------------------------------
# /events/, rebuilt to the reference in the client's deck.
# ---------------------------------------------------------------------------
IT.update({
    "Events & Private Dining": "Eventi e Sala Privata",
    "Events &amp; Private Dining": "Eventi e Sala Privata",
    "Eventi e Sala Privata": "Eventi e Sala Privata",
    "The Private Room": "La Sala Privata",
    "Fully private, for milestone dinners, corporate tables and celebrations.":
        "Completamente privata, per cene importanti, tavoli aziendali e feste.",
    "The Long Table": "La Tavolata",
    "A single table through the middle of the room, for a party that wants to be seen.":
        "Un unico tavolo nel mezzo della sala, per una tavolata che vuole farsi vedere.",
    "Full Buyout": "Esclusiva Totale",
    "The whole room, dining and lounge, with the kitchen and the bar to yourself.":
        "Tutto il locale, sala e salotto, con la cucina e il bar a disposizione.",
    "seated": "sedute",
    "standing": "in piedi",
    "Up to 120": "Fino a 120",
    "Event enquiry": "Richiesta eventi",
    "Tell us what you are planning": "Raccontaci cosa stai organizzando",
    "Date, headcount and which room, and we will come back to you with what is free and a per-head price.":
        "Data, numero di persone e quale sala: ti diciamo cosa è libero e il prezzo a persona.",
    "Events & Private Dining in Brampton | Amami Italia":
        "Eventi e Sala Privata a Brampton | Amami Italia",
})

IT.update({
    "Make a Reservation": "Prenota un tavolo",
    "Hours of Operation": "Orari di apertura",
    "Reserve now": "Prenota ora",
    "Find a Table": "Trova un tavolo",
    "Eight or more is best arranged by phone &mdash;": "Da otto persone in su è meglio per telefono &mdash;",
    "Eight or more is best arranged by phone —": "Da otto persone in su è meglio per telefono —",
})

IT.update({"Welcome to": "Benvenuti da"})

# ---------------------------------------------------------------------------
# /events/ rebuilt again, to the group-booking reference.
# ---------------------------------------------------------------------------
IT.update({
    "Group Booking &amp; Private Events": "Gruppi ed Eventi Privati",
    "Group Booking & Private Events": "Gruppi ed Eventi Privati",
    "8+ Guests": "Da 8 persone",
    "&amp; Private Events": "ed eventi privati",
    "Event Enquiry": "Richiesta eventi",
    "See the Menus": "Guarda i menù",
    "A corporate table, a birthday, a wedding lunch or the whole room for an evening — the private room seats twenty-two, the long table thirty, and the building holds a hundred and twenty when you take all of it.":
        "Un tavolo aziendale, un compleanno, un pranzo di nozze o tutta la sala per una sera: "
        "la sala privata tiene ventidue persone, la tavolata trenta, e il locale intero "
        "centoventi quando lo prendi tutto.",
    "For groups of eight or more, or a private event, write to": 
        "Per gruppi da otto persone in su, o per un evento privato, scrivi a",
    "or call": "oppure chiama",
    "Capacity": "Capienza",
    "Full Buyout": "Esclusiva Totale",
    "Standing": "In piedi",
    "Seated": "Sedute",
    "Dress Code": "Come vestirsi",
    "Address": "Indirizzo",
    "For press enquiries and media requests, see":
        "Per richieste stampa e materiali per i media, vedi",
    "Events & Private Dining in Brampton | Amami Italia":
        "Gruppi ed Eventi Privati a Brampton | Amami Italia",
})

IT.update({
    "Skip to the content": "Vai al contenuto",
    "Pick a date, a time and a party size and book without leaving the page. Eight or more is best arranged by phone.":
        "Scegli data, ora e numero di persone e prenota senza lasciare la pagina. "
        "Da otto persone in su è meglio per telefono.",
    "Book on OpenTable": "Prenota su OpenTable",
})

IT.update({
    "Every step happens here &mdash; find a table, pick a time, add your details. If the form does not load, book on OpenTable. Eight or more is best arranged by phone.":
        "Ogni passaggio avviene qui — trova un tavolo, scegli l'ora, inserisci i tuoi dati. "
        "Se il modulo non si carica, prenota su OpenTable. Da otto persone in su è meglio per telefono.",
    "Every step happens here — find a table, pick a time, add your details. If the form does not load,":
        "Ogni passaggio avviene qui — trova un tavolo, scegli l'ora, inserisci i tuoi dati. Se il modulo non si carica,",
    "book on OpenTable": "prenota su OpenTable",
    "Eight or more is best arranged by phone.": "Da otto persone in su è meglio per telefono.",
})

# The note is split across text nodes by the inline link, and the annotation
# pass works on the HTML source — so the keys carry the entity, not the glyph.
IT.update({
    "Every step happens here &mdash; find a table, pick a time, add your details. If the form does not load,":
        "Ogni passaggio avviene qui &mdash; trova un tavolo, scegli l'ora, inserisci i tuoi dati. "
        "Se il modulo non si carica,",
    ". Eight or more is best arranged by phone.":
        ". Da otto persone in su è meglio per telefono.",
})

# ---------------------------------------------------------------------------
# Client copy pass, 2026-09-03. Machine-authored like the rest of this file and
# NOT yet read by a native speaker — the English here is very idiomatic ("the
# group chat", "bad ideas", "buon appetito, baby"), so these are the entries
# most likely to need a rewrite before any campaign runs in Italian.
# ---------------------------------------------------------------------------
IT.update({
    # home
    "Dinner looks better in red.": "La cena è più bella in rosso.",
    "Pasta. Vino. Late nights. That’s the plan.":
        "Pasta. Vino. Nottate lunghe. Il piano è questo.",
    "Book a Table": "Prenota un tavolo",
    "See the Menu": "Guarda il menù",
    "The good old days are tonight.": "I bei tempi sono stasera.",
    "The lights are low.": "Le luci sono basse.",
    "The wine is open.": "Il vino è aperto.",
    "The pasta is worth getting sauce on your shirt for.":
        "La pasta vale una macchia di sugo sulla camicia.",
    "Welcome to Amami. Pull up a chair.": "Benvenuti da Amami. Tirate su una sedia.",
    "No shortcuts. Just sauce.": "Niente scorciatoie. Solo sugo.",
    "Fresh pasta. Proper ingredients. The kind of food that makes the table go quiet for a second.":
        "Pasta fresca. Ingredienti veri. Il cibo che fa zittire la tavola per un secondo.",
    "Then everybody starts talking again.": "Poi ricominciano tutti a parlare.",
    "Take a Look at the Menu": "Dai un'occhiata al menù",
    "Come for dinner. Lose track of time.": "Vieni a cena. Perdi il conto delle ore.",
    "Date night, birthday night, Thursday night—it all works here.":
        "Serata romantica, compleanno, giovedì qualunque—qui va bene tutto.",
    "Order the antipasti. Get the pasta. Say yes when someone asks, “Dessert?”":
        "Ordina gli antipasti. Prendi la pasta. Di' di sì quando qualcuno chiede: “Dolce?”",
    "Eat slow. Stay late.": "Mangia piano. Resta fino a tardi.",
    "A little Italy. A lot of amore.": "Un po' d'Italia. Tanto amore.",
    "Your table is waiting.": "Il tuo tavolo ti aspetta.",
    "Bring a date. Bring the group chat. Bring the person who always steals fries.":
        "Porta un appuntamento. Porta la chat di gruppo. Porta quello che ruba sempre le patatine.",
    "Just don’t skip the tiramisu.": "Basta che non salti il tiramisù.",

    # chef
    "Chef Isabella": "Chef Isabella",
    "Meet Chef Isabella. She takes pasta personally.":
        "Ecco la Chef Isabella. La pasta per lei è una cosa personale.",
    "Chef Isabella is the heart of the Amami kitchen.":
        "La Chef Isabella è il cuore della cucina di Amami.",
    "She is here for the handmade pasta, the slow-cooked sauce, the extra parmigiano, "
    "and the kind of dinner people keep talking about on the drive home.":
        "È qui per la pasta fatta a mano, il sugo cotto piano, il parmigiano in più e le "
        "cene di cui si parla ancora in macchina, tornando a casa.",
    "No fuss. No shortcuts. Just Italian food done properly.":
        "Niente storie. Niente scorciatoie. Solo cucina italiana fatta come si deve.",
    "“If you’re not using bread to finish the sauce, we’re not done yet.”":
        "«Se non usi il pane per finire il sugo, non abbiamo ancora finito.»",
    "Meet the Chef": "Conosci la chef",
    "The sauce has a boss.": "Il sugo ha un capo.",
    "From Chef Isabella’s kitchen": "Dalla cucina della Chef Isabella",
    "Cooking with the classics in mind": "Cucina con i classici in mente",
    "Her food is about the things that matter: pasta with bite, sauce with depth, "
    "ingredients that speak for themselves, and plates that make people lean in for "
    "one more forkful.":
        "La sua cucina è fatta di ciò che conta: pasta al dente, sugo con profondità, "
        "ingredienti che parlano da soli e piatti che ti fanno allungare la mano per "
        "un'altra forchettata.",
    "It is comfort food with a little swagger. It is Italian, the way it should "
    "feel—generous, loud, warm, and impossible to leave behind.":
        "È cucina di conforto con un po' di sfrontatezza. È italiana come dovrebbe "
        "essere: generosa, rumorosa, calda e impossibile da lasciare.",
    "She doesn’t rush the sauce. Neither should you.":
        "Lei non ha fretta con il sugo. Nemmeno tu dovresti.",
    "T-bone, aged forty-five days, sold by the kilo. Order it for the table.":
        "Fiorentina, frollata quarantacinque giorni, venduta al chilo. Ordinala per la tavola.",
    "Potato gnocchi, basil pesto, pine nuts, stracciatella on top.":
        "Gnocchi di patate, pesto di basilico, pinoli e stracciatella sopra.",
    "Lamb chops, rosemary and lemon, straight off the grill.":
        "Costolette d'agnello, rosmarino e limone, direttamente dalla griglia.",

    # our story
    "Italian food. Italian energy.": "Cucina italiana. Energia italiana.",
    "No rules—except never leave without dessert.":
        "Nessuna regola—tranne una: non andare via senza dolce.",
    "Amami is for long dinners, loud tables, first dates, family birthdays, and "
    "“let’s just get one drink” that turns into a full evening.":
        "Amami è fatto per le cene lunghe, i tavoli rumorosi, i primi appuntamenti, i "
        "compleanni in famiglia e i “prendiamo solo un bicchiere” che diventano una "
        "serata intera.",
    "We love the classics. We love a dramatic pasta twirl. We love a bottle of red in "
    "the middle of the table.":
        "Amiamo i classici. Amiamo una girata di pasta teatrale. Amiamo una bottiglia "
        "di rosso in mezzo al tavolo.",
    "Most of all, we love the feeling of being somewhere you do not want to leave yet.":
        "Soprattutto, amiamo la sensazione di stare in un posto da cui non vuoi ancora "
        "andartene.",
    "A table worth staying at.": "Un tavolo per cui vale la pena restare.",
    "Italian food has always known the secret: eat slowly, pour generously, and make "
    "room for one more.":
        "La cucina italiana conosce il segreto da sempre: mangia piano, versa "
        "generosamente e fai posto a un altro.",
    "That is Amami.": "Questo è Amami.",

    # menu
    "The Menu": "Il Menù",
    "Order like you mean it.": "Ordina con convinzione.",
    "Start with something to share. End with something sweet. Somewhere in the middle, "
    "have the pasta.":
        "Comincia con qualcosa da dividere. Finisci con qualcosa di dolce. Nel mezzo, "
        "prendi la pasta.",
    "Everything here is made for the middle of the table.":
        "Qui è tutto pensato per il centro della tavola.",
    "Go ahead—order too much. That is the Italian way.":
        "Vai pure—ordina troppo. È il modo italiano.",
    "Not up yet. Call and we’ll tell you what’s on.":
        "Non ancora online. Chiama e ti diciamo cosa c'è.",
    "Go on. Order another plate.": "Dai. Ordina un altro piatto.",
    "Nobody ever remembers the night they played it safe.":
        "Nessuno si ricorda la sera in cui è andato sul sicuro.",
    "This list isn’t up yet. Call 905-794-3366 and we’ll read it to you.":
        "Questa lista non è ancora online. Chiama il 905-794-3366 e te la leggiamo noi.",
    "Hungry yet?": "Ti è venuta fame?",
    "Start here": "Si comincia",
    "A little something before the main event.": "Qualcosina prima dell'evento principale.",
    "The pasta": "La pasta",
    "Twirl first. Talk later.": "Prima arrotola. Poi parla.",
    "The main thing": "Il piatto forte",
    "Big flavours. Clean plates. All served with grilled seasonal vegetables and "
    "fingerling potatoes.":
        "Sapori decisi. Piatti puliti. Tutti serviti con verdure di stagione grigliate "
        "e patate novelle.",
    "Sweet talk": "Parole dolci",
    "You were always going to order dessert.": "Il dolce lo avresti ordinato comunque.",
    "A good idea in a bottle.": "Una buona idea in bottiglia.",
    "Lunch and dinner, from noon until we close.":
        "Pranzo e cena, da mezzogiorno fino alla chiusura.",

    # events
    "Make a night of it.": "Fanne una serata.",
    "Birthdays. Engagements. Work wins.": "Compleanni. Fidanzamenti. Vittorie di lavoro.",
    "Or just a very serious excuse to eat pasta with your favourite people.":
        "O solo una scusa molto seria per mangiare pasta con le persone che preferisci.",
    "At Amami, celebrations are best served family-style.":
        "Da Amami, le feste si servono meglio in stile famiglia.",
    "Bring the guest list. Bring the good outfit. Bring a reason to toast.":
        "Porta la lista degli invitati. Porta il vestito bello. Porta un motivo per brindare.",
    "We will bring the food, the wine, and the kind of table people do not want to leave.":
        "Noi portiamo il cibo, il vino e il tipo di tavolo da cui nessuno vuole alzarsi.",
    "Eight or more, or anything private — write to":
        "Da otto persone in su, o per qualcosa di privato — scrivi a",
    "Plan Your Party": "Organizza la tua festa",
    "Plan your party": "Organizza la tua festa",
    "You invite them. We feed them.": "Tu li inviti. Noi li sfamiamo.",
    "Tell us what you’re planning": "Raccontaci cosa stai organizzando",
    "Give us the date, how many, and which room. We’ll come back with what’s free and "
    "a price per head.":
        "Dacci la data, quante persone e quale sala. Ti diciamo cosa è libero e il "
        "prezzo a testa.",
    "We answer within a business day.": "Rispondiamo entro un giorno lavorativo.",

    # contact, visit, faq
    "Ciao, bella.": "Ciao, bella.",
    "Find us. Call us. Come hungry.": "Trovaci. Chiamaci. Vieni affamato.",
    "Got a question? Planning something special? Need to know if there is room for one more?":
        "Hai una domanda? Stai organizzando qualcosa di speciale? Vuoi sapere se c'è "
        "posto per un altro?",
    "Send us a note.": "Scrivici due righe.",
    "Things people ask us.": "Le domande che ci fanno.",
    "Come and find us. Mayfield Road, top end of Brampton.":
        "Vieni a trovarci. Mayfield Road, all'estremità nord di Brampton.",

    # reservation (the restored page)
    "Save your seat.": "Prenota il tuo posto.",
    "We’ll save the good table.": "Noi teniamo il tavolo buono.",
    "Dinner plans look good on you.": "I programmi per cena ti stanno bene.",
    "Book ahead for date nights, birthdays, family dinners, or any night that needs "
    "pasta and a glass of something red.":
        "Prenota in anticipo per le serate romantiche, i compleanni, le cene di "
        "famiglia o qualsiasi sera che chieda pasta e un bicchiere di rosso.",
    "Arrive hungry. We’ll handle the rest.": "Arriva affamato. Al resto pensiamo noi.",
    "More people. More pasta. More fun.": "Più gente. Più pasta. Più divertimento.",
    "Groups": "Gruppi",
    "Bringing the whole crew? Get in touch for group dining and celebrations.":
        "Porti tutta la compagnia? Scrivici per cene di gruppo e feste.",
})

# ---------------------------------------------------------------------------
# Second copy pass, 2026-09-04 — the lines that were still house copy, rewritten
# plainer and more playful, plus the six landing pages that had been showing
# briefs. Machine-authored; still wants a native read.
# ---------------------------------------------------------------------------
IT.update({
    # our story
    "Tuscan food doesn’t show off. Bread, beans, good oil, and nobody trying to "
    "impress you. That’s the cooking this kitchen came out of.":
        "Il cibo toscano non fa scena. Pane, fagioli, olio buono e nessuno che cerca di "
        "impressionarti. Da lì viene la cucina di questo posto.",
    "How it gets made": "Come si fa",
    "Nobody learns this out of a book. You learn it standing next to someone who already "
    "knows. Pasta gets rolled here in the morning. The sauce goes on before the doors open.":
        "Queste cose non si imparano dai libri. Si imparano accanto a chi le sa già fare. "
        "La pasta si tira qui la mattina. Il sugo va sul fuoco prima che apriamo.",
    "Two of you on a Tuesday. Twenty of you on a Saturday. Same room, same welcome. It "
    "gets loud, and that’s the idea. Caledon and Vaughan are ten minutes up the road.":
        "In due un martedì. In venti un sabato. Stessa sala, stessa accoglienza. Si alza "
        "la voce, ed è quello il bello. Caledon e Vaughan sono a dieci minuti.",

    # chef
    "Comfort food with a little swagger. Three she gets asked about most.":
        "Cucina di conforto con un po' di sfrontatezza. I tre che le chiedono di più.",

    # after dark
    "Dinner finishes and nobody asks you to leave. Forty-three things to drink once the "
    "plates are gone &mdash; port, amari, grappa, and coffee with something in it.":
        "La cena finisce e nessuno ti manda via. Quarantatré cose da bere quando i piatti "
        "sono spariti &mdash; porto, amari, grappa e caffè con dentro qualcosa.",
    "Twelve seats at the counter. Sixty standing in the lounge, thirty sitting down. "
    "Come in for one and see how it goes.":
        "Dodici posti al banco. Sessanta in piedi nel salotto, trenta seduti. Entra per "
        "uno e vedi come va.",
    "Once dinner turns over, this is where it carries on. Music up, plates smaller.":
        "Quando la cena finisce, si continua qui. Musica su, piatti più piccoli.",
    "Twelve seats, no reservation. Sit here if you’re early, or on your own.":
        "Dodici posti, senza prenotazione. Siediti qui se sei in anticipo, o da solo.",
    "Taking the room for the night? Send us the date and how many of you there are.":
        "Vuoi la sala per la serata? Mandaci la data e quanti siete.",

    # faq
    "Yes. Book online or ring us. Walk in and we’ll do what we can.":
        "Sì. Prenota online o chiamaci. Se entri senza prenotare, facciamo il possibile.",
    "Free, right outside.": "Gratuito, proprio davanti.",
    "Yes. Tell us when you book, then tell your server again when you sit down.":
        "Sì. Dillo quando prenoti, poi ripetilo al cameriere quando ti siedi.",
    "The degustazione, yes. It needs notice, so call ahead.":
        "La degustazione, sì. Serve preavviso, quindi chiama prima.",
    "Call and ask — 905-794-3366. We’ll give you a straight answer.":
        "Chiama e chiedi — 905-794-3366. Ti diamo una risposta chiara.",
    "Yes. A hundred and twenty of you if you take the lot.":
        "Sì. Centoventi persone se prendete tutto.",

    # visit
    "Free, right outside the door.": "Gratuito, proprio davanti alla porta.",
    "Getting in": "L'accesso",
    "Step-free entry and an accessible washroom.":
        "Ingresso senza gradini e bagno accessibile.",
    "Getting here": "Come arrivare",
    "We’re on Mayfield at the top of Brampton. Caledon, Bolton and Vaughan are all a "
    "short drive.":
        "Siamo su Mayfield, in cima a Brampton. Caledon, Bolton e Vaughan sono tutte a "
        "pochi minuti di macchina.",

    # 404 + legal
    "It happens. Here’s the menu, a table, and how to find us.":
        "Capita. Ecco il menù, un tavolo e come trovarci.",
    "Still being written. If you need an answer now, call":
        "Ancora in scrittura. Se ti serve una risposta subito, chiama",

    # gift cards, journal, careers
    "Give somebody dinner. Hard to wrap, easy to spend.":
        "Regala una cena. Difficile da incartare, facile da spendere.",
    "Notes. Some about food, some about Brampton.":
        "Appunti. Qualcuno sul cibo, qualcuno su Brampton.",
    "If you can cook, or carry four plates without looking at them, come and talk to us.":
        "Se sai cucinare, o portare quattro piatti senza guardarli, vieni a parlarci.",

    # landing pages
    "An evening for two, and nobody rushing you.":
        "Una serata per due, e nessuno che vi mette fretta.",
    "Get a booth. Order the burrata. Take your time over the pasta. When the plates go "
    "you don’t have to — the lounge is the same room, later.":
        "Prendete un séparé. Ordinate la burrata. Con la pasta, con calma. Quando "
        "portano via i piatti non dovete andarvene — il salotto è la stessa sala, più tardi.",
    "What to expect": "Cosa aspettarsi",
    "Low light, a booth if we’ve got one, and no one hurrying you out.":
        "Luci basse, un séparé se ne abbiamo uno libero, e nessuno che vi manda via.",
    "What it costs": "Quanto costa",
    "Pasta from $28, secondi from $38. Dessert is not optional.":
        "Pasta da 28 $, secondi da 38 $. Il dolce non è facoltativo.",
    "How to book": "Come prenotare",
    "Book online, or call 905-794-3366.": "Prenota online, o chiama il 905-794-3366.",
    "Dinner where people can actually hear each other.":
        "Una cena in cui ci si sente parlare.",
    "The private room takes sixteen to twenty-two with the door shut. Ask for a set menu "
    "if you want the bill known before anyone orders. Give us a few days and it’s easier "
    "on everybody.":
        "La sala privata tiene da sedici a ventidue persone a porta chiusa. Chiedi un menù "
        "fisso se vuoi sapere il conto prima che qualcuno ordini. Dacci qualche giorno ed "
        "è più semplice per tutti.",
    "A door that closes. Sixteen to twenty-two seated.":
        "Una porta che si chiude. Da sedici a ventidue seduti.",
    "Set menus are quoted per head. Tell us the budget and we’ll build to it.":
        "I menù fissi si quotano a persona. Dicci il budget e lo costruiamo su quello.",
    "Send an event enquiry, or call 905-794-3366.":
        "Manda una richiesta per eventi, o chiama il 905-794-3366.",
    "Get everyone in one room.": "Tutti quanti in una sala sola.",
    "Birthdays, anniversaries, christenings, whatever you’re marking. Twenty-two in the "
    "private room. Thirty down the long table. A hundred and twenty if you take the "
    "whole building.":
        "Compleanni, anniversari, battesimi, qualunque cosa festeggiate. Ventidue nella "
        "sala privata. Trenta al tavolo lungo. Centoventi se prendete tutto il locale.",
    "Family-style if you want it. Loud either way.":
        "Alla familiare, se volete. Rumoroso in ogni caso.",
    "Gratuity": "Servizio",
    "18% is added automatically for six or more.":
        "Il 18% viene aggiunto automaticamente da sei persone in su.",
    "Down the hill from Caledon.": "Giù dalla collina di Caledon.",
    "We’re on Mayfield Road at the top end of Brampton, which puts us on the Caledon side "
    "of the city. Park outside, free, and walk straight in.":
        "Siamo su Mayfield Road, all'estremità nord di Brampton, quindi dalla parte di "
        "Caledon. Parcheggi fuori, gratis, ed entri.",
    "Where we are": "Dove siamo",
    "6261 Mayfield Rd, #140. Free parking outside.":
        "6261 Mayfield Rd, #140. Parcheggio gratuito davanti.",
    "When we’re open": "Quando siamo aperti",
    "Tuesday to Sunday from noon. Closed Mondays.":
        "Da martedì a domenica da mezzogiorno. Lunedì chiuso.",
    "A short run from Bolton.": "A due passi da Bolton.",
    "Mayfield Road, straight across the top of Brampton. Free parking when you get here, "
    "which is not nothing on a Friday.":
        "Mayfield Road, dritto lungo il bordo nord di Brampton. Parcheggio gratuito "
        "quando arrivi, che di venerdì non è poco.",
    "Worth the drive from Vaughan and Woodbridge.":
        "Vale il viaggio da Vaughan e Woodbridge.",
    "West along Mayfield and you’re here. Free parking, and you won’t be circling the "
    "block looking for it.":
        "Verso ovest su Mayfield e sei arrivato. Parcheggio gratuito, senza girare "
        "l'isolato per cercarlo.",

    # menu band
    "Everything here is made for the middle of the table. Go ahead—order too much. That "
    "is the Italian way.":
        "Qui è tutto pensato per il centro della tavola. Vai pure—ordina troppo. È il "
        "modo italiano.",
    "or write to": "o scrivi a",
})

# Hard cut, 2026-09-04 — shorter lines, same meaning.
IT.update({
    '18% for six or more.':
        '18% da sei persone in su.',
    'A Tuscan town with the wall still round it. Bread, beans, good oil.':
        'Una città toscana con le mura ancora intorno. Pane, fagioli, olio buono.',
    'A door that closes.':
        'Una porta che si chiude.',
    'Aperitivo, and after.':
        'Aperitivo, e dopo.',
    'Call and ask — 905-794-3366.':
        'Chiama e chiedi — 905-794-3366.',
    'Celebrations are best served family-style.':
        'Le feste vengono meglio servite alla familiare.',
    'Date, how many, which room.':
        'Data, quante persone, quale sala.',
    'Dinner finishes and nobody asks you to leave.':
        'La cena finisce e nessuno ti manda via.',
    'Eat slowly. Pour generously. Make room for one more.':
        'Mangia piano. Versa generosamente. Fai posto a un altro.',
    'Event enquiry, or 905-794-3366.':
        'Richiesta eventi, o 905-794-3366.',
    'Family-style. Loud either way.':
        'Alla familiare. Rumoroso in ogni caso.',
    'Forty-five days, by the kilo.':
        'Quarantacinque giorni, al chilo.',
    'Forty-three things to drink. Twelve seats at the counter.':
        'Quarantatré cose da bere. Dodici posti al banco.',
    'Get a booth. Order the burrata. Stay for the lounge.':
        'Prendete un séparé. Ordinate la burrata. Restate per il salotto.',
    'Hard to wrap. Easy to spend.':
        'Difficile da incartare. Facile da spendere.',
    'If you can cook, come and talk to us.':
        'Se sai cucinare, vieni a parlarci.',
    'Isabella’s run. Needs notice.':
        'La sequenza di Isabella. Serve preavviso.',
    'Long dinners, loud tables, first dates, family birthdays, and “let’s just get one drink” that turns into a full evening.':
        'Cene lunghe, tavoli rumorosi, primi appuntamenti, compleanni in famiglia e i “prendiamo solo un bicchiere” che diventano una serata intera.',
    'Low light. Nobody hurrying you.':
        'Luci basse. Nessuno che vi mette fretta.',
    'Mayfield Road, straight across the top of Brampton. Free parking.':
        'Mayfield Road, dritto lungo il bordo nord di Brampton. Parcheggio gratuito.',
    'Mayfield Road, the Caledon side of Brampton. Park outside, free.':
        'Mayfield Road, dal lato Caledon di Brampton. Parcheggi fuori, gratis.',
    'Mayfield, top of Brampton. Caledon, Bolton and Vaughan are a short drive.':
        'Mayfield, in cima a Brampton. Caledon, Bolton e Vaughan sono a pochi minuti.',
    'Music up, plates smaller.':
        'Musica su, piatti più piccoli.',
    'Nobody remembers the night they played it safe.':
        'Nessuno si ricorda la sera in cui è andato sul sicuro.',
    'Not up yet. Call and ask.':
        'Non ancora online. Chiama e chiedi.',
    'Online, or 905-794-3366.':
        'Online, o 905-794-3366.',
    'Our people come with it.':
        'I nostri vengono con il cibo.',
    'Out of the oven.':
        'Dal forno.',
    'Out the door.':
        'Fuori porta.',
    'Pasta from $28, secondi from $38.':
        'Pasta da 28 $, secondi da 38 $.',
    'Pasta rolled in the morning. Sauce on before we open.':
        'Pasta tirata la mattina. Sugo sul fuoco prima di aprire.',
    'Pesto, pine nuts, stracciatella.':
        'Pesto, pinoli, stracciatella.',
    'Port, amari, grappa. Coffee with something in it.':
        'Porto, amari, grappa. Caffè con dentro qualcosa.',
    'Rosemary, lemon, off the grill.':
        'Rosmarino, limone, dalla griglia.',
    'Set menus, per head.':
        'Menù fissi, a persona.',
    'Sixteen to twenty-two, with the door shut. Set menus if you want the bill known first.':
        'Da sedici a ventidue, a porta chiusa. Menù fissi se vuoi sapere il conto prima.',
    'Taking the room for the night? Send us the date.':
        'Vuoi la sala per la serata? Mandaci la data.',
    'The degustazione. It needs notice.':
        'La degustazione. Serve preavviso.',
    'The room':
        'La sala',
    'Thirty-two dishes. The steaks are aged 45 days, sold by the kilo.':
        'Trentadue piatti. Le bistecche sono frollate 45 giorni, vendute al chilo.',
    'Trays and platters, delivered.':
        'Vassoi e piatti, consegnati.',
    'Tuesday to Sunday from noon.':
        'Da martedì a domenica da mezzogiorno.',
    'Tuscany first.':
        'Prima la Toscana.',
    'Twelve seats, no reservation.':
        'Dodici posti, senza prenotazione.',
    'Twenty-two in the private room. Thirty at the long table. A hundred and twenty if you take the building.':
        'Ventidue nella sala privata. Trenta al tavolo lungo. Centoventi se prendete tutto il locale.',
    'Two on a Tuesday. Twenty on a Saturday. It gets loud.':
        'In due un martedì. In venti un sabato. Si alza la voce.',
    'West along Mayfield and you’re here. Free parking.':
        'Verso ovest su Mayfield e sei arrivato. Parcheggio gratuito.',
    'Yes. A hundred and twenty if you take the lot.':
        'Sì. Centoventi se prendete tutto.',
    'Yes. Online or by phone.':
        'Sì. Online o per telefono.',
    'Yes. Tell us when you book, and again at the table.':
        'Sì. Dillo quando prenoti, e di nuovo al tavolo.',
})

# Reservation page, 2026-09-04 — the one page the copy passes had missed.
IT.update({
    "Not loading?": "Non si carica?",
    ". Eight or more, call us.": ". Da otto persone in su, chiamaci.",
    "Bringing the whole crew?": "Porti tutta la compagnia?",
    "Semi formal in the evening. Collared shirt and trousers, or a dress.":
        "Semi formale la sera. Camicia con collo e pantaloni, o un abito.",
    "Running late": "In ritardo",
    "Call us.": "Chiamaci.",
    "Six or more, call. Gratuity of 18% applies.":
        "Da sei persone in su, chiama. Si applica il 18% di servizio.",
    "Port, amaro, grappa, coffee. No table wine.":
        "Porto, amaro, grappa, caffè. Niente vino da tavola.",
})

IT.update({
    "Pull up a chair.": "Tirati su una sedia.",
    "Dinner’s ready when you are.": "La cena è pronta quando lo sei tu.",
    "Come hungry.": "Vieni affamato.",
})
