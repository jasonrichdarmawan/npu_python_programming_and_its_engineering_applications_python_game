# How to run the game?

- Type in the terminal `$ python main.py`

   To quit, press `Q` or `esc`.

# How to play the game?

- How to shoot? Press the `spacebar`.
- How to move? Press the `arrows`.
   - `←` to move to the left.
   - `↑` to go up.
   - `→` to move to the right.
   - `↓` to go down.

# Improvement Plan

- [x] Direction Enum
      1. `Direction.LEFT`: Move the fighter jet to the left.
      2. `Direction.RIGHT`: Move the fighter jet to the right.
      3. `Direction.UP`: Move the fighter jet up.
      4. `Direction.DOWN`: Move the fighter jet down.

- [x] Moveable Class
      1. **Definition**: A base class for all moveable objects in the game.
      2. **Attributes**:
         - `speed`: The speed of the object.
         - `x`: The x-coordinate of the object.
         - `y`: The y-coordinate of the object.
      3. **Methods**:
         - `move(direction: Direction)`: Move the object in the specified direction.

- [x] FighterJet Class (inherits from Moveable class)
      1. **Definition**: A fighter jet controlled by the user or AI.
      2. **Attributes**:
         1. `speed`: The speed of the fighter jet.
         2. `bullets_left`: The number of bullets left in the fighter jet.
      3. **Methods**:
         1. `move(direction: Direction)`: Move the fighter jet in the specific direction.
         2. `shoot()`: Fire a bullet from the fighter jet.

- [x] Bullet Class (inherits from Moveable class)
      1. **Definition**: A bullet fired by the fighter jet.
      2. **Attributes**:
         1. `speed`: The speed of the bullet.
         2. `x`: The x-coordinate of the bullet.
         3. `y`: The y-coordinate of the bullet.
         4. `direction`: The direction in which the bullet is moving. This should be one of the values from the `Direction` enum
      3. **Methods**:
         1. `move()`: Move the bullet in its current direction.

- [ ] ArtificialIntelligence Class
      1. **Definition**: An artificial intelligence to control the fighter jet.
      2. **Attributes**:
         1. `fighter_jet`: The fighter jet controlled by the AI.
      3. **Methods**:
         1. `decide_move()`: Decide the direction to move the fighter jet to avoid bullets or other aircraft.
         2. `decide_shoot()`: Decide whether to shoot to hit other aircraft.
         3. `execute()`: Execute the decided actions (move and shoot).

- [x] GameEngine Class
      1. **Definition**: The core logic of the game.
      2. **Methods**:
         1. `check_collisions()`: Detect and handle collisions between bullets and fighter jets or between fighter jets.
            1. `check_collision(obj1, obj2)`: Check if obj1 and obj2 collide.
            2. `handle_collision(obj1, obj2)`: Handle the collision between obj1 and obj2.
      2. `update()`: Update the game state, including moving objects and checking for collisions.
      3. `render()`: Render the game objects on the screen.