from ast import Continue
from os import name
from random import random
from classes.game import Person, bcolors
from classes.magic import spell
from classes.inventory import Item
import random

# Create Black Magic
fire = spell("Fire", 10, 100, "black") # (self, name, cost, dmg, type)
thunder = spell("Thunder", 10, 100, "black")
blizzard = spell("Blizzard", 10, 100, "black")
meteor = spell("Meteor", 20, 200, "black")
quake = spell("Quake", 14, 140, "black")

# Create White Magic
cure = spell("Cure", 12, 120, "white")
cura = spell("Cura", 18, 200, "white")

#Create Some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "fully restore HP/MP ", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully Restores prty's HP/MP", 9999)
#weapons-throughable
grenade = Item("Grenade", "throughable", "Deals 500 Damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_item = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
{"item":superpotion, "quantity": 5}, {"item":elixer, "quantity": 5},
{"item":hielixer, "quantity": 2}, {"item":grenade, "quantity": 5}]
# Instantiate people
player1 = Person("Dev :", 5000, 50, 180, 30, player_magic, player_item) #(self,name, hp, mp, atk, df, magic, Items)
player2 = Person("Ram :", 4500, 50, 140, 30, player_magic, player_item)
player3 = Person("Bot :", 4000, 50, 120, 30, player_magic, player_item)

enemy1 = Person("Villan: ", 4000, 50, 100, 50, enemy_spells, [])
enemy2 = Person("Roofi: ", 3500, 40, 85, 45, enemy_spells, [])
enemy3 = Person("Meeka: ", 3000, 45, 80, 40, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "GAME STARTED***" + bcolors.ENDC)

while running:
      print ("====================")

      print("\n\n")
      print("NAME            " + bcolors.OKGREEN + "HEALTH" + bcolors.ENDC + "                                     " + bcolors.OKBLUE + "MAGIC POINTS" + bcolors.ENDC)


      for player in players:
         
         player.get_player_stats()
         
      print("\n")

      for enemy in enemies:
         enemy.get_enemy_stats()
      
      for player in players:

         player.choose_action()
         choice = input("choose Your Action:")
         index = int(choice) - 1

         if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print ("You attacked " + enemies[enemy].name.replace(" ","") + " for ", dmg, " Points of damage.")

            if enemies[enemy].get_hp() == 0:
               print(enemies[enemy].name.replace(" ","") + "has died")
               del enemies[enemy]

         elif index == 1:

            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
               continue


            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
               print (bcolors.FAIL + "\nNot Enough Mp\n" + bcolors.ENDC)
               continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
               player.heal(magic_dmg)
               print(bcolors.FAIL + "\n" + spell.name + "heals for ", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_tartet(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print (bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                   print(enemies[enemy].name.replace(" ","") + "has died")
                   del enemies[enemy]


         elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Your Item= ")) - 1

            if item_choice == -1:
               continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0 :
               print(bcolors.FAIL + "\n" + "Noone Left..." + bcolors.ENDC)
               continue

            player.items[item_choice]["quantity"]  -= 1

            if item.type == "potion":
               player.heal(item.prop)
               print(bcolors.OKBLUE + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

               if item.name == "MegaElixer":
                  for i in players:
                     i.hp = i.maxhp
                     i.mp = i.maxhp
               else:

                  player.hp = player.maxhp
                  player.mp = player.maxmp
               print(bcolors.OKBLUE + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
               enemy = player.choose_tartet(enemies)

               enemies[enemy].take_damage(item.prop)
               
               print(bcolors.OKBLUE + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

               if enemies[enemy].get_hp() == 0:
                  print(enemies[enemy].name.replace(" ","") + "has died")
                  del enemies[enemy]
      #chek if battle is over
      defeated_enemies = 0
      defeated_players = 0

      for enemy in enemies:
         if enemy.get_hp() == 0:
            defeated_enemies += 1
      for player in players:
         if player.get_hp() == 0:
            defeated_players +=1
      #check if player won
      if defeated_enemies == 2:
         print(bcolors.OKGREEN + "You Win" + bcolors.ENDC)
         running = False
      
      #check if enemy won
      elif defeated_players == 2:
         print (bcolors.OKBLUE + bcolors.FAIL + "Your enemy has defeated you" + bcolors.ENDC)
         running = False
      print("\n")
      #empty attack phase
      for enemy  in enemies:
         enemy_choice = random.randrange(0, 2)

         if enemy_choice == 0:
            #chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print (enemy.name.replace(" ","") + "attackes " + players[target].name.replace(" ","") + "for ", enemy_dmg)
         
         elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
               enemy.heal(magic_dmg)
               print(bcolors.OKBLUE + spell.name + "heals " + enemy.name + " for ", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ","") + "'s" + spell.name + "deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ","") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                   print(players[target].name.replace(" ","") + "has died")
                   del players[player]
            #print("Enemy choose", spell, "damage is ", magic_dmg)