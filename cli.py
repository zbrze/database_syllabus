from cli_app import App, Command
from pandas import DataFrame
from src.db_helpers import DBHelpers
class GetStudentInfo(Command):

    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname of student", default=None, required=False)
        parser.add_argument("--lastname", "-l", type=str, help="lastname of student", default=None, required=False)
        parser.add_argument("--pesel", "-p", type=str, help="pesel of student", default=None, required=False)
        parser.add_argument("--album", "-a", type=str, help="album number of student", default=None, required=False)

    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        pesel = self.app.args.pesel
        album = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.get_student_info, fname, lname, pesel, album)
            print(DataFrame(result))


class TutorsCourses(Command):

    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--fname", "-f", type=str, help="firstname of tutor", required=True)
        parser.add_argument("--lname", "-l", type=str, help="lastname of tutor", required=True)

    def run(self):
        fname = self.app.args.fname
        lname = self.app.args.lname
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.tutors_courses, fname, lname)
            print()
            print(fname + " " + lname + "\'s" + " courses:")
            print()
            print(DataFrame(result))        


class Syllabus(App):
    """Syllabus app."""
    def __init__(self):
        super().__init__()
        self.db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))

    def register_commands(self):
        self.add_command("student_info", GetStudentInfo)
        self.add_command("tutors_courses", TutorsCourses)

# komendy sie wola tak standardowo np. python cli.py tutors_courses -f Leszek -l Siwik
# https://github.com/jsphpl/python-cli-app
# DataFrame() robi tabelke z danych jesli dostanie liste slownikow wiec mozna tak wyswietlac dane
# Kazda komenda to jedna klasa no i trzeba podopisywac te klasy zeby korzystaly z tych funkcji z DBHelpers co juz mamy

if __name__ == "__main__":
    app = Syllabus()
    app.run()

