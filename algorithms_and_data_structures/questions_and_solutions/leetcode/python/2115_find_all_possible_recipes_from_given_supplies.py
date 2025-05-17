from collections import deque
class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        if len(recipes) <= 0: return []
        
        inEdges = defaultdict(int)
        adjList = defaultdict(list)

        for i in range(len(recipes)):
            for ingredient in ingredients[i]: 
                adjList[ingredient].append(recipes[i])
                inEdges[recipes[i]] += 1
        
        sources = deque(supplies)

        while sources:
            v = sources.popleft()
            for child in adjList[v]:
                inEdges[child] -= 1
                if inEdges[child] == 0: sources.append(child)
        
        res = []
        for recipe in recipes:
            if inEdges[recipe] == 0: res.append(recipe)

        return res