
import BlackBoxTesterView
import BlackBoxTesterModel

class Controller():
    def __init__(self, the_model, the_view):
        self.model = the_model.Model(self) # BlackBoxTesterModel.Model()
        self.view = the_view.View() # BlackBoxTesterView.View()
        self.view.centerPanel.scriptstab.LoadBtn.bind("<Button>",self.scriptSelectionLoadButtonClick)

    def run(self): # need to run as thread????
        self.view.run()

    def clear(self,event):
        pass

    def scriptSelectionLoadButtonClick(self,event):
        print("scriptSelectionLoadButtonClick")
        self.view.centerPanel.scriptstab.timeLabel.config(text ='changed')

if __name__ == '__main__':
    c = Controller()
    c.run()