StarTrac

Instalacija:
	- zavisnosti:
		- Django (1.7.1)
		- GitPython (0.3.6)
			http://gitpython.readthedocs.org/en/stable/intro.html
			# pip install gitpython
	
	- podesavanja:
		- GIT_REPO_PATH
			putanja do pracenog git repozitorijuma 
			nalazi se u: src/StarTrac/settings.py
			podrazumevana vrednost (repozitorijum samog projekta): "../.git"
	
Funkcionalnosti:
	- Kanban:
		-Osnovni prikaz kanban table podeljene u 4 sekcije u kojima se zadatak moze naci Created On Wait Accepted Closed gde se u svakoj koloni nalaze taskovi tog stanja
		-Moguca je manipulacija taskovima mehanizmom drag-drop pri cemu se vrsi izmena stanja i dodaje se event promene stanja u timeline
		-Prilikom zatvaranja taska nudi se opcija kako se zatvara.
		
	- Milestones:
		-Omogucava prikaz svih milestone-ova sa procentualnim prikazom zatvorenih taskova.U listi svih takodje je dostupan prikaz broja komentara, i taskova
		-Moguce je prikaz pojedinacnih milestone-ova kao i izmena vrednosti. U detaljima je dostupan i prikaz svih povezanih taskova.
		-Za svaki pojedinacni milestone moguce je dobiti i graficki prika odnosa stanja u kom se task nalazi, odnosa prioriteta taskova, kao i prikaz zatvorenih taskova.
		-Dodavanje novog milestone-a
		
	- Requirements:
		-Omogucava prikaz svih zahteva, gde svaki u listi prikazuje i koliko je zatvorenih taskova. Prikazuje i broj komentara i broj taskova za svaki pojedinacni zahtev.
		-Dodavanje novog zahteva izmena postojeceg
		-Prikaz detalja za svaki zahtev. Pored osnovnih detalja prikazuju se i komentari i taskovi za taj zahtev
		-Za svaki pojedinacni milestone moguce je dobiti i graficki prika odnosa stanja u kom se task nalazi, odnosa prioriteta taskova, kao i prikaz zatvorenih taskova.
		
	- Tasks:
		- Listu zadataka je moguce filtrirati po stanju odabirom odgovarajuceg taba na vrhu stranice, boja svakog reda odgovara prioritetu zadatka (siva ako je zatvoren).
		- Kada se zadatak kreira inicijalno je u stanju 'created', moze se prebaciti u stanje 'on wait' (spreman za izvrsenje), kada mu se dodeli korisnik prelazi u stanje 'assigned', a kada se odredi resolve type prelazi u stanje 'closed'.
	
	- Time line:
		- Prikazuju se svi dogadjaji grupisani po datumu sa odgovarajucim detaljima i korisnikom vezanim za dogadjaj. Klikom na odredjeni red prikazuje se modalni dijalog sa linkovima ka detaljima  entiteta povezanih sa dogadjajem.
		- Moguce je otici i na detalje korisnika koji je kreirao dogadjaj, ukoliko je u pitanju komit i postoji korisnik sa istim email-om kao i komiter taj korisnik se uzima kao kreator, inace se samo prikazuje ime komitera.
		
	- Repository:
		- Prikazuje se sadrzaj repozitorijuma (fajl stablo) (podrazumevana grana je master ili ako ne postoji prva grana koja postoji).
		- Moguce je odabrati granu koja se prikazuje iz menija Branches (sidebar levo).
		- Moguce je prikazati sadrzaj fajle klikom na fajlu u stablu.
		- Moguce je prikazati listu komita (svih ili samo ispod odredjene grane) odabirom u meniju Commits.
		- Moguce je prikazati detalje komita, pregledati sadrzaj repozitorijuma za odredjeni komit i pregledati razlike u odnosu na prethodni komit.
		- Na listi razlika se prikazuju komiti/grane izmedju kojih se gleda razlika, tip razlike i putanja do fajla.
		- Za svaki fajl je moguce gledati razlike uporedo (pre i posle) i patch iz prethodne u narednu verziju.
		- Na stranici Diff (iz sidebar-a levo) je moguce odabrati dve grane/komita i prikazati razlike izmedju njih. Grane se zadaju odabirom iz padajuceg menija, a komiti se zadaju upisivanjem hex_sha vrednosti (moze se videti u detaljima komita).
		- putanja ka repou se definise u src/StarTrac/settings.py u polju GIT_REPO_PATH, podrazumevana vrednost je putanja ka repozitorijumu koji obuhvata sam projekat ("../.git")
	
	- Komentari:
		- Moguce je postaviti komentare vezane za Task, Milestone i Requirement.
		
	-Graficki prikaz