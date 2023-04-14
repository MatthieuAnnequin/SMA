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

    def __init__(self, unique_id, model, name, criterion_list, engine_list, agents_list):
        """ Create a new motor agent.
        """
        super().__init__(unique_id, model, name)

        self.__preferences = Preferences()

        self.first_step = True

        self.list_other_agent = [x for x in agents_list if x != name]
        self.best_motor = self.__preferences.most_preferred([engine['item'] for engine in engine_list])
        

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

        if self.first_step and self.get_name() == "agent1":
            agent_y = random.choice(self.list_other_agent)
            self.send_message(Message(self.get_name(),agent_y,MessagePerformative.PROPOSE, self.best_motor))
            print(self.get_name() + " propose " + str(self.best_motor.get_name()) + " à " + agent_y)
            self.first_step = False

        
        for message in self.get_new_messages():
            #print(str(message))
            if message.get_performative() == MessagePerformative.PROPOSE:
                self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.ASK_WHY, "Pourquoi ?"))
            elif message.get_performative() == MessagePerformative.ASK_WHY:
                agent_y = message.get_dest()
                self.send_message(Message(self.get_name(),"agent2",MessagePerformative.PROPOSE, self.best_motor.get_name() + " car " ))

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
    
    def get_argument(engine):
        pass
        



if __name__ == "__main__":
    # Init the model and the agents
     #To complete
    motormodel = SpeakingModel()
    criterion_list = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                    CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                    CriterionName.NOISE]
    engine_list = motor_generator(2, criterion_list )
    agents_list = ['agent1', 'agent2']
    agent1 = MotorAgent(0, motormodel, 'agent1',criterion_list, engine_list, agents_list)
    agent2 = MotorAgent(1, motormodel, 'agent2',criterion_list, engine_list, agents_list)
    motormodel.schedule.add(agent1)
    motormodel.schedule.add(agent2)
    print(agent1.get_preferences().most_preferred([engine_list[0]["item"], engine_list[1]["item"]]).get_name())

    step = 0
    while step < 10:
        motormodel.step()
        step += 1