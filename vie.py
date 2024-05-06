class Vie:
    def __init__(self,num,larg):
        self.y=100
        self.num=num
        self.vie=540
        self.deg=0
        self.larg=larg
        if num==1: 
            self.x=50
            self.x_deg=self.x        
        else:
            self.x=larg-50-self.vie         
            self.x_deg=self.x +self.vie
            
            
    def get_vie(self):
        return self.vie
    
    
    
    def degat(self,degat,defense):
        if self.num==1:
            self.vie-=degat-defense
            self.deg+=degat-defense
            self.x+=degat-defense
        else:
            self.vie-=degat-defense
            self.deg+=degat-defense
            self.x_deg-=degat-defense
            
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    
    
    def get_deg(self):
        return self.deg
    def get_x_deg(self):
        return self.x_deg
    def reset_vie(self):
        self.y=100
        self.vie=540
        self.deg=0
        if self.num==1: 
            self.x=50
            self.x_deg=self.x        
        else:
            self.x=self.larg-50-self.vie         
            self.x_deg=self.x +self.vie