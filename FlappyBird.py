#Importing libraries
from tkinter import *
import time
from PIL import ImageTk, Image
import random


#SETTING CONSTANTS
path = 'flappy-bird.png'
background = 'background2.jpg'
WIDTH = 400
HEIGHT = 400
x_speed = -0.25
bird_g = 0.0006
bird_speed = 0
score = 0
frameCount = 0
divider = 300

#DEFINING KEY LISTENER FUNCTION
def keyPressed(event):
	global x_speed
	global bird_speed
	global bird_g
	input = event.keysym
	if(input=="Up"):
		bird_g+=0.003
		x_speed-=0.1
	elif(input=="Down"):
		x_speed+=0.1
	elif(input=="space"):
		bird_speed=-0.13
	


class MainScreen:
	def __init__(self,width,height,parent,bird,background):
		''' Initializing the Main screen properties'''

		self.parent = parent
		self.bird = bird
		self.parent.resizable(False,False)
		self.canvas = Canvas(self.parent,width=width,height=height,bg='white')
		self.parent.title('Main Screen')
		self.canvas.pack()
		self.background = background
		self.bg = self.canvas.create_image(0,0,image=self.background)
		self.canvas.move(self.bg,0,110)
		self.begin_game()
		self.parent.mainloop()

	def begin_game(self):

		global score
		global divider
		
		self.bird_controller = self.bird.show(self.canvas)
		self.bird_coords = self.canvas.coords(self.bird_controller)
		self.parent.bind("<Key>",keyPressed)
		numbers = []


		self.pipes = []
		self.not_dead = True
		score1 = self.canvas.create_text(200,40,text='Score: {}'.format(str(int(score/divider))),fill='white',font=('Times new roman',15,'bold'))
		#self.line=self.canvas.create_line(self.bird_coords[0]+12,0,self.bird_coords[0]+12,400)

		
		
		############'''Game Main Loop'''##############
		
		while self.not_dead:
			global frameCount
			global bird_speed
			
			global bird_g
			
			bird_speed+=bird_g
			frameCount+=1
			if(frameCount%1800 == 0):
				pipe = Pipe(400,0,430,30,80)
				self.pipes.append(pipe.show(self.canvas))
			self.pipes = [x for x in self.pipes if not self.determine(x)]


			#Moving the pipes
			for pipelist in self.pipes:
				for pipe in pipelist:
					self.canvas.move(pipe,-0.07,0)
					self.bird_coords = self.canvas.coords(self.bird_controller)
				if(self.bird_coords[1]+20>367):
					bird_speed=0
					self.canvas.move(self.bird_controller,0,-bird_g)
				else:
					self.canvas.move(self.bird_controller,0,bird_speed)
				if(self.is_collided(self.bird_controller,self.pipes)):
					
					print("{} CONGRATULATIONS!! YOUR SCORE IS {}".format("Amr",int(score/divider)))
					self.not_dead = False

				else:
					pass

			next_pipe = self.detect_next_pipe()
			if(next_pipe):
				if(self.bird_coords[0]>self.canvas.coords(next_pipe[0])[0]):
					score+=1

			
			self.canvas.itemconfigure(score1, text=str(str(int(score/divider))))


			
			self.canvas.tag_raise(score1)
			self.canvas.update()
	def detect_next_pipe(self):
		dist_dict = {}
		bird_coords = self.bird_coords
		for pipelist in self.pipes:
			for pipe in pipelist:
				pipe_coords = self.canvas.coords(pipe)
				if(pipe_coords[2]-bird_coords[0]>0):
					dist_dict.update({pipe:pipe_coords[0]})

		
		r = list(dist_dict)
		return r



	def determine(self,x):
		if(self.canvas.coords(x[0])[2]>0):
			return False
		else:
			return True
	def is_collided(self,bird,pipes):
		bird_coords = self.canvas.coords(bird)
		for pipelist in pipes:
			for pipe in pipelist:
				pipe_coords = self.canvas.coords(pipe)
				if(bird_coords[0]+12>pipe_coords[0] and bird_coords[0]+12<pipe_coords[2] and bird_coords[1]+10>pipe_coords[1] and
					bird_coords[1]-10<pipe_coords[3]):
					return True

class Pipe: 	
	def __init__(self,x1,y1,x2,y2,gap):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.gap = gap
		
	def show(self,canvas):
		gap_y = random.randint(40,315)
		pipes = []
		pipes.append(canvas.create_rectangle(self.x1,0,self.x2,gap_y-self.gap/2,fill='green'))
		pipes.append(canvas.create_rectangle(self.x1,gap_y+self.gap/2,self.x2,354.5,fill='green'))
		return pipes

	
class Bird:
	def __init__(self,x1,y1,x2,y2,icon):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.icon = icon

	def show(self,canvas):
		return canvas.create_image(self.x1,self.y1,image=self.icon)



root = Tk()

img = Image.open(path)
bg = Image.open(background)

bird = Bird(200,210,230,240,ImageTk.PhotoImage(img))

main_screen = MainScreen(WIDTH,HEIGHT,root,bird,ImageTk.PhotoImage(bg))
