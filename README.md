![enter image description here](https://www.pngfind.com/pngs/m/685-6856951_pokemon-gotta-catch-em-all-hd-png-download.png)

**This project is the 4th assignment given in the Object Oriented course, Ariel University.**
**The project revolves around implmenting a game which runs on a directed weighted graph**

## ***Results***

|Level|Result| - |Level| Result|
|--|--|--|--|--|
|0|100 |-|8|67|
|1|437 |-|9|388|
|2|164 |-|10|59|
|3|602 |-|11| 1226|
|4|67 |-|12|40 |
|5|392|-|13|201 |
|6| 52|-|14 |109 |
|7| 302|-|15 |250 |

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


## **How to run :** 
- Download the files.
- Copy the path to the jar file location.
- Pick either one of the exsisting graphs inside the data file (G1, G2, G3).
- Open cmd and type the following :
```console
cd src
```
- Now type in the terminal : (please notice that you need to choose a number between 0-15 to pick the level wanted)
```console
java -jar Ex4_Server_v0.0.jar 0-15
```
