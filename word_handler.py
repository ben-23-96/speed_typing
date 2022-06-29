from requests import get


class WordHandler():
    def __init__(self):
        self.words_list = []
        self.incorrect_words_list = []
        self.current_word_index = 0
        self.correct_word_count = 0

    def generate_word_list(self):
        """retrieves a list of 100 random words from a api"""
        self.reset()
        response = get('https://random-word-api.herokuapp.com/word?number=100')
        words = response.json()
        self.words_list.extend(words)

    def reset(self):
        """resets all attributes to default values"""
        self.words_list = []
        self.incorrect_words_list = []
        self.correct_word_count = 0
        self.current_word_index = 0

    def check_typing_word_correctly(self, word_being_typed):
        """returns true if the word being typed matches the word to be typed so far, otherwise return false"""
        current_word = self.words_list[self.current_word_index]
        letter_index = len(word_being_typed)
        if current_word[:letter_index] == word_being_typed:
            return True
        else:
            return False

    def word_completed(self, word_typed):
        """if the that has been typed is correct adds 1 to the correct word count, otherwise adds the incorrect word and its counterpart to the incorrect word list.
         Adds 1 to the current word index"""
        current_word = self.words_list[self.current_word_index]
        if word_typed == current_word:
            self.correct_word_count += 1
        else:
            word_dict = {'original word': current_word,
                         'typed word': word_typed}
            self.incorrect_words_list.append(word_dict)
        self.current_word_index += 1
