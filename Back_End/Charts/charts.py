import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')
plt.rcParams["figure.figsize"] = (11, 7)


class ChartsController:

    def __init__(self, connection):
        self.__connection = connection

    # View the capacity, number of medicines, food, number of refugees and number of volunteers at each camp (bar chart)
    def camps_status(self):
        c = self.__connection.cursor()
        c.execute(f'SELECT camp_id, capacity, num_medicine, num_food FROM camps GROUP BY camp_id')
        data = c.fetchall()

        camp_id, capacity, num_medicine, num_food = [], [], [], []

        width = 0.15

        for row in data:
            camp_id.append(row[0])
            capacity.append(row[1])
            num_medicine.append(row[2])
            num_food.append(row[3])

        c.execute(f'SELECT SUM(familySize), campID FROM refugeeProfile GROUP BY campID')
        data = c.fetchall()

        family_size = []
        camps_with_refugees = []

        for row in data:
            family_size.append(row[0])
            camps_with_refugees.append(row[1])

        c.execute(f'SELECT COUNT(username), camp_id FROM users WHERE is_active = 1 AND is_admin = 0 GROUP BY camp_id')
        data = c.fetchall()

        active_volunteers = []
        camps_with_volunteers = []

        for row in data:
            active_volunteers.append(row[0])
            camps_with_volunteers.append(row[1])

        for i in camp_id:
            if i not in camps_with_refugees:
                camps_with_refugees.append(i)
                family_size.append(0)
            if i not in camps_with_volunteers:
                camps_with_volunteers.append(i)
                active_volunteers.append(0)

        labels = [x + 1 for x in range(max(camp_id))]

        for i, v in enumerate(labels):
            if v not in camp_id:
                camp_id.insert(i, v)
                camps_with_refugees.insert(i, v)
                camps_with_volunteers.insert(i, v)
                capacity.insert(i, 0)
                num_medicine.insert(i, 0)
                num_food.insert(i, 0)
                family_size.insert(i, 0)
                active_volunteers.insert(i, 0)

        capacity = plt.bar(np.arange(1, len(camp_id) + 1, 1) - 2 * width, capacity, width=width, label='Max capacity')
        meds = plt.bar(np.arange(1, len(camp_id) + 1, 1) - width, num_medicine, width=width, label='Medicines')
        food = plt.bar(np.arange(1, len(camp_id) + 1, 1), num_food, width=width, label='Food')
        num_refugees = plt.bar(np.arange(1, len(camp_id) + 1, 1) + width, family_size, width=width,
                               label='Current number of refugees')
        num_volunteers = plt.bar(np.arange(1, len(camp_id) + 1, 1) + 2 * width, active_volunteers, width=width,
                                 label='Number of active volunteers')

        plt.title('Camps overall status')
        plt.xlabel('Camp ID')
        plt.ylabel('Number')
        plt.bar_label(capacity, padding=3)
        plt.bar_label(meds, padding=3)
        plt.bar_label(food, padding=3)
        plt.bar_label(num_refugees, padding=3)
        plt.bar_label(num_volunteers, padding=3)
        plt.legend(handles=[capacity, meds, food, num_refugees, num_volunteers])
        newlst = range(min(camp_id), max(camp_id) + 1)
        plt.xticks(newlst)
        plt.get_current_fig_manager().set_window_title('Admin > Camp Analytics > Camps Status chart')
        return plt.show()

    # View the medical needs for all camps (stacked bar chart)
    def updated_camp_medical_needs(self):
        c = self.__connection.cursor()
        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "Medical" '
            f'GROUP BY campID')
        data = c.fetchall()

        medical, surgical, psychiatric, camp_id, no_illness, multiple = [], [], [], [], [], []

        for row in data:
            medical.append(row[0])
            camp_id.append(row[1])
            surgical.append(0)
            psychiatric.append(0)
            no_illness.append(0)
            multiple.append(0)

        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "Surgical" '
            f'GROUP BY campID')
        data = c.fetchall()

        for row in data:
            surgical.append(row[0])
            camp_id.append(row[1])
            medical.append(0)
            psychiatric.append(0)
            no_illness.append(0)
            multiple.append(0)

        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "Psychiatric" '
            f'GROUP BY campID')
        data = c.fetchall()

        for row in data:
            psychiatric.append(row[0])
            camp_id.append(row[1])
            medical.append(0)
            surgical.append(0)
            no_illness.append(0)
            multiple.append(0)

        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "Multiple" '
            f'GROUP BY campID')
        data = c.fetchall()

        for row in data:
            multiple.append(row[0])
            camp_id.append(row[1])
            medical.append(0)
            surgical.append(0)
            no_illness.append(0)
            psychiatric.append(0)

        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "Multiple" '
            f'GROUP BY campID')
        data = c.fetchall()

        for row in data:
            multiple.append(row[0])
            camp_id.append(row[1])
            medical.append(0)
            surgical.append(0)
            no_illness.append(0)
            psychiatric.append(0)

        c.execute(
            f'SELECT COUNT(medicalConditions)*10, campID FROM refugeeProfile WHERE medicalConditions = "None" '
            f'GROUP BY campID')
        data = c.fetchall()

        for row in data:
            no_illness.append(row[0])
            camp_id.append(row[1])
            medical.append(0)
            surgical.append(0)
            multiple.append(0)
            psychiatric.append(0)

        c.execute('SELECT DISTINCT(camp_id) from camps')
        data = c.fetchall()

        check_for_empty_camps = []

        for row in data:
            check_for_empty_camps.append(row[0])
        if len(check_for_empty_camps) > max(camp_id):
            x_marker = len(check_for_empty_camps)
        else:
            x_marker = max(camp_id)

        width = 0.5
        medical_con = plt.bar(camp_id, medical, width=width, label='Medical', bottom=no_illness)
        surgical_con = plt.bar(camp_id, surgical, width=width, label='Surgical', bottom=no_illness)
        psychiatric_con = plt.bar(camp_id, psychiatric, width=width, label='Psychiatric', bottom=no_illness)
        multiple_con = plt.bar(camp_id, multiple, width=width, label='Multiple specialties', bottom=no_illness)
        no_illness = plt.bar(camp_id, no_illness, width=width, label='None')
        plt.title('Medical needs across all camps')
        plt.xlabel('Camp ID')
        plt.ylabel('Number')
        newlst = range(min(camp_id), x_marker + 1)
        plt.xticks(newlst)
        plt.legend(handles=[medical_con, surgical_con, psychiatric_con, multiple_con, no_illness])
        plt.get_current_fig_manager().set_window_title('Admin > Camp Analytics > Camps Medical Status chart')
        return plt.show()

    # View medical needs for the volunteer's camp only (pie chart)
    def volunteer_camp_medical_needs(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f'SELECT COUNT(medicalConditions)*2.5 FROM refugeeProfile WHERE campID = {camp_id} AND '
                  f'medicalConditions = "No Illness"')
        data = c.fetchall()
        values = []
        for row in data:
            values.append(row[0])
        c.execute(f'SELECT COUNT(medicalConditions)*2.5 FROM refugeeProfile WHERE campID = {camp_id} AND '
                  f'medicalConditions = "Medical"')
        data = c.fetchall()
        for row in data:
            values.append(row[0])
        c.execute(f'SELECT COUNT(medicalConditions)*2.5 FROM refugeeProfile WHERE campID = {camp_id} AND '
                  f'medicalConditions = "Surgical"')
        data = c.fetchall()
        for row in data:
            values.append(row[0])
        c.execute(f'SELECT COUNT(medicalConditions)*2.5 FROM refugeeProfile WHERE campID = {camp_id} AND '
                  f'medicalConditions = "Psychiatric"')
        data = c.fetchall()
        for row in data:
            values.append(row[0])
        c.execute(f'SELECT COUNT(medicalConditions)*2.5 FROM refugeeProfile WHERE campID = {camp_id} AND '
                  f'medicalConditions = "Multiple"')
        data = c.fetchall()
        for row in data:
            values.append(row[0])
        labels = ['None', 'Medical condition', 'Surgical condition', 'Psychiatric condition', 'Multiple specialties']

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.1f}%  ({v:d})'.format(p=pct, v=val)

            return my_autopct

        explode = (0.03, 0.03, 0.03, 0.03, 0.03)
        plt.pie(values, labels=labels, explode=explode, autopct=make_autopct(values))
        plt.axis('equal')
        plt.get_current_fig_manager().set_window_title('Volunteer > Camp Insights > Camp Medical status')
        return plt.show()

    # View the capacity status of the volunteer's camp (pie chart)
    def volunteer_camp_capacity_status(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f'SELECT SUM(familySize) FROM refugeeProfile WHERE campID = {camp_id}')
        data = c.fetchall()
        values = []

        for row in data:
            values.append(row[0])

        c.execute(f'SELECT capacity FROM camps WHERE camp_id = {camp_id}')
        data = c.fetchall()

        for row in data:
            values.append(row[0] - values[0])

        explode = (0.08, 0)
        labels = ['Current number of refugees', 'Remaining capacity']

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.1f}%  ({v:d})'.format(p=pct, v=val)

            return my_autopct

        plt.pie(values, explode=explode, labels=labels, shadow=True, autopct=make_autopct(values))
        plt.axis('equal')
        plt.get_current_fig_manager().set_window_title('Volunteer > Camp Insights > Camp capacity')
        return plt.show()

    # View the number of active and inactive volunteers at the volunteer's camp (pie chart)
    def active_inactive_volunteer_camp_status(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f'SELECT COUNT(username) FROM users WHERE camp_id = {camp_id} AND is_active = 1 AND is_admin = 0')
        data = c.fetchall()
        values = []

        for row in data:
            values.append(row[0])

        c.execute(f'SELECT COUNT(username) FROM users WHERE camp_id = {camp_id} AND is_active = 0 AND is_admin = 0')
        data = c.fetchall()

        for row in data:
            values.append(row[0])

        explode = (0.08, 0)
        labels = ['Active volunteers', 'Inactive volunteers']

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.1f}%  ({v:d})'.format(p=pct, v=val)

            return my_autopct

        plt.pie(values, explode=explode, labels=labels, shadow=True, autopct=make_autopct(values))
        plt.axis('equal')
        plt.get_current_fig_manager().set_window_title('Volunteer > Camp Insights > Camp volunteers')
        return plt.show()
