# Artificial Intelligence - PacMan

## Intro

[The Pacman Projects](http://ai.berkeley.edu/project_overview.html) by the University of California, Berkeley.

![](https://camo.githubusercontent.com/0f3f9a6773aec44f398aa1934aeef75e760fd96538b99ddb3ae28f2e53affead/687474703a2f2f61692e6265726b656c65792e6564752f696d616765732f7061636d616e5f67616d652e676966)

> In this project, Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. Try to build general search algorithms and apply them to Pacman scenarios.

Start a game by the command:

    $ python pacman.py

You can see the list of all options and their default values via:

    $ python pacman.py -h


## HW1 Search  
In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.  

* DFS  

        $ python pacman.py -l tinyMaze -p SearchAgent
        $ python pacman.py -l mediumMaze -p SearchAgent
        $ python pacman.py -l bigMaze -z .5 -p SearchAgent 
     
* BFS

        $ python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
        $ python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
        
* UCS

        $ python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
        $ python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
        $ python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
        
* Astar

        $ python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic 
        
* Corner problem, Corner heuristic  
    
        $ python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem  
        $ python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5  
    
* Eating all the dots  
    
        $ python pacman.py -l trickySearch -p AStarFoodSearchAgent  

## HW2 Multi-Agent
In this project, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will implement both minimax and expectimax search and try your hand at evaluation function design.  

## HW3 Reinforcement Learning
In this project, you will implement value iteration and Q-learning. You will test your agents first on Gridworld (from class), then apply them to a simulated robot controller (Crawler) and Pacman.

## Credits  
This is the homework project for the course CSE511 Introduction to Artificial Intelligence (2020 Fall), at Washington University in St. Louis
Instructor:  William Yeoh
