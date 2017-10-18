import datetime

shortVowels = ["I", "A", "O", "}", "@"]
longVowels = ["i", "y", "e", "|", "a", "o", "u", ")"]
vowels = ["A", "E", "}", "O", "I", "a", "e", "i", "y", "|", "o", "u", ")", "@", "!", "(", "*", "<", "K", "L", "M"] #contains short-vowels, longs-vowels and borrowed vowels
glides = ["w", "j"]
liquids = ["l", "r"]
nasals = ["m", "n", "N"]
stops = ["p", "b", "t", "d", "k", "g"]
fricatives = ["f", "v", "s", "z", "x", "G", "h", "S"]
diphthongs = ["K", "L", "M"]

def InitialSplitWordOnSyllable(word):
    wordLength = len(word)
    vowelPositions = []
    for i in range(wordLength):
        letter = word[i]
        if letter in vowels:
            vowelPositions.append(i)

    outputWord = word
    for i in range(2, len(vowelPositions) + 1):
        outputWord = outputWord[0:vowelPositions[-i] + 2] + " " + outputWord[vowelPositions[-i] + 2:]

    return outputWord

# illegal letter combinations (pm, lf, lm)
def fixIllegalCombinationsSyllable(input, firstLetter, secondLetter):
    syllables = input.split()
    for i in range(len(syllables)):
        if firstLetter + secondLetter in syllables[i]:
            syllables[i - 1] += firstLetter
            syllables[i] = syllables[i][1:]

    return " ".join(syllables)

def fixDoubleVowels(input):
    syllables = input.split()
    for i in range(len(syllables)):
        if syllables[i][-2] in vowels and syllables[i][-1] in vowels:
            syllables[i + 1] = syllables[i][-1] + syllables[i + 1]
            syllables[i] = syllables[i][0:-1]

    return " ".join(syllables)

def fixSonorantConsonents(input):
    syllables = input.split()
    for i in range(len(syllables)):
        for char in range(len(syllables[i])):
            if syllables[i][char] in vowels:
                leftLowestRank = 0
                rightLowestRank = 0
                rightChange = False
                for leftI in range(0, char)[:-1]:
                    rank = getSonorant(syllables[i][leftI])
                    if rank > leftLowestRank:
                        leftLowestRank = rank
                        continue
                    syllables[i - 1] = syllables[i - 1] + syllables[i][0:leftI]
                    syllables[i] = syllables[i][leftI:]
                    break

                for rightI in range(char + 1, len(syllables[i])):
                    rank = getSonorant(syllables[i][rightI])
                    if rank > rightLowestRank:
                        rightLowestRank = rank
                        continue
                    syllables[i + 1] = syllables[i][rightI:] + syllables[i + 1]
                    syllables[i] = syllables[i][0:rightI]
                    rightChange = True
                    break

                if rightChange:
                    break

    return " ".join(syllables)

def getSonorant(input):
    if input in glides:
        return 1
    if input in liquids:
        return 2
    if input in nasals:
        return 3
    if input in stops or input in fricatives:
        return 4

def splitOnSyllables(input):
    output = []
    words = input.split(" ")
    for word in words:
        output.append(InitialSplitWordOnSyllable(word))

    return "".join(output)

def createOutputFile(output):
    currentDatetime = datetime.datetime.now()
    parsedDatetime = str(currentDatetime.day) + "-" + str(currentDatetime.month) + "-" + str(currentDatetime.year) + "_" + str(currentDatetime.hours) + ":" + str(currentDatetime.minutes) + ":" + str(currentDatetime.seconds)
    with open("syllabificatiion_" + parsedDatetime + ".txt", "w+") as f:
        for line in output:
            f.write(line + "\n")

if __name__ == "__main__":
    #lines = []
    #with open("corpus.txt", "r+") as f:
    #    lines.append(f.readline())

    #output = []
    #for i in range(len(lines)):
    #    output.append(splitOnSyllables(lines[i]))

    #createOutputFile(output)
    #print output

    print fixSonorantConsonents(InitialSplitWordOnSyllable("meklmekl"))