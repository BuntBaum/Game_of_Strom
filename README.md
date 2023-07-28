# Game of Strom (work in progress)

## Idee
Game of Strom kombiniert die typischen Funktionen einer Energy Management Software (https://en.wikipedia.org/wiki/Energy_management_software) mit spielerischen Elementen. Es ermöglicht sowohl eine Anwendung durch einen Menschen als auch den Einsatz von KI-Technologien zur autonomen und möglichst optimalen Steuerung durch einen Agenten.

## Spielziel
Das Ziel ist es die Stromkosten eines Haushaltes zu minimieren und gleichzeitig den Komfort auf dem benötigten Niveau zu halten. Je besser man dies erreicht umso mehr Punkte erhält man zur Belohnung.

## Spielelemente
Game of Strom ist derzeit in der Entwicklung. Zunächst entsteht ein Prototyp für einen spezifischen Haushalt mit folgender Ausgangslage:

- Dynamischer stündlicher Strompreis (Tibber)
- PV-Anlage (7,2 kWp)
- Heimspeicher (BYD, 5kWh)
- Wechselrichter (Kostal Plenticore)
- Elektroauto (Zoe, 50kWh)
- Wärmepumpe für Raumheizung und Warmwasser (Stiebel Eltron, 5kW)
- intelligente Heizkörperregler (Fritz Dect 301)
- Smart Home Server (Home Assistant)

## Ablauf
- Der Spieler erhält Grafiken und sieht alle relevanten Daten via Home Assistant.
- Dies umfasst etwa Strompreise, Wetter-Beobachtungen und -Prognosen, Stromerzeugung via PV, Energie im Speicher und im Auto sowie Temperaturen.
- Man kann sich entscheiden das Auto zu laden, den Speicher zu befüllen oder zu nutzen, Warmwasser zu erzeugen sowie die Heizung hoch- oder runterzudrehen.
- Die Aktionen werden ausgeführt und man erhält kurze Zeit später die neue Situation und die zuletzt erzielten Punkte.
- Nach Ablauf von 24 Stunden ist das Spiels beendet und man erfährt seine Performanz.
- Man kann entweder selbst spielen oder einen via Reinforcement Learning optimierten KI-Agenten nutzen.

## Steuerung Heimspeicher

- Der Spieler kan den Heimspeicher bei günstigen Strompreisen befüllen und die Energie in teuren Phasen nutzen.
- Dies muss zunächst im Wechselrichter freigeschaltet werden. Dann kann via Modbus die Be- und Entladeleistung angegeben werden.
- Sobald das erste Modbus-Steuersignale gesendet werden, wird das externe Batteriemanagement aktiv. Es wechselt dann nicht mehr in den internen Modus zurück. Dieser wird erst nach einem Neustart des Wechselrichters wieder aktiv.
- Die externe Batteriesteuerung wird bei Game of Strom über eine Pyscript App (Python) durchgeführt. Pyscript ist eine Community Integration für Home Assistant. Siehe https://github.com/custom-components/pyscript
- Die externe Steuerung greift auf Sensor-Werte des Wechselrichters zurück. Diese werden per Kostal Plenticore Integration in Home Assistant verfügbar. Siehe https://www.home-assistant.io/integrations/kostal_plenticore/
  
- Zur Installation der Pyscript App kann man auf die im Game of Strom hinterlegten Dateien zurückgreifen. Diese müssen wie folgt in Home Assistant angelegt werden:  
- Home Assistant: config/configuration.yaml
- Home Assistant: config/pyscript/config.yaml 
- Home Assistant: config/pyscript/apps/kostal_battery_control/__init__.py

Die Pyscript App sorgt zunächst nur dafür, dass sich das externe Management etwa so verhält wie das interne Management des Wechselrichters. Jedoch hat man nun die Möglichkeit über das Setzen des minimalen SOC den Speicher auch aus dem Netz zu beladen. Hierzu wird künftig über Game of Strom auch eine komfortable Steuerungsmöglichkeit bereitgestellt. Bis dahin kann man die Funktion kostal_set_battery_min_soc in Home Assistant nutzen, welche hier definiert ist: Home Assistant/scripts/kostal_control.yaml


## Steuerung Auto-Speicher
todo

## Steuerung Warmwassererzeugung
todo

## Steuerung Raumheizung
todo

## Infos zu Stromerzeugung, Strompreise und Stromkosten
todo

## Infos zu Wetterbeobachtungen und -Prognosen
todo

