#!/ usr / bin /env python3

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from communication.preferences.Value import Value
import random


class Argument :
    """ Argument class .
    This class implements an argument used during the interaction .

    attr :
    decision :
    item :
    comparison_list :
    couple_values_list :
    """

    def __init__(self, boolean_decision, item):
        """ Creates a new Argument .
        """
        self.boolean_decision = boolean_decision
        self.item = item
        self.comparison_list = list()
        self.couple_values_list = list()

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """ Adds a premiss comparison in the comparison list .
        """
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))
        
    
    def add_premiss_couple_values(self, criterion_name, value):
        """ Add a premiss couple values in the couple values list .
        """
        self.couple_values_list.append(CoupleValue(criterion_name, value))
        

    def List_supporting_proposal(self, preferences) :
        """ Generate a list of premisses which can be used to support an item
        : param item : Item - name of the item
        : return : list of all premisses PRO an item (sorted by order of importance
        based on agent’s preferences)
        """
        criterion_list = preferences.get_criterion_name_list()
        for criterion_name_1 in criterion_list:
            value = self.item.get_value(preferences, criterion_name_1)
            if value == Value.VERY_GOOD or value == Value.GOOD:
                self.add_premiss_couple_values(criterion_name_1, value)
            for criterion_name_2 in criterion_list:
                if criterion_name_2 != criterion_name_1 and criterion_name_1 == preferences.is_preferred_criterion(criterion_name_1, criterion_name_2):
                    self.add_premiss_comparison(criterion_name_1, criterion_name_2)
        list_of_supporting_proposal = self.comparison_list + self.couple_values_list
        return list_of_supporting_proposal
        
    def List_attacking_proposal(self, preferences) :
        """ Generate a list of premisses which can be used to attack an item
        : param item : Item - name of the item
        : return : list of all premisses CON an item ( sorted by order of importance
        based on preferences )
        """
        criterion_list = preferences.get_criterion_name_list()
        for criterion_name_1 in criterion_list:
            value = self.item.get_value(preferences, criterion_name_1)
            if value == Value.VERY_BAD or value == Value.BAD:
                self.add_premiss_couple_values(criterion_name_1, value)
            for criterion_name_2 in criterion_list:
                if criterion_name_2 != criterion_name_1 and criterion_name_1 == preferences.is_preferred_criterion(criterion_name_1, criterion_name_2):
                    self.add_premiss_comparison(criterion_name_1, criterion_name_2)
        list_of_attacking_proposal = self.comparison_list + self.couple_values_list
        return list_of_attacking_proposal  

    def support_proposal(self, preferences):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """
        list_of_supporting_proposal = self.List_supporting_proposal(preferences)
        support_proposal = list_of_supporting_proposal[0]
        if support_proposal.type == 'CoupleValue':
            value = support_proposal.value
            criterion_name = support_proposal.criterion_name
            argument = str(criterion_name) + ' = ' + str(value)
        else:
            best_criterion_name = support_proposal.best_criterion_name 
            worst_criterion_name = support_proposal.worst_criterion_name 
            argument = str(best_criterion_name) + ' > ' + str(worst_criterion_name)
        return argument

    def get_list_of_counter_arguments(self, preferences, argument):
        list_of_attacking_arguments = self.List_attacking_proposal(preferences)
        print(list_of_attacking_arguments)
        list_of_counter_arguments = list()
        for attacking_argument in list_of_attacking_arguments:
            if attacking_argument.type == 'CoupleValue':
                print(attacking_argument.criterion_name, attacking_argument.value)
                if str(attacking_argument.criterion_name) in argument:
                    list_of_counter_arguments.append(attacking_argument)
            else:
                print(attacking_argument.best_criterion_name, attacking_argument.worst_criterion_name)
                if str(attacking_argument.worst_criterion_name) in argument:
                    list_of_counter_arguments.append(attacking_argument)
        return list_of_counter_arguments

    # def get_counter_argument(self, preferences, argument):
    #     list_of_counter_arguments = self.get_list_of_counter_arguments(preferences, argument)
    #     counter_proposal = list_of_counter_arguments[0]
    #     if counter_proposal.type == 'CoupleValue':
    #         value = counter_proposal.value
    #         criterion_name = counter_proposal.criterion_name
    #         counter_argument = str(criterion_name) + ' = ' + str(value)
    #     else:
    #         best_criterion_name = counter_proposal.best_criterion_name 
    #         worst_criterion_name = counter_proposal.worst_criterion_name 
    #         counter_argument = str(best_criterion_name) + ' > ' + str(worst_criterion_name)
    #     return counter_argument
    
    def get_counter_argument(self, preferences, argument, engine_list):
        possible_counter_arguments = list()
        if argument.type == 'CoupleValue':
            criterion_name = argument.criterion_name
            agent_value = self.item.get_value(preferences, criterion_name)
            if argument.value.value > agent_value.value:
                possible_counter_arguments.append(str(criterion_name) + ' = ' + str(agent_value))
            for engine in engine_list:
                engine_value = engine.get_value(preferences, criterion_name)
                if preferences.is_preferred_item(engine, self.item) and preferences.is_item_among_top_10_percent(engine,engine_list) and engine_value.value > agent_value.value:
                    possible_counter_arguments.append(str(engine) + ', ' + str(criterion_name) + ' = ' + str(agent_value))
        else:
            best_criterion_name = argument.best_criterion_name
            worst_criterion_name = argument.worst_criterion_name
        return random.choice(possible_counter_arguments)            