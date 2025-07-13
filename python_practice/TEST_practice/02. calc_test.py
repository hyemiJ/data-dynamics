from enum import Enum
import re

class Operator(Enum):
    """
    [Enum]해당 기호에 알맞는 계산을 수행합니다.

    :Member:
        PLUS = '+'
        MINUS = '-'
        MUL = '*'
        DIV = '/'
    """
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'

    def calc(self, value1, value2):
        """
        해당하는 연산자일 경우 앞의 값과 뒤의 값을 계산합니다.
        값은 float를 전제로 합니다.
        :param value1:              (float)앞의 값
        :param value2:              (float)뒤의 값
        :raises ZeroDivisionError : 0을 나눌 수 없습니다.
        :return:                    (float)계산의 결과 값
        """
        if self == Operator.PLUS:
            return value1 + value2
        elif self == Operator.MINUS:
            return value1 - value2
        elif self == Operator.MUL:
            return value1 * value2
        elif self == Operator.DIV:
            if value2 == 0:
                raise ZeroDivisionError("0을 나눌순 없다")
            return value1 / value2

def parse_list(data_lst, type1, type2):
    """
    일치하는 연산자들의 앞,뒤의 값을 계산합니다.
    :param data_lst: (list)입력값을 연산자와 숫자를 리스트로 숫자와 연산자를 통해 계산을 수행합니다. [3, '-', 2,'+', 1.5]
    :param type1:    (Operator)곱셈, 나눗셈을 선 수행하기 위해 2개의 Enum을 받아 계산을 수행합니다.
    :param type2:    (Operator)곱셈, 나눗셈을 선 수행하기 위해 2개의 Enum을 받아 계산을 수행합니다.
    :return:
        list: 2개의 Enum 연산을 수행한 결과를 리스트의 형태로 반환합니다.
    """

    i = 1
    while i < len(data_lst):
        if isinstance(data_lst[i], str) and data_lst[i] in (type1.value, type2.value):
            op = Operator(data_lst[i])
            data_lst[i - 1] = op.calc(data_lst[i - 1], data_lst[i + 1])
            del data_lst[i:i + 2]
        else:
            i += 1
    return data_lst

def calculate(lst):
    """
    입력값을 그대로 받아 전체 계산을 수행합니다.
    :param lst:                 (list) input()의 입력 값
    :raises ZeroDivisionError : 0을 나눌 수 없습니다.
    :return:                    float : 계산이 완료된 값
    """
    data = []
    for str_data in lst:
        try:
            data.append(float(str_data))
        except ValueError:
            data.append(str_data)
    
    try:
        data = parse_list(data, Operator.MUL, Operator.DIV)  # 곱셈,나눗셈 먼저 실행
    except ZeroDivisionError:
        print("0을 나눌 수 없다.")
        return None

    data = parse_list(data, Operator.PLUS, Operator.MINUS)  # 덧셈,뺼셈 실행
    #print(data)
 
    return data[0]

# 실행부
user_input = input('사칙연산 계산기 숫자와 기호를 입력해주세요')
calc_data_list = re.findall(r'\d+(?:\.\d+)?|[+\-*/]', user_input)  # 공백 무시와 함께 소수점 및 연산자만 추출
print(calculate(calc_data_list))
