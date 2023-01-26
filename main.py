import os.path
import sys
import enum

import GetLex
import Parse
import Semantic

# -*- coding: utf-8 -*-
 
TestType = enum.Enum(
    value='TestTypes',
    names = [
        ('lexer_tests', 1),
        ('parse_tests', 2),
        ('parser_tests', 3),
        ('semantic_tests', 4),
    ],
)

if __name__ == '__main__':
    testnum = 4
    #testnum = int(input('\nВведите: <1> для лексического анализатора, <2> для анализа простых выражений,\n<3> для синтаксического анализатора, <4> для семантического анализатора: '))
    correctd = 0

    directory = list(TestType)[testnum - 1].name
    test_type = list(TestType)[testnum - 1].value

    length = len([name for name in os.listdir(directory) if os.path.isfile(directory + "\\" + name)]) // 2 + 1

    for i in range(1, length):
        if i < 10:
            test_name = f'{directory}\\0{i}(_test).txt'
            answer_name = f'{directory}\\code_answ\\{i}.txt'
            check_name = f'{directory}\\0{i}(answer).txt'
        else:
            test_name = f'{directory}\\{i}(_test).txt'
            answer_name = f'{directory}\\code_answ\\{i}.txt'
            check_name = f'{directory}\\{i}(answer).txt'

        with open(answer_name, 'w', encoding="utf-8") as fw:
            if test_type == TestType['lexer_tests'].value:
                lexAnalizer = GetLex.LexAnalyzer(test_name)
                try:
                    lexem = lexAnalizer.getLex()
                    while lexem.lex:
                        fw.write(lexem.output() + '\n')
                        lexem = lexAnalizer.nextLex()
                except Exception as e:
                    fw.write(str(e))
            elif test_type == TestType['parse_tests'].value:
                parser = Parse.Parser(test_name)
                try:
                    result = parser.parseExpression()
                    result.Print(fw, 0)
                except Exception as e:
                    fw.write(str(e))
            elif test_type == TestType['parser_tests'].value:
                parser = Parse.Parser(test_name)
                result = parser.parseProgramm()
                result.Print(fw, 0)
            elif test_type == TestType['semantic_tests'].value:
                parser = Semantic.Parser(test_name)
                result = parser.parseProgramm()
                result.Print(fw, 0)

        with open(answer_name, "r", encoding="utf-8") as thisf, open(check_name, "r", encoding="utf-8") as correct:
            while True:
                answer = thisf.readline()
                checker = correct.readline()
                if answer.split() != checker.split():
                    print(test_name)
                    print(f'Тест №{i} выявил ошибку\n')
                    print("Ошибка в выражении " + str(checker))
                    print(checker + answer)
                    break
                if answer == "":
                    print(test_name)
                    print(f'Тест №{i} выполнен успешно\n\n')
                    correctd += 1
                    break

    print(f'\nВерных тестов {correctd}/{length - 1}\n\n')
