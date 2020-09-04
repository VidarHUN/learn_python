from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def print_task(rows, date=False):
    if len(rows) == 0:
        print("Nothing to do!")
    elif not date:
        for i in range(len(rows)):
            print("{}. {}".format(i + 1, rows[i].task))
    elif date:
        for i in range(len(rows)):
            print("{}. {}. {} {}".format(i + 1, rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b')))
    print("")

def todays_tasks():
    today = datetime.now()
    print("Today {} {}:".format(today.day, today.strftime('%b')))
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print_task(rows)


def weeks_tasks():
    today = datetime.now()
    for i in range(7):
        w_day = today + timedelta(days=i)
        print("{} {} {}:".format(w_day.strftime('%A'), w_day.day, w_day.strftime('%b')))
        print_task(session.query(Table).filter(Table.deadline == w_day.date()).all())


def print_all_tasks():
    # Get all rows (list)
    rows = session.query(Table).order_by(Table.deadline).all()
    print("Today:")
    print_task(rows, date=True)


def missed_tasks():
    print("Missed tasks: ")
    today = datetime.now()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        print_task(rows, date=True)


def add_task():
    task = input("Enter task\n").strip()
    deadline = input("Enter deadline\n").strip()
    # Add row
    new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    print("Choose the number of the task you want to delete: ")
    rows = session.query(Table).order_by(Table.deadline).all()
    print_task(rows, date=True)
    selection = int(input().strip())
    session.delete(rows[selection - 1])
    session.commit()
    print("The task has been deleted!")


def _exit():
    print("Bye!")


def menu():
    print(*[
        "1) Today's tasks",
        "2) Week's tasks",
        "3) All tasks",
        "4) Missed tasks",
        "5) Add task",
        "6) Delete task",
        "0) Exit"
    ], sep='\n')

    return {
        "1": todays_tasks,
        "2": weeks_tasks,
        "3": print_all_tasks,
        "4": missed_tasks,
        "5": add_task,
        "6": delete_task,
        "0": _exit
    }


while True:
    actions = menu()
    selection = input().strip()
    if selection == "0":
        todo = actions.get(selection)
        todo()
        break
    todo = actions.get(selection)
    todo()
