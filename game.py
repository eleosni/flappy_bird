import arcade as ar
import random

WIDTH = 1280
HEIGHT = 720
TITLE = 'flappy_bird'

map_scale = 0.7
GRAVITY = 0.4
class Menu(ar.View):
    def on_show(self):
 #цвет заднего фона
        ar.set_background_color(ar.color.ICEBERG)
    def on_draw(self):
        pic = ar.load_texture("resources/Images/phone.png")
        width, height = self.window.get_size()
        self.window.set_viewport(0, width, 0, height)
        ar.draw_texture_rectangle(width/2, height/2, width, height, pic)
        ar.draw_text("Нажмите enter для старта", width/2, height - 100, ar.color.RED, 30, anchor_x="center")
        ar.draw_text("Нажмите E для хода", width/2, height - 200, ar.color.RED, 30, anchor_x="center")
        ar.draw_text("Нажмите Win+D для выхода из полноэкранного режима", width/2, height - 300, ar.color.RED, 30, anchor_x="center")
    def on_key_press(self, key, modifiers):
        if key == ar.key.F:
 #возврат в обычный режим окна
            self.window.set_fullscreen( not self.window.fullscreen )
 #обратный возврат в полноэкранный режим
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)
        if key == ar.key.ENTER:
            mygame = Mygame()
            mygame.setup()
            self.window.show_view(mygame)
# основной class
class Mygame(ar.View):
    # метод(функция) инициализации (создания переменных)
    def __init__(self):
        super().__init__()
        self.timer = 0
        #команда для полноэкранного режима 
        #width, height = self.get_size()
        #self.set_viewport(0, width, 0, height)
        
        self.block_list = None
        self.enemy_list = None

        self.player = None
        self.Physics_engine = None
    
        self.record = 0

        #  переменные для движения экрана   
        self.view_left = 0
        self.view_bottom = 0
        self.restart = 1 #переменная подсчета попыток
        self.background_music = ar.load_sound("resources/audio/Catch.mp3")
        self.background_music.play(0.5)

    # метод установки начальных значений
    def setup(self):
        ar.set_background_color(ar.color.BLUE_SAPPHIRE)  

        self.block_list = ar.SpriteList() # добавление в список
        self.trub_list = ar.SpriteList()
        self.collision_list = ar.SpriteList()
        self.point_list = ar.SpriteList()

        self.music_list = ["resources/audio/Jump_1.mp3", "resources/audio/Jump_2.mp3",  "resources/audio/End.mp3", "resources/audio/point_1.mp3" ]
        self.music_jump = ar.Sound(self.music_list[0])
        self.music_point = ar.Sound(self.music_list[2])
        self.music_end = ar.Sound (self.music_list[3])

        self.hp = 1

        self.score = 0
        my_map = "resources/maps/map_3.json"
        self.tile_map = ar.load_tilemap(my_map, map_scale)
        self.scene = ar.Scene.from_tilemap(self.tile_map)

    

        # Код для загрузки слоев
        # 1) присвоение переменной слоя
        # 2) присвоение списком переменной со слоем
        # block_layer_name = 'block'
        self.block_list = self.tile_map.sprite_lists['block']

        # trub_layer_name = 'trub'
        self.trub_list = self.tile_map.sprite_lists['trub']
        # point_layer_name = 'point'
        self.point_list = self.tile_map.sprite_lists['point']

        self.player = ar.Sprite('resources/Images/yellowbird-upflap.png',0.9)
        self.player.center_x = 50
        self.player.center_y = 400

        # код добавления физики
        self.Physics_engine = ar.PhysicsEnginePlatformer(self.player, self.block_list, GRAVITY)

    # метод зарисовки
    def on_draw(self):
        ar.start_render()
        self.player.draw()
        self.trub_list.draw()
        self.block_list.draw()
        ar.draw_text(f'Points:{self.score}',self.view_left + 50, self.view_bottom + 500,ar.color.YELLOW_ORANGE,20)
        ar.draw_text(f'Record:{self.record}',self.view_left + 50, self.view_bottom + 550,ar.color.YELLOW_ROSE,20)
        ar.draw_text(f'Попытка:{self.restart}',self.view_left + 50, self.view_bottom + 600,ar.color.YELLOW_ROSE,20)
        if self.restart == 6:
           ar.draw_text("Вы исчерпали 5 попыток, начните игру заново", self.view_left+WIDTH/2, self.view_bottom+HEIGHT/2, ar.color.RED,30, anchor_x="center")

    # метод обновления внутри игры
    def update(self,delta_time):
        if self.hp <= 0:
            return
        self.player.update()
        self.Physics_engine.update()
        if self.score >= self.record:
            self.record = self.score
      
      

        if True:
            # движение экрана с игроком
            ar.set_viewport(self.view_left,WIDTH + self.view_left,self.view_bottom ,HEIGHT +self.view_bottom)

            # движение экрана вправо
            right_boundary = self.view_left + WIDTH - 640
            if self.player.right > right_boundary:
                # if self.player.right < 984: # условие остановки передвижения экрана
                    self.view_left += self.player.right - right_boundary

            left_boundary = self.view_left + 200
            if self.player.left < left_boundary:
                 if self.player.left > 200:  # условие остановки передвижения экрана
                    self.view_left -= left_boundary - self.player.left

    # команда для передвижения экрана
        for trub in self.trub_list:
            if ar.check_for_collision(trub,self.player):

               self.restart +=1
               self.setup()
               self.view_left = 0
               self.music_end.play()


        for point in self.point_list:
            if ar.check_for_collision(point,self.player):

                self.score += 1
                point.kill()

    # метод управления клавиатурой
    def on_key_press(self,key,modifiers):
        if key == ar.key.E:
            self.player.change_y = 6
            self.player.change_x = 2
            self.music_jump.play(0.5)
            if self.restart==6:
                self.restart =1
                self.record = 0
                self.setup()
                self.music_end.play()
 
        if key == ar.key.F:
 #возврат в обычный режим окна
            self.window.set_fullscreen( not self.window.fullscreen )
 #обратный возврат в полноэкранный режим
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)
       

    # метод для остановки игрока если нет нажатия
    def on_key_release(self,key,modifiers):
        if key == ar.key.E:
            self.player.change_y = 0
        
# основная функция
def main():
    # присвоение к переменной основнго класса
    window = ar.Window(WIDTH,HEIGHT,TITLE, fullscreen=True)
#    window = Mygame(WIDTH,HEIGHT,TITLE)
    

    mygame = Mygame()
    mygame.setup()
    window.show_view(mygame)

 
   
    menu = Menu()
    window.show_view(menu)
    ar.run()

# вызов функции
main()