import os.path
import sys
import enum

import GetLex
import Parse
import Semantic

# -*- coding: utf-8 -*-

if __name__ == '__main__':
    testnum = 2
    correctd = 0

    TestType = enum.Enum(
        value='TestTypes',
        names = [
            ('lexer_tests', 1),
            ('parse_tests', 2),
            ('parser_tests', 3),
            ('semantic_tests', 4),
        ],
    )

    for test_type in TestType:
        if (test_type.value == testnum):
            directory = test_type.name
            testtype = test_type.value

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

        if testtype == TestType['lexer_tests'].value:
            lexAnalizer = GetLex.LexAnalyzer(testname)
            try:
                lexem = lexAnalizer.getLex()
                while lexem.lex:
                    fw.write(lexem.output() + '\n')
                    lexem = lexAnalizer.nextLex()
            except Exception as e:
                fw.write(str(e))
        elif testtype == TestType['parse_tests'].value:
            parser = Parse.Parser(testname)
            try:
                result = parser.parseExpression()
                result.Print(fw, 0)
            except Exception as e:
                fw.write(str(e))
        elif testtype == TestType['parser_tests'].value:
            parser = Parse.Parser(testname)
            result = parser.parseProgramm()
            result.Print(fw, 0)
        elif testtype == TestType['semantic_tests'].value:
            parser = Semantic.Parser(testname)
            result = parser.parseProgramm()
            result.Print(fw, 0)

        fw.close()

        print(testname)

        # Вывод итога теста:
        with open(answname, "r", encoding="utf-8") as thisf, open(checkname, "r", encoding="utf-8") as correct:
            while True:
                answer = thisf.readline()
                checker = correct.readline()
                if answer.split() != checker.split():
                    print(f'Тест №{i} провален\n')
                    print("Ошибка в выражении " + str(checker))
                    print(checker + answer)
                    break
                if answer == "":
                    print(f'\nТест №{i} выполнен успешно\n\n')
                    correctd += 1
                    break

    print('\n')
    print(f'Верных тестов {correctd}/{length - 1}\n')
    print('\n')
