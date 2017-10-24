import datetime
import bigram_segmentation.test_utils

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

# This function splits a word into syllables in the following way: It always splits the consonants between two vowels. The first consonant after the first vowel belongs to the first syllable, all other consonants (if any) belong to the second syllable. For example  "rusten" becomes "rus-ten" and "papapa" becomes "pap-ap-a"

def InitialSplitWordOnSyllable(word):
    # We first determine the locations of the vowels
    wordLength = len(word)
    vowelPositions = []
    for i in range(wordLength):
        letter = word[i]
        if letter in vowels:
            vowelPositions.append(i)

    outputWord = word
    # We keep splitting between two vowels until every syllable contains just one vowel
    for i in range(2, len(vowelPositions) + 1):
        outputWord = outputWord[0:vowelPositions[-i] + 2] + "-" + outputWord[vowelPositions[-i] + 2:]
    if outputWord[-1] == '-':
    	outputWord = outputWord[0:-1]
    return outputWord

# illegal letter combinations (pm, lf, lm, ...)
# If a syllable starts with a illegal letter combination, the first letter is moved to the previous syllable
def fixIllegalCombinationsSyllable(input, firstLetter, secondLetter): # input is a word that is already divided into syllables (but syllabification may be wrong)
    syllables = input.split('-')
    for i in range(len(syllables)):
        if firstLetter + secondLetter in syllables[i]:
            syllables[i - 1] += firstLetter
            syllables[i] = syllables[i][1:]

    return "-".join(syllables)

# Our initial split function always splits after a vowel+consonant, while if there's only one consonant between two vowels, that consonant should belong to the second syllable. This function fixes that.
def fixSingleConsonant(input):
    syllables = input.split('-')
    for i in range(len(syllables)):
        # If the first letter of a syllable is a vowel and the last letter of the previous syllable is a consonant, we move the consonant
        #print('hoi      '+ syllables[i])
        if syllables[i][0] in vowels:
            if i - 1 < 0:
                continue
            if not syllables[i - 1][-1] in vowels:
                syllables[i] = syllables[i - 1][-1] + syllables[i]
                syllables[i - 1] = syllables[i - 1][0:-1]

    return "-".join(syllables)


# fixes two vowels in a row
def fixDoubleVowels(input):
    syllables = input.split('-')
    for i in range(len(syllables)):
        if len(syllables[i]) >= 2:
            # if the two last letters in a syllable are both vowels, the second vowel moves to the next syllable
            if syllables[i][-2] in vowels and syllables[i][-1] in vowels:
                if i + 1 == len(syllables): # an extra empty syllable is created when needed
                    syllables.append('')
                syllables[i + 1] = syllables[i][-1] + syllables[i + 1]
                syllables[i] = syllables[i][0:-1]

    return "-".join(syllables)

# This function makes sure that the onset and the code are ranked correctly by sonorancy
def fixSonorantConsonants(input): # input is a word initially split into syllables
    syllables = input.split('-')
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
                    # If the last character need to move to the right, then an extra syllable is created at the end
                    if i + 1 == len(syllables):
                        syllables.append('')
                    # All characters that have lower rank than some character closer to the vowel are moved to the next syllable
                    syllables[i + 1] = syllables[i][rightI:] + syllables[i + 1]
                    syllables[i] = syllables[i][0:rightI]
                    change = True
                    break

                if change:
                    break
        i += 1

    return "-".join(syllables)

# In Dutch, the letter "h" can never be at the coda. This function fixes that.
def removeHFromCoda(input):
    syllables = input.split('-')
    for i in range(len(syllables)):
        for char in range(len(syllables[i])):
            change = False
            # search for the vowel in the syllable to find the coda (to the right of the vowel)
            if syllables[i][char] in vowels:
                for rightI in range(char + 1, len(syllables[i])):
                    # search for an "h" in the coda and move it to next syllable
                    if syllables[i][rightI] == 'h':
                        if i + 1 == len(syllables):
                            syllables.append('')
                        syllables[i + 1] = syllables[i][rightI:] + syllables[i + 1]
                        syllables[i] = syllables[i][0:rightI]
                        change = True
                        break
                if change:
                    break

    return "-".join(syllables)

def getSonorant(input):
    if input in glides:
        return 1
    if input in liquids:
        return 2
    if input in nasals:
        return 3
    if input in stops or input in fricatives:
        return 4
    return 0

# In this function, we combine the InitialSplitWordOnSyllable function together with all other functions to fix errors in the initial split.
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
        print(str(i + 1) + ": " + input[i])

def createOutputFile(output):
    currentDatetime = datetime.datetime.now()
    parsedDatetime = str(currentDatetime.day) + "-" + str(currentDatetime.month) + "-" + str(currentDatetime.year) + "_" + str(currentDatetime.hour) + ":" + str(currentDatetime.minute) + ":" + str(currentDatetime.second)
    with open("syllabification_" + ".txt", "w+") as f:
        for line in output:
            f.write(line + "\n")

if __name__ == "__main__":
    with open("corpus/CGN-NL-50k-utt.txt", "r+") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    #with open("corpus/DSWC-Syllabified-(1).txt", "r+") as f:
    #    originalLines = f.readlines()
    #originalLines = [line.strip() for line in originalLines]

    output = []
    for i in range(len(lines)):
        output.append(splitOnSyllables(lines[i]))


    #(true_positives, true_negatives, false_positives, false_negatives) = (0, 0, 0, 0)
    #for j in range(len(lines)):
    #    result = bigram_segmentation.test_utils.compare_lines(originalLines[j], output[j], "-")
    #    true_positives += result[0]
    #    true_negatives += result[1]
    #    false_positives += result[2]
    #    false_negatives += result[3]

    #print("TP: {0}\nTN: {1}\nFP: {2}\nFN: {3}".format(true_positives, true_negatives, false_positives, false_negatives))
    #result = bigram_segmentation.test_utils.test_rates([true_positives, true_negatives, false_positives, false_negatives])
    #print("True Positive Rate: {0}\nFalse Positive Rate: {1}\nTrue Negative Rate: {2}".format(result[0], result[1], result[2]))

    createOutputFile(output)
    #prettyPrint(output)