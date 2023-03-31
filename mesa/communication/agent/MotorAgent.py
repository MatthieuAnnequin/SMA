import random

from communication.agent.CommunicatingAgent import CommunicatingAgent

from communication.preferences.Preferences import Preferences

from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.motor.MotorGenerator import motor_generator
from communication.agent.Model import SpeakingModel 



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
        random.shuffle(criterion_list)
        self.__preferences.set_criterion_name_list(criterion_list)

        # Initialize agent scales by criterion
        for engine in engine_list:
            engine_scale = self.generate_agent_scale(max_value = 10, min_value = 0)
            engine_item = engine['item']
            for criterion in criterion_list:
                agent_rank = self.get_agent_rank(engine_scale, engine['criterion'][criterion])
                self.__preferences.add_criterion_value(CriterionValue(engine_item, criterion, agent_rank))



    def step(self):
        """ The step methods of the agent called by the scheduler at each time tick.
        """
        super().step()  
        print('test')
        if len(self.get_new_messages()) == 0 and self.get_name() != "agent2":
            self.send_message(Message(self.get_name(),"agent2",MessagePerformative.PROPOSE, "Bonjour"))
            print('sent')
        for message in self.get_new_messages():
            print(str(message))
            if message.get_performative() == MessagePerformative.PROPOSE:
                self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.PROPOSE, "Bonjour"))
            else:
                self.send_message(Message(self.get_name(),"agent2",MessagePerformative.PROPOSE, "Bonjour"))
            # if message.get_performative() == MessagePerformative.QUERY_REF:
            #     self.send_message(Message(message.get_dest(), message.get_exp(), MessagePerformative.INFORM_REF, self.__v))
            # elif message.get_performative() == MessagePerformative.PROPOSE:
            #     self.__v = message.get_content()
            #     print(str(self.get_name()) + ' change v à ' + str(self.__v))
            # elif message.get_performative() == MessagePerformative.INFORM_REF:
            #     if self.__v != message.get_content():
            #         self.send_message(Message(message.get_dest(), message.get_exp(), MessagePerformative.PROPOSE, self.__v))
            #         print(str(self.get_name()) + ' propose à ' + str(message.get_exp()) + ' la valeur ' + str(self.__v))                
            
 


    def generate_agent_scale(self, max_value = 10, min_value = 0):
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
        
    def get_preferences(self):
        return self.__preferences
        



if __name__ == "__main__":
    # Init the model and the agents
     #To complete
    motormodel = SpeakingModel()
    criterion_list = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                    CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                    CriterionName.NOISE]
    engine_list = motor_generator(2, criterion_list )
    print(engine_list)
    agent1 = MotorAgent(0, motormodel, 'agent1',criterion_list, engine_list)
    agent2 = MotorAgent(1, motormodel, 'agent2',criterion_list, engine_list)
    motormodel.schedule.add(agent1)
    motormodel.schedule.add(agent2)
    print(agent1.get_preferences().most_preferred([engine_list[0]["item"], engine_list[1]["item"]]).get_name())

    step = 0
    while step < 10:
        motormodel.step()
        step += 1