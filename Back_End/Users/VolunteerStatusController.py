from Back_End.Users.VolunteerStatus import VolunteerStatus
from Back_End.Camps.CampsController import CampsController
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController


class VolunteerStatusController:
    def __init__(self, connection):
        self.connection = connection
        self.camps_controller = CampsController(connection)
        self.refugee_controller = RefugeeProfileController(connection)

    # returns list of volunteerStatus objects ordered where the first camp needs the most intervention
    def initialise(self):
        camp_ids = self.camps_controller.get_list_of_camp_ids()

        list_of_volunteer_status_obj = []

        for i in range(len(camp_ids)):
            rating_for_each_day = [None] * 7

            camp_id = camp_ids[i]
            camp_name = self.camps_controller.get_camp_name(camp_id)
            urgency_rating = 0

            volunteers_availabilities = self.get_all_volunteer_avalibility(
                camp_id)  # returns [0, 1, 3, 2, ...]
            num_refugees_by_camp = self.refugee_controller.number_of_refugees_by_camp(
                camp_id)

            for j in range(7):
                rating_for_day = self.get_rating(
                    camp_id, volunteers_availabilities[j], num_refugees_by_camp)
                # should return a tuple e.g. ('X', 2)
                rating_for_each_day[j] = rating_for_day

            for k in range(7):
                if rating_for_each_day[k][0] == "X":
                    urgency_rating += 1

            monday = rating_for_each_day[0][0]
            tuesday = rating_for_each_day[1][0]
            wednesday = rating_for_each_day[2][0]
            thursday = rating_for_each_day[3][0]
            friday = rating_for_each_day[4][0]
            saturday = rating_for_each_day[5][0]
            sunday = rating_for_each_day[6][0]

            volunteer_status_obj = VolunteerStatus(camp_id, camp_name, urgency_rating,
                                                   monday, tuesday, wednesday, thursday, friday, saturday, sunday)
            list_of_volunteer_status_obj.append(volunteer_status_obj)

        return list_of_volunteer_status_obj

    def get_all_volunteer_avalibility(self, camp_id):
        volunteers_availabilities = [0] * 7

        c = self.connection.cursor()
        query = "SELECT availability FROM users WHERE camp_id = ? AND is_admin = 0"
        c.execute(query, [camp_id])
        result = c.fetchall()
        for i in range(7):
            for j in range(len(result)):
                if result[j][0][i] == "T":
                    volunteers_availabilities[i] += 1

        return volunteers_availabilities

    def get_rating(self, camp_id, number_volunteers, number_refugees):
        severity_rating = 0

        volunteers_needed = (0.1 * number_refugees) - number_volunteers

        volunteers_needed //= 1

        if abs(int(volunteers_needed)) >= 2:
            return (f"{abs(int(volunteers_needed))}", severity_rating)
        else:
            return (f"{abs(int(volunteers_needed))}", severity_rating)
