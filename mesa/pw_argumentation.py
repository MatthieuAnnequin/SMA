import random

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
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
from arguments.Argument import Argument


class ArgumentAgent(CommunicatingAgent):
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """

    def __init__(self, unique_id, model, name, agents_list):
        """ Create a new motor agent.
        """
        super().__init__(unique_id, model, name)
        self.model = model
        
        # Generate agent Preferences
        self.generate_preferences()

        self.first_step = True

        self.list_other_agent = [x for x in agents_list if x != name]
        self.best_motor = self.__preferences.most_preferred([engine['item'] for engine in model.engine_list])
        self.top_10_percent_list = self.__preferences.top_10_percent_list([engine['item'] for engine in model.engine_list])
        
       

    def step(self):
        super().step()

        # agent1 starts the process by offering its best motor
        if self.first_step and self.get_name() == "agent1":
            agent_y = random.choice(self.list_other_agent)
            self.send_message(Message(self.get_name(), agent_y, MessagePerformative.PROPOSE, self.best_motor.get_name()))
            print(self.get_name() + " propose " + str(self.best_motor.get_name()) + " à " + agent_y)
            self.first_step = False

        
        for message in self.get_new_messages():
            print(message)
            if message.get_performative() == MessagePerformative.PROPOSE:
                motor_name = message.get_content()
                top_10_percent_list_name = [item.get_name() for item in self.top_10_percent_list]
                if motor_name in top_10_percent_list_name:
                    self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.ACCEPT, motor_name))
                else:
                    self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.ASK_WHY, motor_name))
            
            elif message.get_performative() == MessagePerformative.ACCEPT:
                motor_name = message.get_content()
                list_available_motor_name = [engine['item'].get_name() for engine in self.model.engine_list]
                if motor_name in list_available_motor_name:
                    self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.COMMIT, motor_name))


            elif message.get_performative() == MessagePerformative.COMMIT:
                motor_name = message.get_content()
                list_available_motor_name = [engine['item'].get_name() for engine in self.model.engine_list]
                
                if motor_name in list_available_motor_name:
                    self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.COMMIT, motor_name))
                    # remove element from list
                    self.get_update_engine_list(motor_name)

            elif message.get_performative() == MessagePerformative.ASK_WHY:
                agent_y = message.get_dest()
                motor_name = message.get_content()
                motor_item = self.get_motor_item(motor_name)
                argumentation = Argument(True, motor_item)
                motor_argument = argumentation.support_proposal(motor_item, self.get_preferences())
                self.send_message(Message(self.get_name(),agent_y, MessagePerformative.ARGUE, motor_name + ":" + str(motor_argument) ))

            elif message.get_performative() == MessagePerformative.ARGUE:
                list_content = message.get_content().split(':')
                motor_name, str_argument = list_content[0], list_content[1]
                print(motor_name, str_argument)
                motor_item = self.get_motor_item(motor_name)
                argumentation = Argument(False, motor_item)
                counter_argument = argumentation.get_counter_argument(self.get_preferences(), str_argument)
                self.send_message(Message(self.get_name(),message.get_exp(), MessagePerformative.ARGUE, motor_name + ":" + str(counter_argument) ))

            

    def get_preference(self):
        return self.preference
    
    def get_update_engine_list(self, motor_name):
        """ remove motor name from engine list"""
        res = []
        for engine in self.model.engine_list:
            if engine['item'].get_name() != motor_name:
                res.append(engine)

        self.model.engine_list = res

    def get_motor_item(self, motor_name):
        for engine in self.model.engine_list:
            if engine['item'].get_name() == motor_name:
                return engine['item']



    def generate_preferences(self):
        # create agent preferences
        self.__preferences = Preferences()

        # Initialize citerion preferences
        random.shuffle(self.model.criterion_list)
        self.__preferences.set_criterion_name_list(self.model.criterion_list)

        # Initialize agent scales by criterion
        for engine in self.model.engine_list:
            engine_scale = self.generate_agent_scale(max_value = 10, min_value = 0)
            engine_item = engine['item']
            for criterion in self.model.criterion_list:
                agent_rank = self.get_agent_rank(engine_scale, engine['criterion'][criterion])
                self.__preferences.add_criterion_value(CriterionValue(engine_item, criterion, agent_rank))
        
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
    







class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model .
    """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True


        # define criterion list
        self.criterion_list = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE]
        
        # generate list of engine
        self.engine_list = motor_generator(2, self.criterion_list )

        # define agents, create them and add them to the model
        agents_list = ['agent1', 'agent2']
        agent1 = ArgumentAgent('agent1', self, 'agent1', agents_list)
        agent2 = ArgumentAgent('agent2', self, 'agent2', agents_list)
        self.schedule.add(agent1)
        self.schedule.add(agent2)

        # To be completed
        #
        # a = ArgumentAgent(id , " agent_name ")
        # a. generate_preferences(preferences)
        # self.schedule .add(a)
        # ...

        

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

    def run_N(self, nb_it):
        for i in range(nb_it):
            self.step()





def launch_test():
    communicating_model = ArgumentModel()

    assert(len(communicating_model.schedule.agents) == 2)
    print("*     get the number of CommunicatingAgent => OK")

    agent0 = communicating_model.schedule.agents[0]
    agent1 = communicating_model.schedule.agents[1]

    assert(agent0.get_name() == 'agent1')
    assert(agent1.get_name() == 'agent2')
    print("*     get_name() => OK")

    agent0.send_message(Message('agent1', 'agent2', MessagePerformative.COMMIT, "Bonjour"))
    agent1.send_message(Message('agent2', 'agent1', MessagePerformative.COMMIT, "Bonjour"))
    agent0.send_message(Message('agent1', 'agent2', MessagePerformative.COMMIT, "Comment ça va ?"))

    assert(len(agent0.get_new_messages()) == 1)
    print(agent0.get_messages())
    assert(len(agent1.get_new_messages()) == 2)
    assert(len(agent0.get_messages()) == 1)
    assert(len(agent1.get_messages()) == 2)
    print("*     send_message() & dispatch_message (instant delivery) => OK")

    MessageService.get_instance().set_instant_delivery(False)

    agent0.send_message(Message('agent1', 'agent2', MessagePerformative.COMMIT, "Bonjour"))
    agent1.send_message(Message('agent2', 'agent1', MessagePerformative.COMMIT, "Bonjour"))
    agent0.send_message(Message('agent1', 'agent2', MessagePerformative.COMMIT, "Comment ça va ?"))

def launch_step():
    print('Launch ArgumentModel')
    argument_model = ArgumentModel()

    step = 0
    while step < 10:
        print(step)
        argument_model.step()
        step += 1


launch_step()


if __name__ == " __main__ ":
    print('Launch ArgumentModel')
    argument_model = ArgumentModel()
    argument_model.run_N(10)

# To be completed