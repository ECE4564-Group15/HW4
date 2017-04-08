#!/usr/bin/env python3


from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

class MinecraftAPI():
	
	def __init__(self):
		self.mineObj = Minecraft.create()

	def getPlayerPosition(self):
		return self.mineObj.player.getPos()

	def setBlock(self,x, y, z, blockType):
                self.mineObj.setBlock(x, y, z, blockType)
                self.x = x
                self.y = y
                self.z = z
	def getCursor(self):
		return Vec3(self.x, self.y, self.z)
	
	def setPlayerPosition(self ,x ,y ,z):
		self.mineObj.player.setPos(x, y, z)

