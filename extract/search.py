def getWords(self, how, length):
    # sanitize
    if how not in ["dgf", "tgf", "dgh", "tgh"]:
        return {}
    if int(len) > 49 or int(len) < 2:
        return {}

    for i in range(count):
        length = self.gc.findLength(lengthObj)
        word = self.gc.findWord(Qdict, depth, length)
        words.append(word)
    return words


def prepare():
    if 'how' in form:
        if how == 'dgf':
            filename = 'resource/qd2g_f.pck'
            depth = 2
            result = findWords(20, self.qd2g_f, 2, len)
        elif form['how'].value == 'tgf':
            result = findWords(20, self.qd3g_f, 3, len)
        elif form['how'].value == 'dgh':
            result = findWords(20, self.qd2g_h, 2, len)
        elif form['how'].value == 'tgh':
            result = findWords(20, self.qd3g_h, 3, len)

    collection = {}
    with open(filename, 'rb') as f:
        collection = pickle.load(f)
    result = findWords(20, collection, depth, length)
    return json.dumps(result)


def findWord(self, quickDict, depth, length):
    word = self.findStart(quickDict, depth)
    while len(word) < length:
        # TODO: sometimes key not found
        try:
            prevSlice = quickDict[word[len(word) - depth:]]
            nextChar = self.findCharacter(prevSlice)
            word += nextChar
        except KeyError as e:
            break
    return word

if __name__ == "__main__":
    print("hello")