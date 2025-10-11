Simulacija dvostrukog klatna

Ocena: 6

Ovaj projekat prikazuje simulaciju dvostrukog klatna (double pendulum) — nelinearnog dinamičkog sistema poznatog po haotičnom ponašanju. Cilj je da se pokaže kako numerička metoda može da prati kretanje sistema i da se uporedi razlika između sekvencijalnog i paralelnog načina izvršavanja simulacije. Program računa kretanje klatna u vremenskim koracima i beleži stanja sistema u fajl. Simulacija se izvodi na dva načina: sekvencijalno – sve se izvršava u jednom procesu, i paralelno – simulacija se deli na više procesa pomoću biblioteke multiprocessing. Na kraju se porede rezultati i vreme izvršavanja između ta dva pristupa. Za numeričku integraciju koristi se Ojlerova metoda, kojom se prate promene uglova i ugaonih brzina po vremenskim koracima. Sekvencijalna verzija (Python) računa se iterativno u jednom procesu, dok se paralelizovana verzija (Python, multiprocessing) deli na segmente koji se obrađuju istovremeno, a rezultati se spajaju u jedan skup podataka. Izlaz simulacije su vremenske serije stanja sistema u formatu:

t, theta1, theta2, omega1, omega2

Ovi podaci se koriste za poređenje vremena izvršavanja i eventualnih numeričkih odstupanja između sekvencijalne i paralelne verzije. Matematička osnova:

Razlika uglova:
δ = θ₂ - θ₁

Imenitelji:
denom₁ = (m₁ + m₂) · l₁ - m₂ · l₁ · cos²(δ)
denom₂ = (l₂ / l₁) · denom₁

Ugaona ubrzanja:
ω̇₁ = (...) / denom₁
ω̇₂ = (...) / denom₂
(gde izrazi zavise od masa, dužina, gravitacije, uglova i njihovih brzina)

Veze između promenljivih:
θ̇₁ = ω₁
θ̇₂ = ω₂

Ojlerov korak:
xₙ₊₁ = xₙ + ẋₙ · Δt
