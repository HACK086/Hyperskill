from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()


class MyClass(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box_num = Column(Integer)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def new_card():
    while True:
        print('\nQuestion:')
        question = input().strip()
        if len(question) != 0:
            while True:
                print('Answer:')
                answer = input().strip()
                if len(answer) != 0:
                    new_data = MyClass(first_column=question, second_column=answer, box_num=1)
                    session.add(new_data)
                    session.commit()
                    break
            break


def add_card():
    while True:
        print('\n1. Add a new flashcard\n2. Exit')
        choice2 = input()
        if choice2 == '1':
            new_card()
        elif choice2 == '2':
            break
        else:
            print('\n' + choice2, 'is not an option')


def practice():
    result_list = session.query(MyClass).all()
    if len(result_list) == 0:
        print('\nThere is no flashcard to practice!\n')
    else:
        for i in range(0, len(result_list)):
            print('\nQuestion: ' + result_list[i].first_column + ':')
            while True:
                print('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:')
                choice3 = input()
                if choice3 == 'y':
                    print('Answer:', result_list[i].second_column)
                    while True:
                        print('press "y" if your answer is correct:\npress "n" if your answer is wrong:')
                        check = input()
                        if check == 'y':
                            result_list[i].box_num += 1
                            break
                        elif check == 'n':
                            result_list[i].box_num = 1
                            break
                        else:
                            print('\n' + check, 'is not an option\n')
                        session.commit()
                    if result_list[i].box_num == 4:
                        session.delete(result_list[i])
                        session.commit()
                    break
                elif choice3 == 'n':
                    break
                elif choice3 == 'u':
                    while True:
                        print('press "d" to delete the flashcard:\npress "e" to edit the flashcard:')
                        choice4 = input()
                        if choice4 == 'd':
                            session.delete(result_list[i])
                            session.commit()
                            break
                        elif choice4 == 'e':
                            print('current question: ' + result_list[i].first_column + '\nplease write a new question:')
                            edit1 = input().strip()
                            if edit1 != "":
                                result_list[i].first_column = edit1
                                session.commit()
                            print('current answer: ' + result_list[i].second_column + '\nplease write a new answer:')
                            edit2 = input().strip()
                            if edit2 != "":
                                result_list[i].second_column = edit2
                                session.commit()
                            break
                        else:
                            print('\n' + choice4, 'is not an option\n')
                    break
                else:
                    print('\n' + choice3, 'is not an option\n')


while True:
    print('\n1. Add flashcards\n2. Practice flashcards\n3. Exit')
    choice1 = input()
    if choice1 == '3':
        print('\nBye!')
        break
    elif choice1 == '1':
        add_card()
    elif choice1 == '2':
        practice()
    else:
        print('\n' + choice1, 'is not an option')