import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	img_path = "Shen_ZhaoY"
	default_situation = ["神赵云", 2, 0, "群"]

	def get_card(self):
		print(self.name, "的摸牌阶段")
		if(self.hp<self.max_hp):
			print("%s发动技能【绝境】并摸了%d张牌" % (self.name,2+self.max_hp-self.hp))
		for i in range(0, 2+self.max_hp-self.hp):
			self.has_card.append(cd.get_new_card())

	def throw(self, num):
		print(self.name, "的弃牌阶段")
		sk_num = max(0,len(self.has_card)-self.hp-2)
		if(num>sk_num):
			num=sk_num
			print("%s发动技能【绝境】"%(self.name))
		print("弃置", num, "张")
		self.has_card.sort(key=lambda x: x.defence_level)
		for i in range(0, num):
			cd.throw_queue.append(self.has_card.pop())
		# op.play(self)
		for item in self.has_card:
			item.show()
			print()

	def multi_need(self, need_id):
		op.delay(300)
		if (self.hp == 1 and 2 in need_id):
			for i in range(len(self.has_card) - 1, -1, -1):
				item = self.has_card[i]
				if (item.type == 3):
					print("%s发动技能【龙魂】将" % (self.name), end="")
					tmp = self.has_card.pop(i)
					cd.throw_queue.append(tmp)
					tmp.show()
					print("作为%s打出" % (cd.card_nm[2]))
					return tmp

		for i in range(0, len(self.has_card)):
			if (self.has_card[i].id in need_id):
				print("%s打出了%s" % (self.name, cd.card_nm[self.has_card[i].id]))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				# op.play(self)
				return tmp
		return 0

	def need(self, need_id, user):
		op.delay(300)
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
		if(self.hp == 1):
			for i in range(len(self.has_card)-1,-1,-1):
				item = self.has_card[i]
				changed = 0
				if(item.type == 2 and need_id == 4):
					changed = 1
				elif(item.type == 0 and need_id == 18):
					changed = 1
				elif(item.type == 1 and need_id == 5):
					changed = 1
				if(changed == 1):
					print("%s发动技能【龙魂】将"%(self.name),end="")
					tmp = self.has_card.pop(i)
					cd.throw_queue.append(tmp)
					tmp.show()
					print("作为%s打出"%(cd.card_nm[need_id]))
					return tmp
			for i in range(len(self.equip)):
				item = self.equip[i]
				if(item.id == 0):continue
				changed = 0
				if (item.type == 2 and need_id == 4):
					changed = 1
				elif (item.type == 0 and need_id == 18):
					changed = 1
				elif (item.type == 1 and need_id == 5):
					changed = 1
				if (changed == 1):
					print("%s发动技能【龙魂】将" % (self.name), end="")
					tmp = item
					cd.throw_queue.append(tmp)
					tmp.show()
					self.equip[i] = cd.Card(0,0,0,i==0)
					print("作为%s打出" % (cd.card_nm[need_id]))
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
		return 0

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
		for item in self.has_card:
			if(self.hp > 1):break
			if(item.type == 1):
				self.need(5,self)