class testClass(object):
    def __init__(self):
        self.text = "this is a test."
    
    def printout(self):
        print self.text


if __name__ == "__main__":
    test = testClass()
    test.printout()