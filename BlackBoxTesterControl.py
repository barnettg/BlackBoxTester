
import BlackBoxTesterView
import BlackBoxTesterModel

class Controller():
    def __init__(self):
        self.model = BlackBoxTesterModel.Model()
        self.view = BlackBoxTesterView.View()
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