pose = "None" #태연님이 만든 포즈값 setPose("포즈이름") 으로 변경해주시면 될듯!
gameEnd = False #게임 종료 여부





def setPose(string):
    global pose
    pose = string
def getPose(string):
    global pose
    return pose

def setGameEnd(string):
    global gameEnd
    gameEnd = True
        
def getGameEnd(string):
    global gameEnd
    return gameEnd



