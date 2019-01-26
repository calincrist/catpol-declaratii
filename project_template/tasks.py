import random
import datetime
from unittest.mock import MagicMock

from moonsheep.tasks import AbstractTask
from moonsheep import verifiers
from moonsheep.decorators import register

import project_template.models as models
import project_template.views
import project_template.forms as forms


@register()
class TaskGetInitialInformation(AbstractTask):
    task_form = forms.TranscribeInitialInformation
    template_name = 'tasks/general_information_task.html'

    def create_mocked_task(self, task_data):
        task_data['info'].update({
            'url': 'http://www.cdep.ro/declaratii/deputati/2016/avere/002a.pdf',
            'page': 10
        })

        return task_data

    def get_presenter(self):
        return super(TaskGetInitialInformation, self).get_presenter()

    def save_verified_data(self, verified_data):
        politician, created = models.Politician.objects.get_or_create(
            name=verified_data['name'],
            surname=verified_data['surname'],
            position=verified_data['position']
        )

        politician.add_position(verified_data['position'])

        income_declaration, created = models.IncomeDeclaration.objects.get_or_create(
            url=self.url,
            politician=politician,
            date=datetime.datetime.strptime(verified_data['date'], "%Y-%m-%d")
        )

    def after_save(self, verified_data):
        # Create a new task for each table, asking the user to transcribe the number of rows
        pass


@register()
class TaskGetDebtsTableRowsCount(AbstractTask):
    task_form = forms.TranscribeDebtsTableRowsCount
    template_name = 'tasks/debts_table_rows_count_task.html'

    def create_mocked_task(self, task_data):
        task_data['info'].update({
            'url': 'http://www.cdep.ro/declaratii/deputati/2016/avere/002a.pdf',
            'page': 10
        })

        return task_data

    def get_presenter(self):
        return super(TaskGetDebtsTableRowsCount, self).get_presenter()

    def save_verified_data(self, verified_data):
        try:
            rows_count = verified_data['rows_count']
            models.OwnedDebtsTable.objects.get_or_create(count=rows_count)
        except Exception as error:
            print("Exception: ", error)


    def after_save(self, verified_data):
        # Create a new task for each table, asking the user to transcribe the number of rows
        pass

@register()
class TaskGetExtraValuableRowsCount(AbstractTask):
    task_form = forms.TranscribeOwnedExtraValuableRowsCount
    template_name = 'tasks/extra_valuable_goods_table_count.html'

    def create_mocked_task(self, task_data):
        task_data['info'].update({
            'url': 'http://www.cdep.ro/declaratii/deputati/2016/avere/002a.pdf',
            'page': 10
        })

        return task_data

    def get_presenter(self):
        return super(TaskGetExtraValuableRowsCount, self).get_presenter()

    def save_verified_data(self, verified_data):
        try:
            rows_count = verified_data['rows_count']
            models.OwnedExtraValuableTable.objects.get_or_create(count=rows_count)
        except Exception as error:
            print("Exception: ", error)

    def after_save(self, verified_data):
        # Create a new task for each table, asking the user to transcribe the number of rows
        pass