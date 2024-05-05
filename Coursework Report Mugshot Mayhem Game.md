# Coursework Report: Mugshot Mayhem Game

## 1. Introduction

### Application Overview

The application is a 2D arcade-style game called **Mugshot Mayhem**. In this game, players control a character tasked with defeating enemies while avoiding enemy attacks. The game features player movement, shooting mechanics, enemy behavior, collision detection, health management, and a timer to track gameplay duration. The game was made to be simple, challenging and most importantly - fun.

### How to Run the Program

To run the program, ensure that you have *Python* and *Pygame* installed on your system as well as all of the additional *.png* files and *Python* scripts in one directory. Then, execute the **main.py** script using *Python*.

### How to Use the Program

- Use the **'w' 'a' 'd'** keys to move the player character (**'a'** to move left, **'d'** to move right, **'w'** to jump).

- Use **SPACEBAR** to shoot (The **SPACEBAR** can be held down to make the player shoot continuously).

- After completing or loosing the level follow the prompts on screen (**'r'** to restart, **'ENTER'** to continue to the next level).

- You can exit (**'ESCAPE'**) or restart (**'r'**) the game at any time.

  

## 2. Body/Analysis

### Code Structure

My application is split into 7 separate python scripts: 

- **main.py**: this python script is responsible for importing all levels and a timer module to coordinate the game's execution. 

- **level1.py**; **level2.py**; **level3.py**: these scripts contain the game logic for different levels of the game. Each level script contains the specificic mechanics, enemy behavior, and player interactions relevant to that level.
- **assets.py**: this script handles the loading of custom textures from the game folder. It centralizes the asset-loading logic, making it easy to manage and import textures into each level script.
- **timer.py**: this script manages the game timer logic. It handles timing-related functionality such as tracking elapsed time, writing and reading from a file, and keeping track of the best time.
- **test.py**: this script contains tests of the core functions of **level1.py**.



### Object-Oriented Programming (OOP) Pillars

1. **Polymorphism:**  *Polymorphism* allows objects of different classes to be treated as objects of a common superclass. It enables methods to be invoked on objects of different types, with the behavior of the method varying based on the object's type. *Polymorphism* is demonstrated in my application through rays and their behavior depending on the character type. It starts in the **'move'** method in **'Ray'** class (*level1.py*):

   

   ```python
   class Ray(pygame.sprite.Sprite):
   	def move(self):
   		if isinstance(self.owner, Enemy):
   			self.rect.x -= 10
   		else:
   			self.rect.x += 20
   	#Further logic
   ```

   

   Which is then used in the **'update'** method of **'RayGroup'** class:

   

   ```python
   class RayGroup(pygame.sprite.Group):
   	def update(self, obstacles, enemy_alive):
   		for ray in self.sprites():
   			ray.move()
   			#Further logic
   ```

   

   The **'update'** method of the **'RayGroup'** class iterates over all ray objects, regardless of whether they belong to the player or enemy. However, the behavior of the rays differ depending on whether they are associated with a player or an enemy, showcasing the principle of polymorphism.

   

2. **Abstraction:** *Abstraction* involves hiding the implementation details of a class and exposing only essential features or behavior to the outside world. It allows complex systems to be modeled and understood at higher levels of abstraction, focusing on what an object does rather than how it does it. *Abstraction* is achieved through the definition of abstract classes and methods, which provide a blueprint for subclasses to implement. Abstract classes cannot be instantiated directly but can be used to define common behavior shared by multiple subclasses. In my application, *abstraction* is demonstrated with the **'Character'** class. It acts like an abstract blueprint for **'Player'** and **'Enemy'** classes, defining common attributes and methods. However, certain methods within the **'Character'** class are left abstract, meaning they are declared but not implemented. This design choice encourages subclasses to provide their own concrete implementations based on their specific requirements (*level1.py*):

   

   ```python
   class Character(ABC, pygame.sprite.Sprite):
   	@abstractmethod
   	def calculate_health_bar_length(self):
   		pass
   
   	@abstractmethod
   	def calculate_health_bar_color(self):
   		pass
   
   	def draw_health_bar(self, surface):
   	#further logic for drawing the health bar
   ```

   

   Then, **'Player'** and **'Enemy'** subclasses extend the **'Character'** class and provide concrete implementations for the abstract methods **'calculate_health_bar_length'** and **'calculate_health_bar_color'**:

   

   ```python
   class Player(Character):
   	def calculate_health_bar_length(self):
   	#further logic to calculate the length of the health bar
   
   	def calculate_health_bar_color(self):
   	#further logic to calculate the color of the health bar
   
   class Enemy(Character):
   	def calculate_health_bar_length(self):
   	#Further logic to calculate the length of the health bar, that differs from the Player class
   
   	def calculate_health_bar_color(self):
   	#Further logic to calculate the color of the health bar, that differs from the Player class
   ```

   

   This implementation of abstraction allows for a clear separation of concerns, where each class focuses on its specific functionality without exposing unnecessary details to other parts of the program showcasing the principle of *abstraction*.

   

3. **Inheritance:** *Inheritance* allows a class to inherit properties and behavior from another class, known as its superclass or parent class. This enables the creation of a hierarchy of classes, where subclasses or children classes can reuse and extend the functionality defined in their parent classes. In my application the **'Character'** class serves as a superclass that encapsulates common attributes and methods shared by both **'Player'** and **'Enemy'** subclasses. By inheriting from the **'Character'** class, the **'Player'** and **'Enemy'** classes inherit properties such as *position*, *size*, *image* and *health* as well as the **'draw_health_bar'** method which is also used to demonstrate abstraction. Here's a snippet of how *inheritance* is implemented in my code (*level1.py*):

   

   ```python
   class Character(ABC, pygame.sprite.Sprite):
   	def __init__(self, x, y, size, image, health):
   		super().__init__()
   		self.image = image
   		self.rect = self.image.get_rect()
   		self.rect.x = x
   		self.rect.y = y
   		self.size = size
   		self.health = health
   	#Other methods and properties
   
   class Player(Character):
   	def __init__(self, x, y):
   		super().__init__(x, y, 60, player_texture, 5)
   		#Player specific attributes
   	#Player specific attributes and methods
   
   class Enemy(Character):
   	def __init__(self, x, y):
   		super().__init__(x, y, 175, player_texture, 100)
   		#Enemy specific attributes
   	#Enemy specific attributes and methods
   ```

   

   By inheriting from the **'Character'** class, both **'Player'** and **'Enemy'** classes inherit its attributes and methods, allowing them to focus on their unique functionalities without duplicating code showcasing the principle of *inheritance*.

   

4. **Encapsulation:** *Encapsulation* emphasizes restricting direct access to an object's internal components and hiding its internal state from the outside world. In my application, encapsulation primarily focuses on maintaining private attributes within classes, restricting direct access to them from external code:

   

   ```python
   class Player(Character):
   	def __init__(self, x, y):
   		super().__init__(x, y, 60, player_texture, 5)
           self.__speed_x = 5
           self.__speed_y = 0
           self.__gravity = 0.5
           self.jumping = False
           self.shooting = False
           self.__shoot_cooldown = 10
           self.__shoot_timer = 0
   	#Further player attributes and methods
   
   class Enemy(Character):
   	def __init__(self, x, y):
           super().__init__(x, y, 175, player_texture, 100)
           self.__shoot_frequency = 20
           self.__shoot_timer = self.__shoot_frequency
           self.can_shoot = True
           self.enemy_rays = enemy_rays
   	#Further enemy attributes and methods
   ```
   
   
   
   In my application I encapsulate the most important character attributes. It provides controlled access through methods, promotes information hiding and reduces the risk of unintentional modifications to the object's internal state, showcasing the principle of *encapsulation*.
   
   

### Design patterns

My application implements two design patterns: **Factory Method** and **Singleton**. Both of them are implemented in the **'Character Factory'** class (*level1.py*):



```python
class CharacterFactory:
	_instance = None
	def __new__(cls):
	if cls._instance is None:
		 cls._instance = super().__new__(cls)
	return cls._instance
```



This part showcases the **Singleton** design pattern. It ensures that only one instance of the **'CharacterFactory'** class is created throughout the application's lifecycle. This ensures that all calls to **'CharacterFactory'** return the same instance. It is suitable in this situation, because it allows all parts of the program to interact with the same instance, promoting consistency and avoiding duplication of resources. In my application there is also no need to instantiate multiple **'CharacterFactory'** objects, since a single instance can handle all character creation requests. It also simplifies the interaction between different parts of the game logic by providing a single point of access to the character creation functionality. 
*Continuing the code:*



```python
    @staticmethod
    def create_character(character_type, x, y, enemy_rays=None):
    	if character_type == "player":
    		return Player(x, y)
    	elif character_type == "enemy":
    		return Enemy(x, y, enemy_rays)
```



This part showcases the **Factory Method** design pattern. It abstracts the process of object creation, allowing subclasses to alter the type of objects that will be created. The **'create_character'** method acts as a factory for creating instances of different character types. It takes parameters such as *'character_type'*, *'x position'*, *'y position'* and optionally *'enemy_rays'* and returns an instance of the appropriate character type based on the provided *'character_type'*. Characters are created in **'Level1'** class:



```python
self.player = CharacterFactory.create_character("player", 20, ground_height - 60)
self.enemy = CharacterFactory.create_character("enemy", 1350, ground_height - 175, self.enemy_rays)
```



*Factory Method* is a suitable design pattern, since it proved flexibility by encapsulating the object creation logic. It allows for easy extension or modification of the object creation process without altering the code. For example, if new character types need to be added in the future, I would be able to simply extend the **'CharacterFactory'** class and override the **'create_character'** method. This pattern also promotes loose coupling between the client code and the concrete classes. Because the object creation logic is centralized in the **'CharacterFactory'** class, it is easier to maintain and refactor the codebase, as all character creation logic is confined to one place.



### Reading From File & Writing to File

In my application, reading from and writing to files is primarily handled by the **timer.py** script. This script manages the game timer and stores the elapsed time of the last game, as well as the best time in a file named **'time.txt'**. All of the levels and **main.py** import this script to ensure that the timer works and is displayed in the game interface correctly.

The **timer.py** script reads the best time achieved by the player from the **'time.txt'** file:



```python
class Timer:
	def read_best_time_from_file(self, filename='time.txt'):
		try:
			with open(filename, 'r') as file:
				lines = file.readlines()
				if lines:
					return float(lines[-1].strip().split(': ')[1].split(' '[0])
				else:
				return float('inf')
		except FileNotFoundError:
			return float('inf')
```



(If the *time.txt* file is not created, the method returns the best time's default value of infinity and it is displayed as *'N/A'* on-screen)
This script also writes the elapsed time and, if the record is beaten, overrides the best time into the *time.txt* file:



```python
    def write_elapsed_time_to_file(self, elapsed_time, filename='time.txt'):
        try:
            with open(filename, 'w') as file:
                file.write(f"Latest Game's Time: {elapsed_time:.2f} seconds\n")
                file.write(f"Best Time: {self.best_time:.2f} seconds\n")
        except Exception as e:
                print(f"An error occurred: {e}")
```



(If the record is not beaten, the best time stays the same) 
This script ensures persistent storage of time data, allowing players to track their progression and improvements across different sessions of gameplay. It also implements reading from and writing into a file.



### Testing

In my application, testing is crucial to ensure that the game functions correctly and reliably under different scenarios. The **test.py** script serves as a dedicated module for testing the core functionalities of the game, primarily focusing on the **level1.py** script. The testing script tests various aspects, including player movement, shooting mechanics, enemy behavior, collision detection, and overall game logic. By systematically testing these components, I can verify that each feature operates as intended and identify any potential bugs or issues. 



## 3. Results and Summary

### Results

- Result: a working video game.
- The implementation of OOP principles greatly improved the organization and modularity of the codebase, leading to easier maintenance and scalability.
- Design patterns enhanced code flexibility and reusability, enabling efficient creation of game objects and ensuring consistent behavior throughout the application.
- The most challenging part was trying to implement the timer, since it had to operate continuously through 4 different scripts and write the data into a *.txt* file.
- The custom sprite and texture creation was also challenging, since it involved learning how to make pixel art and then scaling it properly to match the hitboxes of the characters.

### Conclusions

My coursework successfully implemented all 4 OOP pillars and 2 design patterns, which led to a well-structured and modular codebase, laying a solid foundation for future enhancements and improvements. In the future, potential enhancements could include adding more levels with unique challenges and environments, introducing new game mechanics and additional characters, as well as refining the user interface and making the game easier to run. Also enhancements could be done to the code itself: splitting level classes into different scripts, reusing classes as well as implementing more design patterns.
The result of my coursework is a simple, yet fully functional video game, containing all the aspects expected in such project.

## 4. Resources

- [Markdown syntax: 'Markdownguide'](https://www.markdownguide.org/basic-syntax/)
- [Polymorphism: 'Stackify'](https://stackify.com/oop-concept-polymorphism/)
- [Python Import from File: 'freeCodeCamp'](https://www.freecodecamp.org/news/python-import-from-file-importing-local-files-in-python/)
- [Encapsulation: 'Geeksforgeeks'](https://www.geeksforgeeks.org/encapsulation-in-python/)
- [Design patterns: 'RefactoringGuru'](https://refactoring.guru/design-patterns/python)

