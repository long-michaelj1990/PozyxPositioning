#### Tag visulaiser script #### mlong 16/01/2019

import json
# import MQTT package        
import paho.mqtt.client as mqtt 
import pygame

class Point:
#'"' "Just a simple container for XY points"""
    def __init__(self, x,y):
         self.x = x
         self.y = y
tag_ids=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
MINIMUM_COORDINATES= Point(0, 0)
MAXIMUM_COORDINATES = Point(32790, 18232)
SCREEN_WIDTH = 847
SCREEN_HEIGHT = 425
# define the colours to be used for visualisation in RGB format
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0 )
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_PURPLE = (126, 38, 119)
GREY = (20, 20, 20)
GREEN = (42, 89, 59)

TAG_MAIN_COLOR_1 = BLACK
TAG_MAIN_COLOR_2= BLUE
TAG_SECONDARY_COLOR = RED
TAG_HISTORY_MAIN_COLOR = GREY
TAG_HISTORY_SECONDARY_COLOR  = GREEN
fontname = 'freesansbold.ttf'
fontsize = 10
antialias = True
colour = 0,0,0
# Create a class that will save the positions of individual tags, convert them to pixels, as well as visualise them in pygame
class PozyxTag():
#"""Pozyx tags have both an ID, a position, and a small history of their positions"""
    def __init__(self, id_, max_path_size=200):             # tag. something
        self.id = id_
        self.position = Point(0, 0)        
        self.max_path_size = max_path_size
        self.saved_positions = []
    def set_position( self, x, y):
        self.position = Point(int(x), int(y))
    def calculate_pixel_position( self, position):
        pixel_x = (position.x - MINIMUM_COORDINATES.x) / PIXEL_RATIO_X
        pixel_y = (position.y - MINIMUM_COORDINATES.y) / PIXEL_RATIO_Y      
        return [pixel_x, pixel_y]

    @property
    def pixel_position(self):
        return self.calculate_pixel_position(self.position) 
    def draw_history(self):
        for saved_position in self.saved_positions:
            pixel_position=self.calculate_pixel_position(saved_position)   
        pygame.draw.circle(game_display,TAG_HISTORY_MAIN_COLOR,[int(pixel_position[0]),int(pixel_position[1])],4,1)
        pygame.draw.circle(game_display, TAG_HISTORY_SECONDARY_COLOR,[int(pixel_position[0]), int( pixel_position[1])],3,0)
        
    def draw_tag_position(self):
        text=str(self.id)
        pixel_position = self.calculate_pixel_position(self.position)
        font = pygame.font.Font(fontname, fontsize)
        textSurf = font.render(text, antialias, colour)
        if self.id<=7:        
            pygame.draw.circle(game_display, TAG_SECONDARY_COLOR, [ int(pixel_position[0]),
            int(pixel_position[1])], 10, 0)
        else:
            pygame.draw.circle(game_display, TAG_MAIN_COLOR_2, [ int(pixel_position[0]),
            int(pixel_position[1])], 10, 0)
            
        game_display.blit(textSurf, [int(pixel_position[0]-5),
            int(pixel_position[1]-5)])
            
    def display(self):     
        self.saved_positions.append(self.position) 
        # If enough data has been collected, plot the path of the tag
        if len( self.saved_positions) > self.max_path_size:
        # eliminate first element of the array so it does not become too Large
            self.saved_positions.pop(0)
            self.draw_history()
        self.draw_tag_position()

         
# host = "192.168.160.43"
host ="10.0.0.254"
port = 1883
topic = "tagsLive"


        ##Connecting to MQTT ##
def on_connect(client, userdata, flags, rc):
       print(mqtt.connack_string(rc))

def on_message(client, userdata, msg):
      tag_data = json.loads(msg.payload.decode())
      try:
          network_id = tag_data["tagId"]
          for tag in tags:
              if network_id ==str(tag.id):
                  tag.set_position(tag_data["data"]["coordinates"]["x"],tag_data["data"]["coordinates"]["y"])
      except Exception as exception:
                   pass

def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed to topic!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port,keepalive=10000)        ###uncomment when in connected locally
client.subscribe(topic)
client.loop_start()

                        
PIXEL_RATIO_X = (MAXIMUM_COORDINATES.x - MINIMUM_COORDINATES.x) / SCREEN_WIDTH
PIXEL_RATIO_Y = (MAXIMUM_COORDINATES.y - MINIMUM_COORDINATES.y) / SCREEN_HEIGHT
tags = [PozyxTag(tag_id) for tag_id in tag_ids]
pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
floorplan_image = pygame.image.load('netball court2.JPG')

exit_game =False
while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game=True
    game_display.fill(WHITE)

    flooplan = pygame.transform.rotate(floorplan_image,0)
    game_display.blit(floorplan_image,[0,0])

    for tag in tags:
        tag.display()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
