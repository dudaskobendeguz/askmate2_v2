import csv


def open_file(file_path):
    with open(file_path, "r") as file:
        data_list = []
        reader = csv.DictReader(file)
        for dictionary in reader:
            data_list.append(dictionary)
    return data_list


def write_file(data_list, file_path, header):
    with open(file_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)


if __name__ == "__main__":
    answers = 'data/answer.csv'
    questions = 'data/question.csv'
    questions = open_file(questions)
    answers = open_file(answers)


