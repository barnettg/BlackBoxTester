# This is a traffic light simulation
# There is a traffic light for north to south traffic and
# a traffic light for east to west traffic
# there are car sensor at appropriate points in the road to detect waiting cars
# There is a train sensor  for a train that crosses N to S traffic
# E to W traffic takes priority
# operation changes depending on the time of day
# a state machine keeps track of the system state
# the system can communicate by serial or network


# this is to be used as a sample system for evaluating the black box tester
#

# states
# NsGreenEwRedState
# NsYellowEwRedState
# NsRedEwRedToEwGreenState
# NsRedEwGreenState
# NsRedEwYellowState
# NsRedEwRedToNsGreenState
# NsRedFlashEwRedFlashState

#operations
# car sensor NS                     a car is waiting on the North-South path
# car sensor EW                     a car is waiting on the East-West path
# train                             a train is in the area
# lights_operating_error            there is an error go to flashing red
# change light                      go to the next state in the sequence

#
# Commands:
# ?readstate  -> returns the state
# traincoming
# traingone
# carwaitingNS
# carwaitingEW
# seterror
# clearerror
# change


class IState(object):
    
    """Interface for state"""
    def change( self ):
        raise NotImplementedError( "Must Implement change method" )
    def train( self ):
        raise NotImplementedError( "Must Implement train method" )
    def car_at_NS (self ):
        raise NotImplementedError( "Must Implement car at North-South method" )
    def car_at_EW( self ):
        raise NotImplementedError( "Must Implement car at East-West method" )
    def lights_operating_error( self ):
        raise NotImplementedError( "Must Implement lights_error method" )
    def lights_operating_error_resolved( self ):
        raise NotImplementedError( "Must Implement lights_error method" )
    
class NsGreenEwRedState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Green and EW Red State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_yellow_EW_red_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() ) # stay in NS priority if no sensors active
    
class NsYellowEwRedState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Yellow and EW Red State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_EW_green_state() ) #
    

class NsRedEwRedToEwGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Red To EW Green State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_green_state() ) #

class NsRedEwGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Green State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_yellow_state() ) #

class NsRedEwYellowState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red and EW Yellow State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() ) #

class NsRedEwRedToNsGreenState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red EW Red To NS Green State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_green_EW_red_state() ) #

class NsRedFlashEwRedFlashState(IState):
    def __init__(self, trafic_machine):
        self.trafic_machine = trafic_machine
        self.name = "NS Red Flash and EW Red Flash State"
        
    def change( self ):
        if self.trafic_machine.error:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_Flash_EW_red_Flash_state() )
            return
        if self.trafic_machine.train_coming:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingEW:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        if self.trafic_machine.carwaitingNS:
            self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() )
            return
        self.trafic_machine.setState(self.trafic_machine.get_NS_red_EW_red_to_NS_green_state() ) #  

#-------------------------------------

class TrafficMachine():
    def __init__(self):
        self.error = False
        self.train_coming = False
        self.carwaitingEW = False
        self.carwaitingNS = False

            
        self.NS_green_EW_red_state = NsGreenEwRedState(self)
        self.NS_yellow_EW_red_state = NsYellowEwRedState(self)
        self.NS_red_EW_red_to_EW_green_state = NsRedEwRedToEwGreenState(self)
        self.NS_red_EW_green_state = NsRedEwGreenState(self)
        self.NS_red_EW_yellow_state = NsRedEwYellowState(self)
        self.NS_red_EW_red_to_NS_green_state = NsRedEwRedToNsGreenState(self)
        self.NS_red_Flash_EW_red_Flash_state = NsRedFlashEwRedFlashState(self)
        
        # initial state
        self.state = self.NS_red_Flash_EW_red_Flash_state

    def setState(self, newState):
        self.state = newState
        #print(self.state.name)
        
    def change(self):
        self.state.change()

    def get_NS_green_EW_red_state(self):
        return self.NS_green_EW_red_state

    def get_NS_yellow_EW_red_state(self):
        return self.NS_yellow_EW_red_state

    def get_NS_red_EW_red_to_EW_green_state(self):
        return self.NS_red_EW_red_to_EW_green_state

    def get_NS_red_EW_green_state(self):
        return self.NS_red_EW_green_state

    def get_NS_red_EW_yellow_state(self):
        return self.NS_red_EW_yellow_state

    def get_NS_red_EW_red_to_NS_green_state(self):
        return self.NS_red_EW_red_to_NS_green_state

    def get_NS_red_Flash_EW_red_Flash_state(self):
        return self.NS_red_Flash_EW_red_Flash_state

    
    

if __name__ == '__main__':
    trafficMachine = TrafficMachine()
    print(trafficMachine.state.name)

    trafficMachine.carwaitingEW = True
    for changes in range(0,8):
        trafficMachine.change()
        #print(str(trafficMachine.state))
        print(trafficMachine.state.name)

