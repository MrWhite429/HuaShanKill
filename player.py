# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import cards as cd
import output as op
import random
import importlib
import os

player_in_game = []
gamer_pos = -1
score = [0] * 100			#胜局数
cd_score = [0]*100			#出牌数
waves_score = [0]*100		#回合数
country_num = {}		#同一势力玩家数
country_score = {}

player_list = []
scripts = {}
country_color = {
	"神1": (200, 0, 0),
	"神2": (130, 70, 130),
	"神3": (20, 130, 0),
	"神4": (70, 130, 130),
	"神5": (20, 20, 80),
	"神6": (100, 100, 100),
	"神7": (130, 20, 70),
	"神8": (200, 200, 200),
	"神9": (200, 200, 0),
	"魏": (70, 70, 130),
	"蜀": (130, 70, 70),
	"吴": (70, 130, 70),
	"群": (130, 130, 70),
}

class Player:
	img_path = "YuzhiboY"

	default_situation = ["士兵",4,0,"群"]

	def __init__(self, situation = default_situation):
		"""situation = (name, hp, gender, country)"""
		name, hp, gender , country = situation
		self.name = name  # 名称
		self.hp = hp  # 体力
		self.max_hp = hp  # 体力上限
		self.drink = 0  # 有没有使用酒
		self.use_kill = 0  # 使用了多少杀
		self.has_card = []  # 手牌
		self.gender = gender
		# 武器，防具，+1，-1，宝物
		self.equip = [cd.Card(0, 0, 0, 1)]
		for i in range(0, 4):
			self.equip.append(cd.Card(0, 0, 0, 0))
		self.judge = []
		self.get_in = [1, 1, 1, 1, 1, 1]
		self.pos = 0			#出牌顺序
		self.seat = 0			#显示的座次
		self.country = country
		self.dead = 0
		self.skill = ["杀", "火杀", "雷杀"]
		self.on_card = []  # 武将牌上的牌
		self.flip = 0  # 是否翻面
		self.connect = 0		#是否横置
		self.attack_dis = 0  # 是否有距离-1特性
		self.defence_dis = 0  # 是否有距离+1特性
		self.auto = 1  # 是否为电脑
		self.fire_col = 1000		#集火系数(死亡为0)

		for i in range(4):
			self.has_card.append(cd.get_new_card())

	def show(self):
		if (self.dead):
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
				print(" 【樂】", end="")
				 
			elif (item.id == 20):
				print(" 【兵】", end="")
				 
			elif (item.id == 21):
				print(" 【闪电】", end="")
				 
		print()
		for item in self.equip:
			if (item.id == 0): continue
			print("├", end="")
			item.show()
			print()

	def std_output(self, x, y, show_score = 1):
		if (self.pos >= len(op.player_img)):
			return
		if(show_score == 1):
			op.write("score:" + str(self.fire_col) + "[" + str(score[self.pos])+"]", x + 100, y - 25, 20)
		pygame.draw.rect(op.screen, country_color.setdefault(self.country,(0,0,0)), [x - 2, y - 2, 124, 164], 0)
		pygame.draw.rect(op.screen, (30,20,0), [x + 20, y, 101, 160], 0)
		op.Stwrite(self.name, x + 18, y + 20, 16, [255, 255, 255])
		tmp = op.player_img[self.pos]
		if (self.dead == 0):
			if(self.flip == 1):
				tmp = op.fliped
			tmp.set_alpha(255)
		else:
			tmp.set_alpha(100)
		op.screen.blit(tmp, [x + 21, y])
		pygame.draw.rect(op.screen, (30, 20, 0), [x - 2, y - 2, 124, 163], 2)
		if(show_score == 1):
			self.self_output(x, y)
		pygame.draw.rect(op.screen, (255, 250, 200), [x + 100, y + 140, 20, 20], 0)
		pygame.draw.rect(op.screen, (30, 0, 20), [x + 100, y + 140, 21, 21], 1)
		op.write(str(len(self.has_card)), x + 120, y + 140, 18)
		if (self.max_hp > 5):
			op.write(str(self.max_hp), x + 18, y + 142, 18, [90, 170, 85])
			op.write(" / ", x + 18, y + 126, 16, [90, 170, 85])
			op.write(str(self.hp), x + 18, y + 110, 18, [90, 170, 85])
		else:
			for i in range(self.max_hp):
				if (i < self.hp):
					op.screen.blit(op.hp1_t, [x + 3, y + 143 - i * 17])
				else:
					op.screen.blit(op.hp0_t, [x + 3, y + 143 - i * 17])
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

	def self_output(self, x, y):
		 pass

	def using(self, now_card):
		if (now_card.id < 4):
			if (self.equip[0].id == 22 and self.use_kill):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
				return 1, now_card
			elif (now_card.id == 1 and self.equip[0].id == 29):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
				now_card.id = 2
			return (self.use_kill == 0), now_card
		elif (now_card.id in [5, 13]):
			return (self.hp < self.max_hp), now_card
		elif (now_card.id > 21):
			nid = now_card.id
			if (nid > 21 and nid < 32):
				return cd.danger_lvl[nid] < cd.danger_lvl[self.equip[0].id], now_card
			elif (nid > 31 and nid < 36):
				return cd.danger_lvl[nid] < cd.danger_lvl[self.equip[1].id], now_card
			elif (nid > 35 and nid < 39):
				return cd.danger_lvl[nid] < cd.danger_lvl[self.equip[2].id], now_card
			elif (nid > 38 and nid < 42):
				return cd.danger_lvl[nid] < cd.danger_lvl[self.equip[3].id], now_card

		return (now_card.id != 18), now_card

	def be_aimed(self, now_card, user):
		if (now_card == 0):
			return 1
		if (now_card.id == 13):
			return self.hp < self.max_hp
		elif (now_card.id == 16):
			return self.equip[0].id != 0
		elif (now_card.id in [8, 9, 10]):
			tmp = 0
			for item in self.equip:
				tmp += item.id
			return len(self.has_card) + tmp > 0
		elif (now_card.id in [11, 12]):
			return self.equip[1].id != 34
		return 1

	def be_defenced(self):
		if (self.equip[0].id == 30):
			print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
			self.use_kill = 0
		elif (self.equip[0].id == 27):
			if (len(self.has_card) > 3):
				self.has_card.sort(key=lambda x: x.defence_level)
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
				pop_card_1 = self.has_card.pop()
				pop_card_2 = self.has_card.pop()
				pop_card_1.show()
				print()
				pop_card_2.show()
				print()
				self.has_card.sort(key=lambda x: x.attack_level)
				return 1

		return 0

	def used(self, now_card):
		# print("%s打出了%s"%(self.name,cd.card_nm[now_card.id]))
		if (now_card == 0): return
		if (now_card.id < 4):
			self.use_kill = 1
			self.drink = 0
		return 1

	def be_used(self, now_card, user):
		return 1

	def need(self, need_id, user):
		# print("需要",self.name,"出",cd.card_nm[need_id])
		op.delay(300)
		cd_score[self.pos] +=0
		if (need_id == 4 and self.equip[1].id == 32 and user.equip[0].id != 25):
			print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
			tmp = cd.get_new_card()
			print("判定结果：", end=" ")
			tmp.show()
			print()
			if (tmp.type == 1 or tmp.type == 3):
				print("[%s]生效" % (cd.card_nm[self.equip[1].id]))
				tmp.id = 4
				return tmp
		for i in range(0, len(self.has_card)):
			if (self.has_card[i].id == need_id):
				if (need_id == 4):
					tmp = ["向后一躲，避开了这一招", "片刻之间已侧身避过", "忽的跳出，早避开这招"]
					st = tmp[random.randint(0, 2)]
					print("%s%s," % (self.name, st))
				elif (need_id == 18):
					st = "早就看出端倪，轻松化开"
					print("%s%s," % (self.name, st))
				elif (need_id in [1, 2, 3]):
					st = self.skill[need_id]
					print("%s接了一记“%s”" % (self.name, st))
				else:
					st = cd.card_nm[need_id]
					print("%s打出了%s" % (self.name, st))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				# op.play(self)
				return tmp
		cd_score[self.pos] -= 0
		return 0

	def multi_need(self, need_id):
		# print("需要", self.name, "出:")
		# for i in need_id:
		#	print(cd.card_nm[i],end=" ")
		print()
		op.delay(300)
		cd_score[self.pos] += 0
		for i in range(0, len(self.has_card)):
			if (self.has_card[i].id in need_id):
				print("%s打出了%s" % (self.name, cd.card_nm[self.has_card[i].id]))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				# op.play(self)
				return tmp
		cd_score[self.pos] -= 0
		return 0

	def contest(self,for_max = 1):		#拼点
		self.has_card.sort(key=lambda x: -1*(x.num + 0.01*x.defence_level))
		tmp = self.has_card.pop(0)
		return tmp


	def response(self, evt):  # 对全局事件的响应
		if (evt[0] == 8):
			print(self.name, "：深表同情")
			 

	def lost_hp(self, num, user, type = 0):		#type=0(无属性),1(火焰),2(雷电)
		if (self.equip[1].id == 35):
			if (num > 1):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
				num = 1
		st = ["%s被掌力击退，向后直跌了%d步，", "%s中了一击，吐出%d口鲜血，", "%s眉头一皱，只知这一掌下去功力已失了%d成，"]
		tmp = st[random.randint(0, 2)]
		print(tmp % (self.name, num))
		self.hp -= num
		while (self.hp < 1):
			if (self.dying() == 0):
				break
			else:
				self.hp += 1
		if (self.hp < 1):
			self.died()
			return num
		upload([4, user, num, self, type])
		return num

	def dying(self):
		if (self.need(5, self) or self.need(6, self)):
			return 1
		for item in player_in_game:
			if (self.country != item.country): continue
			if (item.need(5, self)):
				return 1
		return 0

	def died(self):
		print("%s猛然向后一倒，口吐鲜血，已是武功俱废" % (self.name))
		self.dead = 1
		upload([8,self])
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
		# print(self.name, "的判定阶段")
		for i in range(0, len(self.judge)):
			item = self.judge[i]
			tmp = cd.get_new_card()
			print("%s判定结果：" % (cd.card_nm[item.id]), end=" ")
			tmp.show()
			print()
			if (item.id == 19):
				self.get_in[3] = (tmp.type == 1)
				if (self.get_in[3] == 0):
					print("%s错过了出牌阶段" % (self.name))
					 
			elif (item.id == 20):
				self.get_in[2] = (tmp.type == 2)
				if (self.get_in[2] == 0):
					print("%s错过了摸牌阶段" % (self.name))
					 
			elif (item.id == 21):
				if (tmp.type == 0 and tmp.num > 1 and tmp.num < 10):
					self.lost_hp(3, self)
				else:
					for i in range(self.pos, len(player_in_game)):
						if (player_in_game[i].dead == 0):
							self.judge.append(item)
							break
					for i in range(self.pos):
						if (player_in_game[i].dead == 0):
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
		self.has_card.sort(key=lambda x: x.attack_level)
		for item in self.has_card:
			item.show()
			print()
		print()
		i = 0
		try_kill = 1
		while (i < len(self.has_card)):
			if (self.dead): return
			item = self.has_card[i]
			# print("in ",end="")
			# item.show()
			if (item.attack_level == 99):
				break
			if (len(self.has_card) > 2 and item.attack_level > 3 and i < len(self.has_card) - 1):
				if (self.equip[0].id == 26 and self.use_kill == 0 and try_kill):
					print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
					pop_card_1 = self.has_card.pop(i)
					pop_card_2 = self.has_card.pop(i)
					tmp = cd.Card(1, (pop_card_1.type % 2) ^ (pop_card_2.type % 2), 1, 1)
					aimer = cd.aiming(tmp, self)
					using_res, item = self.using(tmp)
					if (using_res and aimer != 0):
						pop_card_1.show()
						print()
						pop_card_2.show()
						print()
						cd.use(tmp, self, aimer)
					else:
						i = -1
						self.has_card.sort(key=lambda x: x.attack_level)
						self.has_card.append(pop_card_1)
						self.has_card.append(pop_card_1)
					try_kill = 0

			aimer = cd.aiming(item, self)
			using_res, item = self.using(item)
			if (using_res and aimer != 0):
				if (len(self.has_card) > i): self.has_card.pop(i)
				if (self.equip[0].id == 31 and item.id < 4 and len(self.has_card) == 0):
					kill_set = cd.aiming_list(item, self)
					i = 0
					if (kill_set != 0):
						while (i < min(len(kill_set), 3)):
							print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
							cd.use(item, self, kill_set[i])
							i += 1
					self.used(item)
				else:
					cd.use(item, self, aimer)
					self.used(item)
				i = -1
				self.has_card.sort(key=lambda x: x.attack_level)
			i += 1
			# op.play(self)
			op.delay(400)

	def throw(self, num):
		print(self.name, "的弃牌阶段")
		print("弃置", num, "张")
		self.has_card.sort(key=lambda x: x.defence_level)
		for i in range(0, num):
			cd.throw_queue.append(self.has_card.pop())
		# op.play(self)
		for item in self.has_card:
			item.show()
			print()

	def end(self):
		print(self.name, "的结束阶段")
		 

	# st = ["。","众人乱做一团。","一时间打的难解难分。","却不知局势已然变化。"]
	# print(st[random.randint(0,3)])

	def wave(self):
		pl_fire_calc()
		if (self.flip):
			self.flip = 0
			print("%s结束翻面状态" % (self.name))
			return
		if (self.get_in[0] and self.dead == 0):
			upload([1, self, 0, 0])
			self.prepare()
			upload([1, self, 0, 1])
		if (self.get_in[1] and self.dead == 0):
			upload([1, self, 1, 0])
			self.in_judge()
			upload([1, self, 1, 1])
		if (self.get_in[2] and self.dead == 0):
			upload([1, self, 2, 0])
			self.get_card()
			upload([1, self, 2, 1])
		if (self.get_in[3] and self.dead == 0):
			upload([1, self, 3, 0])
			self.event()
			upload([1, self, 3, 1])
		if (self.get_in[4] and self.dead == 0):
			upload([1, self, 4, 0])
			self.throw(max(0, len(self.has_card) - self.hp))
			upload([1, self, 4, 1])
		if (self.get_in[5] and self.dead == 0):
			upload([1, self, 5, 0])
			self.end()
			upload([1, self, 5, 1])
		self.get_in = [1, 1, 1, 1, 1, 1]
		self.use_kill = 0
		self.drink = 0
		waves_score[self.pos] += 1


def init():
	global gamer_pos,player_in_game
	op.has_end = 1

	for i in range(len(player_in_game)):
		player_in_game[i].pos = i
		player_in_game[i].seat = i
		if (player_in_game[i].auto == 0):
			gamer_pos = i
	if(gamer_pos == -1): return
	for i in range(0,gamer_pos):
		player_in_game[i].seat = gamer_pos - i -1
	player_in_game[gamer_pos].seat = gamer_pos
	for i in range(gamer_pos+1,len(player_in_game)):
		player_in_game[i].seat = len(player_in_game) - i + gamer_pos
	pl_fire_calc()



def distance(user, aimer):  # user到aimer的距离
	if (user.pos == aimer.pos):
		return 0
	added = (aimer.equip[2].id != 0 + aimer.defence_dis) - (user.equip[3].id != 0 + user.attack_dis)
	x = min(user.pos, aimer.pos)
	y = max(user.pos, aimer.pos)
	disa, disb = 1, 1
	for i in range(x + 1, y):
		disa += player_in_game[i].dead == 0
	for i in range(y + 1, len(player_in_game)):
		disb += player_in_game[i].dead == 0
	for i in range(0, x):
		disb += player_in_game[i].dead == 0
	# print(aimer.name,aimer.defence_dis,aimer.attack_dis)
	# print(user.name,user.defence_dis,user.attack_dis)
	return min(disa, disb) + added


def upload(evt):		#全域响应
	for i in range(len(player_in_game)):
		if(player_in_game[i].dead == 0):
			player_in_game[i].response(evt)
	if(evt[0] == 4):
		if(evt[3].connect == 1 and evt[4] != 0):
			evt[3].connect = 0
			user,num,type = evt[1],evt[2],evt[4]
			for item in player_in_game:
				if(item.connect == 1):
					item.connect = 0
					item.lost_hp(num,user,type)


def game_over():
	tmp = 0
	for item in player_in_game:
		if (item.dead == 1): continue
		tmp = item.country
		break
	for item in player_in_game:
		if (item.dead == 1): continue
		if (item.country != tmp):
			return 0
	return 1

def pl_fire_calc():
	country_num = {}
	for item in player_in_game:
		country_num[item.country] = 0
	for item in player_in_game:
		if(item.dead == 1):continue
		country_num[item.country] += 1
	for item in player_in_game:
		item.fire_col = (2**country_num[item.country])*10 - len(item.has_card)
		item.fire_col *= item.dead-1

def import_pl():
	s = os.walk("resources/player")
	tmp = []
	for it in s:
		tmp.append(it)
	global player_list
	player_list = tmp[0][1]
	re_list = []
	for item in player_list:
		if(os.path.exists("resources/player/%s/%s.py"%(item,item))==0):
			re_list.append(item)
	for item in re_list:
		player_list.remove(item)
	for item in player_list:
		st = "resources.player.%s.%s"%(item,item)
		print(st)
		now = importlib.import_module(st)
		scripts[item] = now.Model






class YuanJH(Player):
	# 【浩劫】：摸牌阶段，你可以获得每名角色的一张手牌，若你以此法获得的牌不足2张，则你
	# 		可以从牌堆顶摸牌到2张。
	# 【体弱】：锁定技，结束阶段，你弃置全部手牌。
	img_path = "YuanJH"

	def get_card(self):
		print(self.name, "的摸牌阶段")
		print("%s发动技能【浩劫】" % (self.name))
		tot = 0
		for item in player_in_game:
			y = item.pos
			if (y == self.pos or item.dead == 1 or len(item.has_card) == 0):
				continue
			tmp = item.has_card
			random.shuffle(tmp)
			tmp_card = tmp[0]
			print("得到了%s的" % (item.name), end="")
			tmp_card.show()
			print()
			self.has_card.append(tmp_card)
			player_in_game[y].has_card.remove(tmp_card)
			tot += 1
		print("还可以摸%d张牌" % (2))
		for i in range(2):
			self.has_card.append(cd.get_new_card())

	def end(self):
		print(self.name, "的结束阶段")
		print("%s发动技能【体弱】" % (self.name))
		self.has_card = []


