# Game of Strom

## Konzept
"Game of Strom" ist eine innovative Plattform, die die typischen Merkmale einer [Energiemanagement-Software](https://en.wikipedia.org/wiki/Energy_management_software) mit spielerischen Aspekten kombiniert. Die Anwendung ermöglicht die direkte Interaktion durch den Benutzer oder den Einsatz von KI-Technologien für eine autonome und optimale Steuerung mittels [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

## Spielziel
Das primäre Ziel des Spiels ist es, die Stromkosten eines Haushalts zu minimieren, während der Wohnkomfort auf dem gewünschten Niveau gehalten wird. Je effizienter die Energieverwaltung, desto mehr Punkte erhält der Spieler.

## Spielelemente
"Game of Strom" ist derzeit in Entwicklung. Der erste Prototyp wird auf einen Haushalt zugeschnitten sein, der folgende Elemente enthält:

- Dynamische stündliche Strompreise ([Tibber](https://tibber.com/en))
- PV-Anlage (7,2 kWp)
- Heimspeicher (BYD, 5kWh)
- Wechselrichter ([PLENTICORE plus 7.0](https://www.kostal-solar-electric.com/de-de/produkte/hybrid-wechselrichter/plenticore-plus/))
- Elektroauto (Renault Zoe R110 Z.E. 50 (52 kWh))
- Wallbox (GO-E Charger, 11kw)
- Wärmepumpe für Raumheizung und Warmwasser ([Stiebel Eltron, 5kW](https://www.stiebel-eltron.de/de/home/produkte-loesungen/erneuerbare_energien/waermepumpe/luft-wasser-waermepumpen/wpl-a-05-07-hk-premium/wpl-a-05-hk-230-premium.html))
- Intelligente Heizkörperregler ([Fritz Dect 301](https://avm.de/produkte/smart-home/fritzdect-301/))
- Smart Home Server ([Home Assistant](https://www.home-assistant.io/))

## Spielablauf
- Der Spieler erhält Übersichtsgrafiken und Zugriff auf alle relevanten Daten über Home Assistant.
- Diese Daten beinhalten Informationen zu Strompreisen, Wetterdaten und -vorhersagen, Stromerzeugung durch PV, Energie in Speicher und Auto sowie Temperaturdaten.
- Der Spieler kann Entscheidungen treffen, z.B. das Auto zu laden, den Speicher zu füllen oder zu entleeren, Warmwasser zu erzeugen oder die Heizung hoch- oder runterzuregeln.
- Die getroffenen Entscheidungen werden ausgeführt und der Spieler erhält kurze Zeit später die aktualisierte Situation und die zuletzt erzielten Punkte.
- Nach 24 Stunden endet das Spiel und der Spieler erhält eine Bewertung seiner Leistung.
- Es besteht die Möglichkeit, selbst zu spielen oder einen durch Reinforcement Learning optimierten KI-Agenten einzusetzen.

## Steuerung des Heimspeichers

- Bei niedrigen Strompreisen kann der Spieler den Heimspeicher laden und die gespeicherte Energie zu Zeiten höherer Preise nutzen.
- Dies muss zuerst im Wechselrichter aktiviert werden. Über Modbus kann dann die Lade- und Entladeleistung festgelegt werden.
- Sobald das erste Modbus-Steuersignal gesendet wird, wird das externe Batteriemanagement aktiviert. Es wechselt danach nicht mehr zurück in den internen Modus, der erst nach einem Neustart des Wechselrichters wieder aktiviert wird.
- Die externe Batteriesteuerung wird in  of Strom durch eine [Pyscript App (Python)](https://github.com/custom-components/pyscript) ausgeführt, eine Community Integration für Home Assistant.
- Die externe Steuerung nutzt Sensorwerte des Wechselrichters, die durch die [Kostal Plenticore Integration](https://www.home-assistant.io/integrations/kostal_plenticore/) in Home Assistant verfügbar gemacht werden.
  
- Für die Installation der Pyscript App können Sie die in "Game of Strom" bereitgestellten Dateien verwenden. Diese müssen wie folgt in Home Assistant angelegt werden:  
    - Home Assistant: `config/configuration.yaml`
    - Home Assistant: `config/pyscript/config.yaml `
    - Home Assistant: `config/pyscript/apps/kostal_battery_control/__init__.py`

Die Pyscript App sorgt dafür, dass das externe Management zunächst ähnlich funktioniert wie das interne Management des Wechselrichters. Mit der zusätzlichen Möglichkeit, den Speicher auch aus dem Netz zu laden, indem der minimale SOC gesetzt wird. 

Eine benutzerfreundliche Steuerung wird künftig über "Game of Strom" bereitgestellt. Bis dahin können Sie die Funktion `kostal_set_battery_min_soc` in Home Assistant nutzen, die hier definiert ist: `Home Assistant/scripts/kostal_control.yaml`

## Steuerung Auto-Speicher
In Bearbeitung

## Steuerung Warmwassererzeugung
In Bearbeitung

## Steuerung Raumheizung
In Bearbeitung

## Informationen zu Stromerzeugung, Strompreisen und Stromkosten
In Bearbeitung

## Informationen zu Wetterbeobachtungen und -Prognosen
In Arbeit
