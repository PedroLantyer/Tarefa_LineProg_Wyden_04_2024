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
    def __init__(self, lpSense, problemName = None) -> None:
        self.lpSense = lpSense #-1 FOR MAX / 1 FOR MIN / 0 FOR EQUAL TO
        if (problemName == None): self.problem = pulp.LpProblem(sense=lpSense)
        else: self.problem = pulp.LpProblem(name=problemName, sense=lpSense)

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
        
    def SetNumModifiers(self, productList):
        try:
            self.numModifierList = []
            for i in range(len(productList)):
                num = int(productList[i].productProfitMargin)
                self.numModifierList.append(num)
        
        except Exception as err:
            print("Failed to set num modifiers")
            print(err)
            return False
        
        else:
            return True

    def SetObjective(self, varList = None, numModifierList = None):
        try:
            if(varList == None): x = self.varList
            else: x = varList
            
            if(numModifierList == None): a = self.numModifierList
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

    def PrintPrimalProblemResults(self):
        try:
            profit = 0
            varValues = []
            varNames = []
            
            for i in range(len(self.varList)):
                varValues.append(self.varList[i].varValue)
                varNames.append(self.varList[i].name)
                profit += (varValues[i] * self.numModifierList[i])

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

def PrimalProblem():
    cafeDaManha = Product("Cafe da Manha", profit=25, category="Integer", lowBound=30, upBound= 130)
    pratoPrincipal = Product("Prato Principal", profit=30, category="Integer", lowBound=20, upBound=70)
    coffeeBreak = Product("Coffee Break", profit=20, category="Integer", lowBound=40, upBound=150)
    jantar = Product("Jantar", profit=40, category="Integer", lowBound=20, upBound=55)
    
    primalProblem = Problem(lpSense=(-1), problemName= "Problema Primal")
    menu = [cafeDaManha, pratoPrincipal, coffeeBreak, jantar]
    
    try:
        if not(primalProblem.SetVariableList(menu)): raise Exception("Failed to set variable list")
        if not(primalProblem.SetNumModifiers(menu)): raise Exception("Failed to set profit margins")
        if not(primalProblem.SetObjective()): raise Exception("Failed to set objective")
        if not(primalProblem.SetConstraint(numModifierList=[1,1,1,1], lpSense=(-1), constraintLimit=350)): raise Exception("Failed to set constraints")
        if not(primalProblem.SolveProblem()): raise Exception("Failed to solve problem")

        if (primalProblem.status == 1):
            if(primalProblem.PrintPrimalProblemResults()): raise Exception("Failed to print results")

    except Exception as err:
        print(err)
        print("Failed to solve primal problem")

if __name__ == "__main__":

    PrimalProblem()

