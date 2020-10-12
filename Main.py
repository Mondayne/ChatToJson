import urllib.request

#request user input
def ReceiveConsoleInput():
	val = input("Enter your message: ") 
	return val

#find mention in string
def FindMentions(string):
	mention = ""	
	for i, character in enumerate(string):	
		if i == 0:
			continue
		if character == " ":
			break
		mention += character
	return mention

#find urls in msg
def FindLinks(string):
	link = ""	
	for i, character in enumerate(string):
		if character == " ":
			break
		link += character
	return link

#find emoticons in string
def FindEmoticons(string):
	emoticon = ""
	for i, character in enumerate(string):
		if character == "(":
			continue
		if character == ")":
			break
		emoticon += character		
	return emoticon

#check if substring is a link
def IsLink(string):
	if len(string) >= 7 and string[0:7] == "http://":
		return True
	elif len(string) >=8 and string[0:8] == "https://":
		return True
	else:
		return False

#check if character is emoticon starter
def IsEmoticon(char):
	if char == "(":
		return True
	else:
		return False

#check if character is mention starter
def IsMention(char):
	if char == "@":
		return True
	else:
		return False

#check if character is new word starter
def IsWord(prevChar, currentChar):
	if prevChar == " " and currentChar != " ":
		return True
	else:
		return False

#form the json return
def FormJson(string):
	jsonReturn = "{"
	emoticons = []
	mentions = []
	links = []
	words = 0

	for i, character in enumerate(string):
		if IsEmoticon(character) == True:	
			emoticons += [FindEmoticons(string[i:len(string)])]
		elif IsLink(string[i:len(string)]) == True:
			links += [FindLinks(string[i:len(string)])]
		elif IsMention(character) == True:
			mentions += [FindMentions(string[i:len(string)])]
		elif i > 0 and IsWord(string[i-1], character) == True:
			words += 1
		elif i == 0 and IsWord(" ", character) == True:
			words += 1

	#build emoticon section
	if len(emoticons) > 0:
		jsonReturn += "\n\t\"emoticons\":["
		for i, emoticon in enumerate(emoticons):
			if i > 0:
				jsonReturn += ","
			jsonReturn += "\n\t\t\"" + emoticons[i] + "\""
		jsonReturn += "\n\t],"
		
	#build mention section
	if len(mentions) > 0:
		jsonReturn += "\n\t\"mentions\":["
		for i, mention in enumerate(mentions):
			if i > 0:
				jsonReturn += ","
			jsonReturn += "\n\t\t\"" + mentions[i] + "\""
		jsonReturn += "\n\t],"

	#build link section
	if len(links) > 0:
		jsonReturn += "\n\t\"links\":["
		for i, link in enumerate(links):
			if i > 0:
				jsonReturn += ","
			url = links[i]
			response = urllib.request.urlopen(url)
			title = str(response.read()).split('<title>')[1].split('</title>')[0]
			jsonReturn += "\n\t\t{\n\t\t\t\"url\": \"" + links[i] + "\",\n\t\t\t\"title\":\"" + title + "\"\n\t\t}"
		jsonReturn += "\n\t],"

	#build word section and return
	jsonReturn += "\n\t\"words\": " + str(words)
	jsonReturn += "\n}"
	return jsonReturn

#testMention = "@john hey, you around?"
#print(FormJson(testMention))

#testEmoticon = "Good morning! (smile) (coffee)"
#print(FormJson(testEmoticon))

#testEmoticonAndUrl = "The World Series is starting soon! (cheer) https://www.mlb.com/ and https://espn.com"
#print(FormJson(testEmoticonAndUrl))

#testAllUrl = "@mary @john (success) such a cool feature! Check this out: https://journyx.com/features-and-benefits/data-validation-tool"
#print(FormJson(testAllUrl))

msg = ReceiveConsoleInput()
print("Input: \"" + msg + "\"")
print("Return (string):\n" + FormJson(msg))

