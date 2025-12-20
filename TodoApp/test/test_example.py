from tkinter import YES
import pytest
def test_equal_or_not_equal():
    assert 4 == 4
    assert 4 != 3


def tesdt_is_instance():
    assert isinstance(4, int)
    assert isinstance(4, float)
    assert isinstance('this is a string', str)


def test_boolean():
    assert True == True
    assert False == False
    validated = True
    assert ('hello' == 'world') is False

class student:
    def __init__(self, first_name:str, last_name:str, major: str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return student("John", "Doe", "Computer Science", 3)


def test_person_inizialization(default_employee):
    assert default_employee.first_name == "John",'First name should be John'
    assert default_employee.last_name == "Doe",'Last name should be Doe'
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3
        





