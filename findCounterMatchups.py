import csv
import math

# Global Variables
HEROES = {'25': 'lina', '26': 'lion', '27': 'shadow_shaman', '20': 'vengefulspirit', '21': 'windrunner', '22': 'zuus', '23': 'kunkka', '28': 'slardar', '29': 'tidehunter', '4': 'bloodseeker', '8': 'juggernaut', '59': 'huskar', '58': 'enchantress', '55': 'dark_seer', '54': 'life_stealer', '57': 'omniknight', '56': 'clinkz', '51': 'rattletrap', '50': 'dazzle', '53': 'furion', '52': 'leshrac', '88': 'nyx_assassin', '89': 'naga_siren', '111': 'oracle', '110': 'phoenix', '113': 'arc_warden', '112': 'winter_wyvern', '82': 'meepo', '83': 'treant', '80': 'lone_druid', '81': 'chaos_knight', '86': 'rubick', '87': 'disruptor', '84': 'ogre_magi', '85': 'undying', '3': 'bane', '7': 'earthshaker', '108': 'abyssal_underlord', '109': 'terrorblade', '102': 'abaddon', '103': 'elder_titan', '100': 'tusk', '101': 'skywrath_mage', '106': 'ember_spirit', '107': 'earth_spirit', '104': 'legion_commander', '105': 'techies', '39': 'queenofpain', '38': 'beastmaster', '33': 'enigma', '32': 'riki', '31': 'lich', '30': 'witch_doctor', '37': 'warlock', '36': 'necrolyte', '35': 'sniper', '34': 'tinker', '60': 'night_stalker', '61': 'broodmother', '62': 'bounty_hunter', '63': 'weaver', '64': 'jakiro', '65': 'batrider', '66': 'chen', '67': 'spectre', '68': 'ancient_apparition', '69': 'doom_bringer', '2': 'axe', '6': 'drow_ranger', '99': 'bristleback', '98': 'shredder', '91': 'wisp', '90': 'keeper_of_the_light', '93': 'slark', '92': 'visage', '95': 'troll_warlord', '94': 'medusa', '97': 'magnataur', '96': 'centaur', '11': 'nevermore', '10': 'morphling', '13': 'puck', '12': 'phantom_lancer', '15': 'razor', '14': 'pudge', '17': 'storm_spirit', '16': 'sand_king', '19': 'tiny', '18': 'sven', '48': 'luna', '49': 'dragon_knight', '46': 'templar_assassin', '47': 'viper', '44': 'phantom_assassin', '45': 'pugna', '42': 'skeleton_king', '43': 'death_prophet', '40': 'venomancer', '41': 'faceless_void', '1': 'antimage', '5': 'crystal_maiden', '9': 'mirana', '77': 'lycan', '76': 'obsidian_destroyer', '75': 'silencer', '74': 'invoker', '73': 'alchemist', '72': 'gyrocopter', '71': 'spirit_breaker', '70': 'ursa', '79': 'shadow_demon', '78': 'brewmaster', '114': 'monkey_king', '120': 'pangolier', '119': 'dark_willow', '121': 'grimstroke'}
API = dota2api.Initialise("1264931900E3211B684F797C4DD7724A", raw_mode=True)


def didHeroWinMatch(heroString, tsvDataRow):
	return (heroString in tsvDataRow[2] and tsvDataRow[1] == 'True') or (heroString in tsvDataRow[3] and tsvDataRow[1] == 'False')

# Given 2 Heroes, shows stats between the two
# 	Output is: Num Games, Winrate of Hero1 against Hero2, Hero1 independent winrate, Hero2 independent winrate
# This method answers "How is hero1 agaisnt hero2"?
def dataForHeroMatchup(heroString1, heroString2):

	if (heroString1 not in HEROES.values()):
		print "Invalid hero string: " + heroString1
		return
	if (heroString2 not in HEROES.values()):
		print "Invalid hero string: " + heroString2
		return


	num_total_games_together = 0
	hero_one_wins_against_hero_two = 0.0

	hero_one_num_picked = 0
	hero_one_wins = 0.0

	hero_two_num_picked = 0
	hero_two_wins = 0.0

	with open("data.tsv") as tsv:
		for line in csv.reader(tsv, dialect="excel-tab"):

			hero_one_won = didHeroWinMatch(heroString1, line)
			hero_two_won = didHeroWinMatch(heroString2, line)

			radiantTeamArray = line[2].split(',')
			direTeamArray = line[3].split(',')

			for i in range(len(radiantTeamArray)):
				radiantTeamArray[i] = radiantTeamArray[i].strip().replace("'", "").replace('[', '').replace(']', '')
			for i in range(len(direTeamArray)):
				direTeamArray[i] = direTeamArray[i].strip().replace("'", "").replace('[', '').replace(']', '')

			if (heroString1 in radiantTeamArray or heroString1 in direTeamArray):
				hero_one_num_picked += 1
			if hero_one_won:
				hero_one_wins += 1

			if (heroString2 in radiantTeamArray or heroString2 in direTeamArray):
				hero_two_num_picked += 1
			if hero_two_won:
				hero_two_wins += 1

			if not ((heroString1 in radiantTeamArray and heroString2 in direTeamArray) or (heroString1 in direTeamArray and heroString2 in radiantTeamArray)):
				continue
			else:
				num_total_games_together += 1
				if hero_one_won:
					hero_one_wins_against_hero_two += 1

	if num_total_games_together > 0:
		print "Number of Total Games Together: " + str(num_total_games_together)
		print heroString1.upper() + " winrate over " + heroString2.upper() + ": " + str(100*hero_one_wins_against_hero_two/num_total_games_together) + "%"
		print heroString1.upper() + " winrate independent of  " + heroString2.upper() + ": " + str(100*hero_one_wins/hero_one_num_picked) + "%"
		print heroString2.upper() + " winrate independent of  " + heroString1.upper() + ": " + str(100*hero_two_wins/hero_two_num_picked) + "%"
	else:
		print "No match data between these two heroes"

# Given Hero, shows which heroes are good against it
# Outputs:	Enemy hero, Num Games Against, Winrate Against, Enemy hero's independent winrate		    	
def bestHeroesAgainstGivenHero(heroString, numTopHeroes):
	data = builHeroToStatsDictionary(heroString)
	newData = convertDict(data)
	sortedKeys = list(reversed(sorted(newData.keys(), key=float)))
	print "Best heroes against " + heroString
	print "Hero,  Number of Games Against, Winrate Against,  Total Winrate (independent of chosen hero)"
	
	# Dict is keyed by winrate, and values are arrays of hero along with data. Need to split values of dict
	# and find top [numTopHeroes] heroes.
	heroCount = 0
	i = 0
	while True:
		if newData[sortedKeys[i]] < 0:
			return
		for hero in newData[sortedKeys[i]]:
			if heroCount >= numTopHeroes:
				return
			print hero
			heroCount += 1
		i += 1

# Converts from shit to more useful shit
def builHeroToStatsDictionary(heroString):
	data = {}
	with open("data.tsv") as tsv:
		for line in csv.reader(tsv, dialect="excel-tab"):
	
			radiantTeamArray = line[2].split(',')
			direTeamArray = line[3].split(',')

			for hero in radiantTeamArray:
				hero = hero.strip().replace("'", "").replace('[', '').replace(']', '')
				if hero == heroString:
					continue
				isHeroOnEnemyTeam = (heroString in line[3])
				
				if hero in data.keys():
					newData = data[hero]
					if isHeroOnEnemyTeam:
						newData[0] += 1
						if line[1] == 'True':
							newData[1] += 1
					newData[2] += 1
					if line[1] == 'True':
						newData[3] += 1

				else: # First time gathering data for this hero
					newData = []
					if isHeroOnEnemyTeam:
						newData.append(1.0)
						if line[1] == 'True':
							newData.append(1.0)
						else:
							newData.append(0.0)
					else:
						newData.append(0.0)
						newData.append(0.0)
					newData.append(1.0)
					if line[1] == 'True':
						newData.append(1.0)
					else:
						newData.append(0.0)
				data[hero] = newData

			for hero in direTeamArray:
				hero = hero.strip().replace("'", "").replace('[', '').replace(']', '')
				if hero == heroString:
					continue
				isHeroOnEnemyTeam = (heroString in line[2])

				if hero in data.keys():
					newData = data[hero]
					if isHeroOnEnemyTeam:
						newData[0] += 1
						if line[1] == 'False':
							newData[1] += 1
					newData[2] += 1
					if line[1] == 'False':
						newData[3] += 1

				else: # First time gathering data for this hero
					newData = []
					if isHeroOnEnemyTeam:
						newData.append(1.0)
						if line[1] == 'True':
							newData.append(1.0)
						else:
							newData.append(0.0)
					else:
						newData.append(0.0)
						newData.append(0.0)
					newData.append(1.0)
					if not line[1]:
						newData.append(1.0)
					else:
						newData.append(0.0)

				data[hero] = newData
	return data

def weighFunction(numGamesAgainst, numWinsAgainst):
	return math.log((numGamesAgainst+1)) * (((numWinsAgainst/numGamesAgainst) * 2) - 1)

def convertDict(data):
	newDict = {}
	for key in data.keys():

		if (data[key][0] < 1 or data[key][2] < 1):
			continue

		newKey = weighFunction(data[key][0], data[key][1])
		newValue = []
		newValue.append(key)
		newValue.append(data[key][0])
		newValue.append(data[key][1]/data[key][0])
		newValue.append(data[key][3]/data[key][2])

		if newKey in newDict.keys():
			newDict[newKey].append(newValue)
		else:
			newDict[newKey] = [newValue]
	return newDict
