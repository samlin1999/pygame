import pygame, sys, time, random
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
pygame.init()

#初始化設定#####################################################################################
#登入音樂
pygame.mixer.music.load("sign in.mp3")
#單位寬與高
width = 60
height = 60
#視窗單位寬與高個數
display_width_num = 25
display_height_num = 15
#角色長與寬
role_width = 90
role_height = 90
#遊戲畫面寬與高個數
width_num = 15
height_num = 13
#視窗大小
display_width = width*display_width_num
display_height = height*display_height_num
#宣告視窗gameDisplay
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('爆爆王')
clock = pygame.time.Clock()
#顏色
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
dark_red = (200,0,0)
green = (0,200,0)
bright_green = (0,255,0)
#遊戲進行速度的單位 (可調整) 目前(半秒)

TIME = pygame.USEREVENT + 1
pygame.time.set_timer(TIME, 500) #遊戲進行速度
#抓取輸入
def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass
def display_box(screen, message):
    #"Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font('123.ttf',18)
    pygame.draw.rect(screen, (200,200,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) + 100,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) + 100,
                    204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (0,0,0)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) +100))
    pygame.display.flip()

def ask(screen, question):
  #"ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string))
  while True:
    inkey = get_key()
    print(inkey)
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    print(current_string)
    display_box(screen, question + ": " + "".join(current_string))
  str = ""
  for c in current_string:
    str = str + c
  print(str)
  return str
#遊戲文字
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("123.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
player_1_name = ""
player_2_name = ""
#遊戲登入畫面
def game_intro():
    global player_1_name, player_2_name
    background = pygame.image.load("background.png")
    screen1 = pygame.transform.scale(background,(display_width,display_height))
    screen = pygame.display.set_mode((display_width,display_height))
    pygame.mixer.music.play(-1)
    screen.blit(screen1,(0,0))
    
    player_1_name = ask(screen, "player1")
    print(player_1_name)
    player_2_name = ask(screen, "player2")
    print(player_2_name)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(screen1,(0,0))
        #screen.fill(white)
        largeText = pygame.font.Font("123.ttf",100)
        TextSurf, TextRect = text_objects("bomb-man", largeText)
        TextRect.center = ((320),(100))
        screen.blit(TextSurf, TextRect)
        
        button("start",300,800,100,50,green,bright_green,game_loop)
        button("end",700,800,100,50,red,dark_red,quitgame)
        
        pygame.display.update()
        clock.tick(15)    
def quitgame():
    pygame.quit()
    quit()   
def game_loop():

	#選擇地圖 (可改變使用的地圖)
	map_number = 1#2
	#map1背景音樂
	pygame.mixer.music.load("01海盜.mp3")
	#map2背景音樂
	#pygame.mixer.music.load("02村莊.mp3")
	pygame.mixer.music.play(-1)
	max_niddle_num = 3
	#本局每位角色
	max_bomb_num = 5 #同一時間持有最大炸彈數
	max_bomb_range = 5 #同一時間最大炸彈爆炸距離
	max_player_speed = 10 #角色速度上限

	#初始化地圖##可做成選擇地圖(關卡)#####(一個關卡包含 1.背景地圖(打底) 2.地圖物件 3.地圖掉落道具(可隨機，可手控))
	class map_object():
		pass
	global times 
	times = 0
	

	#建造地圖
	map = [] #地圖lsit

	#map01##包含 1 背景地圖 2 物件地圖 3 道具地圖#############################
	#背景地圖(打底) (只有將圖片放上去)
	map_1_0 =  [ 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #1
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #2
				 1, 1, 1, 1, 1, 1,12,12,12, 1, 1, 1, 1, 1, 1, #3
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #4
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #5
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #6
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #7
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #8
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #9
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #10
				 1, 1, 1, 1, 1, 1,12,12,12, 1, 1, 1, 1, 1, 1, #11
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1, #12
				 1, 1, 1, 1, 1, 1,10,11,10, 1, 1, 1, 1, 1, 1] #13
				 
	#地圖物件 (放置圖片, 可否行走, 可否破壞, 是否有掉落物)
	map_1 =[ 1, 1, 2, 3, 2, 6,10,11, 9, 6, 8, 2, 8, 2, 8, #1
			 1, 4, 9, 4, 9, 7, 9,11,10, 7, 2, 3, 2, 3, 2, #2
			 3, 2, 3, 2, 3, 6,12, 9, 9, 6, 8, 9, 8, 9, 8, #3
			 9, 4, 9, 4, 9, 7, 9,11,10, 7, 3, 2, 3, 2, 3, #4
			 2, 3, 2, 3, 2, 6,10,11, 9, 6, 8, 9, 8, 9, 8, #5
			 3, 4, 3, 4, 3, 7, 9, 9,10, 1, 2, 3, 2, 3, 2, #6
			 7, 6, 7, 6, 7, 6,10,11, 9, 6, 7, 6, 7, 6, 7, #7
			 2, 3, 2, 3, 2, 1, 9,11,10, 7, 2, 4, 2, 4, 2, #8
			13, 9,13, 9,13, 6,10, 9, 9, 6, 3, 2, 3, 2, 3, #9
			 3, 3, 3, 2, 3, 7, 9,11,10, 7, 9, 4, 9, 4, 9, #10
			13, 9,13, 9,13, 6,12,12, 9, 6, 2, 3, 2, 3, 2, #11
			 2, 3, 2, 3, 2, 7, 9, 9,10, 7, 9, 4, 9, 4, 1, #12
			13, 9,13, 9,13, 6,10,11, 9, 6, 3, 2, 3, 1, 1] #13
			
	#掉落物地圖 (只能使用一次(第一次掉落物)) #-1無or掉落過 #0隨機(包含無) #1水球 #2神奇藥水 #3溜冰鞋 #4烏龜 #5飛碟
	prop_map_1=[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #1
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #2
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #3
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #4
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #5
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #6
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #7
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #8
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #9
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #10
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #11
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #12
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #13
				 

	#map02##包含 1 背景地圖 2 物件地圖 3 道具地圖#############################
	#背景地圖(打底) (只有將圖片放上去)
	map_2_0 =  [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, #1
				 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, #2
				 1, 1, 1, 1, 1, 1,10,10,10,10,10,10,11,10,10, #3
				 1, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, 1,10, #4
				 1, 1, 1, 1,10,10,10,10,10,10,10, 1, 1, 1, 1, #5
				 1, 1, 1, 1,10, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, #6
				10,10,10,11,10, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, #7
				 1, 1, 1, 1,10, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, #8
				 1, 1, 1, 1,10, 1, 1, 1,10,10,10, 1, 1, 1, 1, #9
				 1, 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, #10
				 1, 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, #11
				 1, 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, #12
				 1, 1, 1, 1,10, 1, 1, 1,11, 1, 1, 1, 1, 1, 1] #13
				 
	#地圖物件 (放置圖片, 可否行走, 可否破壞, 是否有掉落物)
	map_2 =[ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, #1
			 7, 7, 6, 7, 6, 4, 1, 7, 1, 8, 1, 4, 1, 7,10, #2
			 7, 6, 7, 6, 6, 1, 9,10, 9,10, 3,10, 3,10,10, #3
			 7, 7, 6, 7, 6, 8,10,13,13, 4, 1, 8, 1,13,10, #4
			 7, 6, 6, 6, 3, 2, 3,10, 3, 2, 3, 1, 6, 7, 7, #5
			 7, 8, 8,13, 2, 4, 6,13, 6,13,10,13, 6, 7, 7, #6
			10,10,10,10, 3, 6, 6, 6, 6, 2,10, 1, 6, 7, 7, #7
			 7,13, 1,13, 2, 8, 6,13, 6, 4, 2,13, 6, 7, 7, #8
			 7, 6, 6, 1, 3, 1, 1, 1, 3,10, 3, 1, 6, 7, 7, #9
			 7, 7, 6, 8, 2,13, 6, 4, 2, 8, 2, 4, 1, 7, 7, #10
			 7, 6, 6, 1, 3, 4, 6, 1, 3, 1, 3, 1, 2, 7, 7, #11
			 7, 7, 6, 4,13, 4, 6, 7,10,13, 1, 8, 1, 7, 7, #12
			 7, 7, 7, 7, 7, 7, 7, 7,10, 7, 7, 7, 7, 7, 7] #13
			
	#掉落物地圖 (只能使用一次(第一次掉落物)) #-1無or掉落過 #0隨機(包含無) #1水球 #2神奇藥水 #3溜冰鞋 #4烏龜 #5飛碟
	prop_map_2=[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #1
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #2
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #3
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #4
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #5
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #6
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #7
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #8
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #9
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #10
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #11
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #12
				 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #13
	#建造針 復活次數
	niddle_1 = pygame.image.load('niddle.png')
	niddle_1_Img = pygame.transform.scale(niddle_1,(width,height))
	
	
	#建造角色  (可做成選角)######################
	role_1 = pygame.image.load('role01.png')
	role_1_Img = pygame.transform.scale(role_1,(role_width,role_height))
	role_2 = pygame.image.load('role02.png')
	role_2_Img = pygame.transform.scale(role_2,(role_width,role_height))

	#角色騎乘後
	role_1_ride = pygame.image.load('ride_turtle01.png')
	role_1_ride_Img = pygame.transform.scale(role_1_ride,(role_width,role_height + 30))
	role_2_ride = pygame.image.load('ride_turtle02.png')
	role_2_ride_Img = pygame.transform.scale(role_2_ride,(role_width,role_height + 30))
	role_3_ride = pygame.image.load('ride_ufo01.png')
	role_3_ride_Img = pygame.transform.scale(role_3_ride,(role_width,role_height + 30))
	role_4_ride = pygame.image.load('ride_ufo02.png')
	role_4_ride_Img = pygame.transform.scale(role_4_ride,(role_width,role_height + 30))

	#死亡
	die_1 = pygame.image.load('dead01.png') #死亡動畫1
	die_1_Img = pygame.transform.scale(die_1,(role_width,role_height))
	die_2 = pygame.image.load('dead02.png')	#死亡動畫2
	die_2_Img = pygame.transform.scale(die_2,(role_width,role_height))

	#道具#(可做成本局是否開放此道具)#######################################################################################
	#水球 可以增加裝置水泡的數量
	prop_1 = pygame.image.load('prop01.png')
	prop_1_Img = pygame.transform.scale(prop_1,(width,height))
	#神奇藥水 可以使水球力量增加一格
	prop_2 = pygame.image.load('prop02.png')
	prop_2_Img = pygame.transform.scale(prop_2,(width,height))
	#溜冰鞋 使人物移動速度增加
	prop_3 = pygame.image.load('prop03.png')
	prop_3_Img = pygame.transform.scale(prop_3,(width,height))
	#烏龜  有機率乘坐慢慢的烏龜，也有機率乘坐到快速的烏龜
	prop_4 = pygame.image.load('prop04.png')
	prop_4_Img = pygame.transform.scale(prop_4,(width,height))
	slow_turtle_speed = 2 
	fast_turtle_speed = 12
	#飛碟 可飛越磚塊
	prop_5 = pygame.image.load('prop05.png')
	prop_5_Img = pygame.transform.scale(prop_5,(width,height))
	ufo_speed = 12
	prop_num = 5 #道具總數 (新增道具時須調整)否則無法隨機掉落道具


	#背景類型##分為可破壞物件和不可破壞物件##可行走物件和不可行走物件##有掉落物物件和無掉落物物件
	#綠磚 背景 不可破壞
	bkg_1 = pygame.image.load('bkg_01.png') 
	bkg_1_Img = pygame.transform.scale(bkg_1,(width,height))
	#紅磚 可破壞
	bkg_2 = pygame.image.load('bkg_02.png') 
	bkg_2_Img = pygame.transform.scale(bkg_2,(width,height + 10))
	#橘磚 可破壞
	bkg_3 = pygame.image.load('bkg_03.png') 
	bkg_3_Img = pygame.transform.scale(bkg_3,(width,height + 10))
	#紅屋 可破壞
	bkg_4 = pygame.image.load('bkg_04.png') 
	bkg_4_Img = pygame.transform.scale(bkg_4,(width,height + 30))
	#樹叢 可破壞
	bkg_6 = pygame.image.load('bkg_06.png') 
	bkg_6_Img = pygame.transform.scale(bkg_6,(width,height + 30))
	#樹 可破壞
	bkg_7 = pygame.image.load('bkg_07.png') 
	bkg_7_Img = pygame.transform.scale(bkg_7,(width,height + 30))
	#黃屋 可破壞
	bkg_8 = pygame.image.load('bkg_08.png') 
	bkg_8_Img = pygame.transform.scale(bkg_8,(width,height + 30))
	#木箱 可破壞
	bkg_9 = pygame.image.load('bkg_09.png') 
	bkg_9_Img = pygame.transform.scale(bkg_9,(width,height + 10))
	#柏油1 不可破壞
	bkg_10 = pygame.image.load('bkg_10.png') 
	bkg_10_Img = pygame.transform.scale(bkg_10,(width,height))
	#柏油2 不可破壞
	bkg_11 = pygame.image.load('bkg_11.png') 
	bkg_11_Img = pygame.transform.scale(bkg_11,(width,height))
	#柏油3 不可破壞
	bkg_12 = pygame.image.load('bkg_12.png') 
	bkg_12_Img = pygame.transform.scale(bkg_12,(width,height))
	#藍屋 可破壞
	bkg_13 = pygame.image.load('bkg_13.png') 
	bkg_13_Img = pygame.transform.scale(bkg_13,(width,height + 30))

	#建造水球############################## 
	bomb_1 = pygame.image.load('ball01.png') #水球動畫1
	bomb_1_Img = pygame.transform.scale(bomb_1,(50,50))
	bomb_2 = pygame.image.load('ball02.png') #水球動畫2
	bomb_2_Img = pygame.transform.scale(bomb_2,(50,50))

	#爆炸#############################################################
	#爆炸衝擊波(中)
	explo_center = pygame.image.load('explosion_center.png') 
	explo_center_Img = pygame.transform.scale(explo_center,(width,height))
	#爆炸衝擊波(左)
	explo_left = pygame.image.load('explosion_left.png') 
	explo_left_Img = pygame.transform.scale(explo_left,(width,height))
	#爆炸衝擊波(右)
	explo_right = pygame.image.load('explosion_right.png') 
	explo_right_Img = pygame.transform.scale(explo_right,(width,height))
	#爆炸衝擊波(上)
	explo_up = pygame.image.load('explosion_up.png') 
	explo_up_Img = pygame.transform.scale(explo_up,(width,height))
	#爆炸衝擊波(下)
	explo_down = pygame.image.load('explosion_down.png') 
	explo_down_Img = pygame.transform.scale(explo_down,(width,height))

	#初始化物件地圖##炸彈地圖##角色設定(皆可手動調整)###################################
	bomb = []
	class ball_detail():
		pass
	for i in range(0, height_num, 1):
		for j in range(0, width_num, 1):
			temp = map_object()
			if map_number == 1:
				temp.bkg = map_1[i*width_num+j] #背景類型
			elif map_number == 2:
				temp.bkg = map_2[i*width_num+j] #背景類型
			temp.bkg_alive = True #背景物件是否存在 (爆炸炸掉後的和無皆為False)
			temp.walk = True #角色是否可行走
			temp.fly = True #角色使否可以飛越
			temp.x = j*width + 5*width #二維矩陣位置
			temp.y = i*height + height #二維矩陣位置
			temp.bomb = False #是否有水球
			temp.explosion = False #是否有爆炸 觸發爆炸衝擊波
			temp.prop = False #道具
			temp.player_1 = False #角色1位置
			temp.player_2 = False #角色2位置
			temp.destroy = False #地圖物件可否破壞
			temp.prop = False #地圖物件是否有掉落物
			temp.drop = False #地圖物件是否要掉落道具(物件死亡後觸發)
			temp.prop_type = 0 #道具種類
			temp.prop_time = 0 #道具出現時間(執行道具動畫用)
			map.append(temp)
			
			ball = ball_detail()
			ball.Img = bomb_1_Img #炸彈動畫1
			ball.Img2 = bomb_2_Img #炸彈動畫2
			ball.player_1 = False #炸彈所屬
			ball.player_2 = False #炸彈所屬
			ball.type = 3 #炸彈種類(外觀)(未使用 預留)
			ball.time = 0 #炸彈放下時間
			ball.delay = 3 #爆炸倒數計時
			ball.explosion = False #炸彈爆炸
			ball.explosion_dir = 'empty' #衝擊波是否存在(方向 left right center up down)
			ball.explosion_delay = 1 #衝擊波存在時間
			ball.explosion_time = 0 #衝擊波出現時間
			ball.x_range = 1 #衝擊波x距離
			ball.y_range = 1 #衝擊波y距離
			ball.alive = False #炸彈是否存在
			bomb.append(ball)
			
	
	class root():
		pass
	
	#角色初始化#### 可調整
	player_1 = root()
	player_1.role = role_1_Img #角色圖片 (可做成換角色)
	player_1.type = 1 # (沒用到)
	if map_number == 1:
		player_1.x = 5*width + width/2 #角色x 
		player_1.y = height + height/2 #角色y
	elif map_number == 2:
		player_1.x = 5*width + width/2 #角色x 
		player_1.y = height * 7 + height/2 #角色y
	player_1.x_change = 0 #角色移動距離(按鍵時改變)
	player_1.y_change = 0 #角色移動距離(按鍵時改變)
	player_1.speed = 5 #角色移動速度
	player_1.i = 0 #角色在map中的位置
	player_1.j = 0 #角色在map中的位置
	player_1.bomb = False #角色是否再放置炸彈
	player_1.bomb_maxnum = 1 #角色放置炸彈最大數
	player_1.bomb_num = player_1.bomb_maxnum #角色持有炸彈數(同一時間放置炸彈數量)
	player_1.bomb_range = 1 #角色炸彈衝擊波距離
	player_1.bomb_delay = 6 #角色炸彈距離爆炸時間 (時間為遊戲單位可調整)
	player_1.alive = True #角色是否存活
	player_1.niddle = max_niddle_num #角色復活次數
	player_1.die = False #角色死亡判斷(遊戲勝利條件)
	player_1.dead_Img = die_1_Img #角色死亡圖片
	player_1.time = 0 #死亡動畫運算時間
	player_1.ride_turtle_Img = role_1_ride_Img
	player_1.ride_ufo_Img = role_3_ride_Img
	player_1.ride = 0 #騎乘
	player_1.ride_speed = 0 #騎乘後移動速度
	player_1.ride_die = False

	#同上
	player_2 = root()
	player_2.role = role_2_Img #角色圖片
	player_2.type = 1 #角色
	if map_number == 1:
		player_2.x = width * (width_num+4) + width/2
		player_2.y = height * height_num + height/2
	elif map_number == 2:
		player_2.x = width * (width_num+4) + width/2
		player_2.y = height * 3 + height/2
	player_2.x_change = 0
	player_2.y_change = 0
	player_2.speed = 5
	player_2.i = 0
	player_2.j = 0
	player_2.bomb = False
	player_2.bomb_maxnum = 1
	player_2.bomb_num = player_2.bomb_maxnum
	player_2.bomb_range = 1
	player_2.bomb_delay = 6
	player_2.alive = True
	player_2.niddle = max_niddle_num #角色復活次數
	player_2.die = False
	player_2.dead_Img = die_1_Img
	player_2.time = 0
	player_2.ride_turtle_Img = role_2_ride_Img
	player_2.ride_ufo_Img = role_4_ride_Img
	player_2.ride = 0 #騎乘
	player_2.ride_speed = 0 #騎乘後移動速度
	player_2.ride_die = False

	

	clock = pygame.time.Clock()
	crashed = False
	font = pygame.font.Font('123.ttf', 30)

	###以上式初始化#####################################################################################

	####draw 和 check#############################################################################################
	#原則上 draw 之前都會有 check 所有動畫皆發生在draw

	##繪製遊戲畫面(核心) ##所有物件繪製和判斷依據
	def draw_map(type):
		for i in range(0, height_num, 1):
			for j in range(0, width_num, 1):
				base_bkg(i, j, 0)
				if type == 0:
					check_destroy_bkg(i, j)
					check_bkg_type(i, j)
					check_prop_type(i, j)
					#text = font.render(str(map[i*width_num+j].bkg_alive), True, (0, 128, 0))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
					#text = font.render(str(bomb[i*width_num+j].explosion_dir), True, (0, 128, 0))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
					#text = font.render(str(map[i*width_num+j].destroy), True, (0, 128, 0))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
					#text = font.render(str(map[i*width_num+j].prop_type), True, (0, 128, 0))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
					#text = font.render(str(map[i*width_num+j].prop_type), True, (0, 128, 0))
					#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
			for j in range(0, width_num, 1):
				check_player_locate(j, i, player_1)
				check_player_locate(j, i, player_2)
				#text = font.render(str(map[i*width_num+j].bomb), True, (0, 128, 0))
				#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
				check_explosion(j, i)
				draw_bomb(j, i)
				#if map[i*width_num+j].bomb == True:
					#if bomb[i*width_num+j].alive == True:
						#text = font.render(str(bomb[i*width_num+j].time), True, (0, 0, 0))
						#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))
						#text = font.render(str(map[i*width_num+j].fly), True, (0, 0, 0))
						#gameDisplay.blit(text, (map[i*width_num+j].x, map[i*width_num+j].y))

	#角色########################################################################################
	#判斷角色位置在地圖中的位置 包含被炸彈炸到判斷 吃到道具判斷
	def check_player_locate(x, y, player):
		if 5*width + width*x + role_width/2 <= player.x + role_width/2 < width*6 + width*x + role_width/2 and height + height*y + role_height <= player.y + role_height < height*2 + height*y + role_height:
			draw_rect(x, y)
			check_hit(x, y, player)
			chech_get_prop(y, x, player)
			if map[y*width_num+x].bkg != 6:
				draw_player(player.x, player.y, player.role, player)
			if player == player_1:
				map[y*width_num+x].player_1 = True
				player_1.i = y
				player_1.j = x
			elif player == player_2:
				map[y*width_num+x].player_2 = True
				player_2.i = y
				player_2.j = x
			if player.bomb == True:
				check_bomb(x, y, player)
		else:
			if player == player_1:
				map[y*width_num+x].player_1 = False
			if player == player_2:
				map[y*width_num+x].player_2 = False

	#繪製角色
	def draw_player(x, y, Img, player):
		if player.alive == True:
			x = x - role_width/2
			y = y - role_height
			if player.ride == 0:
				gameDisplay.blit(Img, (x,y))
			elif player.ride == 1:
				gameDisplay.blit(player.ride_turtle_Img, (x,y - 30))
			elif player.ride == 2:
				gameDisplay.blit(player.ride_ufo_Img, (x,y - 30))
			
	#角色碰觸衝擊波
	def check_hit(x, y, player):
		if bomb[y*width_num + x].explosion_dir != 'empty':
			if bomb[y*width_num+x].explosion_time + bomb[y*width_num+x].explosion_delay > times:
				if player.ride == 0:
					player.alive = False
					if player.niddle <= 0:
						player.die = True
				else:
					player.ride_die = True
				
			elif player.ride_die == True:
				player.ride = 0
				player.ride_die = False

	#繪製角色死亡動畫
	def draw_player_dead(player):
		if player.alive == False:
			x = 0
			y = 0
			if times - player.time != 1:
				player.time = times
				x = player.x - role_width/2
				y = player.y - role_height/2 - role_height/3 + 5

			else:
				x = player.x - role_width/2
				y = player.y - role_height/2 - role_height/3 - 5
			gameDisplay.blit(player.dead_Img, (x,y))
			gameDisplay.blit(die_2_Img, (x,y - height/2))
	#道具############################################################################################
	#判斷道具種類
	def check_prop_type(i, j):
		if map[i*width_num+j].prop == True and map[i*width_num+j].drop == True:
			if map_number == 1:
				if prop_map_1[i*width_num+j] == 0:
					map[i*width_num+j].prop_type = random.randint(0, prop_num)
					prop_map_1[i*width_num+j] = -1
					print('prop ' + str(map[i*width_num+j].prop_type))
				# map.prop_type #0無 #1水球 #2神奇藥水 #3溜冰鞋 #4烏龜 #5飛碟
				if prop_map_1[i*width_num+j] == 0: #無
					map[i*width_num+j].prop_type = 0
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1 
				if prop_map_1[i*width_num+j] == 1: #水球
					map[i*width_num+j].prop_type = 1
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1
				if prop_map_1[i*width_num+j] == 2: #神奇藥水
					map[i*width_num+j].prop_type = 2
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1
				if prop_map_1[i*width_num+j] == 3: #溜冰鞋
					map[i*width_num+j].prop_type = 3
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1
				if prop_map_1[i*width_num+j] == 4: #烏龜 #ride 1
					map[i*width_num+j].prop_type = 4
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1
				if prop_map_1[i*width_num+j] == 5: #ufo #ride 2
					map[i*width_num+j].prop_type = 5
					map[i*width_num+j].prop_time = times
					prop_map_1[i*width_num+j] = -1
			
			elif map_number == 2:
				if prop_map_2[i*width_num+j] == 0:
					map[i*width_num+j].prop_type = random.randint(0, prop_num)
					prop_map_2[i*width_num+j] = -1
					print('prop ' + str(map[i*width_num+j].prop_type))
				# map.prop_type #0無 #1水球 #2神奇藥水 #3溜冰鞋 #4烏龜 #5飛碟
				if prop_map_2[i*width_num+j] == 0: #無
					map[i*width_num+j].prop_type = 0
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1 
				if prop_map_2[i*width_num+j] == 1: #水球
					map[i*width_num+j].prop_type = 1
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1
				if prop_map_2[i*width_num+j] == 2: #神奇藥水
					map[i*width_num+j].prop_type = 2
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1
				if prop_map_2[i*width_num+j] == 3: #溜冰鞋
					map[i*width_num+j].prop_type = 3
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1
				if prop_map_2[i*width_num+j] == 4: #烏龜 #ride 1
					map[i*width_num+j].prop_type = 4
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1
				if prop_map_2[i*width_num+j] == 5: #ufo #ride 2
					map[i*width_num+j].prop_type = 5
					map[i*width_num+j].prop_time = times
					prop_map_2[i*width_num+j] = -1
			
			if map[i*width_num+j].prop_type == 1:
				draw_prop(i, j, prop_1_Img)
			if map[i*width_num+j].prop_type == 2:
				draw_prop(i, j, prop_2_Img)
			if map[i*width_num+j].prop_type == 3:
				draw_prop(i, j, prop_3_Img)
			if map[i*width_num+j].prop_type == 4:
				draw_prop(i, j, prop_4_Img)
			if map[i*width_num+j].prop_type == 5:
				draw_prop(i, j, prop_5_Img)

	#繪製道具動畫
	def draw_prop(i, j, Img):
		if times - map[i*width_num+j].prop_time != 1:
			map[i*width_num+j].prop_time = times
			gameDisplay.blit(Img, (map[i*width_num+j].x,map[i*width_num+j].y-5))
		else:
			gameDisplay.blit(Img, (map[i*width_num+j].x,map[i*width_num+j].y-10))

	#判斷角色是否吃到道具 道具效果
	def chech_get_prop(i, j, player):
		if map[i*width_num+j].prop_type != 0 and player.ride != 2:
			print('get_prop:' + str(i)+ str(j) + str(map[i*width_num+j].prop_type) + str(map[i*width_num+j].player_1) + str(map[i*width_num+j].player_2))
			if map[i*width_num+j].prop_type == 1:
				player.bomb_maxnum += 1
				player.bomb_num += 1
				map[i*width_num+j].prop_type = 0
				if player.bomb_maxnum > max_bomb_num:
					player.bomb_maxnum = max_bomb_num
				if player.bomb_num > max_bomb_num:
					player.bomb_num = max_bomb_num
			elif map[i*width_num+j].prop_type == 2:
				player.bomb_range += 1
				map[i*width_num+j].prop_type = 0
				if player.bomb_range > max_bomb_range:
					player.bomb_range = max_bomb_range
			elif map[i*width_num+j].prop_type == 3:
				player.speed += 1
				map[i*width_num+j].prop_type = 0
				if player.speed > max_player_speed:
					player.speed = max_player_speed
			elif map[i*width_num+j].prop_type == 4:
				player.ride = 1
				turtle_type = random.randint(0, 1)
				if turtle_type == 0: #slow
					player.ride_speed = slow_turtle_speed
				elif turtle_type == 1:
					player.ride_speed = fast_turtle_speed
				map[i*width_num+j].prop_type = 0
			elif map[i*width_num+j].prop_type == 5:
				player.ride = 2
				player.ride_speed = ufo_speed
			map[i*width_num+j].prop_type = 0
			map[i*width_num+j].prop = False

	#地圖##########################################################################################
	#判斷背景物件種類
	def check_bkg_type(i, j):
		if map[i*width_num+j].bkg == 0: #地圖物件 方塊 不掉道具
			draw_rect(j, i)
			map[i*width_num+j].walk = False
			map[i*width_num+j].destroy = False
			map[i*width_num+j].drop = False
			map[i*width_num+j].fly = True
		if map[i*width_num+j].bkg == 1: #可走 綠磚 不可破壞 不掉道具 可飛行
			base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 2: #不可走 紅磚 可破壞 掉道具 可飛行
			if map[i*width_num+j].bkg_alive == True and bomb[i*width_num+j].explosion_dir == 'empty':
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/6, bkg_2_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = True
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 3: #不可走 橘磚 可破壞 掉道具 可飛行
			if map[i*width_num+j].bkg_alive == True and bomb[i*width_num+j].explosion_dir == 'empty':
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/6, bkg_3_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = True
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 4: #不可走 紅屋 不可破壞 不掉道具 不可飛行
			if map[i*width_num+j].bkg_alive == True:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/2, bkg_4_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = False
				map[i*width_num+j].fly = False
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 6: #可走 樹叢 可破壞 不掉道具 可飛行
			if map[i*width_num+j].bkg_alive == True and bomb[i*width_num+j].explosion_dir == 'empty':
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/2, bkg_6_Img)
				map[i*width_num+j].walk = True
				map[i*width_num+j].destroy = True
				map[i*width_num+j].drop = False
				map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 7: #不可走 樹 不可破壞 不掉道具 不可飛行
			if map[i*width_num+j].bkg_alive == True:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/2, bkg_7_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = False
				map[i*width_num+j].fly = False
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 8: #不可走 黃屋 不可破壞 不掉道具 不可飛行
			if map[i*width_num+j].bkg_alive == True:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/2, bkg_8_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = False
				map[i*width_num+j].fly = False
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 9: #不可走 木箱 可破壞 掉道具 可飛行
			if map[i*width_num+j].bkg_alive == True and bomb[i*width_num+j].explosion_dir == 'empty':
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/6, bkg_9_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = True
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 10: #可走 柏油1 不可破壞 不掉道具 可飛行
			if map[i*width_num+j].bkg_alive == False:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_10_Img)
				map[i*width_num+j].walk = True
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
				if map[i*width_num+j].bomb == True:
					map[i*width_num+j].walk = False
					map[i*width_num+j].fly = False
				else:
					map[i*width_num+j].walk = True
					map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 11: #可走 柏油2 不可破壞 不掉道具 可飛行
			if map[i*width_num+j].bkg_alive == False:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_11_Img)
				map[i*width_num+j].walk = True
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
				if map[i*width_num+j].bomb == True:
					map[i*width_num+j].walk = False
					map[i*width_num+j].fly = False
				else:
					map[i*width_num+j].walk = True
					map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 12: #可走 柏油3 不可破壞 不掉道具 可飛行
			if map[i*width_num+j].bkg_alive == False:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_12_Img)
				map[i*width_num+j].walk = True
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = True
				map[i*width_num+j].fly = True
				if map[i*width_num+j].bomb == True:
					map[i*width_num+j].walk = False
					map[i*width_num+j].fly = False
				else:
					map[i*width_num+j].walk = True
					map[i*width_num+j].fly = True
			else:
				base_bkg(i, j, 1)
		if map[i*width_num+j].bkg == 13: #不可走 藍屋 不可破壞 不掉道具 不可飛行
			if map[i*width_num+j].bkg_alive == True:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y - height/2, bkg_13_Img)
				map[i*width_num+j].walk = False
				map[i*width_num+j].destroy = False
				map[i*width_num+j].drop = False
				map[i*width_num+j].fly = False
			else:
				base_bkg(i, j, 1)

	#基礎背景物件
	def base_bkg(i, j, type):
		if type == 0:
			if map_number == 1:
				if map_1_0[i*width_num+j] == 1:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_1_Img)
				elif map_1_0[i*width_num+j] == 10:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_10_Img)
				elif map_1_0[i*width_num+j] == 11:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_11_Img)
				elif map_1_0[i*width_num+j] == 12:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_12_Img)
			elif map_number == 2:
				if map_2_0[i*width_num+j] == 1:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_1_Img)
				elif map_2_0[i*width_num+j] == 10:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_10_Img)
				elif map_2_0[i*width_num+j] == 11:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_11_Img)
				elif map_2_0[i*width_num+j] == 12:
					draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_12_Img)
		if type == 1:
			if map_number == 1:
				map[i*width_num+j].bkg = map_1_0[i*width_num + j]
			elif map_number == 2:
				map[i*width_num+j].bkg = map_2_0[i*width_num + j]
			if map[i*width_num+j].bkg == 1:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_1_Img)
			elif map[i*width_num+j].bkg == 10:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_10_Img)
			elif map[i*width_num+j].bkg == 11:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_11_Img)
			elif map[i*width_num+j].bkg == 12:
				draw_bkg(map[i*width_num+j].x, map[i*width_num+j].y, bkg_12_Img)
			
			
			map[i*width_num+j].bkg_alive = False
			map[i*width_num+j].destroy = False
			map[i*width_num+j].fly = True
			if map[i*width_num+j].bomb == True:
				map[i*width_num+j].walk = False
				map[i*width_num+j].fly = False
			else:
				map[i*width_num+j].walk = True
				map[i*width_num+j].fly = True
			

	#繪製地圖
	def draw_bkg(x, y, Img):
		gameDisplay.blit(Img, (x, y))

	#測試用地圖物件
	def draw_rect(x, y):
		a = pygame.Rect(5*width + width*x, height + height*y, width, height)
		pygame.draw.rect(gameDisplay, red, a, 5)

	#判斷物件是否被衝擊波摧毀
	def check_destroy_bkg(i, j):
		if bomb[i*width_num+j].explosion_dir != 'empty' and map[i*width_num+j].bkg_alive == True and map[i*width_num+j].destroy == True:
			map[i*width_num+j].bkg_alive = False
			map[i*width_num+j].bkg = 1
			map[i*width_num+j].prop = True
			print('destroy', str(i), str(j))
	#炸彈#####################################################################################
	#判斷是否可放置炸彈 炸彈位置
	def check_bomb(x, y, player):
		temp = 0
		if player.bomb == True and player.bomb_num > 0 and map[y*width_num+x].bomb == False and map[y*width_num+x].bkg_alive == False:
			temp -= 1
			if temp < 0:
				player.bomb_num -= 1
				if map[y*width_num+x].bomb == False:
					bomb[y*width_num+x].time = times
					if player == player_1:
						map[y*width_num+x].bomb = True
						map[y*width_num+x].walk = False
						#map[y*width_num+x].fly = False
						bomb[y*width_num+x].alive = True
						bomb[y*width_num+x].player_1 = True
						bomb[y*width_num+x].x_range = player_1.bomb_range
						bomb[y*width_num+x].y_range = player_1.bomb_range
						bomb[y*width_num+x].delay = player_1.bomb_delay
					elif player == player_2:
						map[y*width_num+x].bomb = True
						map[y*width_num+x].walk = False
						#map[y*width_num+x].fly = False
						bomb[y*width_num+x].alive = True
						bomb[y*width_num+x].player_2 = True
						bomb[y*width_num+x].x_range = player_2.bomb_range
						bomb[y*width_num+x].y_range = player_2.bomb_range
						bomb[y*width_num+x].delay = player_2.bomb_delay
					

	#繪製炸彈動畫
	def draw_bomb(x, y):
		if map[y*width_num+x].bomb == True:
			if bomb[y*width_num+x].alive == True:
				if times %2 != 1:
					gameDisplay.blit(bomb[y*width_num+x].Img, (map[y*width_num+x].x,map[y*width_num+x].y))
				else:
					gameDisplay.blit(bomb[y*width_num+x].Img2, (map[y*width_num+x].x,map[y*width_num+x].y))

	#衝擊波###########################################################################################
	#判斷是否有衝擊波(炸彈引爆)
	def check_explosion(x, y):
		if bomb[y*width_num+x].alive == True:
			
			if bomb[y*width_num+x].time + bomb[y*width_num+x].delay > times:
				bomb[y*width_num+x].explosion = False
				bomb[y*width_num+x].alive = True
			else:
				if bomb[y*width_num+x].player_1 == True:
					player_1.bomb_num += 1
				if bomb[y*width_num+x].player_2 == True:
					player_2.bomb_num += 1
				map[y*width_num+x].bomb = False
				map[y*width_num+x].walk = True
				bomb[y*width_num+x].player_1 = False
				bomb[y*width_num+x].player_2 = False
				bomb[y*width_num+x].explosion = True
				bomb[y*width_num+x].alive = False
		if bomb[y*width_num+x].explosion == True:
			bomb[y*width_num+x].explosion_time = times
			check_explosion_range(x, y)
			bomb[y*width_num+x].explosion = False
		if bomb[y*width_num+x].explosion_time + bomb[y*width_num+x].explosion_delay > times:
			draw_explosion(x, y)
			bomb[y*width_num+x].explosion = False
		else:
			bomb[y*width_num+x].explosion = False
			#bomb[y*width_num+x].explosion_dir = 'empty'

	#判斷衝擊波影響範圍
	def check_explosion_range(x, y):
		bomb[y*width_num+x].explosion_dir = 'center' 
		
		explosion_up = y - bomb[y*width_num+x].y_range
		if explosion_up < 0:
			explosion_up = 0
		explosion_down = y + bomb[y*width_num+x].y_range
		if explosion_down > 12:
			explosion_down = 12
		explosion_left = x - bomb[y*width_num+x].x_range
		if explosion_left < 0:
			explosion_left = 0
		explosion_right = x + bomb[y*width_num+x].x_range
		if explosion_right > 14:
			explosion_right = 14

		for i in range(1, bomb[y*width_num+x].x_range+1, 1):
			if x - i >= explosion_left:
				if map[y*width_num+x - i].bkg_alive == False:
					bomb[y*width_num+x - i].explosion_time = times
					bomb[y*width_num+x - i].explosion_dir = 'left'
				else:
					bomb[y*width_num+x - i].explosion_dir = 'left'
					break
		for i in range(1, bomb[y*width_num+x].x_range+1, 1):
			if x + i <= explosion_right:
				if map[y*width_num+x + i].bkg_alive == False:
					bomb[y*width_num+x + i].explosion_time = times
					bomb[y*width_num+x + i].explosion_dir = 'right'
				else:
					print('right', str(x+i), y)
					bomb[y*width_num+x + i].explosion_dir = 'right'
					print(str(bomb[y*width_num+x + i].explosion_dir))
					break
		for i in range(1, bomb[y*width_num+x].y_range+1, 1):
			if y-i >= explosion_up:
				if map[y*width_num+x - i*width_num].bkg_alive == False:
					bomb[y*width_num+x - i*width_num].explosion_time = times
					bomb[y*width_num+x - i*width_num].explosion_dir = 'up'
				else:
					bomb[y*width_num+x - i*width_num].explosion_dir = 'up'
					break
		for i in range(1, bomb[y*width_num+x].x_range+1, 1):
			if y+i <= explosion_down:
				if map[y*width_num+x + i*width_num].bkg_alive == False:
					bomb[y*width_num+x + i*width_num].explosion_time = times
					bomb[y*width_num+x + i*width_num].explosion_dir = 'down'
				else:
					bomb[y*width_num+x + i*width_num].explosion_dir = 'down'
					break

	#繪製衝擊波
	def draw_explosion(x, y):
		if bomb[y*width_num+x].explosion_dir == 'center':
			gameDisplay.blit(explo_center_Img, (map[y*width_num+x].x,map[y*width_num+x].y))
		elif bomb[y*width_num+x].explosion_dir == 'left':
			gameDisplay.blit(explo_left_Img, (map[y*width_num+x].x,map[y*width_num+x].y))
		elif bomb[y*width_num+x].explosion_dir == 'right':
			gameDisplay.blit(explo_right_Img, (map[y*width_num+x].x,map[y*width_num+x].y))
		elif bomb[y*width_num+x].explosion_dir == 'up':
			gameDisplay.blit(explo_up_Img, (map[y*width_num+x].x,map[y*width_num+x].y))
		elif bomb[y*width_num+x].explosion_dir == 'down':
			gameDisplay.blit(explo_down_Img, (map[y*width_num+x].x,map[y*width_num+x].y))
		#衝擊波摧毀道具
		if bomb[y*width_num+x].explosion_dir != 'empty':
			if map[y*width_num+x].prop_type != 0:
				map[y*width_num+x].prop_type = 0
				print(map[y*width_num+x].prop_type)
		#text = font.render(str(bomb[y*width_num+x].time), True, (0, 0, 0))
		#gameDisplay.blit(text, (map[y*width_num+x].x, map[y*width_num+x].y))



	###角色控制 #######################################################################################
	###player_1 w a s d space(放置炸彈) r(重生)
	###palyer_2 up left down right 數字鍵0(放置炸彈) 右側ENTER(重生)
	def control(player):
		if player == player_2 and player.alive == True:
			if player.ride == 0:
				temp_speed = player.speed
			else:
				temp_speed = player.ride_speed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.x_change = -temp_speed
				elif event.key == pygame.K_RIGHT:
					player.x_change = temp_speed
				elif event.key == pygame.K_UP:
					player.y_change = -temp_speed
				elif event.key == pygame.K_DOWN:
					player.y_change = temp_speed
				if event.key == pygame.K_KP0:
					player.bomb = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					player.x_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					player.y_change = 0
				if event.key == pygame.K_KP0:
					player.bomb = False
					
		if player == player_1 and player.alive == True:
			if player.ride == 0:
				temp_speed = player.speed
			else:
				temp_speed = player.ride_speed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					player.x_change = -temp_speed
				elif event.key == pygame.K_d:
					player.x_change = temp_speed
				if event.key == pygame.K_w:
					player.y_change = -temp_speed
				elif event.key == pygame.K_s:
					player.y_change = temp_speed
				if event.key == pygame.K_SPACE:
					player.bomb = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					player.x_change = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					player.y_change = 0
				if event.key == pygame.K_SPACE:
					player.bomb = False
		if player.alive == False:
			if event.type == pygame.KEYDOWN:
				if player == player_1 and player.niddle > 0:
					if event.key == pygame.K_r:
						player_1.alive = True
						player_1.niddle -= 1
				if player == player_2 and player.niddle > 0:
					if event.key == pygame.K_KP_ENTER:
						player_2.alive = True
						player_2.niddle -= 1
			player.x_change = 0
			player.y_change = 0
			player.bomb = False

	##移動角色 判斷是否出界 有bug
	def move(player):
		pre_x = player.x
		pre_y = player.y
		player.x += player.x_change
		player.y += player.y_change
		
		if player.x < 5*width:
			player.x = 5*width
		if player.x > display_width - 6*width + role_width/2:
			player.x = display_width - 6*width + role_width/2 - 1
			
			
		if player.y < height:
			player.y = height
		if player.y > display_height - height:
			player.y = display_height - height-1
		
		if player.j > 0:
			if map[player.i * width_num + player.j].x > player.x:
				if player.ride == 0 or player.ride == 1:
					if map[player.i * width_num + player.j - 1].walk == False:
						print(map[player.i * width_num + player.j].x, map[player.i * width_num + player.j].y)
						player.x = map[player.i * width_num + player.j].x
				elif player.ride == 2:
					if map[player.i * width_num + player.j - 1].fly == False:
						print(map[player.i * width_num + player.j].x, map[player.i * width_num + player.j].y)
						player.x = map[player.i * width_num + player.j].x
		if player.j < 14:
			if map[player.i * width_num + player.j+1].x <= player.x:
				if player.ride == 0 or player.ride == 1:
					if map[player.i * width_num + player.j + 1].walk == False:
						player.x = map[player.i * width_num + player.j].x + width - 1
						print(map[player.i * width_num + player.j].x, map[player.i * width_num + player.j].y)
				elif player.ride == 2:
					if map[player.i * width_num + player.j + 1].fly == False:
						player.x = map[player.i * width_num + player.j].x + width - 1
						print(map[player.i * width_num + player.j].x, map[player.i * width_num + player.j].y)
		if player.i > 0:
			if map[player.i * width_num + player.j].y > player.y:
				if player.ride == 0 or player.ride == 1:
					if map[(player.i-1) * width_num + player.j].walk == False:
						player.y = map[player.i * width_num + player.j].y
						print(player.i, player.j)
				elif player.ride == 2:
					if map[(player.i-1) * width_num + player.j].fly == False:
						player.y = map[player.i * width_num + player.j].y
						print(player.i, player.j)
		if player.i < 12:
			if map[(player.i+1) * width_num + player.j].y <= player.y:
				if player.ride == 0 or player.ride == 1:
					if map[(player.i+1) * width_num + player.j].walk == False:
						player.y = map[player.i * width_num + player.j].y + height - 1
						print(player.i, player.j)
				elif player.ride == 2:
					if map[(player.i+1) * width_num + player.j].fly == False:
						player.y = map[player.i * width_num + player.j].y + height - 1
						print(player.i, player.j)
	
	def check_win():
		if player_1.die == True or player_2.die == True:
			if player_1.die == True and player_2.die == False:
				text = font.render('player2 WIN',True,black)
				gameDisplay.blit(text, (display_width/2, display_height/2))
			elif player_1.die == False and player_2.die == True:
				text = font.render('player1 WIN',True,black)
				gameDisplay.blit(text, (display_width/2, display_height/2))
			elif player_1.die == True and player_2.die == True:
				text = font.render('DUEL',True,black)
				gameDisplay.blit(text, (display_width/2, display_height/2))
			crashed = True
	####主程式
	while (crashed == False):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
				pygame.mixer.music.load("sign in.mp3")
				pygame.mixer.music.play(-1)
			control(player_1)
			control(player_2)
			if event.type == TIME:
				times = times+1

		move(player_1)
		move(player_2)
		gameDisplay.fill(white)
		draw_map(0) #顯示地圖
		draw_player_dead(player_1)
		draw_player_dead(player_2)
		#print(times)
		#draw_prop(ball.x, ball.y, ball.Img)
		#text = font.render(str(times), True, (0, 0, 0))
		#gameDisplay.blit(text, (20, 20))
		text = font.render('player1:' + str(player_1_name),True,black)
		print(player_1_name)
		gameDisplay.blit(text, (100, 40))
		gameDisplay.blit(bomb_1_Img,(110,80))
		text = font.render(str(player_1.bomb_maxnum),True,black)
		gameDisplay.blit(text, (200, 80))
		gameDisplay.blit(prop_2_Img,(100,140))
		text = font.render(str(player_1.bomb_range),True,black)
		gameDisplay.blit(text, (200, 150))
		gameDisplay.blit(prop_3_Img,(100,200))
		text = font.render(str(player_1.speed - 4),True,black)
		gameDisplay.blit(text, (200, 210))
		gameDisplay.blit(niddle_1_Img,(100,260))
		text = font.render(str(player_1.niddle),True,black)
		gameDisplay.blit(text, (200, 280))
		
		
		text = font.render('player2:' + str(player_2_name),True,black)
		print(player_2_name)
		gameDisplay.blit(text, (1300, 340))
		gameDisplay.blit(bomb_1_Img,(1310,380))
		text = font.render(str(player_2.bomb_maxnum),True,black)
		gameDisplay.blit(text, (1400, 410))
		gameDisplay.blit(prop_2_Img,(1300,470))
		text = font.render(str(player_2.bomb_range),True,black)
		gameDisplay.blit(text, (1400, 480))
		gameDisplay.blit(prop_3_Img,(1300,540))
		text = font.render(str(player_2.speed - 4),True,black)
		gameDisplay.blit(text, (1400, 540))
		gameDisplay.blit(niddle_1_Img,(1300,650))
		text = font.render(str(player_2.niddle),True,black)
		gameDisplay.blit(text, (1400, 610))
		check_win()
		pygame.display.update()
		clock.tick(60)
	
game_intro()
game_loop()
pygame.quit()
quit()