class Agent:
    def act(self):
        pass
    
    def _act_wrapper(self):
        print('Base-class pre-code!')

        self.act()

        print('Base-class post-code!')
