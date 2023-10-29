# Game of Strom (Spielanleitung)

## Konzept
"Game of Strom" ist eine innovative Plattform, die die typischen Merkmale einer [Energiemanagement-Software](https://en.wikipedia.org/wiki/Energy_management_software) mit spielerischen Aspekten kombiniert. Die Anwendung ermöglicht die direkte Interaktion durch den Benutzer oder den Einsatz von KI-Technologien für eine autonome und optimale Steuerung mittels [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

Beispielsweise erfolgt die Steuerung des Batteriespeichers für das Haus derzeit über dieses Dashboard:
![image](https://github.com/BuntBaum/Game_of_Strom/assets/140110546/1c424dab-0ede-4bea-b3f3-9e57608aa48e)
Oben kann der minimale Ladezustand der Batterie als `Action` gesetzt werden. Darunter befinden sich verschiedene `States` welche wichtige Systemzustände darstellen und dem Spieler dabei helfen geeignete Aktionen zu wählen.


## Spielziel
Das primäre Ziel des Spiels ist es, die Stromkosten eines Haushalts zu minimieren, während der Wohnkomfort auf dem gewünschten Niveau gehalten wird. Je effizienter die Energieverwaltung, desto mehr Punkte erhält der Spieler.

## Spielelemente
"Game of Strom" ist derzeit in Entwicklung. Der erste Prototyp wird auf einen Haushalt zugeschnitten sein, der folgende Elemente enthält:

- Dynamische stündliche Strompreise ([Tibber](https://tibber.com/en))
- PV-Anlage (7,2 kWp)
- Heimspeicher (BYD, 5kWh)
- Wechselrichter ([PLENTICORE plus 7.0](https://www.kostal-solar-electric.com/de-de/produkte/hybrid-wechselrichter/plenticore-plus/))
- Elektroauto ([Renault Zoe R110 Z.E. 50 (52 kWh)](https://en.wikipedia.org/wiki/Renault_Zoe))
- Wallbox ([GO-E Gemini Flex, 22kW)](https://go-e.com/de-de/produkte/go-e-charger-gemini-flex))
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
In Bearbeitung


# Game of Strom (game instructions)

## Concept
"Game of Strom" is an innovative platform that combines the typical features of an [energy management software](https://en.wikipedia.org/wiki/Energy_management_software) with playful aspects. The application allows direct interaction by the user or the use of AI technologies for autonomous and optimal control using [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

## Game Objective
The primary goal of the game is to minimize the electricity costs of a household while maintaining living comfort at the desired level. The more efficient the energy management, the more points the player receives.

## Game Elements
"Game of Strom" is currently under development. The first prototype will be tailored to a household that includes the following elements:

- Dynamic hourly electricity prices ([Tibber](https://tibber.com/en))
- PV system (7.2 kWp)
- Home storage (BYD, 5kWh)
- Inverter ([PLENTICORE plus 7.0](https://www.kostal-solar-electric.com/de-de/produkte/hybrid-wechselrichter/plenticore-plus/))
- Electric car (Renault Zoe R110 Z.E. 50 (52 kWh))
- Wallbox (GO-E Charger, 11kw)
- Heat pump for room heating and hot water ([Stiebel Eltron, 5kW](https://www.stiebel-eltron.de/de/home/produkte-loesungen/erneuerbare_energien/waermepumpe/luft-wasser-waermepumpen/wpl-a-05-07-hk-premium/wpl-a-05-hk-230-premium.html))
- Intelligent radiator controllers ([Fritz Dect 301](https://avm.de/produkte/smart-home/fritzdect-301/))
- Smart Home Server ([Home Assistant](https://www.home-assistant.io/))

## Gameplay
- The player receives overview graphics and access to all relevant data via Home Assistant.
- This data includes information about electricity prices, weather data and forecasts, power generation through PV, energy in storage and car as well as temperature data.
- The player can make decisions, e.g., to charge the car, fill or empty the storage, generate hot water, or regulate the heating up or down.
- The decisions made are executed, and the player receives the updated situation and the last points scored shortly after.
- After 24 hours, the game ends, and the player receives an evaluation of his performance.
- There is the option to play yourself or use an AI agent optimized through Reinforcement Learning.

## Home Storage Control
- At low electricity prices, the player can charge the home storage and use the stored energy at times of higher prices.
- This must first be activated in the inverter. The charging and discharging power can then be set via Modbus.
- As soon as the first Modbus control signal is sent, the external battery management is activated. After that, it no longer switches back to the internal mode, which is only reactivated after a restart of the inverter.
- The external battery control is carried out in "Game of Strom" by a [Pyscript App (Python)](https://github.com/custom-components/pyscript), a community integration for Home Assistant.
- The external control uses sensor values of the inverter, which are made available by the [Kostal Plenticore Integration](https://www.home-assistant.io/integrations/kostal_plenticore/) in Home Assistant.
- For the installation of the Pyscript App, you can use the files provided in "Game of Strom". These must be created as follows in Home Assistant:
    - Home Assistant: `config/configuration.yaml`
    - Home Assistant: `config/pyscript/config.yaml `
    - Home Assistant: `config/pyscript/apps/kostal_battery_control/__init__.py`

The Pyscript App ensures that the external management initially works similarly to the internal management of the inverter. With the additional possibility to also load the storage from the grid by setting the minimum SOC. 

User-friendly control will be provided in the future via "Game of Strom". Until then, you can use the function `kostal_set_battery_min_soc` in Home Assistant, which is defined here: `Home Assistant/scripts/kostal_control.yaml`

## Car Storage Control
Under Construction

## Hot Water Generation Control
Under Construction

## Room Heating Control
Under Construction

## Information on Power Generation, Electricity Prices, and Electricity Costs
Under Construction

## Information on Weather Observations and Forecasts
Under Construction


