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

illegalCombinations = ["pm", "pf", "mk", "tm", "tp", "tk"]

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

    return outputWord#fjgskjdkjgjh

# illegal letter combinations (pm, lf, lm)
def fixIllegalCombinationsSyllable(input, firstLetter, secondLetter):
    syllables = input.split()
    for i in range(len(syllables)):
        if firstLetter + secondLetter in syllables[i]:
            syllables[i - 1] += firstLetter
            syllables[i] = syllables[i][1:]

    return " ".join(syllables)

def fixSingleConsonant(input):
    syllables = input.split()
    for i in range(len(syllables)):
        if syllables[i][0] in vowels:
            if i - 1 < 0:
                continue
            if not syllables[i - 1][-1] in vowels:
                syllables[i] = syllables[i - 1][-1] + syllables[i]
                syllables[i - 1] = syllables[i - 1][0:-1]

    return " ".join(syllables)


# fixes two vowels in a row
def fixDoubleVowels(input):
    syllables = input.split()
    for i in range(len(syllables)):
        if len(syllables[i]) >= 2:
            if syllables[i][-2] in vowels and syllables[i][-1] in vowels:
                if i + 1 == len(syllables):
                    syllables.append('')
                syllables[i + 1] = syllables[i][-1] + syllables[i + 1]
                syllables[i] = syllables[i][0:-1]

    return " ".join(syllables)

# This function makes sure that the onset and the code are ranked correctly by sonorancy
def fixSonorantConsonants(input): # input is a word initially split into syllables
    syllables = input.split()
    i = 0
    while i < len(syllables):
        for char in range(len(syllables[i])):
            # search for the vowel in the syllable
            if syllables[i][char] in vowels:
                leftLowestRank = 0
                rightLowestRank = 0
                change = False
                for leftI in range(0, char)[::-1]:
                    # 's' is a special character that can be at the beginning of a word without acting as a part of the onset
                    if syllables[i][leftI] == 's':
                        continue
                    rank = getSonorant(syllables[i][leftI])
                    if rank > leftLowestRank:
                        leftLowestRank = rank
                        continue
                    # If the first character need to move to the left, then an extra syllable is created at the beginning
                    if i  == 0:
                        syllables = [''] + syllables
                        i += 1
                    # All characters that have lower rank than some character closer to the vowel are moved to the previous syllable
                    syllables[i - 1] = syllables[i - 1] + syllables[i][0:leftI + 1]
                    syllables[i] = syllables[i][leftI + 1:]
                    change = True
                    break

                for rightI in range(char + 1, len(syllables[i])):
                    rank = getSonorant(syllables[i][rightI])
                    if rank >= rightLowestRank:
                        rightLowestRank = rank
                        continue
                    if i + 1 == len(syllables):
                        syllables.append('')
                    syllables[i + 1] = syllables[i][rightI:] + syllables[i + 1]
                    syllables[i] = syllables[i][0:rightI]
                    change = True
                    break

                if change:
                    break
        i += 1

    return " ".join(syllables)

def removeHFromCoda(input):
    syllables = input.split()
    for i in range(len(syllables)):
        for char in range(len(syllables[i])):
            # search for the vowel in the syllable
            change = False
            if syllables[i][char] in vowels:
                for rightI in range(char + 1, len(syllables[i])):
                    if syllables[i][rightI] == 'h':
                        if i + 1 == len(syllables):
                            syllables.append('')
                        syllables[i + 1] = syllables[i][rightI:] + syllables[i + 1]
                        syllables[i] = syllables[i][0:rightI]
                        change = True
                        break
                if change:
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
        splittedWord = InitialSplitWordOnSyllable(word)
        splittedWord = fixSonorantConsonants(splittedWord)
        splittedWord = fixDoubleVowels(splittedWord)
        splittedWord = fixSingleConsonant(splittedWord)

        for letters in illegalCombinations:
            splittedWord = fixIllegalCombinationsSyllable(splittedWord, letters[0], letters[1])

        output.append(splittedWord)

    return " ".join(output)

def prettyPrint(input):
    for i in range(len(input)):
        print str(i + 1) + ": " + input[i]

def createOutputFile(output):
    currentDatetime = datetime.datetime.now()
    parsedDatetime = str(currentDatetime.day) + "-" + str(currentDatetime.month) + "-" + str(currentDatetime.year) + "_" + str(currentDatetime.hours) + ":" + str(currentDatetime.minutes) + ":" + str(currentDatetime.seconds)
    with open("syllabificatiion_" + parsedDatetime + ".txt", "w+") as f:
        for line in output:
            f.write(line + "\n")

def compareResults(input, correctSource):
    with open(correctSource, "r+") as f:
        return #TODO find a way to compute hit rates etc.

if __name__ == "__main__":
    lines = []
    with open("corpus/manually_syllabified_corpus.txt", "r+") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    output = []
    for i in range(len(lines)):
        output.append(splitOnSyllables(lines[i]))

    #compareResults(output, "corpus/DSWC-Syllabified.txt")

    #createOutputFile(output)
    prettyPrint(output)