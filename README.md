![enter image description here](https://e7.pngegg.com/pngimages/405/350/png-clipart-pokemon-logo-pokemon-logo.png)

**This project is the 4th assignment given in the Object Oriented course, Ariel University.**
**The project revolves around implmenting a game which runs on a directed weighted graph**

## ***Results***

|Level|Result| - |Level| Result|
|--|--|--|--|--|
|0| |-|8|67|
|1| |-|9|388|
|2| |-|10|59|
|3| |-|11| 1226|
|4| |-|12|40 |
|5| |-|13|201 |
|6| |-|14 |109 |
|7| |-|15 |250 |

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



---------------------------------------------------------------------------------------------

## **Classes :** 

All information about the graph and GraphAlgo implementation can be found in the link below: 
[Directed Weighted Graphs 3rd assignment link](https://github.com/Netanel94/Ariel-OOP-3)

**Pokemon :**
|Field| Desciption|
|--|--|
| value| The value of the pokemon using a float|
| type| Types of the pokemon: UP and DOWN|
| pos|Postion of the pokemon using tuple |
| edge| The edge in which the pokemon resides on using Source and Destination nodes via tuple|
| agent_inc|Boolean which says if this pokemon was assigned to an agent|
| picked|Boolean if the pokemon was picked by an agent |

**Agent :**
|Field| Desciption|
|--|--|
|ID |ID of an agent |
|Value | The amount of pokemon's value this agent collected|
|Src | The node where the agent is currently on|
|Dest | The node where the agent will go to next|
|Speed |Speed of the agent |
|Pos | Position of an agent using tuple|
|Curr_Path | The path in which the agent should walk on|
|Pokemon_List |The pokemons assigned to this agent |

**Game :**
|Field| Desciption|
|--|--|
| G| Graph|
| Agents| Agents list|
| Pokemons|Pokemon list |
| min_x| Minimum 'x' value|
| min_y|Maximum 'y' value |
| max_x| Minimum 'x' value|
| max_y| Maximum 'y' value|

|Functions| Desciption|
|--|--|
| Scale| Scaling function|
| load_pokemons| Loading the Pokemons from the client|
| duplicate_list| Minor Function to duplicate a list|
| load_agents|  Loading the Agents from the client|
| find_pokemon_edge| A function to find the exact edge in which a specific pokemon resides on|
| check_if_on_edge| A minor worker function of find_pokemon_edge|
| load_graph| Loading the graph from the client|
| drawArrowLine|A function which draws a line|
| update_agent|A functio|
| paint|A function which defines the GUI|
| check_if_poke_list_correct|Checking if the pokemon list is indeed the right pokemon list |
| create_all_list_tuple_permutations|Creating a list which holds all the permutations of a pokemons list using their postion |
| check_agent_pos|Checks the agent current position |

-------------------------------------------------------------------------

## **Pokemon Assign algorhitm :** 

-------------------------------------------------------------------------

## **How to Run :** 
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
