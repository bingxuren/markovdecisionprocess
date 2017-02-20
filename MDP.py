#Bingxu Ren
#programming assignment 6, CSC339 AI
#contains both value iteration and policy iteration

import copy

def createMDP():
	#initialize states in a an array
	states = [0] * 16
	for i in range(16):
		states[i] = i

	#initialize actions using numbers 0 to 3
	actions = [0, 1, 2, 3]   ##{0: '^', 1: '<', 2: '>', 3: 'v'}

	#initialize transition models, 3d array 16x16x4
	transition_model = [[[0.0 for x in range(4)] for y in range(16)] for z in range(16)]
	ss = 0  #s'
	for s in states:
		for a in actions:
			if a == 0:
				if (s / 4) == 3:
					ss = s - 4
				else:
					ss = s + 4
				transition_model[ss][s][a] += 0.7
				if (s / 4) == 0:
					ss = s + 4
				else:
					ss = s - 4
				transition_model[ss][s][a] += 0.2
				transition_model[s][s][a] += 0.1
			elif a == 1:
				if (s % 4) != 0:
					ss = s - 1
				else:
					ss = s + 1
				transition_model[ss][s][a] += 0.7
				if (s % 4) == 3:
					ss = s - 1
				else:
					ss = s + 1
				transition_model[ss][s][a] += 0.2
				transition_model[s][s][a] += 0.1
			elif a == 2:
				if (s % 4) == 3:
					ss = s - 1
				else:
					ss = s + 1
				transition_model[ss][s][a] += 0.7
				if (s % 4) == 0:
					ss = s + 1
				else:
					ss = s - 1
				transition_model[ss][s][a] += 0.2
				transition_model[s][s][a] += 0.1
			else:
				if (s / 4) == 0:
					ss = s + 4
				else:
					ss = s - 4
				transition_model[ss][s][a] += 0.7
				if (s / 4) == 3:
					ss = s - 4
				else:
					ss = s + 4
				transition_model[ss][s][a] += 0.2
				transition_model[s][s][a] += 0.1


	'''for i in range(16):
		for j in range(16):
			print transition_model[i][j]'''

	#initialize rewards, flat array
	rewards = [0] * 16
	for i in range(16):
		rewards
		if i == 10:
			rewards[10] = 100
		elif i == 12:
			rewards[12] = 200
		elif i % 2 == 0:
			rewards[i] = 0
		else:
			rewards[i] =50

	return (states, actions, transition_model, rewards)

def valueIteration(mdp):
	states = mdp[0]
	actions = mdp[1]
	t = mdp[2]  #transition model
	r = mdp[3]  #reward
	gamma = 0.95
	uu = [0]*16  #initialize U' , all 0
	sumOverActions = [0]*4
	delta = 0
	improving = True
	while improving:
		u = copy.deepcopy(uu)  #prevent object pointer
		delta = 0
		for s in states:
			sumOverActions = [0]*4
			for a in actions:
				#sumOverActions[a] = 0
				for ss in states:
					sumOverActions[a] += t[ss][s][a]*u[ss]
			uu[s] = r[s] + gamma*max(sumOverActions)
			delta = max(delta, abs(uu[s] - u[s]))
		improving = (delta >= 0.001* (1-gamma)/gamma)

	policy = [0]*16  #default policy, all moving upward
	valueOfActions = [0]*4
	for s in states:
		policy[s] = 0
		for a in actions:
			valueOfActions[a] = 0
			for ss in states:
				valueOfActions[a] += t[ss][s][a]*u[ss]
		policy[s] = valueOfActions.index(max(valueOfActions))
	#print policy
	#print u
	return policy, u

def policyIteration(mdp):
	states = mdp[0]
	actions = mdp[1]
	t = mdp[2]  #transition model
	r = mdp[3]  #reward
	u = [0]*16  #initialize u to all 0
	sumOverActions = [0]*4
	gamma = 0.95
	policy = [1]*16
	unchanged = False
	while not unchanged:
		for k in range(1, 100):
			for s in states:
				total = 0
				for ss in states:
					a = policy[s]
					total += t[ss][s][a]*u[ss]
				u[s] = r[s] + gamma*total
		unchanged = True
		for s in states:
			#find the best policy
			sumOverActions = [0]*4
			for a in actions:
				#sumOverActions[a] = 0
				for ss in states:
					sumOverActions[a] += t[ss][s][a]*u[ss]
			maxA = max(sumOverActions)
			bestA = sumOverActions.index(maxA)
			if maxA > sumOverActions[policy[s]]:
				policy[s] = bestA
				unchanged = False
		'''if unchanged:
			break'''

	#print policy, u
	return policy, u
def printPolicy(policies):
	print 'policy:\n'
	#format the output
	po = ''
	#split the list into four rows
	r1 = policies[0:4]
	r2 = policies[4:8]
	r3 = policies[8:12]
	r4 = policies[12:16]
	for p in r4:
		if p == 0:
			po = po + '^    '
		elif p == 1:
			po = po + '<    '
		elif p == 2:
			po = po + '>    '
		elif p == 3:
			po = po + 'v    '
	po = po + '\n'
	for p in r3:
		if p == 0:
			po = po + '^    '
		elif p == 1:
			po = po + '<    '
		elif p == 2:
			po = po + '>    '
		elif p == 3:
			po = po + 'v    '
	po = po + '\n'
	for p in r2:
		if p == 0:
			po = po + '^    '
		elif p == 1:
			po = po + '<    '
		elif p == 2:
			po = po + '>	'
		elif p == 3:
			po = po + 'v    '	
	po = po + '\n'
	for p in r1:
		if p == 0:
			po = po + '^    '
		elif p == 1:
			po = po + '<    '
		elif p == 2:
			po = po + '>    '
		elif p == 3:
			po = po + 'v    '
	po = po + '\n'
	print po

def printUtility(utilities):
	print 'value function:\n'
	#round all numbers
	u = [int(ele) for ele in utilities]
	#split the list into four rows
	r1 = u[0:4]
	r2 = u[4:8]
	r3 = u[8:12]
	r4 = u[12:16]
	uo = ''
	for el in r4:
		uo = uo + str(el) + '    '
	uo = uo + '\n'
	for el in r3:
		uo = uo + str(el) + '    '
	uo = uo + '\n'
	for el in r2:
		uo = uo + str(el) + '    '
	uo = uo + '\n'
	for el in r1:
		uo = uo + str(el) + '    '
	uo = uo + '\n'
	print uo

def main():
	mdp = createMDP()
	policy1, utility1 = valueIteration(mdp)
	policy2, utility2 = policyIteration(mdp)

	#print out the map
	print 'map:\n'
	m = 's12  s13  s14  s15\n s8   s9  s10  s11\n s4   s5   s6   s7\n s0   s1   s2   s3\n'
	print m
	print 'value iteration:\n'
	#print out the policy
	printPolicy(policy1)
	#print out the value function
	printUtility(utility1)

	print 'policy iteration:\n'
	printPolicy(policy2)
	printUtility(utility2)
main()


