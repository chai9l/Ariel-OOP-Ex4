![enter image description here](https://i.imgur.com/mSCTk6k.png)

**This project is the 4th assignment given in the Object Oriented course, Ariel University.**
**The project revolves around implmenting a game which runs on a directed weighted graph**

![gif](https://i.imgur.com/cuIxGdE.gif)

## ***Results***

|Level|Result| - |Level| Result|
|--|--|--|--|--|
|0|125 |-|8|58|
|1|344 |-|9|415|
|2|214 |-|10|159|
|3|636 |-|11| 1174|
|4|146 |-|12|40 |
|5|429|-|13|256 |
|6| 79|-|14 |159 |
|7| 337|-|15 |292 |

# **Classes**
In this section you can find a variety of classes and their methods with a brief explanation on what the method do.
|Class| Desciption|
|--|--|
|DiGraph| This class represents the Graph in which the game "map" is played on|
|GraphAlgo|This class represents the algorithms that work on our graph aka game map|
|Pokemon|This class represents the Pokemons that are needed to be picked on the game map|
|Agent|This class represents the Agents which move towards the pokemons to collect them|
|client|This class holds all the game's information, i.e number of agents for a specific level etc..|
|game|This class represents the game itself.|


## **How to Run :** 
**Option 1 :**
- Download the files.
- Open the python's terminal
- Now type in the terminal : 
(Please notice that you need to choose a number between 0-15 to pick the level wanted)
```console
java -jar Ex4_Server_v0.0.jar 0-15
```
- Hit the run button

**Option 2:**
- Download the files.
- Open two cmd windows.
- In window number one, type:

(*Please notice that Path represents the path to the Ex4 folder on you'r computer*)

(*Please notice that you need to choose a number between 0-15 to pick the level wanted*)

```console
cd Path
Ex4_Server_v0.0.jar 0-15
```
![serverboot](https://i.imgur.com/lQQkETO.png)
- In window number two, type:
```console
python Game.py
```
![gameboot](https://i.imgur.com/34kHmIX.png)
