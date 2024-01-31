id_text = 15

with open('test_answ.txt', 'r') as test_data:
    print(test_data.read().format(id = id_text))