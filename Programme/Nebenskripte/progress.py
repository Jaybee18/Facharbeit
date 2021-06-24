import sys, os, time
os.system('color')

class progressBar():
    def __init__(self, **kwargs):
        self.inPercent = True
        self.title = ''
        self.startValue = 0
        self.maxValue = 100 #default 100 because of percent
        self.lenOfBar = 10 #ten hashtags on default
        self.filledChar = '#'
        self.emptyChar = '-'
        self.steps = 1 #default for percent
        self.value = 0 #not to be edited
        self.sleepTime = 0.02
        self.successMessage = "done"
        self.errorMessage = "ERROR"

        self.tempDict = {'inPercent':self.inPercent, 'title':self.title, 'startValue':self.startValue, 'maxValue':self.maxValue, 'lenOfBar':self.lenOfBar, 'filledChar':self.filledChar, 'emptyChar':self.emptyChar, 'steps':self.steps, 'sleepTime':self.sleepTime, 'successMessage':self.successMessage, 'errorMessage':self.errorMessage}

        for element in kwargs:
            try:
                if(type(kwargs[element]) == type(self.tempDict[element])):
                    self.tempDict[element] = kwargs[element]
                else:
                    raise ValueError
            except KeyError as e:
                print(f'\033[91mKeyError: the parameter \033[4m{element}\033[0m\033[91m is not defined in class progressBar\033[0m')
            except ValueError as e:
                print(f'\033[91mTypeError: the value of the parameter \033[4m{element}\033[0m is of type {type(element)} but it has to be of type {type(self.tempDict[element])}\033[0m')
            except:
                print('\033[91munexpected error occured while setting the arguments\033[0m')
                raise #print occured error
        
        self.values = {'inPercent':self.tempDict['inPercent'], 'title':self.tempDict['title'], 'startValue':self.tempDict['startValue'], 'maxValue':self.tempDict['maxValue'], 'lenOfBar':self.tempDict['lenOfBar'], 'filledChar':self.tempDict['filledChar'], 'emptyChar':self.tempDict['emptyChar'], 'steps':self.tempDict['steps'], 'sleepTime':self.tempDict['sleepTime'], 'successMessage':self.tempDict['successMessage'], 'errorMessage':self.tempDict['errorMessage'], 'value':self.value}
        if(self.values['inPercent'] and 'maxValue' in kwargs):
            raise Exception('\033[91mArgumentError: argument \033[4mmaxValue\033[0m\033[91m not allowed when using percent\033[0m')
        if(not self.values['inPercent'] and 'maxValue' not in kwargs):
            raise Exception('\033[91mArgumentError: argument \033[4mmaxValue\033[0m\033[91m has to be given when not using percent\033[0m')
        if(self.values['startValue'] >= self.values['maxValue']):
            raise Exception('\033[91mValueError: argument \033[4mstartValue\033[0m\033[91m cant be greater than \033[4mmaxValue\033[0m\033[91m\033[0m')


    def setValue(self, newValue):
        progress = ''
        hashtags = ''
        minuses = ''
        title = self.values['title']
        doPrint = True

        if(self.values['inPercent']):
            if(newValue >= self.values['maxValue']):
                #color bar green when successfull
                progress = '100% ' + self.values['successMessage'] + ' \033[0m'
                title = '\033[92m' + title
                newValue = self.values['maxValue'] #prevent from overflowing the bar
            elif(newValue < 0):
                #clear line completely
                cl = ''
                for i in range(os.get_terminal_size()[0]):
                    cl += ' '
                print(cl, end='\r')
                #color bar red on error
                progress = self.values['errorMessage'] + ' \033[0m'
                title = '\033[91m' + title
                self.onError("Value for progress out of range")
                doPrint = False
            else:
                progress = str(newValue) + '%' #update the shown progress if acitvated
            
            for i in range(int(newValue / (100/self.values['lenOfBar']))):
                hashtags += self.values['filledChar']
            for i in range(self.values['lenOfBar'] - len(hashtags)):
                minuses += self.values['emptyChar']
        else:
            progress = str(newValue) + ' / ' + str(self.values['maxValue'])
            if(newValue >= self.values['maxValue']):
                #color bar green when successfull
                progress += ' ' + self.values['successMessage'] + ' \033[0m\n'
                title = '\033[92m' + title
            elif(newValue < 0):
                #clear line completely
                cl = ''
                for i in range(os.get_terminal_size()[0]):
                    cl += ' '
                print(cl, end='\r')
                #color bar red on error
                progress =  self.values['errorMessage'] + ' \033[0m'
                title = '\033[91m' + title
                self.onError('Value for progress out of range')
                doPrint = False
            for i in range(int(newValue / (self.values['maxValue']/self.values['lenOfBar']))):
                hashtags += self.values['filledChar']
            for i in range(self.values['lenOfBar']-int(newValue / (self.values['maxValue']/self.values['lenOfBar']))):
                minuses += self.values['emptyChar']
            
        #print updated progress
        if(doPrint):
            print(f'{title}[{hashtags}{minuses}] {progress}', end='\r')

    def update(self):
        self.values['value'] += self.values['steps']
        self.setValue(self.values['value'])

    def onError(self, *reason):
        minuses = ''
        for i in range(self.values['lenOfBar']):
            minuses += '-'
        a = self.values['errorMessage']
        b = self.values['title']
        print(f'\033[91m{a} {b}[{minuses}] Reason : {reason[0]}\033[0m')

    def reset(self):
        self.values['value'] = 0

    def start(self):
        print(str(self.values['title']) + '[]', end='\r')
        while self.values['value'] < self.values['maxValue']:
            self.update()
            time.sleep(self.values['sleepTime'])
        #self.setValue(-1) remove!!!!!
        print('')

    def getCurrentValue(self):
        return self.values['value']

    def getMaxValue(self):
        return self.values['maxValue']

class animation():
    def __init__(self, **kwargs):
        self.intervall = 0.1
        self.currentFrame = 0 #not changeable
        self.iterations = 100 #only used when calling self.start()
        self.anim = [' - ', ' \ ', ' | ', ' / ', ' - ', ' | ', ' / ']
        self.values = {'intervall':self.intervall, 'iterations':self.iterations, 'currentFrame':self.currentFrame, 'anim':self.anim}

        for element in kwargs:
            try:
                if(type(kwargs[element]) == type(self.values[element])):
                    self.values[element] = kwargs[element]
                else:
                    raise ValueError
            except KeyError as e:
                print(f'\033[91mKey Error: the parameter \033[4m{element}\033[0m\033[91m is not defined in class animation\033[0m')
            except ValueError as e:
                print(f'\033[91mType Error: the value of the parameter \033[4m{element}\033[0m is of type {type(element)} but it has to be of type {type(self.values[element])}\033[0m')
            except:
                print('\033[91munexpected error occured while processing the arguments\033[0m')
                raise
        
        tempArr = self.values['anim']
        tempHighest = 0
        for frame in tempArr:
            if(len(frame) > tempHighest):
                tempHighest = len(frame)
        for i in range(len(tempArr)):
            tempStr = ''
            for j in range(tempHighest-len(self.values['anim'][i])):
                tempStr += ' '
            self.values['anim'][i] = self.values['anim'][i] + tempStr
            
    
    def update(self, beforestring, afterstring):
        self.values['currentFrame'] += 1
        if(self.values['currentFrame'] > len(self.values['anim'])-1):
            self.values['currentFrame'] = 0
        tempString = str(self.values["anim"][self.values['currentFrame']])
        print(f'{beforestring}{tempString}{afterstring}', end='\r')

    def start(self, **kwargs):
        beforestring =''
        afterstring = ''
        for element in kwargs:
            if(element == "beforestring"):
                beforestring = kwargs[element]
            if(element == "afterstring"):
                afterstring = kwargs[afterstring]
        for i in range(self.values['iterations']):
            self.update(beforestring, afterstring)
            time.sleep(self.values['intervall'])
            #print(str(self.anim[self.currentFrame]), end='\r')
        print('')

def getBarParameters():
    a = {'inPercent':'boolean', 'showProgress':'boolean', 'title':'string', 'startValue':'integer', 'maxValue':'integer', 'lenOfBar':'integer', 'filledChar':'string/char', 'emptyChar':'string/char', 'steps':'integer', 'sleepTime':'float', 'successMessage':'string', 'errorMessage':'string'}
    print(a)