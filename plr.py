from sys import *

class Token:
	t = None
	v = None
	def __init__(self, t, v):
		self.t = t
		self.v = v

class varTok:
	t = "varTok"
	n = None
	v = None
	def __init__(self, n, v):
		self.n = n
		self.v = v

class addTok:
	t = "addTok"
	f = None
	s = None
	def __init__(self,f, s):
		self.f = f
		self.s = s

	def exe(self):
		global vars
		vars[self.f].v += vars[self.s].v

class addNumTok:
	t = "addTok"
	f = None
	s = None
	def __init__(self,f, s):
		self.f = f
		self.s = s

	def exe(self):
		global vars
		vars[self.f].v += self.s.v

#DEFINITION TOKS
class defTok:
	t = "defTok"
	n = None
	c = []
	def __init__(self, n):
		self.n = n

class callDefTok:
	t = "callDefTok"
	n = None
	def __init__(self, n):
		self.n = n

	def exe(self):
		global defs
		for i in range(0, len(defs)):
			if defs[i].n == self.n:
				for j in range(0, len(defs[i].c)):
					defs[i].c[j].exe()





#Function Toks
class DisplayTok:
	t = "displayTok"
	v = []
	def __init__(self, v):
		self.v = v

	def exe(self):
		for i in range(0, len(self.v)):
			if self.v[i].v == "\n":
				print("")
			else:
				print(self.v[i].v)



file = list(open(argv[1], "r").read())
#print(file)

toks = []
newToks = []
vars = []
defs = []

def lex():
	#LEX
	tok = ""
	global toks
	strState = 0
	varState = 0
	numState = 0
	comState = 1
	defState = 0
	callDefState = 0

	line = 1
	for char in file:
		#print(char)
		if comState == 0:
			if char == "\n":
				line += 1
				comState = 0
			if char == "%" and strState == 0 and varState == 0 and defState == 0 and numState == 0:
				comState = 1
			elif char == "\"" and strState == 0 and varState == 0 and defState == 0 and numState == 0:
				strState = 1
				tok = ""
			elif char == "\"" and strState == 1:
				strState = 0
				toks.append(Token("string", tok))
				tok = ""
			elif char == "*" and varState == 0 and defState == 0 and strState == 0 and numState == 0:
				varState = 1
				tok = ""
			elif (char == " " or char == "\n") and varState == 1 and defState == 0 and strState == 0 and numState == 0:
				toks.append(Token("var", tok))
				varState = 0
				tok = ""
			elif char == "$" and numState == 0 and defState == 0 and varState == 0 and strState == 0:
				numState = 1
				tok = ""
			elif char == "~" and defState == 0 and numState == 0 and varState == 0 and strState == 0:
				defState = 1
				tok = ""
			elif (char == " " or char == "\n") and defState == 1 and numState == 0 and varState == 0 and strState == 0:
				toks.append(Token("defStart", tok))
				defState = 0
				tok = ""
			elif (char == " " or char == "\n") and defState == 0 and numState == 1 and varState == 0 and strState == 0:
				toks.append(Token("num", int(tok)))
				numState = 0
				tok = ""
			elif char == "@" and callDefState == 0 and defState == 0 and numState == 0 and varState == 0 and strState == 0:
				callDefState = 1
				tok = ""
			elif (char == " " or char == "\n") and callDefState == 1 and defState == 0 and numState == 0 and varState == 0 and strState == 0:
				toks.append(Token("callDef", tok))
				callDefState = 0
				tok = ""
			else:
				tok += char
#				print(tok)
				if strState == 0 and varState == 0:
					if tok == " " or tok == "\t":
						tok = ""
					elif tok == "=":
						toks.append(Token("op", "="))
						tok = ""
					elif tok == "+":
						toks.append(Token("op", "+"))
						tok = ""
					elif tok == "\n":
						tok = ""
					elif tok == "{":
						toks.append(Token("ident", "{"))
						tok = ""
					elif tok == "}":
						toks.append(Token("ident", "}"))
						tok = ""
					elif tok == "display":
						toks.append(Token("func", "display"))
						tok = ""
					elif tok == "End" or tok == "end" or tok == "END":
						toks.append(Token("defEnd", "end"))
						tok = ""
		elif char == "\n":
			comState = 0

					#TESTING#
#	##############################################
#	for i in range(0, len(toks)):
#		print( toks[i].t, ":", toks[i].v )
#	print("")
#	print("Your File Contains:", line, "Lines")
#	###############################################

def readToks():
	global toks
	global newToks
	global vars
	global defs
	newDefState = 0
	i = 0

	while i < len(toks):
#		print(toks[i].t)
		if toks[i].t == "var":
			i += 1
			if toks[i].t == "op":
				if toks[i].v == "=":
					i += 1
					#if toks[i].t == "var":
					#else:
					varExists = False
					for j in range(0, len(vars)):
						if vars[j].n == toks[i-2].v:
							varNum = j
							varExists = True
					if varExists == True:
						vars[varNum].v = toks[i].v
#						print("Var Changed: ", toks[i-2].v, " : ", toks[i].v)
					elif varExists == False:
						vars.append(varTok(toks[i-2].v, toks[i].v))
#						print("Var Created: ", toks[i-2].v, " : ", toks[i].v)
				elif toks[i].v == "+":
					i += 1
					if toks[i].v == "=":
						i += 1
						if toks[i].t == "var":

							firstVar = 0
							for j in range(0, len(vars)):
								if vars[j].n == toks[i-3].v:
									firstVar = j
									break

							secondVar = 0
							for j in range(0, len(vars)):
								if vars[j].n == toks[i].v:
									secondVar = j
									break



#							print(firstVar, secondVar)
							if newDefState == 0:
								newToks.append(addTok(firstVar, secondVar))
							elif newDefState == 1:
								tempDef.c.append(addTok(firstVar, secondVar))

						elif toks[i].t == "num":
							firstVar = 0
							for j in range(0, len(vars)):
								if vars[j].n == toks[i-3].v:
									firstVar = j
									break

							if newDefState == 0:
								newToks.append(addNumTok(firstVar, toks[i]))
							elif newDefState == 1:
								tempDef.c.append(addNumTok(firstVar, toks[i]))

		elif toks[i].t == "func":
			if toks[i].v == "display":
				i += 1
				if toks[i].v == "{":
					i += 1
					tempArr = []
					for j in range(i, len(toks)):
#						print(toks[j].t)
						if toks[j].v == "}":
							i = j
							break
						elif toks[j].t == "var":
							for k in range(0, len(vars)):
#								print(vars[k].n, ":", toks[j].v)
								if vars[k].n == toks[j].v:
									tempArr.append(vars[k])
#									print("FOUND A MATCH")
						else:
							tempArr.append(toks[j])

					if newDefState == 0:
						newToks.append(DisplayTok(tempArr))
					elif newDefState == 1:
						tempDef.c.append(DisplayTok(tempArr))

		elif toks[i].t == "defStart":
			tempDef = defTok(toks[i].v)
			newDefState = 1

		elif toks[i].t == "defEnd":
			newDefState = 0
			defs.append(tempDef)

		elif toks[i].t == "callDef":
			newToks.append(callDefTok(toks[i].v))
			
		i += 1
					#TESTING#
#	##############################################
#	print("-=-=-=-=-=-=-=-=-=-=-=-")
#	print("NEW TOKS")
#	for i in range(0, len(newToks)):
#		print( newToks[i].t )
#	print("-=-=-=-=-=-=-=-=-=-=-=-")
#	###############################################

def exe():
	global newToks
	print("\n\n\n\n\n\n\n\n\n")
	print(">-<    PolaR    >-<")
	print("\n")
	for i in range(0, len(newToks)):
		newToks[i].exe()
	print("\n")
#	print(">-<    PolaR    >-<")

def run():
	lex()
	readToks()
	exe()

run()
