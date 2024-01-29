# Povpraševalni jezik

Na tej strani je podrobneje predstavljen formalizem, s pomočjo katerega iščemo po skladenjsko razčlenjenih korpusih na spletnem vmesniku [Drevesnik](https://orodja.cjvt.si/drevesnik/). Temelji na povpraševalnem jeziku, razvitem znotraj orodja [dep_search](https://github.com/TurkuNLP/dep_search), ki smo ga za potrebe iskanja po slovenskih korpusih prilagodili tako, da poleg iskanja po oblikoslovnih in odvisnostnih skladenjskih oznak sheme [Universal Dependencies](https://universaldependencies.org/) omogoča tudi iskanje po oblikoskladenjskih oznakah sheme [JOS](https://nl.ijs.si/jos/). Možnosti iskanja so v nadaljevanju ponazorjene z nekaj izbranimi iskalnimi pogoji, na katere lahko tudi kliknemo in si ogledamo rezultate tovrstne poizvedbe v ročno označenem korpusu SSJ (naključni zadetki v krajših povedih).

## Lastnosti pojavnice

### Iskanje po besednih oblikah

Po besedni obliki pojavnice iščemo z vnosom poljubnega niza znakov. Primeri:

*   [hodim](https://orodja.cjvt.si/drevesnik/show/demo1a/sl/0/10) poišče vse pojavnice z obliko _hodim_, zapisano s samimi malimi črkami
*   [Delo](https://orodja.cjvt.si/drevesnik/show/demo2a/sl/0/10) poišče vse pojavnice z obliko _Delo_, zapisano z veliko začetnico

<!---
Izpuščeno, ker iskanje po atributih ali vrednostih tako ali tako ne dela, dela samo iskanje po polnem paru Atribut=Vrednost.

V malo verjetnem primeru, da je vneseno besedilo enake oblike kot ena izmed [oblikoslovnih oznak](https://universaldependencies.org/u/feat/index.html), orodje poišče pojavnice s to oznako. V tem primeru iskano besedno obliko zapišemo v narekovajih:

*   ["Gen"](http://bionlp-www.utu.fi/dep_search/?db=English&search=%22Person%22) poišče vse pojavnice z obliko _Gen_ in ne pojavnic z oznako _Gen_, ki označujejo pojavnice v rodilniku.
-->

Po osnovni obliki besede (lemi) iščemo s predpono **L=**:

*   [L=hoditi](https://orodja.cjvt.si/drevesnik/show/demo2b/sl/0/10) poišče vse pojavitve pojavnic z lemo _hoditi_

### Iskanje po oblikoslovnih lastnostih

Besedno vrsto in druge oblikoslovne lastnosti pojavnice lahko opredelimo na dva načina, saj so vsi korpusi označeni tako z označevalno shemo <a href="https://nl.ijs.si/jos/" target="_blank">JOS</a> kot <a href="https://universaldependencies.org/" target="_blank">Universal Dependencies</a> (UD). Oba sistema sta dobro dokumentirana in primerljiva z vidika ustreznosti naslavljanja specifik slovenščine, zato je izbira enega ali drugega odvisna predvsem od uporabnikovih preferenc.

#### Oblikoslovne lastnosti po shemi JOS

Po oblikoskladenjskih oznakah JOS iščemo s predpopono `X=`, pri čemer je pri teh oznakah podprta tudi uporaba posebnih operatorjev `.` (ki nadomešča poljuben znak) in `*` (ki nadomešča poljubno število pojavitev znaka na levi). Glede na specifike naloženih korpusov je trenutno možno zgolj iskanje po angleški različici oznak. Primeri:

*   [X=Ncfsl](https://orodja.cjvt.si/drevesnik/show/demo3a/sl/0/10) poišče vse pojavnice z oznako za občne samostalnike ženskega spola v mestniku ednine
*   [X=Ncf.l](https://orodja.cjvt.si/drevesnik/show/demo4a/sl/0/10) poišče vse pojavnice z oznako za občne samostalnike ženskega spola v mestniku poljubnega števila
*   [X=Ncf.\*](https://orodja.cjvt.si/drevesnik/show/demo5a/sl/0/10) poišče vse pojavnice z oznako za občne samostalnike ženskega spola poljubnega sklona in števila

#### Oblikoslovne lastnosti po shemi UD

Po besedni vrsti UD iščemo z vpisom iskane besedne vrste, po drugih oblikoslovnih lastnostih pa z opisom iskane oznake v obliki para atributa in njegove vrednosti, npr. `Kategorija=Oznaka`. 

*   [NOUN](https://orodja.cjvt.si/drevesnik/show/demo6a/sl/0/10) poišče vse pojavnice z besedno vrsto _NOUN_ (občni samostalniki).
*   [VerbForm=Inf](https://orodja.cjvt.si/drevesnik/show/demo7a/sl/0/10) poišče vse pojavnice z oznako za nedoločnike. 

<!---
Izpuščeno, ker iskanje po atributih ali vrednostih tako ali tako ne dela, dela samo iskanje po polnem paru Atribut=Vrednost.

Iščemo lahko tudi zgolj po oznakah, a orodje v primeru več različnikih kategorij s to oznako kot rezultat vrne samo zadetke znotraj najpogostejše kategorije. V teh primerih je zato priporočljivo iskanje z eksplicitno izpisano kombinacijo kategorije in oznake.
...
*   [Par](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=Par) searches for all tokens in partitive case (Note: _Par_ is interpreted to mean _Case=Par_)
...
*   [Past](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=Past) searches for all past tense verbs (Note: _Past_ is interpreted to mean _Tense=Past_. Other possible category for _Past_ is _PartForm_, and to search for past participles _PartForm=Past_ must be typed.)
...
Možno je tudi iskanje po kategorijah brez opredelitve oznak:

*   [PartForm](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=PartForm) poišče deležnike v vseh oblikah: sedanjiku (PartForm=Pres), pretekliku (PartForm=Past) ...
--->

### Posebni operatorji
  
Vse zgoraj navedene lastnosti pojavnice lahko med seboj tudi kombiniramo s posebnima operatorjema **&** (in) oz. **|** (ali):

*   [lepo&X=R.\*](https://orodja.cjvt.si/drevesnik/show/demo8a/sl/0/10) poišče vse pojavnice z obliko _lepo_, ki so po shemi JOS označene kot prislov (in ne npr. pridevnik)
*   [L=delati|L=narediti](https://orodja.cjvt.si/drevesnik/show/demo9a/sl/0/10) poišče vse pojavnice z lemo _delati_ ali _narediti_
*   [NOUN&Number=Plur](https://orodja.cjvt.si/drevesnik/show/demo10a/sl/0/10) poišče vse samostalnike v množini
*   [L=prst&Gender=Masc](https://orodja.cjvt.si/drevesnik/show/demo11a/sl/0/10) poišče vse pojavnice z lemo _prst_ moškega spola

Pri iskanju po besednih oblikah, lemah in oznakah lahko uporabimo tudi **negacijo** z vpisom operatorja **!** pred lastnostjo, po kateri ne želimo iskati. Primeri:

*   [L=biti&!AUX](https://orodja.cjvt.si/drevesnik/show/demo12a/sl/0/10) poišče vse pojavnice z lemo _biti_, ki niso označene kot pomožni glagol
*   [ADJ&!X=A.\*](https://orodja.cjvt.si/drevesnik/show/demo13a/sl/0/10) poišče vse pojavnice, ki so po shemi UD označene kot pridevnik, po shemi JOS pa ne

Za iskanje po pojavnicah brez opredeljenih lastnosti uporabimo podčrtaj (`_`).

## Iskanje po skladenjskih relacijah

Skladenjske relacije zapisujemo z operatorjema `<` in `>`, ki posnemata puščice, s kakršnimi so običajno ponazorjena skladenjska razmerja med besedami v odvisnostno razčlenjenih povedih (odvisnostnih drevesih).

*   `A < B` pomeni, da je pojavnica A podrejena pojavnici B, npr. _deževno_ < _jutro_
*   `A > B` pomeni, da je pojavnica A nadrejena pojavnici B, npr. _berem_ > _časopis_

Podčrtaj `_` predstavlja _katerokoli pojavnico_, torej pojavnico, ki ji ne želimo opredeliti dodatnih lastnosti. Spodaj navajamo nekaj preprostih primerov iskanj po odvisnostnih skladenjskih strukturah:

*   [delo < \_](https://orodja.cjvt.si/drevesnik/show/demo14a/sl/0/10) poišče vse pojavnice z obliko _delo_, ki so podrejene neki drugi pojavnici
*   [delo > \_](https://orodja.cjvt.si/drevesnik/show/demo15a/sl/0/10) poišče vse pojavnice z obliko _delo_, ki so nadrejene neki drugi pojavnici
*   [\_ < delo](https://orodja.cjvt.si/drevesnik/show/demo16a/sl/0/10) poišče vse pojavnice, ki so podrejene pojavnici z obliko _delo_

Cilj poizvedbe je vedno pojavnica na skrajni levi, ki se v rezultatih tudi obarva zeleno. Čeprav iskalna pogoja `delo > _` in `_ < delo` opisujeta isto skladenjsko strukturo, so prikazani rezultati drugačni.

**Vrsto skladenjske relacije** med pojavnicama lahko podrobneje opredelimo za relacijskim operatorjem (puščico), npr. `_ <vrsta _` ali `_ >vrsta _`. Več možnih tipov relacije ločimo z operatorjem `|` (_ali_), kot rezultat iskanja pa so prikazane strukture, ki ustrezajo vsaj enemu izmed navedenih tipov.

*   [\_ <cop \_](https://orodja.cjvt.si/drevesnik/show/demo17a/sl/0/10) poišče vse vezne glagole (tj. pojavnice, ki so cilj relacije `cop`)
*   [\_ >nsubj \_](https://orodja.cjvt.si/drevesnik/show/demo18a/sl/0/10) poišče vse povedke z izraženim samostalniškim osebkom (tj. pojavnice, ki so izvor relacije `nsubj`)  
*   [\_ <nsubj|<csubj \_](https://orodja.cjvt.si/drevesnik/show/demo19a/sl/0/10) poišče vse pojavnice v vlogi osebka - tako samostalniške kot stavčne osebke (osebkove odvisnike).

Z nizanjem operatorjev lahko opredelimo več odvisnostnih relacij neke pojavnice naenkrat:

*   [\_ >obj \_ >iobj \_](https://orodja.cjvt.si/drevesnik/show/demo20a/sl/0/10) poišče vse pojavnice, ki so nadrejene tako premim kot nepremimim predmetom (povedke z dvojno vezljivostjo) 
*   [\_ <amod \_ >advmod \_](https://orodja.cjvt.si/drevesnik/show/demo21a/sl/0/10) poišče vse pojavnice, ki so označene kot pridevniški prilastki in so obenem nadrejene določilu v obliki prislova
*   [\_ >nmod \_ >nmod \_](https://orodja.cjvt.si/drevesnik/show/demo22a/sl/0/10) poišče vse pojavnice z najmanj dvema samostalniškima določiloma

Hierarhijo odvisnostnih relacij opredelimo z oklepaji:

*   [\_ >nmod \_ >nmod \_](https://orodja.cjvt.si/drevesnik/show/demo23a/sl/0/10) poišče pojavnice z dvema istoležnima oz. vzporednima samostalniškima določiloma (določili sta hierarhično enakovredni)
*   [\_ >nmod (\_ >nmod \_)](https://orodja.cjvt.si/drevesnik/show/demo24a/sl/0/10) poišče pojavnice s samostalniškim določilom, ki ga določa neko drugo samostalniško določilo (eno določilo je nadrejeno drugemu)

Za **negacijo** uporabljamo operator `!`, ki ga je mogoče uporabiti tako v kombinaciji z operatorjema `<` in `>` kot s posamičnimi vrstami relacij. Primeri:

*   [\_ >nmod \_ !>case \_](https://orodja.cjvt.si/drevesnik/show/demo25a/sl/0/10) poišče vsa samostalniška določila, ki niso predložne zveze (samostalnik ni nadrejen nekemu predlogu)
*   [\_ >nmod \_ >!case \_](https://orodja.cjvt.si/drevesnik/show/demo26a/sl/0/10) poišče vsa samostalniška določila, ki so nadrejene neki strukturi, a ne predlogu
<!--- ta kombinacija ne dela kot pričakovano - vrne tudi advcl z mark ... najbrž manjka 'for every dependent'
*   [\_ <advcl \_ !>mark \_](http://bionlp-www.utu.fi/dep_search/?db=English&search=_%20%3Cadvcl%20_%20%21%3Emark%20_) searches for heads of unmarked adverbial clauses (governed by advcl but not governing mark)
*   [\_ <nsubj \_ >!amod \_](http://bionlp-www.utu.fi/dep_search/?db=English&search=_%20%3Cnsubj%20_%20%3E%21amod%20_) searches for subjects which governs something but it cannot be an adjective (governed by nsubj and governs something which is not amod)
--->
*   [\_ <nsubj \_ !(>amod|>acl) \_](https://orodja.cjvt.si/drevesnik/show/demo27a/sl/0/10) poišče osebke brez pridevniških prilastkov ali prilastkovih odvisnikov

Pri negaciji celotne relacije (npr. `_ !>amod _`) lahko med zadetki torej pričakujemo tudi pojavnice brez podrejenih elementov, medtem ko negacija vrste relacije (npr. `_ >!amod _`) pomeni, da mora imeti pojavnica vsaj en podrejeni element (ki pa ni _amod_).

**Smer** odvisnostne relacije lahko opredelimo z operatorjema `@R` and `@L`, ki določata, ali se skrajno desna pojavnica iskalnega pogoja pojavlja desno oz. levo od iskane pojavnice (tj. skrajno leve pojavnice iskalnega pogoja).

*   [VERB >nsubj@R \_](https://orodja.cjvt.si/drevesnik/show/demo28a/sl/0/10) poišče glagole, ob katerih samostalniški osebek (_nsubj_) stoji desno od glagola
*   [\_ >amod@L \_ >amod@R \_](https://orodja.cjvt.si/drevesnik/show/demo29a/sl/0/10) poišče pojavnice z najmanj dvema različnima pridevniškima prilastkoma, pri čemer en stoji levo, drugi pa desno od odnosnice
*   [\_ <case@L \_](https://orodja.cjvt.si/drevesnik/show/demo30a/sl/0/10) poišče označevalce sklona, ki se za razliko od prevladujočih predpozicij (predlogov) pojavljajo za samostalniškim jedrom (t. i. postpozicije)

## Združevanje iskalnih pogojev

Več ločenih iskalnih pogojev lahko združimo z operatorjem `+`. Združeni iskalni pogoj v obliki `pogoj1 + pogoj2 + pogoj3` vrne vse povedi (drevesa), ki izpolnjujejo vse tri pogoje hkrati.

*   [VERB >aux \_ + Tense=Pres](https://orodja.cjvt.si/drevesnik/show/demo31a/sl/0/10) poišče vse povedi, v katerih se pojavljata tako sestavljeni glagol kot glagol v sedanjiku

## Univerzalni iskalni pogoji

Z operatorjem `->` lahko opredelimo tudi pogoj, ki velja za vse iskane pojavnice (tj. pojavnice ali strukture na levi strani tega operatorja). Primeri:

*   [\_ -> NOUN](https://orodja.cjvt.si/drevesnik/show/demo32a/sl/0/10) poišče povedi, v katerih so vse pojavnice označene kot samostalniki
*   [NOUN -> NOUN >amod \_](https://orodja.cjvt.si/drevesnik/show/demo33a/sl/0/10) poišče povedi, v katerih imajo vsi samostalniki pridevniški prilastek
