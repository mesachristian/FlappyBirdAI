# Tutorial Flappy Bird con IA

## DOCUMENTACIÓN
- Neat : [https://neat-python.readthedocs.io/en/latest/]
- Pygame : [https://www.pygame.org/docs/]

1. Definir los objetos que se deben usar.
- Pajaro: Debido a que la solución se realiza con un algoritmo genetico se usan varias instancias de pajaros.
- Tubo: Son los obtaculos que encuentra el pajaro. Tienen movimiento posici,on y longotud.
- Suelo: El suelo al moverse se aprovecha la ventaja de la POO para crear metodos que permitan este efecto visual.

2. Crear el archivo .py 

3. Descargar las librerias
- pygame
- neat
- random
- os
- time

4. Crear las constantes para el tamaño de la ventana e importar las imagenes para volverlas elementos en una variable.

## Clase pajaro

5. Crear la clase Bird con sus constantes.

6. Crear el metodo init el cual tiene los atributos del pajaro
``` PYTHON
def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tilt = 0  
    self.tick_count = 0 # Keeps track of the "time" passed since the bird moved
    self.velocity = 0
    self.height = self.y
    self.image_time_counter = 0
    self.current_image = self.IMAGES[0]  
```

7. Crear el metodo jump que se va a encargar del movimiento del pajaro en el eje y.

8. Crear el metodo move que se llama cada vez que se actualice el frame de la pantalla para actualizar la posición del pajaro.
```PYTHON
    def move(self):
        self.tick_count += 1 # One unit of time passsed

        dy = ( self.velocity*self.tick_count ) + ( 1.5 * self.tick_count**2 ) # Physics ecuation D = Vo*t + (a*t^2)/2

        if dy >= 16: # Trunk the change of displacement for visual effects
            dy = 16

        if dy < 0:
            dy = -2

        self.y += dy

        if dy < 0 or self.y < self.height + 50: # Bird moving up
            if self.tilt < self.ROTATION:
                self.tilt = self.ROTATION

        else: # Bird moving down
            if self.tilt > -90 : 
                self.tilt -= self.ROTATION_VELOCITY
```

9. Crear el metodo get_bird_image que me permite ver la imagen del pajaro para que esta sea renderizada en la pantalla

## Creación del juego

10. Crear la pantalla y el bucle principal del juego.
```PYTHON
    bird = Bird(150,150)
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        update_window(window,bird)
    
    pygame.quit()
    quit()
```

## Creación del pipe

11. Crear la clase pipe con su metodo init.
```PYTHON
class Pipe():
    VELOCITY = 5
    GAP = 200

    def __init__(self,x):
        self.x = x
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        
        self.height = random.randrange(50,400)
        self.top_pipe_position = self.height - self.PIPE_TOP.get_height()
        self.bottom_pipe_position = self.height + self.GAP
```

12. Crear el metodo move
```PYTHON
def move(self):
    self.x -= self.VELOCITY
```

13. Crear un metodo para retornar las imagenes de los pipe de modo que estas puedan ser renderizadas
```PYTHON
    def get_pipe_images(self):
        top_pipe = (self.PIPE_TOP, (self.x,self.top_pipe_position))
        bottom_pipe = (self.PIPE_BOTTOM, (self.x,self.bottom_pipe_position)) 
        return ( top_pipe , bottom_pipe )
```

## Juego
14. Crear metodo de detección de colisiones
```PYTHON
def check_collision(bird : Bird, pipe: Pipe):
    bird_mask = bird.get_mask()
    top_pipe_mask = pipe.get_top_pipe_mask()
    bottom_pipe_mask = pipe.get_bottom_pipe_mask()

    # Distances between bird pixels and pipe pixels
    top_offset = ( pipe.x - bird.x , pipe.top_pipe_position - round(bird.y) )
    bottom_offset = ( pipe.x - bird.x , pipe.bottom_pipe_position - round(bird.y) )

    # Check collision by checking if the pixels overlap
    top_colide = bird_mask.overlap(top_pipe_mask, top_offset)
    bottom_colide = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

    if top_colide or bottom_colide:
        return True
    
    return False
```

## Creación de la clase Base
15. Crear la clase Base y su constructor
```PYTHON
class Base:

    IMAGE = BASE_IMAGE
    VELOCITY = 5

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.IMAGE.get_width()
```

16. La base va a moverse hacia la izquierda y para poder implementar un efecto visual de una base infinita se van a concatenar dos imagenes de la base por lo cual se moveran por un metodo y habra una interfaz que nos permita recuperar la información de la posición en x de ambas bases

```PYTHON
    def move(self):
        self.pos_x_image_1 -= self.VELOCITY
        self.pos_x_image_2 -= self.VELOCITY

        if self.pos_x_image_1 + self.WIDTH < 0:
            self.pos_x_image_1 = self.WIDTH

        if self.pos_x_image_2 + self.WIDTH < 0:
            self.pos_x_image_2 = self.WIDTH

    def get_base_image_and_positions(self):
        pos_image_1 = (self.pos_x_image_1, self.pos_y)
        pos_image_2 = (self.pos_x_image_2, self.pos_y)

        return (self.IMAGE, pos_image_1, pos_image_2)
```

## Juego
17. Crear una lista de pipes y generar nuevos pipes cuando se pasen
18. Chekear colisiones del pajaro con los pipes o el suelo
```PYTHON
        pipes_for_remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            
            if check_collision(bird, pipe):
               pass
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_for_remove.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True 

        if add_pipe : 
            score += 1
            pipes.append(Pipe(WINDOW_WIDTH + 100))

        for pipe in pipes_for_remove:
            pipes.remove(pipe)

        if bird.y + bird.current_image.get_height > 500:
            pass
```

19. Pintar el punatje
```PYTHON
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans",50)
score_label = SCORE_FONT.render("Score: " + str(score),1,(255,255,255))
window.blit(score_label, (WINDOW_WIDTH - score_label.get_width() - 15, 10))
```