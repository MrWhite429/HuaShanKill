# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import player as pl
import cards as cd
import room as rm
import gamer as gm

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption(u'三国杀 v0.3.0')
debug_mode = 0
play_ground = pygame.image.load("resources/background/play_background.jpg")
play_ground = pygame.transform.smoothscale(play_ground, (1000, 600))
title_ground = pygame.image.load("resources/background/title_background.jpg")
title_ground = pygame.transform.smoothscale(title_ground, (1000, 600))
type_img = []
type_img.append(pygame.image.load("resources/cards/type_0.jpg"))
type_img.append(pygame.image.load("resources/cards/type_1.jpg"))
type_img.append(pygame.image.load("resources/cards/type_2.jpg"))
type_img.append(pygame.image.load("resources/cards/type_3.jpg"))
hp0 = pygame.image.load("resources/general/hp0.png")
hp1 = pygame.image.load("resources/general/hp1.png")
fliped = pygame.image.load("resources/general/fliped.jpg")
fliped = pygame.transform.smoothscale(fliped, (100, 160))
hp0_t = pygame.transform.smoothscale(hp0, (14, 14))  # 他人阴阳鱼
hp1_t = pygame.transform.smoothscale(hp1, (14, 14))
hp0_g = pygame.transform.smoothscale(hp0, (20, 20))  # 玩家阴阳鱼
hp1_g = pygame.transform.smoothscale(hp1, (20, 20))
pygame.mixer_music.load("resources/sounds/bgm.mp3")
in_title = 1
in_edit = 1
in_design = 1
player_img = []
card_img = []
has_confirm = 0
has_cancel = 0
has_end = 0
choices_num = [0] * 120
skills_num = [0] * 120
speedup_time = 1  # 快进倍数


def scale(Surface, sx, sy):
	return pygame.transform.smoothscale(Surface, (sx, sy))


def delay(delay_time):
	if (speedup_time > 10000): return
	pygame.time.delay(delay_time // speedup_time + 1)


def pl_alpha_init():
	for item in pl.player_in_game:
		s = "resources/player/%s/%s.jpg" % (item.img_path, item.img_path)
		print(s)
		tmp = pygame.image.load(s)
		tmp = pygame.transform.smoothscale(tmp, (100, 160))
		player_img.append(tmp)


def init():
	pygame.mixer_music.play(-1)
	player_img.clear()
	card_img.clear()
	rm.add()
	pl_alpha_init()
	for i in range(43):
		s = "resources/cards/card" + str(i) + ".jpg"
		print(s)
		tmp = pygame.image.load(s)
		card_img.append(tmp)
		pygame.draw.rect(screen, [255, 0, 0], [290, 500, (i + 1) * 10, 10])
		pygame.draw.rect(screen, [30, 20, 0], [290, 500, 430, 10], 2)
		pygame.display.flip()


def write(string, x, y, size, color=(0, 0, 0)):
	font = pygame.font.Font(u'C:/Windows/Fonts/f.TTF', size)
	text = font.render(string.zfill(2), 1, color)
	textpos = text.get_rect()
	textpos.topright = [x, y]
	screen.blit(text, textpos)


def Stwrite(string, x, y, size, color=(0, 0, 0)):  # 竖排
	font = pygame.font.Font(u'C:/Windows/Fonts/f.ttf', size)
	for i in range(len(string)):
		text = font.render(string[i], 1, color)
		textpos = text.get_rect()
		textpos.topright = [x, y + i * size]
		screen.blit(text, textpos)


def use_card_arrow(user_pos, aimer_pos):
	user_pos += 1
	aimer_pos += 1
	tot = len(pl.player_in_game)
	# tx = user_pos * 1000 / tot
	# ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
	# if (pl.player_in_game[user_pos - 1].auto == 1):
	#	tx, ty = 924, 520
	# pygame.draw.line(screen,[0,0,255],[tx,ty],[500,300],2)
	tx = (aimer_pos - (aimer_pos > pl.gamer_pos and pl.gamer_pos != -1)) * 1000 / (tot + (pl.gamer_pos == -1))
	ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
	if (pl.player_in_game[aimer_pos - 1].auto == 0):
		tx, ty = 924, 520
	pygame.draw.line(screen, [255, 0, 0], [tx, ty], [500, 300], 2)
	pygame.display.flip()
	delay(100)


class Button:
	def __init__(self, string, x, y, size, func, num=-1,in_skill=0):
		self.string, self.x, self.y, self.size = string, x, y, size
		self.width, self.height = len(self.string) * self.size, self.size
		self.num = num
		self.func = func
		self.in_skill = in_skill

	def check(self):
		pos = pygame.mouse.get_pos()
		dx, dy = self.x - pos[0], pos[1] - self.y
		return dx > 0 and dx < self.width and dy > 0 and dy < self.height

	def show(self):
		if (debug_mode):
			pygame.draw.rect(screen, (255, 0, 0), [self.x - self.width, self.y, self.width, self.height], 2)
		# pygame.draw.rect(screen, (200, 190, 150), [self.x - self.width-2, self.y-2, self.width+2, self.height+2], 0)
		# pygame.draw.rect(screen, (70, 50, 30), [self.x - self.width-2, self.y-2, self.width+2, self.height+2], 2)
		color = [0, 0, 0]
		if (self.check()):
			color = [255, 255, 0]
		write(self.string, self.x, self.y, self.size, color)

	def response(self):
		global choices_num
		# print(self.string)
		if (self.num != -1):
			choices_num[self.num] = 1
		else:
			if(self.in_skill != 0):
				self.func(self.in_skill)

			elif(self.func != 0):
				self.func()


class Label:
	def __init__(self, string, x, y, size):
		self.string, self.x, self.y, self.size = string, x, y, size
		self.width, self.height = len(self.string) * self.size, self.size

	def check(self):
		return 0

	def show(self):
		if (debug_mode):
			pygame.draw.rect(screen, (0, 0, 255), [self.x - self.width, self.y, self.width, self.height], 2)
		write(self.string, self.x, self.y, self.size, [0, 0, 0])

	def response(self):
		pass


class card_borad:
	def init(self, list):
		pass


def judge(title, ty, tsize, choices, cy, csize, func):
	"""title为选择的标题，choices为list填写所有选项"""
	task_queue.clear()
	task_queue.append(Label(title, 500 + tsize / 2 * len(title), ty, tsize))
	for i in range(len(choices)):
		x = 200 + 600 * ((i + 1) / (len(choices) + 1))
		task_queue.append(Button(choices[i], x + csize / 2 * len(choices[i]), cy, csize, i, i))
	while (sum(choices_num) < 1):
		if (func != 0):
			func()
	task_queue.clear()
	for i in range(len(choices_num)):
		if (choices_num[i] == 1):
			return i
	return -1


def update():
	pygame.display.flip()


def game_quit():
	pygame.quit()
	exit(0)


def game_start():
	global in_title
	in_title = 0

def edit_end():
	global in_edit
	in_edit = 0

def design_end():
	global in_design
	in_design = 0

def confirm():
	global has_confirm
	has_confirm = 1


def cancel():
	global has_cancel
	has_cancel = 1


def end_stage():
	global has_end
	has_end = 1


task_queue = []
skill_queue = []


def title():
	task_queue.clear()
	task_queue.append(Button("开始游戏", 580, 350, 40, game_start))
	task_queue.append(Button("退出", 540, 400, 40, game_quit))

	while (in_title):
		screen.fill(0)
		screen.blit(title_ground, [0, 0])
		write("三国杀", 725, 140, 150)
		for item in task_queue:
			item.show()
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit(0)
			if event.type == MOUSEBUTTONDOWN:
				for item in task_queue:
					if (item.check()):
						item.response()


def design():
	task_queue.clear()
	page = 1
	max_page = max(len(pl.player_list),len(gm.gamer_list))//14+1
	print(pl.scripts)
	for i in range(0, 14):
		if (i >= len(pl.player_list)): break
		item = pl.scripts[pl.player_list[i]]()
		pl.player_in_game.append(item)
	pl_alpha_init()
	pl.init()
	while(in_design):
		screen.fill(0)
		screen.blit(title_ground, [0, 0])
		for i in range(0,14):
			if (i >= len(pl.player_in_game)): break
			item = pl.player_in_game[i]
			item.std_output(20 + (i % 7) * 140, 20 + (i // 7) * 180, 0)

		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_q:
					if(page>1):
						page -= 1
						print("down")
				if event.key == K_q:
					if(page< max_page):
						page += 1
						print("up")
			if event.type == MOUSEBUTTONDOWN:
				for item in task_queue:
					if (item.check()):
						item.response()

def edit():
	pl.import_pl()
	gm.import_pl()
	print(pl.player_list)
	task_queue.clear()
	task_queue.append(Button("确定",650,450,25,edit_end))
	task_queue.append(Button("插入", 400, 450, 25, design))
	player_frame = []
	for i in range(rm.room_max_seat):
		player_frame.append([20+(i%7)*140,20+(i//7)*180])
	while (in_edit):
		screen.fill(0)
		screen.blit(title_ground, [0, 0])
		for item in player_frame:
			x,y = item
			pygame.draw.rect(screen,[30,20,0],[x,y,120,160],1)
		for item in task_queue:
			item.show()
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit(0)
			if event.type == MOUSEBUTTONDOWN:
				for item in task_queue:
					if (item.check()):
						item.response()
				# mpos = pygame.mouse.get_pos()
				# for i in range(rm.room_max_seat):
				# 	x, y = player_frame[i]
				# 	if(x<mpos[0]<x+120 and y<mpos[1]<y+160):
				# 		print(i)
				# 		design()
				# 		break







def cards_show():
	while (len(cd.throw_queue) > 1):
		cd.throw_queue.pop(0)
	for i in range(len(cd.throw_queue)):
		if (i >= len(cd.throw_queue)):
			break
		item = cd.throw_queue[i]
		if (item.alpha < 20):
			cd.throw_queue.remove(item)
			continue
		item.std_output(200 + 72 * i, 300, 70, 100)

		cd.throw_queue[i].alpha -= 15


def act_check():
	global speedup_time,debug_mode
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit(0)
		if event.type == MOUSEBUTTONDOWN:
			for item in task_queue:
				if (item.check()):
					item.response()
			if (pl.gamer_pos != -1):
				pl.player_in_game[pl.gamer_pos].choose()
				for item in skill_queue:
					if (item.check()):
						item.response()
		if event.type == pygame.KEYDOWN:
			if event.key == K_s:
				if 1 == speedup_time:
					speedup_time = 10000000
				else:
					cd.throw_queue = []
					speedup_time = 1
			if event.key == K_d:
				debug_mode ^= 1



def play(now_player):
	if (now_player == 0 or now_player.dead):
		return
	# delay(5)
	tot = len(pl.player_in_game)
	screen.blit(play_ground, [0, 0])

	dx = 500 - (71 * len(cd.throw_queue)) / 2
	for i in range(len(cd.throw_queue)):
		if (i >= len(cd.throw_queue)):
			break
		item = cd.throw_queue[i]

		if (item.alpha < 50):
			cd.throw_queue.remove(item)
			continue
		item.std_output(dx + i * 71, 300, 70, 100)
		cd.throw_queue[i].alpha *= 0.9 / speedup_time
	# delay(10)
	chosen_seat = [0] * 120
	if (pl.gamer_pos != -1):
		for i in range(120):
			if (pl.player_in_game[pl.gamer_pos].pl_chosen[i] == 1):
				chosen_seat[pl.player_in_game[i].seat] = 1
		for i in range(1, tot + 1):
			tx = (i - (i > pl.gamer_pos and pl.gamer_pos != -1)) * 1000 / (tot + (pl.gamer_pos == -1))
			ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
			tx -= 60
			ty -= 80
			for item in pl.player_in_game:
				if (item.seat == i - 1):
					item.std_output(tx, ty)
			# pl.player_in_game[i-1].std_output(tx,ty)
			if (pl.gamer_pos != -1):
				if (chosen_seat[i - 1] == 1):  # 被选中的框
					if (i == pl.gamer_pos + 1):
						tx, ty = 850, 440
					pygame.draw.rect(screen, [255, 255, 0], [tx - 1, ty - 1, 122 + (i == pl.gamer_pos + 1) * 30, 162],
									 5)
			if (i - 1 == now_player.seat):
				if (pl.player_in_game[i - 1].auto == 1):
					pygame.draw.rect(screen, [255, 255, 0], [tx - 1, ty - 1, 122, 162], 1)
				else:
					pygame.draw.rect(screen, [255, 255, 0], [849, 439, 151, 161], 1)
		for item in skill_queue:
			item.show()
	else:
		for i in range(1, tot + 1):
			tx = (i - (i > pl.gamer_pos and pl.gamer_pos != -1)) * 1000 / (tot + (pl.gamer_pos == -1))
			ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
			tx -= 60
			ty -= 80
			# for item in pl.player_in_game:
			# 	if(item.seat == i-1):
			# 		item.std_output(tx, ty)
			pl.player_in_game[i - 1].std_output(tx, ty)
			if (i - 1 == now_player.seat):
				pygame.draw.rect(screen, [255, 255, 0], [tx - 1, ty - 1, 122, 162], 1)
	for item in task_queue:
		item.show()

	pygame.display.flip()
