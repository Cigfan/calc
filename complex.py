import math

import sys

def minimalNumber(x):
    x = round(x, 3)
    if type(x) is str:
        if x == '':
            x = 0
    f = float(x)
    if f.is_integer():
        return int(f)
    else:
        return f

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

class ComplexNumber:

    def __init__(self, a, b=0, is_complex=True):
        # either a+jb or a + arg(b)
        if is_complex:
            self.r = a
            self.j = b
        else:
            degrees = (b/360)*2*math.pi
            self.r = math.cos(degrees) * a
            self.j = math.sin(degrees) * a

    def __add__(self, num):
        return ComplexNumber(self.r + num.r, self.j + num.j)

    def __sub__(self, num):
        return ComplexNumber(self.r - num.r, self.j - num.j)

    def toArg(self):
        if self.r == 0:
            if self.j > 0:
                div = math.pi / 2
            else:
                div = - math.pi / 2
            
            if self.j == 0:
                div = 0
        else:
            div = math.atan(self.j / self.r)

        return [
            math.sqrt(self.r**2 + self.j**2),
            360 * div/(2*math.pi)
        ]

    def __mul__(self, num):
        this = self.toArg()
        other = num.toArg()
        return ComplexNumber(this[0] * other[0], this[1] + other[1], False)

    def __eq__(self, num):
        if not num:
            return False
        if not self.r == num.r:
            return False
        if not self.j == num.j:
            return False
        return True

    def __truediv__(self, num):
        this = self.toArg()
        other = num.toArg()
        #print(this, other)
        return ComplexNumber(this[0] / other[0], this[1] - other[1], False)


    def getFormattedComplex(self):
        r = round(self.r, 3)
        j = round(self.j, 3)
        s = ""
        if not r == 0 or j == 0:
            s += str(minimalNumber(r))
        if not j == 0:
            if j > 0 and len(s) > 0:
                s += "+"
            elif j < 0:
                s += "-"
            s += "j"
            if not abs(j) == 1:
                s += str(minimalNumber(abs(j)))
        return s     

    def __repr__(self):
        arg1, arg2 = self.toArg()

        s = self.getFormattedComplex()
        if not arg2 == 0:
            s += " [%s<%s°]" % (minimalNumber(arg1), minimalNumber(arg2))
        return s


if __name__ == '__main__':
    action = None
    num = ComplexNumber(0)

    variables = {}
    this = None

    last_ans = None
    x = 0
    
    while True:
        data = input(" <<< ")
       
        try:
            STORE_IN = None

            if len(data) == 0:
                data  = " "
            
            split = data.split(" ")
            for item in split:
                done = False

                if item.endswith("="):
                    STORE_IN = item.replace("=", "").lower()
                    continue

                if item.lower() in variables:
                    this = variables[item.lower()]
                    done = True

                if '<' in item:
                    a, b = item.split("<")
                    A = float(a)
                    B = float(b)
                    this = ComplexNumber(A, B, False)
                    done = True
                    #print(item, "parsed to", this)

                # handle methods
                if done == False and len(item) < 3 and not hasNumbers(item):
                    done = True
                    if '*' in item:
                        action = 1
                    elif '/' in item:
                        action = 2
                    elif '+' in item:
                        action = 3
                    elif '-' in item:
                        action = 4
                    else:
                        done = False

                #print(done, action)
                # handle x+jY
                if not done and len(item) > 0:
                    method = None
                    if "+" in item:
                        method = "+"
                    elif "-" in item:
                        method = "-"
                    elif "j" in item:
                        if len(item) == 1:
                            item = "j1"
                        this = ComplexNumber(0, float(item.replace("j","")))
                    else:
                        this = ComplexNumber(float(item), 0)

                    if method:
                        #print("m", method, item)
                        if "j" in item:
                            a,B = item.split(method)
                            if "j" in a:
                                a, B = B, a
                            if len(B) == 1:
                                B = "j1"
                        else:
                            a = item
                            B = "0"

                        if len(a) == 0:
                            a = "0"

                        a = float(a)
                        b = float(B.replace("j", ""))
                        if method == "-":
                            b = -b

                        #print(a, b)
                    
                        this = ComplexNumber(a, b)
                    # print(item, "parsed to", this)

                if not this == None:
                    if action:
                        #print(num, "&&", this)
                        if action == 1:
                        # print("*")
                            res = num * this
                        elif action == 2:
                        #  print("/")
                            res = num / this
                        elif action == 3:
                        #  print("+")
                            res = num + this
                        elif action == 4:
                        # print("-")
                            res = num - this
                        else:
                            res = num
                        action = None

                        num = res
                        this = None
                    else:
                        num = this
                        this = None
            
            if not STORE_IN == None:
                variables[STORE_IN] = num


            if not num == last_ans:
                x += 1
                if x > 9:
                    x = 0
                
                variables["a"+  str(x)] = num
                last_ans = num

            variables["ans"] = num
        

            #this = num

            print("A" + str(x) + ">", num)
        except Exception as e:
            print("Error:", str(e))