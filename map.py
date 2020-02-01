import pygame,sys,os
from pygame.locals import *
from random import randint

class Map:
    UpMap=""
    MapName=""
    NowMap=""
    LV=""
    NextMap=""
    Exits=[]
    Doors=[]
    Buildings=[]
    PassedMap=[]
    Lock=0 #0上 1解锁
    def __init__(self,Scr,Wallimg,ExitImg,DoorImg,PlayerImg,Font):
        self.Scr=Scr
        self.WallImg=Wallimg
        self.ExitImg=ExitImg
        self.DoorImg=DoorImg
        self.PlayerImg=PlayerImg
        self.Font=Font
    def DoneMapData(self,Data):
        self.Data=Data
        Data=str(Data).split("#")
        self.UpMap=Data[0]
        self.NextMap=Data[2]
        Data=Data[1].split(".")
        self.MapName=Data[0]
        Data=Data[1].split("%")
        self.NowMap=Data[0]
        if self.NowMap!="0":
            self.LV=Data[2]
        #添加到已经经过的地图列表中
        self.PassedMap.append(self.MapName)
    def ToUPorNext(self,Kind):#0 up 1next  #更换地图
        if Kind==0:
            File=open("data/save/maps/"+self.UpMap+".ini","r")
            Data=File.read()
            File.close()
        else:
            File=open("data/save/maps/"+self.NextMap+".ini","r")
            Data=File.read()
            File.close()
        self.DoneMapData(Data)
        print(self.NowMap)
    def ToNowMap(self,InOrOut):#0 in 1 out
        #判断是否可以打开----进入----退出
       if self.Lock==1 or self.LV=="0":
            if InOrOut==0:
                self.Back=self.MapName
                #self.MapName=self.NowMap+"^none"
                self.MapName="test^none"
                self.BeforeDoorXY=self.Doors[0]
            else:
                self.MapName=self.Back #恢复
       else:
        self.ShowText("无法打开：门卡等级不够。")
        return 1 #0yes 1no

    def ShowText(self,Text):
        Show=self.Font.render(Text,True,(255,255,255))
        self.Scr.blit(Show,(0,0))
        pygame.display.update()
    def ToMap(self):#打印地图
        self.Code=self.MapName.split("^")
        self.Code=self.Code[0]
        #读取地图文件
        File=open("data/mapdata/maps/"+self.Code+".map","r")
        self.Map=File.readlines()
        File.close()
        #读取地图配置文件
        File=open("data/mapdata/maps/"+self.Code+"-s.map","r")
        Data=File.readlines()
        File.close()
        self.MapX=int(Data[0].strip())
        self.MapY=int(Data[1].strip())
        # 打印地图到屏幕;记录门的坐标
        self.Scr.fill((0,0,0))
        self.Doors=[]
        self.Exits=[]
        for i_y in range(self.MapY + 1):
            for j_x in range(self.MapX + 1):
                pos = [i_y * 32, j_x * 32]
                if self.Map[i_y][j_x] == "W":
                    self.Scr.blit(self.WallImg, (pos[1], pos[0]))
                if self.Map[i_y][j_x] == "D":
                    self.Scr.blit(self.ExitImg, (pos[1], pos[0]))
                    ExitXY=[j_x,i_y]
                    self.Exits.append(ExitXY)
                if self.Map[i_y][j_x] == "M":
                    self.Scr.blit(self.DoorImg, (pos[1], pos[0]))
                    DoorXY=[j_x,i_y]
                    self.Doors.append(DoorXY)
                if self.Map[i_y][j_x] == "O":
                    self.Scr.blit(self.DoorImg, (pos[1], pos[0]))
    def PrintPlayer(self,PlayerX,PlayerY):
        self.ToMap()
        self.Scr.blit(self.PlayerImg,(PlayerX*32,PlayerY*32))
