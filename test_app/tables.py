from .models import Profile
from table import Table
from table.columns import Column


class ProfileTable(Table):
    id = Column(field='id', header='ID')
    firstname = Column(field='first_name', header='First Name', searchable=True)
    lastname = Column(field='last_name', header='Last Name')
    gender = Column(field='gender', header='Gender')
    address = Column(field='address', header='Address')
    income = Column(field='income_annual', header='Annual Income')

    class Meta:
        model = Profile
