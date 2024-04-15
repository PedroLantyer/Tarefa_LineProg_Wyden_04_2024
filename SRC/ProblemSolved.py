import pulp
import os    

class TextHandling:
    def __init__(self) -> None:
        pass

    def ReplaceUnderlines(self, str):
        if(str.count("_") > 0):
            formatedStr = ""
            for char in str:
                if char == "_": formatedStr += " "
                else: formatedStr += char
            return formatedStr
        return str
    
    def ClearScreen(self):
        match os.name.upper():
            case "NT":
                os.system("cls")
            case _:
                pass

class Product:
    def __init__(self, productName, profit, category, lowBound=None, upBound=None) -> None:
        self.productName = productName
        self.category = category
        self.productProfitMargin = profit

        if(lowBound != None): self.lowBound = lowBound
        else: self.lowBound = None
        if(upBound != None): self.upBound = upBound
        else: self.upBound = None

    def SetVariable(self):
        try:
            self.productVariable = pulp.LpVariable(name=self.productName, lowBound=self.lowBound, upBound=self.upBound, cat=self.category)
        
        except Exception as err:
            print("Failed to create Variable")
            print(err)
            return False
        
        else:
            return True
        
    def GetVariable(self):
            return self.productVariable

class ProductionCosts:
    def __init__(self, varName, category ,lowBound ,upBound=None) -> None:
        self.varName = varName
        self.varCategory = category
        
        if(lowBound != None): self.lowBound = lowBound
        else: self.lowBound = None
        if(upBound != None): self.upBound = upBound
        else: self.upBound = None
    
    def SetVariable(self):
        try:
            self.productionCostVariable = pulp.LpVariable(name=self.varName, lowBound=self.lowBound, upBound=self.upBound, cat=self.varCategory)

        except Exception as err:
            print("Failed to create Variable")
            print(err)
            return False
        
        else:
            return True

    def GetVariable(self):
        return self.productionCostVariable

class Problem:
    def __init__(self, lpSense, problemName = None) -> None:
        self.InitalizeClasses()
        self.lpSense = lpSense #-1 FOR MAX / 1 FOR MIN / 0 FOR EQUAL TO
        if (problemName == None): 
            self.problem = pulp.LpProblem(sense=lpSense)
            self.problemName = None
        else: 
            self.problem = pulp.LpProblem(name=problemName, sense=lpSense)
            self.problemName = problemName
        

    def InitalizeClasses(self):
        self.txtHandling = TextHandling()

    def SetVariableList(self, varList):
        try:
            self.varList = []
            
            for i in range(len(varList)):
                if not(varList[i].SetVariable()): raise Exception("Failed to get Variables")
                self.varList.append(varList[i].GetVariable())
        
        except Exception as err:
            print(err)
            return False

        else:
            return True
    
    def SetNumModifiers(self, varList, numModifierList = None):
        try:
            self.numModifierList = []
            if(numModifierList == None):
                for i in range(len(varList)):
                    
                    match (self.problemName):
                        case "Problema Primal":
                            numMod = int(varList[i].productProfitMargin)
                        case "Problema Dual":
                            numMod = int(varList[i].upBound)
                        case _:
                            raise Exception("Invalid Problem type")
                    
                    self.numModifierList.append(numMod)
            
            else:
                self.numModifierList = numModifierList

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

    def SetVarValuesAndVarNames(self):
        try:
            self.varValues = []
            self.varNames = []
            for i in range(len(self.varList)):
                    self.varValues.append(self.varList[i].varValue)
                    self.varNames.append(self.varList[i].name)
        except Exception as err:
            print(err)
            return False
        else:
            return True
                
    def GetVarValues(self):
        return self.varValues

    def SetOptimalValue(self):
        try:
            self.optimalValue = 0
            for i in range(len(self.varList)):
                self.optimalValue += (self.varValues[i] * self.numModifierList[i])
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True

    def GetOptimalValue(self):
        return self.optimalValue
    
    def PrintPrimalProblemResults(self):
        try:
            print("Resultados:")
            print("Lucro: R$%.2f" % self.optimalValue)
            for i in range(len(self.varValues)):
                print("%s: %d unidade(s)" % (self.txtHandling.ReplaceUnderlines(self.varNames[i]), self.varValues[i]))
            print("")
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True
        
    def PrintDualProblemResults(self):
        try:
            print("Resultados: ")
            print("Soma do custo minimo das 4 refeicoes: R$%.2f" % self.optimalValue)
            for i in range(len(self.varValues)):
                print("%s: R$%.2f" % (self.txtHandling.ReplaceUnderlines(self.varNames[i]), self.varValues[i]))
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
    almoco = Product("Almoço", profit=30, category="Integer", lowBound=20, upBound=70)
    coffeeBreak = Product("Coffee Break", profit=20, category="Integer", lowBound=40, upBound=150)
    jantar = Product("Jantar", profit=40, category="Integer", lowBound=20, upBound=55)
    
    primalProblem = Problem(lpSense=(-1), problemName= "Problema Primal")
    menu = [cafeDaManha, almoco, coffeeBreak, jantar]
    
    try:
        if not(primalProblem.SetVariableList(menu)): raise Exception("Failed to set variable list")
        if not(primalProblem.SetNumModifiers(menu)): raise Exception("Failed to set profit margins")
        if not(primalProblem.SetObjective()): raise Exception("Failed to set objective")
        if not(primalProblem.SetConstraint(numModifierList=[1,1,1,1], lpSense=(-1), constraintLimit=350)): raise Exception("Failed to set constraints")
        if not(primalProblem.SolveProblem()): raise Exception("Failed to solve problem")
        if not(primalProblem.SetVarValuesAndVarNames()): raise Exception("Failed to set Variable values, and Variable Names")
        if not(primalProblem.SetOptimalValue()): raise Exception("Failed to set optimal value for primal problem")

        if (primalProblem.status == 1):
            return primalProblem

    except Exception as err:
        print(err)
        print("Failed to solve primal problem")

def DualProblem():
    prodCostsCafeDaManha = ProductionCosts(varName="Custo de produção do cafe da manha", category="Integer", lowBound=10, upBound=35)
    prodCostsAlmoco = ProductionCosts(varName="Custo de produção do almoço", category="Integer", lowBound=15, upBound=45)
    prodCostsCoffeeBreak = ProductionCosts(varName="Custo de produção do coffee break", category="Integer", lowBound=8, upBound=30)
    prodCostsJantar = ProductionCosts(varName="Custo de produção do jantar", category="Integer", lowBound=22, upBound=60)

    dualProblem = Problem(lpSense=1, problemName="Problema Dual")
    prodCosts = [prodCostsCafeDaManha, prodCostsAlmoco, prodCostsCoffeeBreak, prodCostsJantar]

    try:
        if not(dualProblem.SetVariableList(prodCosts)): raise Exception("Failed to set variable list")
        if not(dualProblem.SetNumModifiers(prodCosts, numModifierList=[1, 1, 1, 1])): raise Exception("Failed to set profit margins")
        if not(dualProblem.SetObjective()): raise Exception("Failed to set objective")
        if not(dualProblem.SetConstraint(numModifierList=[1,1,1,1], lpSense=1, constraintLimit=100)): raise Exception("Failed to set constraints")
        if not(dualProblem.SolveProblem()): raise Exception("Failed to solve problem")
        if not(dualProblem.SetVarValuesAndVarNames()): raise Exception("Failed to set Variable values, and Variable Names")
        if not(dualProblem.SetOptimalValue()): raise Exception("Failed to set optimal value for primal problem")
        
        if (dualProblem.status == 1):
            return dualProblem

    except Exception as err:
        print(err)
        print("Failed to solve dual problem")

if __name__ == "__main__":

    txtHandle = TextHandling()
    primalProblemResult = PrimalProblem()
    dualProblemResult = DualProblem()
    txtHandle.ClearScreen()
    primalProblemResult.PrintPrimalProblemResults()
    dualProblemResult.PrintDualProblemResults()
    
    

