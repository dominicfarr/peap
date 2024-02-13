import calendar
import re


class TD:
    __match_rule = {
        "pattern": "TD®Aeroplan®Visa Infinite",
        "label": "TD Aeroplan Visa",
        "class": "TD",
    }

    def __init__(self):
        super(TD, self).__init__()
        self.statement_period = TD_Statement_Period()
        self.td_row_extractor = TD_Row_Extractor()

    def is_match(self, test_value=""):
        pattern = self.__match_rule.get("pattern", "")
        return pattern

    def process(self, pdf_file, reader, results_callback, dlq_callback):
        statement_period = self.statement_period.get_statement_period(
            reader.pages[0].extract_text()
        )

        if statement_period is not None:
            for page in reader.pages:
                extracted_text = page.extract_text()
                rows = self.td_row_extractor.extract(extracted_text, statement_period)

                for row in rows:
                    results_callback(*row, self._category(row[2]))
                
        else:
            dlq_callback(pdf_file, "TD Processor failed to find a statement period")

    def _category(self, text=""):
        if self._find(
            [
                "SMIGGLE",
                "UNIQLO",
                "TELZE",
                "THEDECKBOXHALIFAX",
                "GUYSFRENCHYS",
                "DOLLARAMA",
                "REDBUBBLE.COM",
                "HUDSON ST1961",
                "SPORTS EXPERTS",
                "BOUTIQUE ARTDEVIVRE",
                "THEHALIFAX WATCH CO.",
                "TOYSRUSONLINE",
                "SARAH&TOM",
                "GAPCANADA",
                "MOUNTAIN WAREHOUSE",
                "BRILLIANTE",
                "NATURE FOLKWELLNESS",
                "sportchek",
                "Amazon.ca",
                "AMZNMktpCA",
                "SHEIN",
                "SHOWCASE",
                "LUSH",
                "GAMESTOP",
                "IKEA",
                "LAWRENCETOWN CANDLE",
                "TWIGGZ",
                "OLDNAVY",
                "MainShopLuga",
                "FREAKLUNCHBOX",
                "SWEETJANE'SGIFTS",
                "ARDENE",
                "LONG&MCQUADE",
                "THEENTERTAINER",
                "MARKS&SPENCER",
                "ZARA",
                "HMHennes",
                "COLES"
            ],
            text,
        ):
            return "Shopping"
        if self._find(["ymca", "WAEGWOLTIC", "EASTPEAKCLIMBING"], text):
            return "Clubs"
        if self._find(["nsltdhalifax"], text):
            return "Shopping."
        if self._find([ "NSLC"], text):
            return "Alcohol"
        if self._find(
            [
                "UNIVERSAL PROPERTY MANAGE",
                "STATIONNEMENT CENTRE-VILL",
                "STEELE MITSUBISHI",
                "SHELLC",
                "PETROCANADA",
                "SPAEASTMAN EASTMAN",
                "ESSO",
                "GWRLONDPADDSSTPADDINGTON",
                "UBR*PENDING.UBER.COM LONDON",
                "SIXT",
                "BPFLYOVER F/STNLONDON",
                "aircan",
                "HALIFAX INTLAIRPORT",
                "UBER*TRIP",
                "TFLTRAVEL",
                "LIM*1RIDES",
                "SWISSINTERN",
                "SWISSAIRLIN",
                "UBERTRIP",
                "Lagardere Fil.217Frankfurt",
                "AlnaturaProduktions u.Frankfurt am",
                "MEYER FEINKOST GMBHFRANKFURT",
                "MORIKI TOGOFRANKFURT AM",
                "SOFITEL FRANKFURT OPERFRANKFURT",
                "MORIKI TOGOFRANKFURT AM",
                "CASUALFOOD FLUGHAFEN FRFrankfurt",
                "Heinemann DutyFree/Fil.3 Frankfurt",
                "INTERCONTI BANQUETIN STJULIANS",
                "OPALLOUNGE STJULIANS",
                "NTERCONTI FRONTOFFSTJULIANS", 
                "GWRSWINDON",
                "LONDON TOURIST GUIDEShadwell",
                "DEUTSCHE LUF",
                "trainline",
                "CHELTENHAM BOROUGH COUNCI"              
            ],
            text,
        ):
            return "Travel"
        if self._find(
            ["Apple", "AmazonChannels", "PARAMOUNT PLUS", "VIACOMCBS STREAMING","TICKETMASTER", "CINEPLEX", "THECAMBRIDGE THEATRE", "LWTheatresGroupLimitedLondon", "CAMBRIDGE THEATRE LONDON"], text
        ):
            return "Entertainment"
        if self._find(
            [
                "NOGGINS ONCOBURG ",
                "ASDASTORES",
                "CO-OPERATIVE FOOD",
                "SAINSBURYS",
                "COOPOURRETAIL",
                "TESCOSTORES",
                "PETE'SDRESDEN",
                "SOBEYS",
                "ATLANTIC SUPERSTORE",
                "SUPERSTORE",
                "WAL-MART",
                "ORGANIC EARTHMARKET",
                "HENNIGAR'S FARMMARKET",
                "SUPERSTOR",
                "WMMORRISONS",
                "CO-OPGROUP",
                "SPARHATHERLEY",
                "SMITHMANN",
                "INTERCONTINENTAL FOODAND"     ,
                "NISALOCAL"    ,
                "LIDLGB"    ,
                "WMMORRISONS",
                "GETAWAY FARMERS &BUTCBEDFORD",
                "BULKBARN"
            ],
            text,
        ):
            return "Groceries"
        if self._find(["INSURANCE", "SIMPLY BUSINESS INS"], text):
            return "Insurance"
        if self._find(["KOODO", "AIRALO", "MOBILE MASTER"], text):
            return "Phone"
        if self._find(
            [
                "CAFFENEROWHITECITYWESLONDON",
                "WAGAMAMA",
                "UDDERLICIOUS LLondon"
                "LEAFWILD UXBRIDGE",
                "131THEPROMENADE CHELTENHAM",
                "CURIOUS CAFE",
                "WAFFLE Cheltenham",
                "THEBELLINN",
                "HEYDARI",
                "RISE&VINE",
                "THEROYALCHELTENHAM",
                "Dominos",
                "BlackGoldCafe",
                "LAKESIDE TAKEAWAY",
                "Garrison Brewing",
                "CINNABON",
                "JUGOJUICE",
                "VILLAMADINA",
                "Subway",
                "KINGOFDONAIR",
                "WHSmithHeathrow",
                "WHSMITH",
                "GWRFOODONTRAINSWINDON",
                "STARBUCKS",
                "MORTY BOBSLTDLondon",
                "OliviaPizzaLondon&BeiLondon",
                "PRETAMANGER",
                "Crussh9",
                "Tonkotsu",
                "MCDONALDS",
                "GAILS",
                "LAVELI BAKERY",
                "NICOBAKES",
                "WILDLEEK",
                "THAIEXPRESS",
                "INDOCHINE BANHMI",
                "CABINCOFFEE",
                "CIRCLE K/IRVING",
                "TRIPLEAAAPIZZAANDGROC",
                "BUBBLE TEAEMPORIUM",
                "TIMHORTONS",
                "SUGARBAKERY",
                "TURBOCHICKEN",
                "SILVER DRAGON",
                "PRETZELMAKER",
                "CHABAATHAI",
                "SUMUP*MILAN MEHTA HARROW",
                "SUSHINAMIROYALE",
                "HARDROCKCAFEMIALUQA",
                "ARDMORE TEAROOM",
                "FRESHLY SQUEEZED",
                "BOBAR",
                "BISTROT INTDORVAL",
                "NOODLE NAMI",
                "KANPAI IZAKAYA",
                "BrewDog Soho",
                "CAYTRESOHO",
                "WWW.TAKEAWAY.JE 01534876163",
                "T4LONDON",
                "NYX*PGGroup"
            ],
            text,
        ):
            return "Eating out"
        if self._find(["HOTSPOT", "IMPARK"], text):
            return "Parking"
        if self._find(
            [
                "PrimeMemberamazon",
                "STARTBOOTSTRAP",
                "NOVORESUME",
                "GODADDY",
                "GoogleStorageLondon",
                "GooglePlay",
                "OPENAI",
                "CHATGPT",
                "ZETTLE_*CHELTENHAM TAX50",
                "AmazonWebServices",
            ],
            text,
        ):
            return "Online Services"
        if self._find(["FAIRVIEW ANIMAL HOSPIT", "PETSMART"], text):
            return "Dog"
        if self._find(
            ["LAWTONS", "WINDWOOD", "SHOPPERS DRUGMART", "LAWEN DENTISTRY", "JVPHARMACY","BOOTS,CHELTENHAM", "HANDNBARBER"], text
        ):
            return "Medical"
        if self._find(
            [
                "ATLANTIC PHOTOSUPPLY",
                "BANHAM",
                "ASHLEY FURNITURE",
                "KENTHALIFAX",
                "CANADIAN TIRE",
                "CDNTIRESTORE",
                "CDNTIRE",
                "THEUPSSTOREHALIFAX",
                "DELS(UK)LIMITED LONDON"
            ],
            text,
        ):
            return "Household"
        if self._find(["RoyalBritishLegionLondon"], text):
            return "Charity"
        if self._find(["HEATING ENGINEERS PINNER", "PIMLICO PLUMBERS LTD"], text):
            return "Vespan"
        else:
            return "uncategorised"

    def _find(self, matches, text):
        for m in matches:
            if text.lower().find(m.lower()) != -1:
                return True
        return False


class TD_Statement_Period:
    __statement_pattern = r"STATEMENT PERIOD: (.*)"
    __data_pattern = r"([A-Z][a-z]+)(\d{2}),(\d{4})to([A-Z][a-z]+)(\d{2}),(\d{4})"

    def __init__(self, *args, **kwargs):
        super(TD_Statement_Period, self).__init__(*args, **kwargs)

    def get_statement_period(self, lines):
        match = re.search(self.__statement_pattern, lines)

        if match is None:
            return None

        extract = match[1].strip().replace(" ", "")

        date_match = re.search(self.__data_pattern, extract)
        if date_match is None:
            return None

        start_date = f"{date_match[3]}-{date_match[1]}-{date_match[2]}"
        end_date = f"{date_match[6]}-{date_match[4]}-{date_match[5]}"

        return {
            "start": start_date,
            "end": end_date,
            "is_rollover": lambda: start_date[:4] != end_date[:4],
        }


class TD_Row_Extractor:
    __pattern = r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC).*"

    def __init__(self, *args, **kwargs):
        super(TD_Row_Extractor, self).__init__(*args, **kwargs)

    def extract(self, raw_extracted_txt, statement_period):
        transaction_rows = [
            line
            for line in raw_extracted_txt.splitlines()
            if re.match(self.__pattern, line)
        ]

        return [self._standardise(row, statement_period) for row in transaction_rows]

    def _standardise(self, line, statement_period):
        pattern = r"^(JAN).*"
        year = (
            statement_period.get("end")[:4]
            if statement_period["is_rollover"]() and re.match(pattern, line)
            else statement_period.get("start")[:4]
        )

        items = line.split(" ")
        if re.match(r"([A-Z]{3}\d+[A-Z]{3}\d+)", line) is not None:
            amount = line.split(" ")[1]
            desc = " ".join(items[2:])
        else:
            amount = line.split(" ")[2]
            desc = " ".join(items[3:])

        date = self._format_date(items[0], year)

        return date, amount, desc

    def _format_line_with_date(self, items, year, amount, desc):
        return f"{self._format_date(items[0], year)}|{amount}|{desc}"

    def _format_date(self, date, year):
        pattern = r"([a-zA-Z]+)(\d+)"

        match = re.search(pattern, date)
        index = str(list(calendar.month_abbr).index(match[1].title()))

        return f"{year}-{index.zfill(2)}-{match[2].zfill(2)}"
