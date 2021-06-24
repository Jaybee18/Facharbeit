from NeuralNetwork import NeuralNetwork
from Nebenskripte.visualize_w_nn import visualize
import sys
import ast

def getNNArchitecture(nn):
    print("=================")
    print("Hidden:")
    for layer in range( len( nn.hidden ) ):
        print(f"\nLayer {layer}:")
        for neuron in range(nn.hidden[layer].getTotalNumberOfNeurons()):
            print(f"\nNeuron {neuron}")
            for weight in range(nn.hidden[layer].getNeruonAtIndex(neuron).getTotalNumberOfWeights()):
                print(f"Weight {weight} : {nn.hidden[layer].getNeruonAtIndex(neuron).getWeightAtIndex(weight)}")
    print("\nOutput:")
    for neuron in range(nn.outputlayer.getTotalNumberOfNeurons()):
        print(f"\nNeuron {neuron}")
        for weight in range(nn.outputlayer.getNeruonAtIndex(neuron).getTotalNumberOfWeights()):
            print(f"Weight {weight} : {nn.outputlayer.getNeruonAtIndex(neuron).getWeightAtIndex(weight)}")
    print("=================")

if __name__ == '__main__':
    arguments_list = [ sys.argv[i] for i in range( len( sys.argv ) ) ][1:]
    neurons_input = None    # -e 2
    neurons_hidden = None   # -h [3, 2, 2]
    neurons_output = None   # -o 1
    iterations = 100_000    # -i 100000
    learningrate = 0.5      # -l 0.5
    showArchitecture = True # -a True
    networkConsole = True   # -n True
    live_visualization=False# -f True

    OS = 20 # console command offset
    try:
        for i in range(0, len(arguments_list), 2):
            if arguments_list[i] == "-e":
                neurons_input = int(arguments_list[i+1])
            elif arguments_list[i] == "-h":
                neurons_hidden = ast.literal_eval(arguments_list[i+1])
            elif arguments_list[i] == "-o":
                neurons_output = int(arguments_list[i+1])
            elif arguments_list[i] == "-i":
                iterations = int(arguments_list[i+1])
            elif arguments_list[i] == "-l":
                learningrate = float(arguments_list[i+1])
            elif arguments_list[i] == "-a":
                showArchitecture = arguments_list[i+1].lower() == "true"
            elif arguments_list[i] == "-n":
                networkConsole = arguments_list[i+1].lower() == "true"
            elif arguments_list[i] == "-f":
                live_visualization = arguments_list[i+1].lower() == "true"
            elif arguments_list[i] == "--h":
                print("neuralNetworkFromConsole.py [-e <integer>] [-h <list>] [-o <integer>] [-i <integer>] [-l <float>] [-a <boolean>] [-n <boolean>] [-f <boolean>] [--h]\n")
                print( "-e <integer>".ljust( OS, ' ' ) + "specifies the number of input neurons [REQUIRED]\n" )
                print( "-h <list>".ljust( OS, ' ' ) + "specifies the number of hidden layers and the number of neurons in each hidden layer [REQUIRED]" )
                print( " " * OS + "parameter must be formatted like this:")
                print( " " * OS + "[number_of_neurons_in_first_hidden_layer,...,number_of_neurons_in_N_hidden_layer]")
                print( " " * OS + "!! without spaces in between the characters !!\n")
                print( "-o <integer>".ljust( OS, ' ' ) + "specifies the number of output neurons [REQUIRED]\n" )
                print( "-i <integer>".ljust( OS, ' ' ) + "specifies the number of training iterations" )
                print( " " * OS + f"the default value is {iterations}\n")
                print( "-l <float>".ljust( OS, ' ' ) + "specifies the learningrate" )
                print( " " * OS + f"the default value is {learningrate}\n")
                print( "-a <boolean>".ljust( OS, ' ' ) + "specifies whether or not the network architecture should be printed" )
                print( " " * OS + "the parameter has to either be True or False")
                print( " " * OS + f"the default value is {showArchitecture}\n")
                print( "-n <boolean>".ljust( OS, ' ' ) + "specifies whether or not the network console should be available" )
                print( " " * OS + "after the network is done training")
                print( " " * OS + f"the default value is {networkConsole}\n")
                print( "-f <boolean>".ljust( OS, ' ' ) + "specifies whether or not the live visualization should be enabled" )
                print( " " * OS + "!! this will impact the performance while training !!" )
                print( " " * OS + f"the default value is {live_visualization}\n" )
                print( "--h".ljust( OS, ' ' ) + "shows this help menu" )
                exit()
    except Exception:
        pass

    if neurons_input is None or neurons_hidden is None or neurons_output is None:
        print("[ERROR] You have to specify the parameters -e, -h and -o\n[ERROR] Or type --h for help")
        exit()

    training_input = ast.literal_eval(input("Training inputs: "))
    training_output = ast.literal_eval(input("Training outputs: "))

    n = NeuralNetwork(neurons_input, neurons_hidden, neurons_output)
    print("[INFO] Neural Network Created!")
    if showArchitecture:
        getNNArchitecture(n)
    print(f"[INFO] Training Started for {iterations} iterations!")
    n.train(training_input, training_output, iterations=iterations, learningrate=learningrate, live_visualization=live_visualization)
    print("[INFO] Training finished!")
    print("=================")
    print("Results:")
    for i in range(len(training_input)):
        print(f"\nTraining input  : {training_input[i]}")
        print(f"Expected Output : {training_output[i]}")
        actual_output = n.predict(training_input[i])
        print(f"Actual Output   : {actual_output}")
        print(f"Error           : {sum([0.5*((training_output[i][j] - actual_output[j]))**2 for j in range(len(actual_output))])}")

    OS = 27 # network console command offset
    if networkConsole:
        print( "=================" )
        print( "Network Console" )
        while True:
            command = input(">>> ").split(' ')
            if len( command ) > 3:
                print("[ERROR] Please make sure not to use spaces inside parameters!")
                continue
            if command[0] == "help":
                print("getWeights".ljust(OS, ' ') + "outputs all weights of the network")
                print(" "*OS + "sorted by   layers left to right")
                print(" "*OS + "            neurons top to bottom")
                print(" "*OS + "            weights top to bottom\n")
                print("getBiasWeights".ljust(OS, ' ') + "outputs all bias weights of the network")
                print(" "*OS + "sorted by   layers left to right")
                print(" "*OS + "            neurons top to bottom\n")
                print("predict [inputs]".ljust(OS, ' ') + "outputs the networks prediction for the given inputs")
                print(" "*OS + "inputs must be formatted like this:")
                print(" "*OS + "[[input_1,...,input_N],...,input_batch_M]")
                print(" "*OS + "!! without spaces in between the characters !!\n")
                print( "visualize [fade]".ljust( OS, ' ' ) + "visualizes the networks prediction for the input range of 0-1" )
                print( " " * OS + "only works with networks that have two input neurons" )
                print( " " * OS + "'fade' enables fade on the visualization (True/False)\n" )
                print("exit".ljust(OS, ' ') + "exits the network console")
                print(" "*OS + "!! you won't be able to access the network anymore !!\n")
                print("help".ljust(OS, ' ') + "shows this help menu")
            elif command[0] == "predict":
                inputs = ast.literal_eval(command[1])
                output = n.predict(inputs)
                print(f"Output : {output}")
            elif command[0] == "visualize":
                try:
                    fade = command[1].lower() == "true"
                    visualize(n, fade)
                except IndexError:
                    print("fade parameter has to be specified and either true or false")
            elif command[0] == "getWeights":
                print(n.getWeights())
            elif command[0] == "getBiasWeights":
                print(n.getBiasWeights())
            elif command[0] == "exit":
                break