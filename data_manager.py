import connection
import util

QUESTIONS_FILE_PATH = 'data/question.csv'
QUESTION_HEADER = ['id', 'username', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

ANSWERS_FILE_PATH = 'data/answer.csv'
ANSWERS_HEADER = ['id', 'username', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

USER_FILE_PATH = 'data/user.csv'
USER_HEADER = ['username', 'password']


def get_questions():
    return connection.open_file(QUESTIONS_FILE_PATH)


def export_questions(question_list):
    connection.write_file(question_list, QUESTIONS_FILE_PATH, QUESTION_HEADER)


def export_answers(answer_list):
    connection.write_file(answer_list, ANSWERS_FILE_PATH, ANSWERS_HEADER)


def get_answers():
    return connection.open_file(ANSWERS_FILE_PATH)


def answers_by_question_id(question_id):
    answers = get_answers()
    answers_list = []
    for answer in answers:
        if answer['question_id'] == question_id:
            answers_list.append(answer)
    return answers_list


def export_new_question(new_question):
    question_list = get_questions()
    question_list.append(new_question)
    export_questions(question_list)


def export_new_answers(new_answer):
    answer_list = get_answers()
    answer_list.append(new_answer)
    export_answers(answer_list)


def register_new_user(user, users):
    users.append(user)
    connection.write_file(users, USER_FILE_PATH, USER_HEADER)
    connection.write_file(users, USER_FILE_PATH, USER_HEADER)
    valid_password = True
    return valid_password

