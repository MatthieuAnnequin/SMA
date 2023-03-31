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

    def __init__(self, unique_id, model, name, criterion_list, engine_list):
        """ Create a new motor agent.
        """
        super().__init__(unique_id, model, name)

        self.__preferences = Preferences()

        # Initialize citerion preferences
        self.__preferences.set_criterion_name_list(random.shuffle(criterion_list))

        # Initialize agent scales by criterion
        for engine in engine_list:
            engine_scale = self.generate_agent_scale(max_value = 10, min_value = 0)
            engine_item = engine['item']
            for criterion in criterion_list:
                agent_rank = self.get_agent_rank(engine_scale, engine['criterion'][criterion])
                self.__preferences.add_criterion_value(CriterionValue(engine_item, criterion, agent_rank))


    def generate_agent_scale(max_value = 10, min_value = 0):
        step = (max_value-min_value)/4
        med = random.uniform((max_value+min_value)/2 - step, (max_value+min_value)/2 + step)
        low = random.uniform(min_value, med)
        high = random.uniform(med, max_value)
        return [low, med, high]
    
    def get_agent_rank(self, engine_scale, engine_value):
        if engine_value < engine_scale[0]:
            return Value.VERY_BAD
        elif engine_value < engine_scale[1]:
            return Value.BAD
        elif engine_value < engine_scale[2]:
            return Value.GOOD
        else:
            return Value.VERY_GOOD

