# Game of Strom (work in progress)

## Spielziel
Das Ziel ist es die Stromkosten eines Haushaltes zu minimieren und gleichzeitig den Komfort auf dem benötigten Niveau zu halten. Je besser man dies erreicht umso mehr Punkte erhält man zur Belohnung.

## Spielelemente

- Dynamischer Strompreis (Tibber)
- PV-Anlage (7,2 kWp)
- Heimspeicher (BYD, 5kWh)
- Wechselrichter (Kostal Plenticore)
- Elektroauto (Zoe, 50kWh)
- Wärmepumpe (Stiebel Eltron, 5kW)
- Smart Home Server (Home Assistant)

## Ablauf
- Der Spieler erhält Grafiken und sieht alle relevanten Daten. Dies umfasst etwa Strompreise, Wetter-Beobachtungen und -Prognosen, Stromerzeugung via PV, Energie im Speicher und Auto und Temperaturen.
- Man kann sich entscheiden das Auto zu laden, den Speicher zu befüllen oder zu nutzen, Warmwasser zu erzeugen sowie die Heizung hoch- oder runterzudrehen.
- Die Aktionen werden ausgeführt und man erhält kurze Zeit später die neue Situation und die zuletzt erzielten Punkte.
- Nach Ablauf von 24 Stunden ist das Spiels beendet und man erfährt seine Performanz.
- Man kann entweder selbst spielen oder einen via Reinforcement Learning optimierten KI-Agenten nutzen.

## Heimspeicher

- Der Spieler kan den Heimspeicher bei günstigen Strompreisen befüllen und die Energie in teuren Phasen nutzen.
- Dies muss zunächst im Wechselrichter freigeschaltet werden. Dann kann via Modbus die Be- und Entladeleistung angegeben werden.
- Sobald das erste Modbus-Steuersignale gesendet werden, wird das externe Batteriemanagement aktiv. Es wechselt dann nicht mehr in den internen Modus zurück. Dieser wird erst nach einem Neustart des Wechselrichters wieder aktiv.
- Die externe Batteriesteuerung wird bei Game of Strom über eine Pyscript App (Python) durchgeführt. Pyscript ist eine Community Integration für Home Assistant. Siehe https://github.com/custom-components/pyscript
- Die externe Steuerung greift auf Sensor-Werte des Wechselrichters zurück. Diese werden per Kostal Plenticore Integration in Home Assostant verfügbar. Siehe https://www.home-assistant.io/integrations/kostal_plenticore/
- Zur Installation der Pyscript App kann man auf die im Game of Strom hinterlegten Dateien zurückgreifen. Diese müssen wie folgt in Home Assistant angelegt werden:  
- Home Assistant: config/configuration.yaml
- Home Assistant: config/pyscript/config.yaml 
- Home Assistant: config/pyscript/apps/kostal_battery_control/__init__.py

## todo: weitere Komponenten: Preise, Wetter, Steuerungen...