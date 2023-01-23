import os.path
import sys

import GetLex
import Parse
import Semantic

# -*- coding: utf-8 -*-

if __name__ == '__main__':
    testtype = '3'
    correctd = 0

    try:
        testtype = sys.argv[1]
        starttest = int(sys.argv[2])
    except:
        pass

    if testtype == '1':
        directory = 'lexer_tests'
    elif testtype == '2':
        directory = 'parse_tests'
    elif testtype == '3':
        directory = 'parser_tests'
    elif testtype == '4':
        directory = 'semantic_tests'
    else:
        raise Exception(
            "Введите 1 для лексического анализатора, 2 для простых выражений, 3 для синтаксического анализатора, 4 для семантического анализатора")

    length = len([name for name in os.listdir(directory) if os.path.isfile(directory + "\\" + name)]) // 2 + 1

    for i in range(1, length):
        if i < 10:
            testname = directory + "\\" + "0" + str(i) + "(_test).txt"
            answname = directory + "\\code_answ\\" + str(i) + ".txt"
            checkname = directory + "\\" + "0" + str(i) + "(answer).txt"
        else:
            testname = directory + "\\" + str(i) + "(_test).txt"
            answname = directory + "\\code_answ\\" + str(i) + ".txt"
            checkname = directory + "\\" + str(i) + "(answer).txt"
        
        fw = open(answname, 'w', encoding="utf-8")

        if testtype == '1':
            lexAnalizer = GetLex.LexAnalyzer(testname)
            try:
                lexem = lexAnalizer.getLex()
                while lexem.lex:
                    fw.write(lexem.output() + '\n')
                    lexem = lexAnalizer.nextLex()
            except Exception as e:
                fw.write(str(e))
        elif testtype == '2':
            parserper = Parse.Parser(testname)
            try:
                result = parserper.parseExpression()
                result.Print(fw, 0)
            except Exception as e:
                fw.write(str(e))
        elif testtype == '3':
            parserper = Parse.Parser(testname)
            result = parserper.parseProgramm()
            result.Print(fw, 0)
        elif testtype == '4':
            parserper = Semantic.Parser(testname)
            result = parserper.parseProgramm()
            result.Print(fw, 0)

        fw.close()
        print(testname)

        # Вывод итога теста:
        with open(answname, "r", encoding="utf-8") as thisf, open(checkname, "r", encoding="utf-8") as correct:
            while True:
                answer = thisf.readline()
                checker = correct.readline()
                if answer.split() != checker.split():
                    print(False)
                    print('\n')
                    print("Ошибка в выражении " + str(checker))
                    print(checker + answer)
                    break
                if answer == "":
                    print(True)
                    print('')
                    correctd += 1
                    break

    print('\n')
    print(f'Верных тестов {correctd}/{length - 1}\n')
    print('\n')
