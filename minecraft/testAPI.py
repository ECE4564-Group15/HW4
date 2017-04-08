#!/usr/bin/env python3

from MinecraftAPI import MinecraftAPI

def main():
        #make a minecraft object mc
	mc = MinecraftAPI()
	#get the current player position in x, y, z
	x, y, z = mc.getPlayerPosition()
	print(x, y, z)

	#set a block at certain position
	stone = 1
	grass = 2
	mc.setBlock(x+1,y,z,stone)
	mc.setBlock(x+2,y,z,grass)

	#set player position
	mc.setPlayerPosition(x+1, y, z)

	#get the position of the last setBlock
	print(mc.getCursor())
main()
