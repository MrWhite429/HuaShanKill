import cards as cd
import player as pl
import output as op
import gamer as gm

class Model(gm.Gamer):
	img_path = "YuzhiboY"

	def skill_0(self):
		print("%s发动技能【作弊】" % (self.name))
		self.has_card.append(cd.get_new_card())
		self.skill_name = [("分身",1,0),("天照",1,0)]
		self.skill_init()

	skill_name = [("作弊",0,skill_0),("分身",1,0),("天照",1,0)]

	def response(self, evt):
		if (evt[0] == 8):
			print(self.name, "：深表同情")
		if(evt[0] == 4):
			if(evt[3].country == self.country):
				x = -1
				while (x == -1):
					op.choices_num = [0] * 120
					x = op.judge(("是否发动技能【分身】获得%d张牌" % (evt[3].max_hp - evt[3].hp)), 360, 30, ["确定","取消"], 400, 30, 0)
				if(x == 0):
					for i in range(evt[3].max_hp - evt[3].hp):
						print("%s发动技能【分身】获得了" % (self.name))
						tmp = cd.get_new_card()
						tmp.show()
						print()
						self.has_card.append(tmp)
		if (evt[0] == 3):
			if (evt[1].pos == self.pos and evt[3].id in [1,2, 3,7,8]):
				if (len(self.has_card) > 0):
					print("%s发动技能【天照】" % (self.name))
					pl.player_in_game[evt[2].pos].lost_hp(1, self)