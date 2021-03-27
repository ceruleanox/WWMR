from random import randint

class MarkovLyrics:
    def __init__(self):
        self.chain = {} 

    def populateMarkovChain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")

            for i in range(len(words) - 1):
                word = words[i]

                if word in self.chain:
                    next_word = words[i+1]
                    self.chain[word].append(next_word)
                else: 
                    next_word=words[i+1]
                    self.chain[word] = [next_word]

    def generateLyrics(self, length=500):
        n = len(self.chain)

        start_index =  randint(0, n-1)
        keys = list(self.chain.keys())
        current_word = keys[start_index].title()
        
        lyrics = current_word + " "

        for _ in range(length):
            # if reaching end of sentence / no new key/value pair in Markov chain
            if current_word not in self.chain: 
                lyrics += "\n"
                next_index = randint(0, n-1)
                current_word = keys[next_index]
            else:
                next_words = self.chain[current_word]
                next_index = randint(0, len(next_words)-1)
                next_word = next_words[next_index]
                lyrics += next_word + " "
                current_word = next_word
        return lyrics

'''
data = ["One night and one more time Thanks for the memories, even though they weren't so great", "And you're a cherry blossom You're about to bloom You look so pretty, but you're gone so soon"]
m = MarkovLyrics()
m.populateMarkovChain(data)
print(m.generateLyrics())
'''