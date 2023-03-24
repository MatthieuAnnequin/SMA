import random

from communication.agent.CommunicatingAgent import CommunicatingAgent

from communication.preferences.Preferences import Preferences

from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value


class MotorAgent(CommunicatingAgent):
    """
    Agent who loves motors
    """

    def __init__(self, unique_id, model, name, criterion_list, item_list):
        """ Create a new motor agent.
        """
        super().__init__(unique_id, model, name)

        self.__preferences = Preferences()

        # Initialize citerion preferences
        self.__preferences.set_criterion_name_list(random.shuffle(criterion_list))

        # Initialize agent scales by criterion
        

        diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
        self.__preferences.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST,
                                                    Value.VERY_GOOD))
        self.__preferences.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION,
                                                    Value.GOOD))
        self.__preferences.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
                                                    Value.VERY_GOOD))
        self.__preferences.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                    Value.VERY_BAD))
        self.__preferences.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE,
                                                    Value.VERY_BAD))

        electric_engine = Item("Electric Engine", "A very quiet engine")
        self.__preferences.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST,
                                                    Value.BAD))
        self.__preferences.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION,
                                                    Value.VERY_BAD))
        self.__preferences.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY,
                                                    Value.GOOD))
        self.__preferences.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                    Value.VERY_GOOD))
        self.__preferences.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE,
                                                    Value.VERY_GOOD))

    def generate_agent_scale(max_value = 10, min_value = 0):
        step = (max_value-min_value)/4
        med = random.uniform((max_value+min_value)/2 - step, (max_value+min_value)/2 + step)
        low = random.uniform(min_value, med)
        high = random.uniform(med, max_value)
        return [low, med, high]

