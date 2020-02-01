import map,pygame,random
from pygame.locals import *

class CrtPlayer:
    #HP,FOOD,SLEEP,SKILL,FOODSPEED,SLEEPSEEPD,PLAYERX,PLAYERY,MAP
    def __init__(self,Maps,Scr,Font):
        self.HP=100
        self.Food=1000
        self.Sleep=2000
        self.FoodSpeed=2
        self.SleepSpeed=2
        self.PlayerX=0
        self.PlayerY=0
        self.PassTimes=0
        self.Day=0
        self.Map="None"
        self.Dir=0 #0Up 1Next 2Now
        self.Item=["测试1","测试2"]
        self.Scr=Scr
        self.Font=Font
        #随机选择地图
        N=len(Maps)-1
        C=random.randint(0,N)
        self.Map=Maps[C]
        #写入文件
        File=open("data/save/player.scpe","w+")
        File.writelines(str(self.HP)+"\n")
        File.writelines(str(self.Food) + "\n")
        File.writelines(str(self.Sleep) + "\n")
        File.writelines(str(self.FoodSpeed) + "\n")
        File.writelines(str(self.SleepSpeed) + "\n")
        File.writelines(str(self.PlayerX) + "\n")
        File.writelines(str(self.PlayerY) + "\n")
        File.writelines(str(self.Map) + "\n")
        File.close()
        #写入物品数据
        File=open("data/save/playeritem.scpe","w+")
        File.close()
        self.ManC()
        self.ReadPlayer()
        print("玩家创建完毕。")
    def ManC(self):
        R=random.randint(1,4)
        if R==1:
            self.Man="D级人员"
        elif R==2:
            self.Man="科研人员"
        elif R==3:
            self.Man="安保人员"
        elif R==4:
            self.Man="清洁工"
    def ReadPlayer(self):
        self.Scr.fill((0,0,0))
        #读取角色说明
        File=open("data/text/"+self.Man+".txt","r",encoding="UTF-8")
        Text=File.readlines()
        TextX=300
        TextY=200
        j=0
        for i in Text:
            ReadText=self.Font.render(i.strip(),True,(255,255,255))
            self.Scr.blit(ReadText,(TextX,TextY+j*30))
            j+=1
        ReadText=self.Font.render("载入中...",True,(255,255,255))
        self.Scr.blit(ReadText, (TextX, TextY + (j+1) * 30))
        pygame.display.update()

    def GetPlayerXY(self,MapName,Map_Exits,OutFromNowMap,BeforeDoorXY):# 0 NowMap外 1NowMAP内
        if OutFromNowMap==0:
            if "F-1" in MapName:
                if self.Dir==0:
                    ExitXY=Map_Exits[0]
                    self.PlayerX=ExitXY[0]
                    self.PlayerY=ExitXY[1]+1
                elif self.Dir==1:
                    ExitXY = Map_Exits[1]
                    self.PlayerX = ExitXY[0]
                    self.PlayerY = ExitXY[1] - 1
            elif "F-2" in MapName:
                if self.Dir == 0:
                    ExitXY = Map_Exits[0]
                    self.PlayerX = ExitXY[0]-1
                    self.PlayerY = ExitXY[1]
                elif self.Dir == 1:
                    ExitXY = Map_Exits[1]
                    self.PlayerX = ExitXY[0]
                    self.PlayerY = ExitXY[1]-1
            elif "F-3" in MapName:
                if self.Dir == 0:
                    ExitXY = Map_Exits[0]
                    self.PlayerX = ExitXY[0]+1
                    self.PlayerY = ExitXY[1]
                elif self.Dir == 1:
                    ExitXY = Map_Exits[1]
                    self.PlayerX = ExitXY[0]
                    self.PlayerY = ExitXY[1]-1
            else:
                self.PlayerX=1
                self.PlayerY=4
        else:
            if "F-2" in MapName:
                self.PlayerX=BeforeDoorXY[0]-1
                self.PlayerY=BeforeDoorXY[1]
            elif "F-3" in MapName:
                self.PlayerX=BeforeDoorXY[0]+1
                self.PlayerY=BeforeDoorXY[1]

    def PlayerMove(self,Dir,MapName,Map_Exits):
        global AimX,AimY
        if Dir=="UP":
            AimY=self.PlayerY-1
            AimX=self.PlayerX
        elif Dir=="DOWN":
            AimY = self.PlayerY + 1
            AimX = self.PlayerX
        elif Dir=="R":
            AimY = self.PlayerY
            AimX = self.PlayerX+1
        elif Dir=="L":
            AimY=self.PlayerY
            AimX=self.PlayerX-1
        #检测是否合法
        Data=str(MapName).split("^")
        File=open("data/mapdata/maps/"+Data[0]+".map","r")
        Map=File.readlines()
        Ojb=Map[AimY][AimX]
        if Ojb=="W":
            return 1#禁止通行
        elif Ojb=="N":
            self.PlayerX=AimX
            self.PlayerY=AimY
            return 0#可以通行
        elif Ojb=="D":
            #判断是那出口
            A = [AimX, AimY]
            if A in Map_Exits[0]:
                self.Dir=1
            else:
                self.Dir=0
            return 2
        elif Ojb=="M":
            return 3
        elif Ojb=="O":
            return 4
    def OpenBackage(self):
        pygame.draw.rect(self.Scr,(0,0,0),((300,400),(300,400)))
        #显示容量
        Much=len(self.Item)
        MuchText=self.Font.render(str(Much)+"/5   背包：",True,(255,255,255))
        self.Scr.blit(MuchText,(300,400))
        i=0
        TextX=300
        TextY=400
        for Text in self.Item:
            ItemText=self.Font.render("["+str(i)+"]"+Text,True,(255,255,255))
            self.Scr.blit(ItemText,(TextX,TextY+i*32+32))
            i+=1
        pygame.display.update()
        OpenBackage=True
        while OpenBackage:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        return
                    if event.key==K_0:
                        self.UseItem(0)
                    if event.key==K_1:
                        self.UseItem(1)
                    if event.key==K_2:
                        self.UseItem(2)
                    if event.key == K_3:
                        self.UseItem(3)
                    if event.key==K_4:
                        self.UseItem(4)

    def UseItem(self,Which):
        pass
    def PrintPlayerData(self):
        HPText=self.Font.render("HP:"+str(self.HP),True,(255,255,255))
        FoodText=self.Font.render("FOOD:"+str(self.Food),True,(255,255,255))
        SleepText=self.Font.render("SLEEP:"+str(self.Sleep),True,(255,255,255))
        TimeText=self.Font.render("时间:"+str(self.PassTimes),True,(255,255,255))
        DayText=self.Font.render("Day:"+str(self.Day),True,(255,255,255))
        #处理MAP
        Data=str(self.Map).split("#")
        Pos=Data[1]
        PosText=self.Font.render("位置:"+str(Pos),True,(255,255,255))
        #显示
        self.Scr.blit(HPText,(700,100))
        self.Scr.blit(FoodText, (700, 150))
        self.Scr.blit(SleepText, (700, 200))
        self.Scr.blit(TimeText, (700, 250))
        self.Scr.blit(DayText, (700, 300))
        self.Scr.blit(PosText, (700,350))
        pygame.display.update()
    def PlayerSpend(self):
        self.Food-=self.FoodSpeed
        self.Sleep-=self.SleepSpeed
        self.PassTimes+=1
        if self.PassTimes>=500:
            self.Day+=1
            self.PassTimes=0
        #检测是否死亡
    def CheckNumber(self):
        if self.Food<=0 or self.HP<=0:
            self.PlayerDead()
        elif self.Day==7:
            print("游戏结束。")
    def PlayerDead(self):
        print("玩家死亡.")