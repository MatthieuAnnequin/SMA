#!/ usr / bin /env python3

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from communication.preferences.Value import Value


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

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2, preferences):
        """ Adds a premiss comparison in the comparison list .
        """
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))
        
    
    def add_premiss_couple_values(self, criterion_name, value):
        """ Add a premiss couple values in the couple values list .
        """
        self.couple_values_list.append(CoupleValue(criterion_name, value))
        

    def List_supporting_proposal(self, item, preferences) :
        """ Generate a list of premisses which can be used to support an item
        : param item : Item - name of the item
        : return : list of all premisses PRO an item (sorted by order of importance
        based on agent’s preferences)
        """
        criterion_list = preferences.get_criterion_name_list()
        for criterion_name_1 in criterion_list:
            value = item.get_value(preferences, criterion_name_1)
            if value == Value.VERY_GOOD or value == Value.GOOD:
                self.add_premiss_couple_values(criterion_name_1, value)
            for criterion_name_2 in criterion_list:
                if criterion_name_2 != criterion_name_1 and criterion_name_1 == preferences.is_preferred_criterion(criterion_name_1, criterion_name_2):
                    self.add_premiss_comparison(criterion_name_1, criterion_name_2)
        list_of_supporting_proposal = self.comparison_list + self.couple_values_list
        return list_of_supporting_proposal
        
    def List_attacking_proposal(self, item, preferences) :
        """ Generate a list of premisses which can be used to attack an item
        : param item : Item - name of the item
        : return : list of all premisses CON an item ( sorted by order of importance
        based on preferences )
        """
        criterion_list = preferences.get_criterion_name_list()
        for criterion_name_1 in criterion_list:
            value = item.get_value(preferences, criterion_name_1)
            if value == Value.VERY_BAD or value == Value.BAD:
                self.add_premiss_couple_values(criterion_name_1, value)
            for criterion_name_2 in criterion_list:
                if criterion_name_2 != criterion_name_1 and criterion_name_1 == preferences.is_preferred_criterion(criterion_name_1, criterion_name_2):
                    self.add_premiss_comparison(criterion_name_1, criterion_name_2)
        list_of_supporting_proposal = self.comparison_list + self.couple_values_list
        return list_of_supporting_proposal  

    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """

