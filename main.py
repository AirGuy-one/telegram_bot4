with open("questions_data/1vs1200.txt", "r", encoding='KOI8-R') as my_file:
    file_contents = my_file.read()

amount = ''
all_phrases = []
questions = []
answers = []
q, a = 0, 0

for i in file_contents:
    if i != '\n':
        amount += i
    else:
        all_phrases.append(amount)
        amount = ''

# Split into questions and answers
tmp_answer = ''
tmp_question = ''
for phrase in all_phrases:
    if q == 1:
        tmp_question += phrase
        q -= 1
        if phrase == '':
            questions.append(tmp_question)
            tmp_question = ''
        else:
            q += 1
    if a == 1:
        tmp_answer += phrase
        a -= 1
        if phrase == '':
            answers.append(tmp_answer)
            tmp_answer = ''
        else:
            a += 1
    if phrase[:6] == 'Вопрос':
        q += 1
    if phrase == 'Ответ:':
        a += 1

for number, i in enumerate(questions):
    print(number + 1, i)
