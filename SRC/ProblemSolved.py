import pulp
import sys

class Product:
    def __init__(self, productName, price, category, lowBound=None, upBound=None) -> None:
        self.productName = productName
        self.category = category
        self.productPrice = price

        if(lowBound != None): self.lowBound = lowBound
        else: self.lowBound = None
        if(upBound != None): self.upBound = upBound
        else: self.upBound = None

    def SetProductVariable(self):
        try:
            self.productVariable = pulp.LpVariable(name=self.productName, lowBound=self.lowBound, upBound=self.upBound, cat=self.category)
        
        except Exception as err:
            print("Failed to create Variable")
            print(err)
            return False
        
        else:
            return True
        
    def GetProductVariable(self):
            return self.productVariable

class Problem:
    def __init__(self, lpSense) -> None:
        self.lpSense = lpSense #-1 FOR MAX / 1 FOR MIN / 0 FOR EQUAL TO
        self.problem = pulp.LpProblem(sense=lpSense)
        pass

    def SetVariableList(self, productList):
        try:
            self.varList = []
            
            for i in range(len(productList)):
                if not(productList[i].SetProductVariable()): raise Exception("Failed to get Variables")
                self.varList.append(productList[i].GetProductVariable())
        
        except Exception as err:
            print(err)
            return False

        else:
            return True
        
    def SetPrices(self, productList):
        try:
            self.priceList = []
            for i in range(len(productList)):
                num = int(productList[i].productPrice)
                self.priceList.append(num)
        
        except Exception as err:
            print("Failed to get num modifiers")
            print(err)
            return False
        
        else:
            return True

    def SetObjective(self, varList = None, numModifierList = None):
        try:
            if(varList == None): x = self.varList
            else: x = varList
            
            if(numModifierList == None): a = self.priceList
            else: a = numModifierList

            e = pulp.LpAffineExpression([(x[i],a[i]) for i in range(len(x))])
            objective = pulp.LpConstraint(e=e, sense=self.lpSense, name="Objective")
            self.problem.setObjective(objective)

        except Exception as err:
            print("Failed to set Objective")
            print(err)
            return False
        
        else:
            return True
        
    def SetConstraint(self, numModifierList, lpSense, constraintLimit, varList=None):
        try:
            if(varList == None): x = self.varList
            else: x = varList
            
            a = numModifierList
            e = pulp.LpAffineExpression([(x[i],a[i]) for i in range(len(x))])
            constraint = pulp.LpConstraint(e=e, sense=lpSense, rhs=constraintLimit)
            self.problem.addConstraint(constraint=constraint)
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True

    def PrintResults(self):
        try:
            profit = 0
            varValues = []
            varNames = []
            
            for i in range(len(self.varList)):
                varValues.append(self.varList[i].varValue)
                varNames.append(self.varList[i].name)
                profit += (varValues[i] * self.priceList[i])

            print("Resultados:")
            print("Lucro: R$%.2f" % profit)
            for i in range(len(varValues)):
                print("%s: %d unidade(s)" % (varNames[i], varValues[i]))
            print("")
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True

    def SolveProblem(self):
        try:
            self.status = self.problem.solve()
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True

if __name__ == "__main__":

    entrada = Product("Entrada", price=15, category="Integer", lowBound=0)
    pratoPrincipal = Product("Prato Principal", price=30, category="Integer", lowBound=0)
    sobremesa = Product("Sobremesa", price=10, category="Integer", lowBound=0)
    
    problem = Problem(lpSense=-1)
    menu = [entrada, pratoPrincipal, sobremesa]
    
    if ( not(problem.SetVariableList(menu)) or 
    not(problem.SetPrices(menu)) or
    not(problem.SetObjective()) or
    not(problem.SetConstraint(numModifierList=[1,1,1], lpSense=(-1), constraintLimit=100)) or
    not(problem.SolveProblem())):
        sys.exit(1)

    if (problem.status == 1):
        if(problem.PrintResults()): sys.exit(0)
        sys.exit(1)

