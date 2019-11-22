from threading import Thread
import numpy as np
import time

# Global variable to store multi-thread result and reference to threads
resultQueue = []
resultQueueMultiThread = []
threads = []

def checkLine(row, res):
    di = {}
    # print("Checking Row: " + str(row) + "\n")
    for i in range(1,10):
        if row[i-1] not in di:
            di[row[i-1]] = 1
        else:
            di[row[i-1]] += 1
    for num in di:
        if di[num] > 1:
            res.append(False)
    res.append(True) 

def checkMatrix(i, j, sudoku, res):
    grid = [sudoku[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
    if len(set(grid)) != len(grid):
        res.append(False)
    else:
        res.append(True)

def checkSudokuMultiThread(sudoku):
    # Check rows
    for i in range(len(sudoku)):
        t = Thread(target=checkLine, args=[sudoku[i], resultQueueMultiThread])
        t.start()
        threads.append(t)
    # Check columns
    transedMatrix = np.transpose(sudoku).tolist()
    for i in range(0, 9):
        t = Thread(target=checkLine, args=[transedMatrix[i], resultQueueMultiThread])
        t.start()
        threads.append(t)
    # Check grid
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            t = Thread(target=checkMatrix, args=(i, j, sudoku, resultQueueMultiThread))
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()
        
    if len(resultQueueMultiThread) == 27 and all(res == True for res in resultQueueMultiThread):
        print("The sudoku is Valid! - multi thread")
    else:
        print("Booom! The sudoku is not valid! - use thread")

def checkSudoku(sudoku):
    # Check rows
    for i in range(len(sudoku)):
        checkLine(sudoku[i], resultQueue)
    # Check columns
    transedMatrix = np.transpose(sudoku).tolist()
    for i in range(0, 9):
        checkLine(transedMatrix[i], resultQueue)
    # Check grid
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            checkMatrix(i, j, sudoku, resultQueue)

    if len(resultQueue) == 27 and all(res == True for res in resultQueue):
        print("The sudoku is Valid!")
    else:
        print("Booom! The sudoku is not valid!")

def main():         
    sudoku = [
            [6, 2, 4, 5, 3, 9, 1, 8, 7],
            [5, 1, 9, 7, 2, 8, 6, 3, 4],
            [8, 3, 7, 6, 1, 4, 2, 9, 5],
            [1, 4, 3, 8, 6, 5, 7, 2, 9],
            [9, 5, 8, 2, 4, 7, 3, 6, 1],
            [7, 6, 2, 3, 9, 1, 4, 5, 8],
            [3, 7, 1, 9, 5, 6, 8, 4, 2],
            [4, 9, 6, 1, 8, 2, 5, 7, 3],
            [2, 8, 5, 4, 7, 3, 9, 1, 6]
        ]

    # Multi Thread
    start_time = time.time()
    checkSudokuMultiThread(sudoku)
    print("--- Multi thread: %s milliseconds ---" % ((time.time() - start_time)*1000))

    # Single Thread
    start_time = time.time()
    t = Thread(target=checkSudoku, args=[sudoku])
    t.start()
    t.join()
    print("--- Single thread: %s milliseconds ---" % ((time.time() - start_time)*1000))

if __name__ == "__main__":
    main()
