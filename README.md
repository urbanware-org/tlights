# tlights

**Table of contents**
*   [Definition](#definition)
*   [Details](#details)
*   [Requirements](#requirements)
*   [Screenshots](#screenshots)
*   [Contact](#contact)

----

## Definition

This is a simple traffic light control demo which simulates typical traffic light behavior.

[Top](#tlights)

## Details

The project consists of a class to create a traffic light object in combination with a picture box (a *QLabel* used as such to be precise). Additionally there is a timer (default *QTimer*) that automates the switching process.

You can either set the traffic light modes manually or automated.

Manual methods:
*   Set red light only
*   Set yellow light only
*   Set red-yellow combination
*   Set green light
*   Power off

Pre-defined automated methods:
*   Switch the traffic light automatically
*   Set the traffic light to standby

The standby mode simply turns off the traffic light and if it is at a yield position, it will flash with its yellow light.

## Requirements

In order to run the project, the *Python* framework (version 2.6 or higher) must be installed on the system.

The graphical user interface is based on *PyQt4*, which must also be installed.

[Top](#tlights)

## Screenshots

The animated screenshots below are from an earlier version, but are almost identical with the current one.

<img src="https://raw.githubusercontent.com/urbanware-org/tlights/master/gif/day.gif" alt="Day" height="400px" width="400x" align="left"/>
<img src="https://raw.githubusercontent.com/urbanware-org/tlights/master/gif/night.gif" alt="Night" height="400px" width="400px"/>

[Top](#tlights)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to <dev@urbanware.org>.

[Top](#tlights)
