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

    dict_motors = dict()
    for i in range (number_of_motors):
        dict_motors["motor" + str(i)] = {"item" : Item("Motor i", "A super cool diesel engine"), "criterion": dict()}
        for criterion in criterion_list:    
            print(CriterionName(criterion))    
            dict_motors["motor" + str(i)]["criterion"][CriterionName(criterion)] = random.randint(0,10)
    return dict_motors

if __name__ == '__main__':
    """Testing the Preferences class.
    """
    print(motor_generator(2, criterion_list = [0, 1, 2, 3, 4]))