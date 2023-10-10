# Evolution Sim
## Inspired by [this](https://www.youtube.com/watch?v=N3tRFayqVtk&ab_channel=davidrandallmiller) youtube video

## General Architecture:

### Classes/Objects:

Indents imply inheritence
- Neuron
    - Input Neuron
        - All subclasses contain float from 0 to 1 that corresponds to their function
        - Shouldn't need different types of input neurons, all they do is store data that is fed to them
        - Types:
            - Age
            - Random Input
            - Distance from north or south border
            - Distance from E/W border
            - Y position in world
            - X position in world
    - Output Neuron
        - Take in list of inputs from connections and return a value from -1 to 1 
        indicating the probability that the output is triggered
        - Calculation is tanh(sum(inputs))
        - Types:
            - Move Forward (Same direction as previous step)
            - Move in x plane
            - Move in y plane
            - Move random direction
    - Internal Neuron
        - Take in list of inputs from connections and return a value from -1 to 1 
        indicating the probability that the output is triggered
        - Calculation is tanh(sum(inputs))
- World
    - Takes in x and y dimensions
- Genome
    - Contains list of Genes
- Gene
    - Stored as 8 hex digits in the video, maybe not necessary in OOP architecture
    - Contains:
        - Input: Input Neuron or Internal Neuron
        - Output: Output Neuron or Internal Neuron
        - Weight: Float from -4 to 4
- Individual
    - Takes in a genome
    - Contains all input/output neuron types + specified num of internal neurons
        - Maybe it doesn't do this and just creates instances of each needed type from genome?
- Sim Controller
- Sim Creator

### Notes:
- TODO: Figure out bit manipulation in individual for decoding hex string
- Internal neurons can feed into themselves, when they do, the value they use as 
input is the value they generated during the previous step
- Remove all connections to neurons that don't have a connection out