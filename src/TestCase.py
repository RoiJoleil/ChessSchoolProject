class TestCase:
    # Test methods to Test if Certain mehtods behave as expected
    def Testing(func, a, b):
        if func(a, b):
            print("Test successfull")
            return True
        else:
            print("actual Result: {test} deviates from expected Result {expectedResult}")
            return False
        
    def checkBool(a:bool, b:bool):
        return a==b
    def TestIsEqual(self, test:bool, expectedResult:bool):
        return self.Testing(self.checkBool, test, expectedResult )
