# Helper file: Used to print the raw HTML that flask will produce using the form.
# For example, if in a form we use {{form.username}}, we can use this file to see what that html looks like

from forms import UserForm, LogoutForm

from app import app


def printhtml():
    with app.test_request_context():
        form = UserForm()
        # noinspection PyProtectedMember
        for field in form._fields:
            print(form.__getitem__(field))
            try:
                print(f'\nValue {form.__getitem__(field).value}\n')
            except  AttributeError:
                print("valueless")
                pass
            print(form.__getitem__(field).id)
            print(form.__getitem__(field).label)
            print(form.__getitem__(field).label.text)

            print("\n")


if __name__ == '__main__':
    printhtml()
