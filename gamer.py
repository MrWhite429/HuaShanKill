# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import cards as cd
import output as op
import player as pl
import random
import os
import importlib

gamer_list = []
scripts = {}

class Gamer:
	img_path = "YuzhiboY"
	can_choose = 0
	pl_can_choose = 0
	now_card = 0
	now_stage = -1
	skill_name = []		#技能名称，是否锁定，对应函数->元组形式
	def __init__(self, name, hp, gender, country, skill=["杀","火杀","雷杀"]):
		self.name = name		#名称
		self.hp = hp			#体力
		self.max_hp = hp		#体力上限
		self.drink = 0			#有没有使用酒
		self.use_kill = 0		#使用了多少杀
		self.has_card = []		#手牌
		self.gender = gender
		# 武器，防具，+1，-1，宝物
		self.equip=[cd.Card(0,0,0,1)]
		for i in range(0,4):
			self.equip.append(cd.Card(0,0,0,0))
		self.judge = []
		self.get_in = [1,1,1,1,1,1]
		self.pos = 0
		self.seat = 0
		self.country = country
		self.dead = 0
		self.skill = skill
		self.on_card = []  #武将牌上的牌
		self.flip = 0      #是否翻面
		self.connect = 0		#是否横置
		self.attack_dis = 0		#是否有距离-1特性
		self.defence_dis = 0	#是否有距离+1特性
		self.auto = 0  # 是否为电脑

		self.chosen = [0]*120		#手牌是否被选中
		self.pl_chosen = [0]*120	#武将是否被选中
		self.using_limit = 0		#出牌阶段是否可以打出
		for i in range(4):
			self.has_card.append(cd.get_new_card())
		self.skill_init()



	def skill_init(self):
		op.skill_queue.clear()
		self.skill_name.sort(key= lambda x:x[1])
		for i in range(len(self.skill_name)):
			item,locked,func = self.skill_name[i]
			# print(item,locked,func)
			if(locked == 0):
				op.skill_queue.append(op.Button(item,840-60*(i//5),440+32*(i%5),25,func,in_skill=self))
			else:
				op.skill_queue.append(op.Label(item,840-60*(i//5),440+32*(i%5),25))



	def choose(self):
		dx = min(95, 550 / (len(self.has_card) + 1))
		tot = len(pl.player_in_game)
		mpos = pygame.mouse.get_pos()
		for i in range(len(self.has_card)):
			if (i >= len(self.has_card)):
				continue
			item = self.has_card[i]
			self.has_card[i].alpha = 255
			if (mpos[0] > 100 + i * dx and mpos[0] < 100 + (i + 1) * dx and mpos[1] > 467 and mpos[1] < 597):
				if(self.using(item)[0] == 0 and self.using_limit == 1):
					continue
				if(self.chosen[i] == 1 or sum(self.chosen)<self.can_choose):
					self.chosen[i] ^= 1
		print(self.pl_can_choose)
		for i in range(1, tot + 1):
			tx = (i - (i > pl.gamer_pos)) * 1000 / tot
			ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
			tx -= 60
			ty -= 80
			if(i == pl.gamer_pos+1):
				tx,ty = 850,440
			for item in pl.player_in_game:
				if(item.seat != i-1):continue
				if(item.be_aimed(self.now_card,self) == 0 or cd.aim(self.now_card,self,item) == 0):
					if(self.using_limit == 1):
						break
				if(mpos[0]>tx and mpos[0]<tx+120+30*(i==pl.gamer_pos) and mpos[1] > ty and mpos[1]<ty+160):
					print(item.name, i-1)
					if(self.pl_chosen[item.pos]==1 or sum(self.pl_chosen)<self.pl_can_choose):
						self.pl_chosen[item.pos] ^= 1



	def show(self):
		if(self.dead):
			return
		print("【", self.country, "】", end="")
		print(self.name, end=" ")
		for _ in range(self.hp):
			print("■", end=" ")
		for _ in range(max(0, self.max_hp - self.hp)):
			print("□", end=" ")
		for i in range(0, len(self.judge)):
			item = self.judge[i]
			if (item.id == 19):
				print(" 【樂】",end="")
			elif (item.id == 20):
				print(" 【兵】", end="")
			elif (item.id == 21):
				print(" 【闪电】", end="")
		print()
		for item in self.equip:
			if(item.id == 0): continue
			print("├",end="")
			item.show()
			print()


	def std_output(self,x,y):
		if (self.pos >= len(op.player_img)):
			return
		op.write("score:"+str(pl.score[self.pos]) + "[" + str(pl.cd_score[self.pos])+"]",950,410,20)
		pygame.draw.rect(op.screen,pl.country_color.setdefault(self.country,(0,0,0)),[850,438,150,162],0)
		pygame.draw.rect(op.screen, [30, 20, 0], [874, 440, 100, 160], 0)
		if (self.dead == 0):
			op.screen.blit(op.player_img[self.pos], [874, 440])
		else:
			tmp = op.player_img[self.pos]
			tmp.set_alpha(100)
			op.screen.blit(tmp, [874, 440])

		pygame.draw.rect(op.screen, [30, 20, 0], [849, 438, 150, 162], 2)
		op.Stwrite(self.name, 872, 472, 20, [255, 255, 255])
		if (self.max_hp > 7):
			op.write(str(self.max_hp), 999, 571, 25, [90, 170, 85])
			op.write(" / ", 999, 551, 22, [90, 170, 85])
			op.write(str(self.hp), 999, 527, 25, [90, 170, 85])
		else:
			for i in range(self.max_hp):
				if (i < self.hp):
					op.screen.blit(op.hp1_g, [977, 574 - 22*i])
				else:
					op.screen.blit(op.hp0_g, [977, 574 - 22*i])
		pygame.draw.rect(op.screen,(255, 250, 200), [852,578,20,20],0)
		op.write(str(len(self.has_card)), 871, 578, 18)
		x,y = 854,440
		op.write(" " + self.country, x + 18, y + 2, 16, [255, 255, 255])
		if (self.equip[0].id != 0):
			tmp = self.equip[0]
			pygame.draw.rect(op.screen, (250, 250, 250), [x + 20, y + 95, 100, 15], 0)
			pygame.draw.rect(op.screen, (30, 0, 20), [x + 20, y + 95, 100, 15], 1)
			op.type_img[tmp.type] = pygame.transform.smoothscale(op.type_img[tmp.type], (13, 13))
			op.screen.blit(op.type_img[tmp.type], [x + 21, y + 96])
			op.write(cd.card_point[tmp.num], x + 45, y + 95, 13)
			op.write(" " + cd.card_nm[tmp.id], x + 120, y + 95, 13)
		if (self.equip[1].id != 0):
			tmp = self.equip[1]
			pygame.draw.rect(op.screen, (250, 250, 250), [x + 20, y + 110, 100, 15], 0)
			pygame.draw.rect(op.screen, (30, 0, 20), [x + 20, y + 110, 100, 15], 1)
			op.type_img[tmp.type] = pygame.transform.smoothscale(op.type_img[tmp.type], (13, 13))
			op.screen.blit(op.type_img[tmp.type], [x + 21, y + 111])
			op.write(cd.card_point[tmp.num], x + 45, y + 110, 13)
			op.write(" " + cd.card_nm[tmp.id], x + 120, y + 110, 13)
		if (self.equip[4].id != 0):
			tmp = self.equip[4]
			pygame.draw.rect(op.screen, (250, 250, 250), [x + 20, y + 125, 100, 15], 0)
			pygame.draw.rect(op.screen, (30, 0, 20), [x + 20, y + 125, 100, 15], 1)
			op.type_img[tmp.type] = pygame.transform.smoothscale(op.type_img[tmp.type], (13, 13))
			op.screen.blit(op.type_img[tmp.type], [x + 21, y + 126])
			op.write(cd.card_point[tmp.num], x + 45, y + 125, 13)
			op.write(" " + cd.card_nm[tmp.id], x + 120, y + 125, 13)
		if (self.equip[2].id != 0):
			tmp = self.equip[2]
			pygame.draw.rect(op.screen, (250, 250, 250), [x + 20, y + 140, 40, 20], 0)
			pygame.draw.rect(op.screen, (30, 0, 20), [x + 20, y + 140, 40, 20], 1)
			op.type_img[tmp.type] = pygame.transform.smoothscale(op.type_img[tmp.type], (13, 13))
			op.screen.blit(op.type_img[tmp.type], [x + 21, y + 143])
			op.write(cd.card_point[tmp.num], x + 42, y + 142, 13)
			op.write("+1", x + 55, y + 140, 17)
		if (self.equip[3].id != 0):
			tmp = self.equip[3]
			pygame.draw.rect(op.screen, (250, 250, 250), [x + 60, y + 140, 40, 20], 0)
			pygame.draw.rect(op.screen, (30, 0, 20), [x + 60, y + 140, 40, 20], 1)
			op.type_img[tmp.type] = pygame.transform.smoothscale(op.type_img[tmp.type], (13, 13))
			op.screen.blit(op.type_img[tmp.type], [x + 61, y + 143])
			op.write(cd.card_point[tmp.num], x + 82, y + 142, 13)
			op.write("-1", x + 95, y + 140, 17)

		for item in self.judge:
			if (item.id == 19):
				pygame.draw.rect(op.screen, [100, 0, 100], [x + 80, y + 5, 15, 15], 0)
				op.write(" 乐", x + 95, y + 5, 15, [255, 255, 255])

			if (item.id == 20):
				pygame.draw.rect(op.screen, [100, 100, 0], [x + 100, y + 5, 15, 15], 0)
				op.write(" 兵", x + 115, y + 5, 15, [255, 255, 255])

			if (item.id == 21):
				pygame.draw.rect(op.screen, [0, 0, 100], [x + 100, y + 25, 15, 15], 0)
				op.write(" 闪", x + 114, y + 26, 15, [255, 255, 255])

		if (self.drink == 1):
			pygame.draw.rect(op.screen, [150, 50, 50], [x + 80, y + 25, 15, 15], 0)
			op.write(" 酒", x + 95, y + 26, 15, [255, 255, 255])
		if (self.connect == 1):
			pygame.draw.rect(op.screen, [100, 100, 100], [x + 20, y + 135, 25, 25], 0)
			op.write(" 连", x + 45, y + 135, 20, [255, 255, 255])

		self.self_output(x, y)


		dx = min(95, 550/(len(self.has_card)+1))
		mpos = pygame.mouse.get_pos()
		for i in range(len(self.has_card)):
			if(i >= len(self.has_card)):
				continue
			item = self.has_card[i]
			self.has_card[i].alpha = 255
			ny = 467 - self.chosen[i] * 30
			item.std_output(100+i*dx,ny,91,130)
			if(self.chosen[i] == 1):
				pygame.draw.rect(op.screen, [255, 255, 0], [100 + i * dx, ny, 91, 130], 1)
			res = self.using(item)
			if (res[0] == 0):
				pygame.draw.line(op.screen, [255, 0, 0], [100 + i * dx, ny], [191 + i * dx, ny + 130], 2)

		for i in range(len(self.has_card)):
			if(i >= len(self.has_card)):
				continue
			item = self.has_card[i]
			self.has_card[i].alpha = 255
			ny = 467 - self.chosen[i] * 30
			if (mpos[0] > 100 + i * dx and mpos[0] < 100 + (i + 1) * dx and mpos[1] > 467 and mpos[1] < 597):
				item.std_output(100 + i * dx, ny, 91, 130)
				pygame.draw.rect(op.screen,[255,255,0],[100+i*dx,ny,91,130],1)
				#item.std_output(mpos[0], mpos[1] - 300, 210, 300)		#放大镜模式


	def throw_hascard(self,num):
		if(len(self.has_card)<num):
			return 0
		last = self.can_choose
		x = 1
		self.can_choose = num
		while (sum(self.chosen) < num or x != 0):
			op.choices_num = [0] * 120
			x = op.judge(("请弃置%d张牌"%(num)), 360, 30, ["确定"], 400, 30, 0)
		for i in range(len(self.chosen)-1,-1,-1):
			if (self.chosen[i] == 1):
				tmp = self.has_card.pop(i)
				print("%s丢掉了" % (self.name), end="")
				tmp.show()
				cd.throw_queue.append(tmp)
		return 1


	def self_output(self,x,y):
		pass

	def using(self,now_card):
		if(now_card == 0):
			return 1
		if(now_card.id<4):
			if(self.equip[0].id == 22 and self.use_kill):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
				return 1,now_card
			elif(now_card.id == 1 and self.equip[0].id == 29):
				print("%s使用了[%s]"%(self.name,cd.card_nm[self.equip[0].id]))
				now_card.id = 2
			return (self.use_kill == 0),now_card
		elif(now_card.id in [5,13]):
			return (self.hp<self.max_hp),now_card
		elif(now_card.id>21 and 0):			#武器优先级参考对于玩家作废
			nid = now_card.id
			if (nid > 21 and nid < 32):
				return cd.danger_lvl[nid]<cd.danger_lvl[self.equip[0].id],now_card
			elif (nid > 31 and nid < 36):
				return cd.danger_lvl[nid]<cd.danger_lvl[self.equip[1].id],now_card
			elif (nid > 35 and nid < 39):
				return cd.danger_lvl[nid]<cd.danger_lvl[self.equip[2].id],now_card
			elif (nid > 38 and nid < 42):
				return cd.danger_lvl[nid]<cd.danger_lvl[self.equip[3].id],now_card

		return (now_card.id in [4,18])^1,now_card

	def be_aimed(self,now_card,user):
		if(now_card == 0):
			return 1
		if(now_card.id==13):
			return self.hp<self.max_hp
		elif(now_card.id==16):
			return self.equip[0].id != 0
		elif(now_card.id in [8,9,10]):
			return len(self.has_card)
		elif(now_card.id in [11,12]):
			return self.equip[1].id != 34
		return 1

	def be_defenced(self):
		if(self.equip[0].id == 30):
			print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
			self.use_kill = 0
		elif (self.equip[0].id == 27):
			if(len(self.has_card)>3):
				op.choices_num = [0] * 120
				ok = 0
				if(op.judge(("是否使用%s?" % (cd.card_nm[27])), 380, 30, ["使用", "不使用"], 420, 30, 0) == 0):
					print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
					x = 1
					self.can_choose = 2
					self.chosen = [0]*120
					while (sum(self.chosen) < 2 or x != 0):
						op.choices_num = [0] * 120
						x = op.judge("请弃置2张牌", 380, 30, ["确定"], 420, 30, 0)
					op.has_end, op.has_confirm, op.has_cancel = 0, 0, 0
					for i in range(len(self.chosen)-1,-1,-1):
						if (self.chosen[i] == 1):
							tmp = self.has_card.pop(i)
							print("%s丢掉了" % (self.name), end="")
							tmp.show()
							cd.throw_queue.append(tmp)
					ok = 1
				self.can_choose = 1
				self.pl_can_choose = 1
				op.has_end, op.has_confirm, op.has_cancel = 0, 0, 0
				op.task_queue.clear()
				op.task_queue.append(op.Button("结束出牌", 750, 400, 30, op.end_stage))
				op.task_queue.append(op.Button("确定", 460, 400, 30, op.confirm))
				op.task_queue.append(op.Button("取消", 590, 400, 30, op.cancel))
				return ok

		return 0

	def used(self,now_card):
		#print("%s打出了%s"%(self.name,cd.card_nm[now_card.id]))
		if(now_card == 0):return
		if(now_card.id <4):
			self.use_kill = 1
			self.drink = 0
		return 1

	def be_used(self,now_card,user):
		return 1

	def need(self,need_id,user):
		#print("需要",self.name,"出",cd.card_nm[need_id])
		op.delay(1000)
		if(need_id == 4 and self.equip[1].id == 32 and user.equip[0].id != 25):
			print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
			tmp = cd.get_new_card()
			print("判定结果：", end=" ")
			tmp.show()
			print()
			if(tmp.type == 1 or tmp.type == 3):
				print("[%s]生效"%(cd.card_nm[self.equip[1].id]))
				tmp.id = 4
				return tmp
		for i in range(0,len(self.has_card)):
			if(self.has_card[i].id == need_id):
				op.choices_num = [0] * 120
				x = op.judge(("是否响应%s打出【%s】?"%(user.name,cd.card_nm[need_id])),
						 380,30,["确定","取消"],420,30,0)
				if(x != 0):
					break
				if (need_id == 4):
					tmp = ["向后一躲，避开了这一招","片刻之间已侧身避过","忽的跳出，早避开这招"]
					st = tmp[random.randint(0,2)]
					print("%s%s," % (self.name, st))
				elif (need_id == 18):
					st = "早就看出端倪，轻松化开"
					print("%s%s," % (self.name, st))
				elif (need_id in [1, 2, 3]):
					st = self.skill[need_id]
					print("%s接了一记“%s”" % (self.name, st))
				else:
					st = cd.card_nm[need_id]
					print("%s打出了%s"%(self.name,st))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				#op.play(self)
				return tmp
		return 0

	def multi_need(self,need_id):
		#print("需要", self.name, "出:")
		#for i in need_id:
		#	print(cd.card_nm[i],end=" ")
		print()
		op.delay(1000)
		for i in range(0,len(self.has_card)):
			if(self.has_card[i].id in need_id):
				op.choices_num = [0] * 120
				x = op.judge(("是否响应打出【%s】?" % (cd.card_nm[self.has_card[i].id])),
							 380, 30, ["确定", "取消"], 420, 30, 0)
				if (x != 0):
					break
				print("%s打出了%s"%(self.name,cd.card_nm[self.has_card[i].id]))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				#op.play(self)
				return tmp
		return 0

	def contest(self,for_max = 1):		#拼点
		self.has_card.sort(key=lambda x: -1*(x.num + 0.01*x.defence_level))
		tmp = self.has_card.pop(0)
		return tmp

	def response(self, evt):  # 对全局事件的响应
		if (evt[0] == 8):
			print(self.name, "：深表同情")


	def lost_hp(self,num,user,type =0):
		if(self.equip[1].id == 35):
			if(num > 1):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
				num = 1
		st=["%s被掌力击退，向后直跌了%d步，","%s中了一击，吐出%d口鲜血，","%s眉头一皱，只知这一掌下去功力已失了%d成，"]
		tmp = st[random.randint(0,2)]
		print(tmp%(self.name,num))
		self.hp -= num
		while(self.hp<1):
			if(self.dying()==0):
				break
			else:
				self.hp += 1
		if(self.hp<1):
			self.died()
			return num
		pl.upload([4, user, num, self,type])
		return num

	def dying(self):
		if(self.need(5,self) or self.need(6,self)):
			return 1
		for item in pl.player_in_game:
			if(self.country != item.country): continue
			if (item.need(5, self)):
				return 1
		return 0

	def died(self):
		print("%s猛然向后一倒，口吐鲜血，已是武功俱废"%(self.name))
		self.dead = 1
		self.equip = []
		self.equip = [cd.Card(0, 0, 0, 1)]
		for i in range(0, 4):
			self.equip.append(cd.Card(0, 0, 0, 0))
		self.judge = []
		self.has_card = []
		self.drink = 0
		self.connect = 0
		self.flip = 0

	def in_judge(self):
		#print(self.name, "的判定阶段")
		for i in range(0,len(self.judge)):
			if(self.need(18,self) != 0):
				continue
			item = self.judge[i]
			tmp = cd.get_new_card()
			print("%s判定结果："%(cd.card_nm[item.id]),end=" ")
			tmp.show()
			print()
			if(item.id == 19):
				self.get_in[3]= (tmp.type == 1)
				if(self.get_in[3] == 0):
					print("%s错过了出牌阶段"%(self.name))
			elif(item.id == 20):
				self.get_in[2] = (tmp.type == 2)
				if (self.get_in[2] == 0):
					print("%s错过了摸牌阶段" % (self.name))
			elif(item.id == 21):
				if(tmp.type == 0 and tmp.num>1 and tmp.num<10):
					self.lost_hp(3,self)
				else:
					for i in range(self.pos,len(pl.player_in_game)):
						if(pl.player_in_game[i].dead == 0):
							self.judge.append(item)
							break
					for i in range(self.pos):
						if(pl.player_in_game[i].dead == 0):
							self.judge.append(item)
							break
		self.judge = []

	def prepare(self):
		print(self.name, "的准备阶段")


	def get_card(self):
		print(self.name, "的摸牌阶段")
		for i in range(0, 2):
			self.has_card.append(cd.get_new_card())

	def event(self):
		print(self.name, "的出牌阶段")
		for item in self.has_card:
			item.show()
			print()
		print()
		self.can_choose = 1
		self.pl_can_choose = 1
		self.using_limit = 1
		op.has_end,op.has_confirm,op.has_cancel = 0,0,0
		op.task_queue.clear()
		op.task_queue.append(op.Button("结束出牌",750,400,30,op.end_stage))
		op.task_queue.append(op.Button("确定", 460, 400, 30, op.confirm))
		op.task_queue.append(op.Button("取消", 590, 400, 30, op.cancel))
		while(op.has_end == 0 and len(self.has_card) != 0):
			if(self.now_card != 0):
				self.pl_can_choose = 1 + (self.now_card.id == 17)
			if(len(op.task_queue)<3):
				op.task_queue.append(op.Button("结束出牌", 750, 400, 30, op.end_stage))
				op.task_queue.append(op.Button("确定", 460, 400, 30, op.confirm))
				op.task_queue.append(op.Button("取消", 590, 400, 30, op.cancel))
			op.has_confirm = 0
			if (op.has_cancel == 1):
				op.has_cancel = 0
				self.chosen = [0] * 120
				self.pl_chosen = [0]*120
			if(sum(self.chosen) == 1):
				for i in range(len(self.chosen)):
					if(i >= len(self.has_card)):
						break
					if(self.chosen[i] != 0):
						self.now_card = self.has_card[i]
				tot = len(pl.player_in_game)
				can_choose_seat = [0]*120
				for item in pl.player_in_game:
					if(item.dead == 0 and cd.aim(self.now_card,self,item)):
						can_choose_seat[item.seat] = 1 + (item.auto==0)
				for i in range(1, tot + 1):
					tx = (i - (i> pl.gamer_pos)) * 1000 / tot
					ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
					tx -= 60
					ty -= 80
					if (can_choose_seat[i - 1]==1):
						pygame.draw.rect(op.screen, [255, 0, 0], [tx - 1, ty - 1, 122, 162], 1)
					elif(can_choose_seat[i - 1]==2):
						pygame.draw.rect(op.screen, [255, 0, 0], [849, 439, 151, 161], 1)
				if(self.now_card == 0):
					continue
				if(op.has_confirm!= 0):
					if (sum(self.pl_chosen) != 0):
						self.has_card.remove(self.now_card)
						for i in range(tot):
							item = pl.player_in_game[i]
							if (self.pl_chosen[i] != 0):
								# cd.throw_queue.append(self.now_card)
								if (item.be_aimed(self.now_card, self) != 0):
									cd.use(self.now_card, self, item)
									self.used(self.now_card)
								else:
									print("无效~")
						self.pl_chosen = [0] * 120
						self.chosen = [0] * 120
						self.now_card = 0
					elif(self.now_card.id in [5,6,11,12,13,14,15,17] or self.now_card.id > 20):
						#cd.throw_queue.append(self.now_card)
						self.has_card.remove(self.now_card)
						if(self.now_card.id == 17):
							self.has_card.append(cd.get_new_card())
							print("%s重铸了"%(self.name))
							self.now_card.show()
							print()
						else:
							cd.use(self.now_card, self,self)
							self.used(self.now_card)
						self.pl_chosen = [0] * 120
						self.chosen = [0] * 120
						self.now_card = 0

					if(pl.game_over() == 1):break
		op.task_queue.clear()
		self.using_limit = 0



	def throw(self,num):
		print(self.name, "的弃牌阶段")
		if(num <= 0):
			return
		print("弃置",num,"张")
		self.can_choose = num
		x = 1
		while (sum(self.chosen) < num or x != 0):
			op.choices_num = [0] * 120
			x = op.judge(("请弃置%d张牌"%(num)), 360, 30, ["确定"], 400, 30, 0)
		for i in range(len(self.chosen)-1,-1,-1):
			if (self.chosen[i] == 1):
				tmp = self.has_card.pop(i)
				print("%s丢掉了" % (self.name), end="")
				tmp.show()
				cd.throw_queue.append(tmp)
		for item in self.has_card:
			item.show()
			print()

	def end(self):
		print(self.name, "的结束阶段")
		#st = ["。","众人乱做一团。","一时间打的难解难分。","却不知局势已然变化。"]
		#print(st[random.randint(0,3)])

	def wave(self):
		if(self.flip):
			self.flip = 0
			print("%s结束翻面状态"%(self.name))
			return
		if(self.get_in[0] and self.dead == 0):
			self.chosen = [0]*100
			self.now_stage = 0
			pl.upload([1, self, 0, 0])
			self.prepare()
			pl.upload([1, self, 0, 1])
		if(self.get_in[1] and self.dead == 0):
			self.chosen = [0] * 100
			self.now_stage = 1
			pl.upload([1, self, 1, 0])
			self.in_judge()
			pl.upload([1, self, 1, 1])
		if(self.get_in[2] and self.dead == 0):
			self.chosen = [0] * 100
			self.now_stage = 2
			pl.upload([1, self, 2, 0])
			self.get_card()
			pl.upload([1, self, 2, 1])
		if(self.get_in[3] and self.dead == 0):
			self.chosen = [0] * 100
			self.now_stage = 3
			pl.upload([1, self, 3, 0])
			self.event()
			pl.upload([1, self, 3, 1])
		if(pl.game_over()):
			return
		if(self.get_in[4] and self.dead == 0):
			self.chosen = [0] * 100
			self.now_stage = 4
			pl.upload([1, self, 4, 0])
			self.throw(max(0, len(self.has_card) - self.hp))
			pl.upload([1, self, 4, 1])
		if(self.get_in[5] and self.dead == 0):
			self.chosen = [0] * 100
			self.now_stage = 5
			pl.upload([1, self, 5, 0])
			self.end()
			pl.upload([1, self, 3, 1])
		self.get_in = [1, 1, 1, 1, 1, 1]
		self.use_kill = 0
		self.drink = 0
		self.now_stage = -1
		pl.waves_score[self.pos] += 1

def import_pl():
	s = os.walk("resources/player")
	tmp = []
	for it in s:
		tmp.append(it)
	global gamer_list
	gamer_list = tmp[0][1]
	re_list = []
	for i in range(len(gamer_list)):
		if(i>=len(gamer_list)):break
		item = gamer_list[i]
		if (os.path.exists("resources/player/%s/%s_G.py" % (item, item)) == 0):
			re_list.append(item)
	for item in re_list:
		gamer_list.remove(item)
	for item in gamer_list:
		st = "resources.player.%s.%s_G" % (item, item)
		print(st)
		now = importlib.import_module(st)
		scripts[item] = now.Model

