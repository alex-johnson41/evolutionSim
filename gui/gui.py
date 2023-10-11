import tkinter as tk
from sim.sim_controller import SimController


class MainWindow():

    def __init__(self, master: tk.Tk):
        self.master = master
        frame_input = tk.Frame(master, height=400, width=400)
        frame_world = tk.Frame(master)
        master.config(background="gray")
        master.geometry("800x500")
        master.title("Neural Network Evolution Simulator")
        input_world_x_size = tk.Entry(frame_input)
        input_world_y_size = tk.Entry(frame_input)
        input_population = tk.Entry(frame_input)
        input_generation_steps = tk.Entry(frame_input)
        input_genome_length = tk.Entry(frame_input)
        input_internal_neurons = tk.Entry(frame_input)

        input_world_x_size.grid(row=0, column=1)
        input_world_y_size.grid(row=1, column=1)
        input_population.grid(row=2, column=1)
        input_generation_steps.grid(row=3, column=1)
        input_genome_length.grid(row=4, column=1)
        input_internal_neurons.grid(row=5, column=1)

        label_world_x_size = tk.Label(
            frame_input,
            text="World x size",
        )
        label_world_y_size = tk.Label(
            frame_input,
            text="World y size",
        )
        label_population = tk.Label(
            frame_input,
            text="Population",
        )
        label_generation_steps = tk.Label(
            frame_input,
            text="Steps per generation",
        )
        label_genome_length = tk.Label(
            frame_input,
            text="Genome length",
        )
        label_internal_neurons = tk.Label(
            frame_input,
            text="Internal Neurons",
        )
        enter_button = tk.Button(
            frame_input,
            text="Run Simulation",
            command=self.run_simulation,
        )
        enter_button.grid(row=6, column = 1)

        label_world_x_size.grid(row=0, column=0)
        label_world_y_size.grid(row=1, column=0)
        label_population.grid(row=2, column=0)
        label_generation_steps.grid(row=3, column=0)
        label_genome_length.grid(row=4, column=0)
        label_internal_neurons.grid(row=5, column=0)
    
        lbl_title = tk.Label(
            text="Neural Network Evolution Simulator", 
            font=("Ariel", 40),
            background="gray",
            ) 
        lbl_title.grid(row=0, columnspan=2, pady=20)

        frame_world.grid(row=1, column=0, columnspan=2)
        frame_input.grid(row=1, column=1)
    
    def run_simulation(self):
        pass
        
root = tk.Tk()
root.title("window")
MainWindow(root)
root.mainloop()