# -*- coding: utf-8 -*-
"""
Email: parssataghipour@gmail.com
@author: SF1917
"""

import unittest
import datetime
import genetic
import random


def get_sums(genes, diagonalSize):
    rows = [0 for _ in range(diagonalSize)]
    columns = [0 for _ in range(diagonalSize)]
    southeastDiagonalSum = 0
    northeastDiagonalSum = 0
    
    for row in range(diagonalSize):
        for column in range(diagonalSize):
            value = genes[row * diagonalSize + column]
            rows[row] += value
            columns[column] += value
        southeastDiagonalSum += genes[row * diagonalSize + row]
        northeastDiagonalSum += genes[row * diagonalSize + 
                                      (diagonalSize - 1 - row)]
        
    return rows, columns, northeastDiagonalSum, southeastDiagonalSum


def get_fitness(genes, diagonalSize, expectedSum):
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
        get_sums(genes, diagonalSize)
        
    sumOfDifferences = sum(int(abs(s - expectedSum))
                           for s in rows + columns +
                           [southeastDiagonalSum, northeastDiagonalSum]
                           if s != expectedSum)
    
    return Fitness(sumOfDifferences)


def display(candidate, diagonalSize, startTime):
    timeDiff = datetime.datetime.now() - startTime
    
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
        get_sums(candidate.Genes, diagonalSize)
        
    for rowNumber in range(diagonalSize):
        row = candidate.Genes[rowNumber * diagonalSize:
            (rowNumber + 1) * diagonalSize]
        print("\t", row, "=", rows[rowNumber])
    print(northeastDiagonalSum, "\t", columns, "\t",
          southeastDiagonalSum)
    print("- - - - - - - - - - -", candidate.Fitness, str(timeDiff))
 
    
def mutate(genes, indexes):
    indexA, indexB = random.sample(indexes, 2)
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA]

    
class Fitness:
    SumOfDifferences = None
    
    def __init__(self, sumOfDifferences):
        self.SumOfDifferences = sumOfDifferences
    
    def __gt__(self, other):
        return self.SumOfDifferences < other.SumOfDifferences
    
    def __str__(self):
        return "{0}".format(self.SumOfDifferences)


class MagicSquareTests(unittest.TestCase):
    def test_size_4(self):
        self.generate(4, 50)
        
    def test_benchmark(self):
        genetic.Benchmark.run(self.test_size_4)
        
    def generate(self, diagonalSize, maxAge):
        nSquared = diagonalSize * diagonalSize
        geneset = [i for i in range(1, nSquared + 1 )]
        expectedSum = diagonalSize * (nSquared + 1 ) / 2
        
        def fnGetFitness(genes):
            return get_fitness(genes, diagonalSize, expectedSum)
        
        def fnDisplay(candidate):
            display(candidate, diagonalSize, startTime)
            
        geneIndexes = [i for i in range(0, len(geneset))]    
            
        def fnMutate(genes):
            mutate(genes, geneIndexes)
        
        def fnCustomCreate():
            return random.sample(geneset, len(geneset))
        
        optimalValue = Fitness(0)
        startTime = datetime.datetime.now()
        best = genetic.get_best(fnGetFitness, nSquared, 
                                optimalValue, geneset, 
                                fnDisplay, fnMutate,
                                fnCustomCreate, maxAge)
        self.assertTrue(not optimalValue > best.Fitness)
        
if __name__ == "__main__":
    unittest.main()        
        

        
        
        
            
            
                            
                
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        