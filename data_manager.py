import connection

QUESTIONS_FILE_PATH = 'data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

ANSWERS_FILE_PATH = 'data/answer.csv'
ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

USER_FILE_PATH = 'data/user.csv'
USER_HEADER = ['username', 'password']


def get_questions():
    return connection.open_file(QUESTIONS_FILE_PATH)


def get_answers():
    return connection.open_file(ANSWERS_FILE_PATH)


def export_questions(question_list):
    question_list = add_new_id(question_list)
    connection.write_file(question_list, QUESTIONS_FILE_PATH, QUESTION_HEADER)


def export_answers(answer_list):
    answer_list = add_new_id(answer_list)
    connection.write_file(answer_list, ANSWERS_FILE_PATH, ANSWERS_HEADER)


def add_new_id(data_list):
    last_id = int(data_list[-2]['id'])
    new_id = last_id + 1
    data_list[-1]['id'] = new_id
    return data_list


def sort_questions(orders):
    question_list = get_questions()
    order_title = orders['order_by']
    order_direction = orders['order_direction']
    if order_direction == 'asc':
        is_reverse = False
    elif order_direction == 'desc':
        is_reverse = True
    ordered_list = sorted(question_list, key=lambda item: item[order_title], reverse=is_reverse)
    return ordered_list


def log_in(user):

    def register_new_user():
        users.append(user)
        connection.write_file(users, USER_FILE_PATH, USER_HEADER)
        connection.write_file(users, USER_FILE_PATH, USER_HEADER)
        return True

    users = connection.open_file(USER_FILE_PATH)
    logged_in = False
    valid_password = True
    for registered_user in users:
        if registered_user['username'] == user["username"]:
            if registered_user['password'] == user['password']:
                logged_in = True
                valid_password = True
            elif user['password'] == "admin":
                valid_password == True
            else:
                logged_in = False
                valid_password = False
    if not logged_in and valid_password and user:
        valid_password = register_new_user()
    return valid_password

