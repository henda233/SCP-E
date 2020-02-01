import pygame,sys,os,player,map,mapset,time
from pygame.locals import *
from random import randint


#初始化
pygame.init()
GameV="1.0B 重置版"
Game_Size=32
Scr_W=1200
Scr_L=810
Scr=pygame.display.set_mode((Scr_W,Scr_L))
pygame.display.set_caption("SCP-E "+GameV)
#载入资源
PlayerImg=pygame.image.load("img/man.jpg")
DoorImg=pygame.image.load("img/door.jpg")
WallImg=pygame.image.load("img/wall.jpg")
Background=pygame.image.load("img/background.jpg")
#修改图片
PlayerImg=pygame.transform.scale(PlayerImg,(Game_Size,Game_Size))
DoorImg=pygame.transform.scale(DoorImg,(Game_Size,Game_Size))
WallImg=pygame.transform.scale(WallImg,(Game_Size,Game_Size))
Background=pygame.transform.scale(Background,(Scr_W,Scr_L))
#字体
MenuFont=pygame.font.SysFont("SimHei",40)
Font=pygame.font.SysFont("SimHei",20)
W=(255,255,255)
B=(0,0,0)

def PrintMenu():
    MenuText=MenuFont.render("SCP-E "+GameV,True,W)
    StartText=Font.render("[1]开始游戏",True,W)
    ExitText=Font.render("[2]退出游戏",True,W)
    Scr.blit(MenuText,(0,200))
    Scr.blit(StartText,(0,300))
    Scr.blit(ExitText, (0, 400))

def PlayerMusic():
    Music=os.listdir("data/music")
    pygame.mixer.init()
    pygame.mixer_music.load("data/music/"+Music[0])
    #显示
    MusicText=Font.render("正在播放： "+Music[0],True,W)
    Scr.blit(MusicText,(0,500))
    pygame.mixer_music.set_volume(0.2)
    pygame.mixer_music.play(start=0.0)

def StartGame():
    #生成地图
    Maps=mapset.Main_MapSet()
    #创建地图
    PaMap=map.Map(Scr,WallImg,DoorImg,DoorImg,PlayerImg,Font)
    #创建角色
    Pa=Load(Maps)
    # 载入地图
    PaMap.DoneMapData(Pa.Map)
    PaMap.ToMap()#打印地图
    #确定角色位置
    Pa.GetPlayerXY(PaMap.MapName,PaMap.Exits,0,[0,0])
    #打印玩家
    PaMap.PrintPlayer(Pa.PlayerX,Pa.PlayerY)
    pygame.display.update()
    PlayerMain(Pa,PaMap)
    pygame.mixer_music.stop()


def PlayerMain(Pa,PaMap):
    while 1:
        for event in pygame.event.get():
            global key
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    key=Pa.PlayerMove("UP",PaMap.MapName,PaMap.Exits)
                if event.key==K_DOWN:
                    key=Pa.PlayerMove("DOWN",PaMap.MapName,PaMap.Exits)
                if event.key==K_RIGHT:
                    key=Pa.PlayerMove("R",PaMap.MapName,PaMap.Exits)
                if event.key==K_LEFT:
                    key=Pa.PlayerMove("L",PaMap.MapName,PaMap.Exits)
                if event.key==K_TAB:
                    Pa.OpenBackage()
                    key=0
                #打印玩家反馈检测
                if key==0:#0 移动 2更换地图 3到达NowMAP
                    PaMap.PrintPlayer(Pa.PlayerX,Pa.PlayerY)
                    pygame.display.update()
                elif key==2:
                    PaMap.ToUPorNext(Pa.Dir)#更换地图
                    PaMap.ToMap()#打印地图
                    Pa.Map=PaMap.Data
                    Pa.GetPlayerXY(PaMap.MapName,PaMap.Exits,0,[0,0])#获得玩家新XY
                    PaMap.PrintPlayer(Pa.PlayerX,Pa.PlayerY)
                    pygame.display.update()
                elif key==3:#进入特殊地形
                    A=PaMap.ToNowMap(0)
                    if A!=1:
                        PaMap.ToMap()
                        Pa.GetPlayerXY(PaMap.MapName,PaMap.Exits,0,[0,0])
                        PaMap.PrintPlayer(Pa.PlayerX, Pa.PlayerY)
                        pygame.display.update()
                elif key==4:#退出特殊地形
                    PaMap.ToNowMap(1)
                    PaMap.ToMap()
                    Pa.GetPlayerXY(PaMap.MapName,PaMap.Exits,1,PaMap.BeforeDoorXY)
                    PaMap.PrintPlayer(Pa.PlayerX, Pa.PlayerY)
                    pygame.display.update()
                Pa.PlayerSpend()
                Pa.PrintPlayerData()

def Load(Maps):
    Pa = player.CrtPlayer(Maps, Scr, Font)
    File=open("data/text/tips.txt","r")
    Tips=File.readlines()
    N=len(Tips)-1
    C=randint(0,N)
    TipsText=Font.render("Tips:"+Tips[C].strip(),True,(255,255,255))
    Scr.blit(TipsText,(300,500))
    pygame.display.update()
    time.sleep(randint(5,10))
    return Pa

def LoadNews():
    File=open("data/text/news.txt","r")
    News=File.readlines()
    TextX = 800
    TextY = 50
    j = 0
    for i in News:
        ReadText = Font.render(i.strip(), True, (255, 255, 255))
        Scr.blit(ReadText, (TextX, TextY + j * 30))
        j += 1

if __name__ == '__main__':
    #显示标题
    Scr.blit(Background,(0,0))
    PrintMenu()
    LoadNews()
    #播放音乐
    PlayerMusic()
    pygame.display.update()
    Run=True
    while Run:
        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_1:
                    StartGame()
                if event.key==K_2:
                    print("退出游戏")
                    sys.exit()