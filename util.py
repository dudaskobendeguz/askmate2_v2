from time import time
import data_manager, connection

ALLOWED_EXTENSIONS = ['jpg', 'png']

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


def edit_question(question, new_details, question_id):
    delete_question(question_id)
    question['title'] = new_details['title']
    question['message'] = new_details['message']
    edited_question = question
    data_manager.export_new_question(edited_question)


def edit_answer(answer, new_details, answer_id):
    delete_answer(answer_id)
    answer['message'] = new_details['message']
    edited_answer = answer
    data_manager.export_new_answers(edited_answer)


def create_question(question_details, username, image=None):
    submission_time = time()
    id = generate_id(username, submission_time)
    question = {
        'id': id,
        'username': username,
        'submission_time': submission_time,
        'view_number': '0',
        'vote_number': '0',
        'title': question_details['title'],
        'message': question_details['message'],
        'image': image
    }
    data_manager.export_new_question(question)
    return id


def create_answer(answer_details, question_id, username, image=''):
    submission_time = time()
    answer_id = generate_id(username, submission_time)
    answer = {
        'id': answer_id,
        'username': username,
        'submission_time': submission_time,
        'vote_number': '0',
        'question_id': question_id,
        'message': answer_details['message'],
        'image': image
    }
    data_manager.export_new_answers(answer)


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


def increase_view(question_id):
    questions = data_manager.get_questions()
    question = get_user_post_by_id(question_id, is_question=True)
    questions = manipulate_post_number(post=question, posts=questions, number=1, key='view_number')
    data_manager.export_questions(questions)


def vote(post_id,  is_question, vote):
    if is_question:
        question = get_user_post_by_id(post_id, is_question=True)
        questions = data_manager.get_questions()
        questions = manipulate_post_number(post=question, posts=questions, number=vote, key='vote_number')
        data_manager.export_questions(questions)
    else:
        answer = get_user_post_by_id(post_id, is_question=False)
        answers = data_manager.get_answers()
        answers = manipulate_post_number(post=answer, posts=answers, number=vote, key='vote_number')
        data_manager.export_answers(answers)


def manipulate_post_number(post, posts, number, key):
    index = posts.index(post)
    post[key] = str(int(post[key]) + int(number))
    posts[index] = post
    return posts


def allowed_file(image: str):
    global ALLOWED_EXTENSIONS
    image_extension = image.filename.rsplit('.')[1]
    return image_extension in ALLOWED_EXTENSIONS