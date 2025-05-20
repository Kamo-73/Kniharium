import requests
import random
from urllib.parse import quote

# Fallback biog - male
FALLBACK_BIO_MALE = [
    "Autor začal písať už v desiatich rokoch, keď vznikli prvé básne inšpirované prírodou a rodinným prostredím, v ktorom vyrastal. Básnické obrazy sa často viazali na zmeny ročných období a melancholickú atmosféru jesene, ktorá sa neskôr stala aj symbolickým rámcom mnohých próz. Postupne sa jeho tvorba prirodzene presunula k písaniu príbehov, no poézia nikdy úplne nezmizla – ostala prítomná v jazyku, rytme aj v symbolike. V mladosti ho výrazne ovplyvnil Stephen King, čo sa odrazilo na temnejších prvkoch v niektorých poviedkach a románoch. Fascinácia strachom, vnútorným napätím a nevysvetliteľnými javmi pretrváva dodnes. Autor verí, že najlepší príbeh je ten, ktorý sa dotkne niečoho osobného, aj keď ho čítateľ zažije v úplne inom svete.",
    "Literárna cesta autora sa začala počas dlhých letných prázdnin na dedine, kde prístup k technológiám bol minimálny a knihy nahrádzali televíziu aj internet. V tom tichu a spomalenom čase vznikla potreba tvoriť – najprv formou denníkov, neskôr ako eseje plné otázok o identite, spoločnosti a zmysle bytia. Tie sa neskôr premenili na psychologické romány, v ktorých sa čitateľ ponára do vnútorného sveta postáv – ich myšlienok, pochybností, spomienok. Témy ako strata, čas, ticho, izolácia či návrat domov sú pre autora charakteristické. Silný vplyv má aj klasická literatúra – najmä Dostojevskij a Kafka – no autor si vybudoval vlastný štýl, ktorý sa vyznačuje introspektívnym tónom a presnosťou výrazu.",
    "Autor sa dlhé roky venoval divadlu a filmovej tvorbe, pričom pôsobil ako dramaturg aj scenárista. Práca s dramatickou štruktúrou a vizuálnym vyjadrovaním sa výrazne odrazila v jeho knihách – dialógy sú živé, dej má napätie a mnohé scény sa čitateľovi doslova premietajú pred očami. Literatúru objavil ako prostriedok, kde môže naplno vyjadriť myšlienky bez produkčných obmedzení. Jeho tvorba často balansuje medzi realitou a snovým svetom – autor verí, že skutočný príbeh sa odohráva medzi tým, čo postavy hovoria, a tým, čo prežívajú. Hoci má za sebou aj experimentálne texty, vždy kladie dôraz na emocionálnu pravdivosť a vnútornú logiku príbehu.",
    "Po rokoch strávených cestovaním po rôznych krajinách a kontinentoch sa autor rozhodol usadiť a spracovať všetky zážitky, stretnutia a premeny, ktoré mu život na cestách priniesol. Kultúrne kontrasty, jazykové bariéry a pocit „byť cudzincom“ sa stali ústrednými motívmi jeho diel. Knihy autora často odrážajú atmosféru miest, kde sa zdržiaval – od rušných ulíc Južnej Ameriky cez pokojné dedinky severnej Európy až po púšte Ázie. Postavy v jeho príbehoch sa často ocitajú na križovatke – medzi minulosťou a budúcnosťou, medzi dvoma jazykmi, dvoma kultúrami či dvoma sebapochopeniami. Autor sa venuje aj písaniu esejí a cestopisov, pričom vždy zdôrazňuje, že cestovanie nie je o mieste, ale o pohľade.",
    "Autor pôvodne študoval fyziku a niekoľko rokov pracoval v akademickom prostredí ako výskumník. Popri vedeckej práci vznikali prvé poviedky, najprv len ako forma úniku z presných rovníc do sveta fantázie, no neskôr sa z písania stala rovnocenná vášeň. Jeho knihy sú známe silným filozofickým podtextom, otázkami o povahe reality, vedomia, času a priestoru. Rád využíva prvky science fiction, no vždy s dôrazom na psychológiu postáv. Čitateľ sa tak často ocitá vo svete, ktorý je len mierne odlišný od nášho, no vnútorne rozkolísaný a plný neviditeľného napätia. Autor verí, že veda a literatúra sú si podobné – obe hľadajú pravdu, len inými cestami.",
    "Autor sa venuje písaniu najmä v neskorých večerných hodinách, keď sa svet stíši a myšlienky získavajú hĺbku. V tichu noci vznikajú melancholické príbehy o ľudskej krehkosti, strate, bolestiach, ale aj tichej nádeji, ktorá pretrváva napriek všetkému. Jazyk autora je jednoduchý, no presný – každé slovo má váhu. Diela často mapujú životné zlomy, ťažké rozhodnutia a vzťahy, ktoré nevyšli, no zanechali stopu. Hlavnou témou je vnútorný svet človeka, jeho potreba byť pochopený a prijatý. Autor nevytvára hrdinov, ale obyčajných ľudí – a práve v ich obyčajnosti nachádza výnimočnosť.",
    "Prvú poviedku autor napísal počas vyučovania matematiky na strednej škole – bola to krátka hororová scéna, ktorá vyvolala zdesenie aj obdiv medzi spolužiakmi. Odvtedy sa začala rozvíjať schopnosť vytvárať napätie, atmosféru a znepokojenie, ktoré sprevádzajú čitateľa až do poslednej strany. Knihy autora balansujú na hranici medzi hororom, psychológiou a existenciálnou drámou. Zlo v jeho príbehoch nie je vždy vonkajšie – často pramení z vnútra postáv. Fascinuje ho ľudská temnota, ale aj to, ako sa postavy vyrovnávajú so strachom, stratou či vinou. Autor sa nebojí nepríjemných tém – verí, že literatúra má právo znepokojovať.",
    "Autor pochádza z malého mesta, kde sa silné príbehy odovzdávali medzi generáciami pri kuchynskom stole. Táto ľudová múdrosť, intuíciu a schopnosť načúvať si preniesol aj do svojej tvorby. Realistické romány, ktoré píše, sa často odohrávajú v prostredí, ktoré dôverne pozná – v malých komunitách, kde každý pozná každého a tajomstvá len zdanlivo spia. Medziľudské vzťahy, generačné konflikty, tiché drámy a rodinné traumy sú častými témami, ktoré spracúva s citom a porozumením. Autor verí, že aj v tých najjednoduchších príbehoch sa ukrýva hlboká pravda – stačí vedieť pozerať a počúvať.",
    "V mladosti autor túžil byť hudobníkom – skladal piesne, hral na klavíri a vystupoval na školských podujatiach. Texty piesní sa časom predĺžili, začali sa rozvetvovať a strácali formu, až sa prirodzene premenili na poviedky. Hudobný rytmus však zostal prítomný – v spôsobe, akým autor skladá vety, v melodike opisov aj v refrénoch myšlienok, ktoré sa v príbehoch opakujú. Jeho tvorba je lyrická, silne obrazotvorná a často sa zaoberá láskou, stratou, spomienkami a snom o inom živote. Autor dokáže z jednoduchého okamihu vytvoriť celú symfóniu emócií. Aj preto ho čitatelia často označujú ako „hudobníka medzi spisovateľmi“.",
    "Autor sa dlho hľadal – začínal s rozprávkami pre deti, prešiel cez poviedky pre mládež, neskôr vyskúšal publicistiku, až kým nenašiel svoj hlas v historickej fikcii. V zrelšom veku sa vrátil k otázkam minulosti a rozhodol sa oživovať zabudnuté obdobia cez literárny príbeh. Zameriava sa najmä na osudy bežných ľudí, ktorí sa ocitli v historicky významných situáciách. Ich rozhodnutia, obavy, túžby a nádeje sú v jeho knihách zobrazené s empatiou a rešpektom. Hoci rešpektuje fakty, vždy dáva priestor emócii a ľudskej pravde. Autor verí, že minulosť nie je mŕtva – len čaká, kým ju niekto opäť rozpovie."
]

# Fallback biog - female
FALLBACK_BIO_FEMALE = [
    "Autorka začala písať už ako dieťa, keď si vymýšľala príbehy pre svoje bábiky a zapisovala ich do školských zošitov. V desiatich rokoch napísala svoju prvú báseň a odvtedy nikdy neprestala tvoriť. Láska k slovu ju sprevádzala počas celého dospievania, no k písaniu sa vrátila naplno až po štúdiách. Jej tvorbu ovplyvnili viacerí autori, najmä Stephen King, vďaka ktorému sa nevyhýba temnejším témam ani psychologickému napätiu. V jej príbehoch sa stretáva každodennosť so záhadou, vnútorné sily postáv často zrkadlia vonkajšie udalosti. Autorka verí, že literatúra má moc odhaliť to, čo bežne skrývame – pred inými, aj pred sebou samými.",
    "Autorka vyrastala obklopená knihami, ktoré jej matka nosila z knižnice. Už ako tínedžerka si viedla čitateľský denník, v ktorom si nevšímala len príbehy, ale analyzovala štýl a rytmus viet. Táto precíznosť sa neskôr odrazila aj v jej vlastnej tvorbe. Hoci začínala s poéziou, jej texty sa postupne rozvinuli do dlhších foriem – najmä do introspektívnych próz, kde sa snúbi jemný jazyk s hlbokým emocionálnym nábojom. V jej knihách nájdeme postavy, ktoré sa hľadajú, zraňujú, odpúšťajú si – často potichu a medzi riadkami. Autorka verí, že skutočné príbehy sa odohrávajú v tichu, v pohľadoch, v rozhodnutiach, ktoré sa zdajú byť malé, no menia všetko.",
    "Autorka pôsobila dlhé roky v oblasti filmu a divadla, kde sa venovala réžii a scenáristike. Dramatická štruktúra, cit pre scénu a schopnosť vystavať silný konflikt sú znaky, ktoré si preniesla aj do literárnej tvorby. V jej knihách je každý dialóg nositeľom napätia a každá situácia má presný rytmus. Postavy sa často ocitajú na hrane – medzi túžbou a zodpovednosťou, medzi tým, čo chcú, a tým, čo si od nich vyžaduje svet. Témy ako identita, hranice slobody či vzťahy medzi ženami sú v jej dielach spracované s jemnosťou, no aj odvahou. Autorka verí, že práve v krehkosti sa ukrýva najväčšia sila.",
    "Po rokoch strávených v zahraničí sa autorka rozhodla usadiť a zachytiť svoje cestovateľské zážitky vo forme príbehov. Spoznávanie kultúr, cudzích jazykov a stret s inakosťou sa stali ústrednými motívmi jej kníh. V jej prózach cítiť atmosféru miest, vôňu trhov, ticho chrámov i ruch ulíc. Hrdinky jej príbehov často hľadajú miesto, kam by patrili – a niekedy ho nájdu práve v sebe. Autorka sa venuje aj esejistike, kde reflektuje spoločenské témy a prepája osobné skúsenosti s univerzálnymi otázkami. Verí, že rozprávanie príbehov je spôsob, ako si človek môže vytvoriť domov kdekoľvek.",
    "Autorka študovala matematiku a informatiku, no počas dlhých večerov si písala vlastné príbehy len pre seba. Časom si uvedomila, že v písaní nachádza rovnakú krásu ako vo vede – logiku, poriadok, ale aj moment prekvapenia. Jej knihy často prepájajú exaktný svet s ľudskou emocionalitou – postavy sa pohybujú v štruktúrovanom priestore, no zároveň sa snažia porozumieť svojim citom a minulosti. Do svojich príbehov rada vkladá otázky o čase, rozhodnutí a dôsledkoch. Autorka tvrdí, že aj najjednoduchšia veta môže obsahovať celý vesmír – ak je správne načasovaná.",
    "Písanie sa pre autorku stalo útočiskom počas náročného životného obdobia. V tichu noci, keď všetko stíchlo, nachádzala útechu v slovách, ktoré spájala do príbehov. Z tejto intímnej potreby vznikli jej prvé diela – melancholické, no nádejeplné. V jej knihách dominujú vnútorné monológy, detailné pozorovania a vývoj postáv, ktoré prechádzajú citovou transformáciou. Hoci sa vyhýba veľkým gestám, jej prózy zasahujú hlboko – dotýkajú sa tém straty, samoty, aj uzdravovania. Autorka verí, že písanie nie je len rozprávanie príbehu, ale aj spôsob, ako liečiť dušu – vlastnú aj čitateľovu.",
    "Autorka písala odjakživa, no prvý skutočný príbeh vznikol v lavici počas hodiny fyziky. Bol to krátky horor, ktorý vyvolal medzi spolužiakmi prekvapenie aj nadšenie. Odvtedy sa v nej prebudila túžba preskúmať temnejšie zákutia ľudskej psychiky. V jej knihách sa objavujú postavy, ktoré čelia vlastnému strachu, vnútorným démonom alebo nevysvetliteľným javom. Autorka má cit pre napätie, často pracuje s nedopovedanosťou, tichom a symbolikou. Nezameriava sa na horor ako žáner, ale na atmosféru – chce, aby čitateľ cítil znepokojenie ešte dlho po dočítaní. Verí, že strach je len iná forma pravdy.",
    "Autorka vyrástla v dedinskom prostredí, kde sa príbehy šírili ústnym podaním. Staré mamy rozprávali o minulosti, susedia o záhadách a deti si vymýšľali strašidelné príhody. Z tejto bohatej tradície si odniesla cit pre rozprávačstvo a schopnosť zachytiť hovorový jazyk aj život v jeho prirodzenej podobe. V jej knihách ožívajú zabudnuté hlasy, staré zvyky a zdanlivo obyčajní ľudia, ktorých osudy sú silné a výnimočné. Venuje sa najmä realistickej próze s prvkami sociálnej tematiky. Autorka verí, že najkrajšie príbehy nie sú vymyslené – len ešte neboli vypovedané.",
    "V detstve sa autorka venovala hudbe – hrala na klavíri a písala texty piesní. Tieto texty boli čoraz dlhšie, až sa z nich stali prózy. Hudobný rytmus si však preniesla aj do svojho štýlu – jej knihy majú svoj vlastný „takt“, opakovanie motívov a melodickú výstavbu viet. Píše najmä o láske, spomienkach, nenápadných stratách a veľkých tichách. Postavy sú často vnímavé, krehké, no zároveň pevné vo svojich hodnotách. Autorka tvrdí, že aj smútok môže byť krásny, ak je vyrozprávaný s nehou. Literatúru vníma ako formu hudby, len bez notovej osnovy.",
    "Autorka si prešla rôznymi fázami – najprv písala pre deti, potom pre mládež, neskôr skúšala žurnalistiku, až napokon objavila historickú fikciu. V tomto žánri sa našla, pretože jej umožňuje spájať rešpekt k minulosti s citom pre rozprávanie. Venuje sa príbehom, ktoré oživujú zabudnuté osudy žien, remeselníkov, ľudí z okraja dejín. Nesústredí sa na veľké mená, ale na malých hrdinov každodennosti. Jej knihy sú dôsledne rešeršované, no vždy s dôrazom na emócie a ľudskosť. Autorka verí, že história nie je len dátum – ale pamäť, ktorú môžeme uchovať práve cez príbeh."
]


def translate_to_czech(text):
    try:
        parts = [text[i:i + 500] for i in range(0, len(text), 500)]
        translated_parts = []
        for part in parts:
            resp = requests.get(f"https://api.mymemory.translated.net/get?q={quote(part)}&langpair=en|cs")
            data = resp.json()
            translated = data['responseData']['translatedText']
            translated_parts.append(translated)
        return " ".join(translated_parts).strip()
    except:
        return text.strip()


def get_description_from_wikipedia(full_name):
    query = quote(full_name)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("extract", "")


def display_biography(first_name, last_name, gender):
    full_name = f"{first_name} {last_name}"
    description_en = get_description_from_wikipedia(full_name)

    if not description_en or len(description_en.strip()) < 50:
        fallback = random.choice(FALLBACK_BIO_MALE if gender == "muž" else FALLBACK_BIO_FEMALE)
        print("⚠️ Popis chýba alebo je příliš krátký – použitý fallback:")
        print(f"📖 Biografie:\n{fallback}")
        return

    description_cz = translate_to_czech(description_en)
    if len(description_cz.strip()) < 50 or "MYMEMORY WARNING" in description_cz.upper():
        fallback = random.choice(FALLBACK_BIO_MALE if gender == "muž" else FALLBACK_BIO_FEMALE)
        print("⚠️ Preklad zlyhal alebo je příliš krátký – použitý fallback:")
        print(f"📖 Biografie:\n{fallback}")
        return

    print(f"📖 Biografie (přeložená):\n{description_cz}")


if __name__ == "__main__":
    first_name = input("Zadej jméno autora/autorky: ")
    last_name = input("Zadej příjmení autora/autorky: ")
    gender = input("Zadej pohlaví (muž/žena): ").strip().lower()

    if gender not in ["muž", "zena", "žena"]:
        print("⚠️ Neplatné pohlaví. Použij 'muž' nebo 'žena'.")
    else:
        gender = "žena" if gender in ["žena", "zena"] else "muž"
        display_biography(first_name, last_name, gender)
