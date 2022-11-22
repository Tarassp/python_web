from faker import Faker
from random import randint
from datetime import date, datetime, timedelta
import sqlite3


class SqliteManager():
    def __init__(self, db_name, sql_file) -> None:
        self.db_name = db_name
        self.sql_file = sql_file

    def create_db(self):
        with open(self.sql_file, 'r') as f:
            sql = f.read()

        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.executescript(sql)
            cur.close()

    def fill_with_fake_data(self):
        sqls = ["INSERT INTO teachers(fullname) VALUES (?)",
                "INSERT INTO disciplines(name, teacher_id) VALUES(?, ?)",
                "INSERT INTO groups(name) VALUES (?)",
                "INSERT INTO students(fullname, group_id) VALUES(?, ?)",
                "INSERT INTO grades(student_id, discipline_id, date_of, grade) VALUES (?, ?, ?, ?)"]

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            for sql, data in zip(sqls, self._generate_data()):
                cur.executemany(sql, data)
            conn.commit()

    def get_five_students_with_highest_GPA_all_subjects(self):
        sql = """
            SELECT s.fullname, ROUND(AVG(gr.grade), 2) average
            FROM students s 
            LEFT JOIN grades gr ON gr.student_id = s.id
            GROUP BY s.fullname
            ORDER BY average DESC
            LIMIT(5);
        """
        return self._execute_query(sql)

    def get_one_student_with_highest_GPA_one_subject(self):
        sql = """
            SELECT s.fullname, d.name, ROUND(AVG(gr.grade), 2) average
            FROM students s 
            LEFT JOIN grades gr ON gr.student_id = s.id
            LEFT JOIN disciplines d ON gr.discipline_id = d.id
            WHERE d.id = 2
            GROUP BY s.fullname
            ORDER BY average DESC
            LIMIT(1);
        """
        return self._execute_query(sql)

    def get_average_score_in_group_one_subject(self):
        sql = """
            SELECT d.name, gr.name, ROUND(AVG(grades.grade), 2) average
            FROM students s 
            LEFT JOIN grades ON grades.student_id = s.id
            LEFT JOIN disciplines d ON grades.discipline_id = d.id
            LEFT JOIN [groups] gr ON gr.id = s.group_id 
            WHERE d.id = 7
            GROUP BY gr.name 
            ORDER BY average DESC;
        """
        return self._execute_query(sql)

    def get_average_score_in_stream(self):
        sql = """
            SELECT ROUND(AVG(g.grade), 2) average
            FROM grades g;
        """
        return self._execute_query(sql)

    def get_courses_taught_by_teacher(self):
        sql = """
            SELECT t.fullname, d.name
            FROM teachers t 
            LEFT JOIN disciplines d ON d.teacher_id = t.id 
            WHERE t.id = 4;
        """
        return self._execute_query(sql)

    def get_list_of_students_in_group(self):
        sql = """
            SELECT s.id, s.fullname, gr.name 
            FROM students s 
            LEFT JOIN [groups] gr ON gr.id = s.group_id
            WHERE gr.id = 1
        """
        return self._execute_query(sql)

    def get_grades_of_students_in_group_in_subject(self):
        sql = """
            SELECT s.id, s.fullname, gr.name, d.name, grades.grade
            FROM grades
            JOIN disciplines d ON d.id = grades.discipline_id
            JOIN students s ON s.id = grades.student_id
            JOIN [groups] gr ON gr.id = s.group_id 
            WHERE gr.id = 1 AND d.id = 3
        """
        return self._execute_query(sql)

    def get_grades_of_students_in_group_in_subject_at_last_lesson(self):
        sql = """
            SELECT s.id, s.fullname, gr.name, d.name, grades.grade, grades.date_of 
            FROM grades
            JOIN disciplines d ON d.id = grades.discipline_id
            JOIN students s ON s.id = grades.student_id
            JOIN [groups] gr ON gr.id = s.group_id 
            WHERE gr.id = 1 AND d.id = 3 AND grades.date_of = (
            SELECT grades.date_of 
            FROM grades
            JOIN students s ON s.id = grades.student_id 
            JOIN [groups] gr ON gr.id = s.group_id 
            WHERE gr.id = 1 AND grades.discipline_id  = 3
            ORDER BY grades.date_of DESC
            LIMIT 1
            );
        """
        return self._execute_query(sql)

    def get_list_courses_student_attending(self):
        sql = """
            SELECT d.name, s.fullname
            FROM grades g
            JOIN students s ON s.id = g.student_id 
            JOIN disciplines d ON d.id = g.discipline_id 
            WHERE g.student_id = 1
            GROUP BY d.name;
        """
        return self._execute_query(sql)

    def get_list_courses_teacher_reads_to_student(self):
        sql = """
            SELECT t.fullname, d.name, s.fullname
            FROM grades g 
            JOIN students s ON s.id = g.student_id 
            JOIN disciplines d ON d.id = g.discipline_id 
            JOIN teachers t ON t.id = d.teacher_id 
            WHERE t.id = 4 AND s.id = 1
            GROUP BY d.name
        """
        return self._execute_query(sql)

    def get_average_score_teacher_gives_to_student(self):
        sql = """
            SELECT DISTINCT s.fullname, t.fullname, ROUND(AVG(g.grade), 2) average
            from grades g 
            JOIN students s ON s.id = g.student_id 
            JOIN disciplines d ON d.id = g.discipline_id 
            JOIN teachers t ON t.id = d.teacher_id 
            WHERE t.id = 4 AND s.id = 1
            GROUP BY s.fullname;
        """

        return self._execute_query(sql)

    def get_average_score_given_by_teacher(self):
        sql = """
            SELECT t.fullname, ROUND(AVG(g.grade), 2) average
            FROM grades g 
            JOIN disciplines d ON d.id = g.discipline_id 
            JOIN teachers t ON t.id = d.teacher_id 
            WHERE t.id = 4
            GROUP BY t.fullname;
        """

        return self._execute_query(sql)

    def _execute_query(self, sql) -> list:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def _generate_data(self):
        fake = Faker('uk-UA')
        number_of_teachers = 5
        number_of_students = 50
        discipline_names = ['Теорія ймовірностей', 'Аналітична геометрія', 'Вища математика', 'Комп\'ютерна графіка', 'Алгоритмічне програмування'
                            'Економіка', 'Хімія', 'Системне програмування', 'Політологія', 'Фізика', 'Веб-програмування', 'Алгоритми і структури даних']
        group_names = ['пр-121', 'пр-122', 'пр-123']

        fake_teachers = zip([fake.name() for _ in range(number_of_teachers)])
        teacher_ids = [randint(1, number_of_teachers)
                       for _ in range(len(discipline_names))]

        fake_disciplines = zip(discipline_names, teacher_ids)

        fake_groups = zip(group_names)

        student_names = [fake.name() for _ in range(number_of_students)]
        group_ids = [randint(1, len(group_names))
                     for _ in range(number_of_students)]
        fake_students = zip(student_names, group_ids)

        fake_grades = []
        start_date = datetime.strptime('2021-09-01', '%Y-%m-%d')
        end_date = datetime.strptime('2022-05-25', '%Y-%m-%d')
        d_range = self._date_range(start_date, end_date)
        for d in d_range:
            disc = randint(1, len(discipline_names))
            studs = [randint(1, number_of_students) for _ in range(3)]
            for student in studs:
                fake_grades.append((student, disc, d.date(), randint(1, 12)))

        return fake_teachers, fake_disciplines, fake_groups, fake_students, fake_grades

    def _date_range(self, start: date, end: date):
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result
