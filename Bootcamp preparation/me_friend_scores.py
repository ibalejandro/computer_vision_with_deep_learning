from collections import Counter


def get_num_questions(answers):
    num_questions = 0
    friend = Counter(answers)
    me = {0: 0, 1: 0}
    if (friend[1] - friend[0]) > 0:
        for i in range(len(answers)):
            me[answers[i]] += 1
            friend[answers[i]] -= 1
            if (me[1] - me[0]) > (friend[1] - friend[0]):
                num_questions = i + 1
                break
    return num_questions

scores = [1, 0, 0, 0, 0, 1]
print(get_num_questions(scores))
