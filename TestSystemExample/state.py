#state pattern example
# from Head first design patterns (java)


class IState(object):
    """Interface for state"""
    def insertQuarter( self ):
        raise NotImplementedError( "Must Implement insertQuarter" )
    def ejectQuarter( self ):
        raise NotImplementedError( "Must Implement ejectQuarter method" )
    def turnCrank (self ):
        raise NotImplementedError( "Must Implement turnCrank method" )
    def dispense( self ):
        raise NotImplementedError( "Must Implement dispense method" )

class SoldState(IState):
    def __init__(self, gbMachine):
        self.gumballMachine = gbMachine
    def insertQuarter( self ):
        print "Please wait we are already giving you a gumball"
        
    def ejectQuarter( self ):
        print "Sorry you already turned the crank"
                
    def turnCrank (self ):
        print "Turning twice doesn't get you another gumball"
        self.gumballMachine.setState(self.gumballMachine.getSoldState())

    def dispense( self ):
        self.gumballMachine.releaseBall()
        if self.gumballMachine.getCount() >0:
            self.gumballMachine.setState(self.gumballMachine.getNoQuarterState())
        else:
            print "Oops, out of gumballs"
            self.gumballMachine.setState(self.gumballMachine.getSoldOutState())

class SoldOutState(IState):
    def __init__(self, gbMachine):
        self.gumballMachine = gbMachine
    def insertQuarter( self ):
        print "Sold out"
        
    def ejectQuarter( self ):
        print "Sold out"
                
    def turnCrank (self ):
        print "Sold out"

    def dispense( self ):
        print "Oops, out of gumballs"
        self.gumballMachine.setState(self.gumballMachine.getSoldOutState())

class NoQuarterState(IState):
    def __init__(self, gbMachine):
        self.gumballMachine = gbMachine
    def insertQuarter( self ):
        print "you inserted a quarter"
        self.gumballMachine.setState(self.gumballMachine.getHasQuarterState())
        
    def ejectQuarter( self ):
        print "you havn't inserted a quarter"
        
    def turnCrank (self ):
        print "you turned but there is no quarter"

    def dispense( self ):
        print "you need to pay first"
        

class HasQuarterState(IState):
    def __init__(self, gbMachine):
        self.gumballMachine = gbMachine
    def insertQuarter( self ):
        print "you can't insert another quarter"
        
    def ejectQuarter( self ):
        print "quarter returned"
        self.gumballMachine.setState(self.gumballMachine.getNoQuarterState())
        
    def turnCrank (self ):
        print "you turned..."
        self.gumballMachine.setState(self.gumballMachine.getSoldState())

    def dispense( self ):
        print "no gumball dispensed"

class GumballMachine():
    def __init__(self, numberOfGumballs):
        self.soldOutState = SoldOutState(self)
        self.noQuarterState = NoQuarterState(self)
        self.hasQuarterState = HasQuarterState(self)
        self.soldState = SoldState(self)
        # initial state
        self.state = self.soldOutState

        self.count = numberOfGumballs
        if numberOfGumballs > 0 :
            self.state = self.noQuarterState

    def insertQuarter(self):
        self.state.insertQuarter()

    def ejectQuarter(self):
        self.state.ejectQuarter()

    def turnCrank(self):
        self.state.turnCrank()

    def insertQuarter(self):
        self.state.insertQuarter()
        
    def dispense(self):
        self.state.dispense()

    def setState(self, newState):
        self.state = newState

    def releaseBall(self):
        print " "
        if self.count != 0 :
            self.count -= 1
            
    def getSoldOutState(self):
        return self.soldOutState

    def getHasQuarterState(self):
        return self.hasQuarterState

    def getNoQuarterState(self):
        return self.noQuarterState

    def getSoldState(self):
        return self.soldState

    def getCount(self):
        return self.count
    
    

if __name__ == '__main__':
    gumballMachine = GumballMachine(2)
    print str(gumballMachine.state)
    gumballMachine.insertQuarter()
    print str(gumballMachine.state)
    gumballMachine.turnCrank()
    print str(gumballMachine.state)
    
    gumballMachine.dispense()
    print str(gumballMachine.state)
    gumballMachine.insertQuarter()
    print str(gumballMachine.state)
    gumballMachine.turnCrank()
    print str(gumballMachine.state)
    
    gumballMachine.dispense()
    print str(gumballMachine.state)
    gumballMachine.insertQuarter()
    print str(gumballMachine.state)
    gumballMachine.turnCrank()
    print str(gumballMachine.state)
    
    gumballMachine.dispense()
    print str(gumballMachine.state)
    
    
