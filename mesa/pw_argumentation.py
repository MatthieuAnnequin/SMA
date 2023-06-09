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
from arguments.CoupleValue import CoupleValue
from arguments.Comparison import Comparison


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
        
        self.current_motor_proposal_name = None

        self.dic_crit = {'PRODUCTION_COST' : CriterionName.PRODUCTION_COST,
                    'CONSUMPTION' : CriterionName.CONSUMPTION,
                    'DURABILITY' : CriterionName.DURABILITY,
                    'ENVIRONMENT_IMPACT' : CriterionName.ENVIRONMENT_IMPACT,
                    'NOISE' : CriterionName.NOISE,}
        self.dic_value = {'.VERY_GOOD' : Value.VERY_GOOD,
                     '.GOOD' : Value.GOOD,
                     '.BAD' : Value.BAD,
                     '.VERY_BAD' : Value.VERY_BAD}
        
        self.list_agent_arguments = []
        self.already_discussed_motor = []
        
       

    def step(self):
        super().step()

        # agent1 starts the process by offering its best motor
        if self.first_step and self.get_name() == "agent1":
            agent_y = random.choice(self.list_other_agent)
            self.send_message(Message(self.get_name(), agent_y, MessagePerformative.PROPOSE, self.best_motor.get_name()))
            self.already_discussed_motor.append(self.best_motor.get_name())
            self.current_motor_proposal_name = self.best_motor.get_name()
            self.first_step = False

        
        for message in self.get_new_messages():
            print(message)
            if message.get_performative() == MessagePerformative.PROPOSE:
                motor_name = message.get_content()
                self.already_discussed_motor.append(motor_name)
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
                agent_y = message.get_exp()
                motor_name = message.get_content()
                motor_item = self.get_motor_item(motor_name)
                argumentation = Argument(True, motor_item)
                motor_argument = argumentation.support_proposal(self.get_preferences())
                self.list_agent_arguments.append((motor_item, motor_argument))
                self.send_message(Message(message.get_dest(),message.get_exp(), MessagePerformative.ARGUE, motor_name + ":" + str(motor_argument) ))

            elif message.get_performative() == MessagePerformative.ARGUE:
                motor_item, argument = self.arguement_parser(message.get_content())
                if self.current_motor_proposal_name == motor_item.get_name():
                    possible_motors = [engine['item'] for engine in self.model.engine_list if not(engine['item'].get_name() in self.already_discussed_motor)]                            
                    argumentation = Argument(False, motor_item)
                    new_item, pro_argument, accept = argumentation.get_pro_argument(self.get_preferences(), argument, possible_motors, self.list_agent_arguments)
                    if accept:
                        self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.ACCEPT, new_item.get_name()))
                    elif new_item.get_name() != motor_item.get_name():
                        self.send_message(Message(message.get_dest(),message.get_exp(), MessagePerformative.PROPOSE, new_item.get_name()))
                    else:
                        self.send_message(Message(message.get_dest(),message.get_exp(), MessagePerformative.ARGUE, new_item.get_name() + ":" + str(pro_argument) ))
                        self.list_agent_arguments.append((new_item, pro_argument))

                else:    
                    possible_motors = [engine['item'] for engine in self.model.engine_list if not(engine['item'].get_name() in self.already_discussed_motor)]                            
                    argumentation = Argument(False, motor_item)
                    new_item, counter_argument, accept = argumentation.get_counter_argument(self.get_preferences(), argument, possible_motors, self.list_agent_arguments)
                    if accept:
                        self.send_message(Message(message.get_dest(),message.get_exp(),MessagePerformative.ACCEPT, new_item.get_name()))
                    elif new_item.get_name() != motor_item.get_name():
                        self.send_message(Message(message.get_dest(),message.get_exp(), MessagePerformative.PROPOSE, new_item.get_name()))
                    else:
                        self.send_message(Message(message.get_dest(),message.get_exp(), MessagePerformative.ARGUE, new_item.get_name() + ":" + str(counter_argument) ))
                        self.list_agent_arguments.append((new_item, counter_argument))


            

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
        self.agent_criterion_list = self.model.criterion_list.copy()
        random.shuffle(self.agent_criterion_list)
        #print(self.unique_id, self.agent_criterion_list)
        self.__preferences.set_criterion_name_list(self.agent_criterion_list)

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
    
    def arguement_parser(self, str_arg):
        item_name = str_arg.split(':')[0]
        item = self.get_motor_item(item_name)
        arg_part = str_arg.split(':')[1]
        if ' and ' in arg_part:
            arg_str_1 =  arg_part.split(' and ')[0]
            arg_str_2 =  arg_part.split(' and ')[1]
            res_arg_1 = self.parse_couple_value(arg_str_1)
            res_arg_2 = self.parse_comparison(arg_str_2)
            return item, res_arg_1
        
        elif ' = ' in arg_part:
            res_arg = self.parse_couple_value(arg_part)
            return item, res_arg
            
        elif ' > ' in arg_part:
            res_arg = self.parse_comparison(arg_part)
            return item, res_arg
        
    def parse_couple_value(self, arg_part):
        crit_str = arg_part.split(' = ')[0]
        value_str = arg_part.split(' = ')[1]
        for crit_name in list(self.dic_crit):
            if crit_name in crit_str:
                criterion = self.dic_crit[crit_name]
        for value_name in list(self.dic_value):
            if value_name in value_str:
                value = self.dic_value[value_name]
        return CoupleValue(criterion, value)
        
    def parse_comparison(self, arg_part):
        crit_1_str = arg_part.split(' > ')[0]
        crit_2_str = arg_part.split(' > ')[1]

        for crit_name in list(self.dic_crit):
            if crit_name in crit_1_str:
                criterion_1 = self.dic_crit[crit_name]

        for crit_name in list(self.dic_crit):
            if crit_name in crit_2_str:
                criterion_2 = self.dic_crit[crit_name]
        return Comparison(criterion_1, criterion_2)

    



    







class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model .
    """
    def __init__(self, n_motors = 5):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True


        # define criterion list
        self.criterion_list = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE]
        
        # generate list of engine
        self.engine_list = motor_generator(n_motors, self.criterion_list )

        # define agents, create them and add them to the model
        agents_list = ['agent1', 'agent2']
        agent1 = ArgumentAgent('agent1', self, 'agent1', agents_list)
        agent2 = ArgumentAgent('agent2', self, 'agent2', agents_list)
        self.schedule.add(agent1)
        self.schedule.add(agent2)
        

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

    def run_N(self, nb_it):
        for i in range(nb_it):
            self.step()



def launch_step():
    print('Launch ArgumentModel')
    argument_model = ArgumentModel()

    step = 0
    while step < 10:
        #print(step)
        argument_model.step()
        step += 1


launch_step()


if __name__ == " __main__ ":
    print('Launch ArgumentModel')
    argument_model = ArgumentModel(n_motors=5)
    argument_model.run_N(20)
