#!/usr/bin/env python3


from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

class MinecraftAPI():
	
        #contruct and connect the minecraft game with python
	def __init__(self):
		self.mineObj = Minecraft.create()

        #return the current position of the player
	def getPlayerPosition(self):
		return self.mineObj.player.getPos()

        #set certain type of blocks with it's coordinates
	def setBlock(self,x, y, z, blockType):
                self.mineObj.setBlock(x, y, z, blockType)
                self.x = x
                self.y = y
                self.z = z

        #return the the position of the last block
	def getCursor(self):
		return Vec3(self.x, self.y, self.z)
	
        #set the server player's position
	def setPlayerPosition(self ,x ,y ,z):
		self.mineObj.player.setPos(x, y, z)

