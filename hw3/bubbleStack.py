import math
def iv(blockList):
    '''
    test docstring:
    >>> blocks = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18]]
    >>> iv(blocks)
    [1, 2, 0, 7, 1, 2, 4, 11, 1, 2, 8, 15, 9, 10, 12, 19, 1, 2]
    '''
    image=[]
    # iv is a two dimensional array, when every a layer has two element, element inside would be xor
    # togather, and then store into one higher layer, the height would be soooo long.
    stack = BubbleStack(int(math.log(len(blockList), 2)))
    current_iv = [0]
    for i in range(0,len(blockList)-1,2):
        a = blockList[i][0] ^ current_iv[0]
        b = blockList[i+1][0] ^ current_iv[0]
        image.append([a])
        image.append([b])
        stack.push([a^b])
        current_iv = stack.pop()
    return image

class BubbleStack:
    # constructor
    stack = []
    def __init__(self, size):
        self.stack = [None]*size
    # public operation:
    '''
    void push(value): put a value into the stack
    int pop():  get a value from the stack
    '''
    def push(self,data):
        '''
        push the iv into stack
        '''
        j=0
        new = data
        while(self.__get(j) != None):
            new = self.__merge(self.__get(j), new)
            j+=1
        self.__set(j, new)
        self.__clear(j)

    def pop(self):
        '''
        get the first value of stack
        '''
        j=0
        while(self.__get(j) == None):
            j+=1
        return self.__get(j)

    # private method
    def __merge(self,a,b):
        data = ""
        # second xor text with iv
        for a1,b1 in zip(a, b):
            # make the string in 0x00 form, or some informaiton would lose
            c = format(a1^b1, '#04x')
            data += c[2:]
        pText = bytes.fromhex(data)
        pText = pText[-5:] + pText[:-5]
        # encrypt text with key in ECB mode
        # return text for next round's iv
        return pText

    def __clear(self, index):
        j=0
        while(j < index):
            self.__set(j, None)
            j+=1

    def __get(self, index):
        return self.stack[index]

    def __set(self, index, value):
        self.stack[index] = value

if __name__ == "__main__":
    import doctest, math, bubbleStack
    doctest.testmod(bubbleStack)  # no test now