import cards as cd
import player as pl
import output as op
import gamer as gm

class Model(gm.Gamer):
	img_path = "SunC"

	skill_name = [("激昂",1,0),("魂姿",1,0)]

	def response(self, evt):
		if (evt[0] == 8):
			print(self.name, "：深表同情")
		if (evt[0] == 2):
			now_card = evt[3]
			if(evt[1].pos == self.pos or evt[2].pos == self.pos):
				if((now_card.id in [1, 2, 3] and now_card.type % 2 == 1) or now_card.id == 7):
					print("%s发动技能【激昂】并获得了" % (self.name))
					tmp = cd.get_new_card()
					tmp.show()
					print()
					self.has_card.append(tmp)


	def prepare(self):
		print(self.name, "的准备阶段")
		if(len(self.skill_name) < 3):
			if(self.hp == 1):
				print("%s发动技能【魂姿】减少1点体力上限并获得了技能【英魂】,【英姿】" % (self.name))
				self.skill_name=[("激昂",1,0),("英魂",1,0),("英姿",1,0)]
				self.skill_init()
				self.max_hp -= 1
				self.hp = min(self.hp,self.max_hp)

		if (len(self.skill_name) >= 3):
			num = self.max_hp - self.hp
			if(num<1):return
			x = -1
			while (x == -1):
				op.choices_num = [0] * 120
				x = op.judge(("是否发动技能【英魂】?"), 360, 30, ["确定", "取消"], 400, 30, 0)
			if(x==1):return
			x = -1
			self.pl_can_choose = 1
			while (x == -1 or sum(self.pl_chosen) < 1):
				op.choices_num = [0] * 120
				x = op.judge(("请选择一名其他角色发动【英魂】"), 360, 30, ["摸%d弃1"%(num),"摸1弃%d"%(num)], 400, 30, 0)
			for i in range(len(pl.player_in_game)):
				item = pl.player_in_game[i]
				if(self.pl_chosen[i] != 0):
					for _ in range(num*(1-x)):
						item.has_card.append(cd.get_new_card())
					if(x==0):
						item.throw(1)
					else:
						maxn = len(item.has_card)
						if(maxn>=num):
							item.throw(num)
						else:
							item.throw(maxn)
							for i in range(4,-1,-1):		#实在不够弃装备
								if(maxn <= num): break
								if(item.equip[i].id !=0):
									tmp = item.equip[i]
									cd.throw_queue.append(tmp)
									item.equip[i] = cd.Card(0,0,0,i==0)
									maxn -= 1
					break

	def get_card(self):
		print(self.name, "的摸牌阶段")
		num = 2
		if((len(self.skill_name)>=3)):
			print("%s发动技能【英姿】" % (self.name))
			num += 1
		for i in range(0, num):
			self.has_card.append(cd.get_new_card())