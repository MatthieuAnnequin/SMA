from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value
from communication.preferences.Preferences import Preferences
import random

def motor_generator(number_of_motors, criterion_list = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                    CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                    CriterionName.NOISE]):
    agent_pref = Preferences()
    agent_pref.set_criterion_name_list(criterion_list)

    list_motors = list()
    for i in range (number_of_motors):
        list_motors.append({"item" : Item("Motor" + str(i), "A super cool diesel engine"), "criterion": dict()})
        for criterion in criterion_list:     
            list_motors[i]["criterion"][CriterionName(criterion)] = random.randint(0,10)
    return list_motors

if __name__ == '__main__':
    """Testing the Preferences class.
    """
    print(motor_generator(2, criterion_list = [0, 1, 2, 3, 4]))