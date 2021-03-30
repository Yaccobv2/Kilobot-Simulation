import skfuzzy as fuzz
from skfuzzy import control as ctrl
import skimage
import numpy as np
import matplotlib.pyplot as plt

def scifuzz(dist, prev_dist):
    """
        Calculates value of M2 engine based of fuzzy rules
        :param: t: Objects which contains simulation time
        :param: t_pause: Objects which contains pause time
        :return: t: Objects which contains simulation time
        :return: enable: Flag enabling movement
        :return: M2_value: Activation value of M2 motor
    """
    # declaration of lingustic variables
    distance = ctrl.Antecedent(np.arange(0, 7000, 1), 'distance')
    prev_distance = ctrl.Antecedent(np.arange(0, 7000, 1),'prev_distance')
    M2F = ctrl.Consequent(np.arange(0, 255, 1), 'M2F')
    #assigning names to fuzzy sets
    names = ['very_close', 'close', 'far']
    # declaration of traingular shape of membership functions
    distance.automf(names=names)
    prev_distance.automf(names=names)

    # declaration of traingular shape of membership functions with sets values and names
    M2F['low'] = fuzz.trimf(M2F.universe, [0, 0, 128])
    M2F['medium'] = fuzz.trimf(M2F.universe, [0, 128, 255])
    M2F['high'] = fuzz.trimf(M2F.universe, [128, 255, 255])

    #Ruleset
    rule1 = ctrl.Rule(distance['very_close'] & prev_distance['close'], M2F['high'])
    rule2 = ctrl.Rule(distance['close'] & prev_distance['far'], M2F['medium'])
    rule3 = ctrl.Rule(distance['very_close'] & prev_distance['close'], M2F['high'])
    rule4 = ctrl.Rule(distance['close'] & prev_distance['close'], M2F['medium'])
    rule5 = ctrl.Rule(distance['far'] & prev_distance['very_close'], M2F['low'])
    rule6 = ctrl.Rule(distance['far'] & prev_distance['close'], M2F['low'])
    rule7 = ctrl.Rule(distance['close'] & prev_distance['far'], M2F['low'])

    #aggregation of rules
    motor_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
    motor = ctrl.ControlSystemSimulation(motor_ctrl)

    #assigning input values to local variables
    distance = dist
    prev_distance = prev_dist

    #assigning assigning those values as model inputs
    motor.input['distance'] = distance
    motor.input['prev_distance'] = prev_distance
    #computes result
    motor.compute()
    #prints output value
    print(motor.output['M2F'])
    #rounds output value
    M2_value = round(motor.output['M2F'])
    return M2_value # returns result
