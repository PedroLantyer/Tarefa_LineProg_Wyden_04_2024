import pulp
import sys

class Product:
    def __init__(self, productName, profit, category, lowBound=None, upBound=None) -> None:
        self.productName = productName
        self.category = category
        self.productProfitMargin = profit

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
        
    def SetProfitMargin(self, productList):
        try:
            self.profitMarginList = []
            for i in range(len(productList)):
                num = int(productList[i].productProfitMargin)
                self.profitMarginList.append(num)
        
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
            
            if(numModifierList == None): a = self.profitMarginList
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
                profit += (varValues[i] * self.profitMarginList[i])

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

    cafeDaManha = Product("Cafe da Manha", profit=25, category="Integer", lowBound=30, upBound= 130)
    pratoPrincipal = Product("Prato Principal", profit=30, category="Integer", lowBound=20, upBound=70)
    coffeeBreak = Product("Coffee Break", profit=20, category="Integer", lowBound=40, upBound=150)
    jantar = Product("Jantar", profit=40, category="Integer", lowBound=20, upBound=55)
    
    primalProblem = Problem(lpSense=-1)
    menu = [cafeDaManha, pratoPrincipal, coffeeBreak, jantar]
    
    if ( not(primalProblem.SetVariableList(menu)) or 
    not(primalProblem.SetProfitMargin(menu)) or
    not(primalProblem.SetObjective()) or
    not(primalProblem.SetConstraint(numModifierList=[1,1,1,1], lpSense=(-1), constraintLimit=350)) or
    not(primalProblem.SolveProblem())):
        sys.exit(1)

    if (primalProblem.status == 1):
        if(primalProblem.PrintResults()): sys.exit(0)
        sys.exit(1)

