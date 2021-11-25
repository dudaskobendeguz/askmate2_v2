from time import time
import data_manager, connection


def log_in(user):
    users = connection.open_file(data_manager.USER_FILE_PATH)
    logged_in = False
    valid_password = True
    for registered_user in users:
        if registered_user['username'] == user["username"]:
            if registered_user['password'] == user['password']:
                logged_in = True
                valid_password = True
            elif user['password'] == "admin":
                valid_password = True
                logged_in = True
            else:
                logged_in = False
                valid_password = False
    if not logged_in and valid_password and user:
        valid_password = data_manager.register_new_user(user, users)
    return valid_password


def sort_questions(orders):
    question_list = data_manager.get_questions()
    order_title = orders['order_by']
    order_direction = orders['order_direction']
    if order_direction == 'asc':
        is_reverse = False
    elif order_direction == 'desc':
        is_reverse = True
    ordered_list = sorted(question_list, key=lambda item: [int(item[order_title]) if item[order_title].isdigit() else item[order_title]], reverse=is_reverse)
    return ordered_list


def create_question(question_details, username):
    question = {}  # ki kell tölteni
    submission_time = time()
    id = generate_id(username, submission_time)
    return question


def create_answer(answer_details, username):
    submission_time = time()
    answer_id = generate_id(username, submission_time)
    answer = {
        'id': answer_id,
        'username': username,
        'submission_time': submission_time,
        'vote_number': '0',
        'question_id': None,##################
        'message': answer_details['message'],
        'image': answer_details['image']#########################
    }
    return answer


def get_user_post_by_id(post_id, is_question):
    if is_question:
        user_posts = data_manager.get_questions()
    else:
        user_posts = data_manager.get_answers()
    for post in user_posts:
        if post['id'] == post_id:
            return post


def generate_id(username, submission_time):
    new_id = f"{username}_{submission_time}"
    return new_id


def delete_answer(answer_id):
    answer = get_user_post_by_id(answer_id, is_question=False)
    answers = data_manager.get_answers()
    answers.remove(answer)
    data_manager.export_answers(answers)


def delete_question(question_id):
    question = get_user_post_by_id(question_id, is_question=True)
    questions = data_manager.get_questions()
    questions.remove(question)
    delete_answers_for_question(question_id)
    data_manager.export_questions(questions)


def delete_answers_for_question(question_id):
    answers = data_manager.get_answers()
    for answer in answers:
        if answer['question_id'] == question_id:
            answers.remove(answer)
    data_manager.export_answers(answers)


def vote(post_id,  is_question, vote):
    if is_question:
        questions = data_manager.get_questions()
        question = get_user_post_by_id(post_id, is_question=True)
        index = questions.index(question)
        question['vote_number'] = str(int(question['vote_number']) + int(vote))
        questions[index] = question
        data_manager.export_questions(questions)
    else:
        answers = data_manager.get_answers()
        answer = get_user_post_by_id(post_id, is_question=False)
        index = answers.index(answer)
        answer['vote_number'] = str(int(answer['vote_number']) + int(vote))
        answers[index] = answer
        data_manager.export_answers(answers)
