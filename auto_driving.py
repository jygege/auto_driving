from collections import deque
import sys
class auto_driving:

    def __init__(self):
            self.x = 0
            self.y = 0
    def direction(self, direct, command):
            if (direct, command) in [("N",  "L"),("S", "R")]:
                return "W"
            elif (direct, command)  in [("N",  "R"),("S", "L")]:
                return "E"
            elif (direct, command)  in [("W",  "R"),("E", "L")]:
                return "N"
            elif (direct, command)  in [("W",  "L"),("E", "R")]:
                return "S"
            
            
    def parse_commands(self, direct, commands):
            new_com = []
            while commands:
                command = commands.popleft()
                if command == "F":
                    new_com.append(direct)
                else:
                    direct = self.direction(direct, command)
                    
            return new_com, direct
        
    def simulation_single(self, car, px, py, direct, commands):
            new_com, direct = self.parse_commands(direct, commands)

            for com in new_com:
                if com == "N" and py < self.y-1:
                    py += 1
                if com == "S" and py > 0:
                    py -= 1
                if com == "W" and px > 0:
                    px -= 1
                if com == "E" and px < self.x-1:
                    px += 1



            return car, (px, py), direct
    
    def simulation_multiple(self, input_lists):
            #input_lists = [[car,x, y, direct, commands, step]]
            num_car = len(input_lists)
            cur_car_pos = {} #car posiitons in current step
            car_direct = {} # car: postition pair
            end_pos = [] # car positons at end of 
            collision = [] #collision car information
            colli_pos = [] #coordination of collisoon
            crashed_cars = {} # list of cars already crushed.
            #store inputs in deque(input-lists)
            while input_lists:
                for i in range(num_car):
                    _input = input_lists.popleft()
                    car, x, y, direct, commands, step = _input

                    if car in crashed_cars:
                        continue

                    elif commands:
                        command = commands.popleft()
                        card, (x, y), direct = self.simulation_single(car, x, y, direct, deque(command))
                        car_direct[car] = direct
                        if (x,y,step+1) not in cur_car_pos and (x, y) not in colli_pos:
                            cur_car_pos[(x,y,step+1)] = car
                            input_lists.append([car, x, y, direct, commands, step+1])
                        else:
                            colli_pos.append((x, y))
                            collision.append([car, x, y, direct, step+1])
                            collision.append([cur_car_pos[(x,y,step+1)], x, y, car_direct[cur_car_pos[(x,y,step+1)]], step+1])
                            crashed_cars[car] = cur_car_pos[(x,y,step+1)]
                            crashed_cars[cur_car_pos[(x,y,step+1)]] = car
                            num_car -= 1

                    else: #simulation completed
                        end_pos.append([car, x, y, direct, step])

                cur_car_pos = {} #reset car_pos at each step
                num_car = len(input_lists)    
                

            return collision , end_pos ,crashed_cars
        
    def main(self):
        field_input = input("""Welcome to Auto Driving Car Simulation!
        Please enter the width and height of the simulation field in x y format:
        
        """)
        self.x, self.y = map(int, field_input.split())
        if self.x >0 and self.y > 0:
            print("You have created a field of {} x {}".format(self.x, self.y))
        else:
            self.main()

        input_lists = deque()
        
        while True:
            option = int(input( """Please choose from the following options:
            1.Add a car to field
            2.Run simulation """))
            if option == 1:
                car_name = input("Please enter nam of the car: ")
                car_pos = input("Please enter the initial position of the car {} in x y Direction format: ".format(car_name))
                x, y , direct = map(str, car_pos.split())
                commands = deque(input("Please enter the commands for car {}:".format(car_name)))
                input_lists.append([car_name, int(x), int(y), direct, commands, 0])

                print("Your current list of cars are:")
                for inputs in input_lists :
                    print(inputs)

        
            elif option == 2:
                collision , end_pos, crashed_cars = self.simulation_multiple(input_lists)
                print("After simulation, the result is:")
                for col_car in collision:
                    car, x, y, direct, step = col_car
                    print("- {}, collides with {} at ({},{}) at step {}".format(car, crashed_cars[car], x,y, step))
                    
                for finished_car in end_pos:
                    car, x, y, direct, step = finished_car
                    print("- {}, ({},{}) {} at step {}".format(car, x, y, direct, step))
                
                option2 = int(input( """
                Please choose from the following options:
                1.Start over
                2.Exit """))
                
                if option2 == 1:
                    self.main()
                else:
                    break

            else:
                option = int(input( """
                Please choose from the following options:
                1.Add a car to field
                2.Run simulation """))
            
        
        sys.exit()
        
        
run = auto_driving()
run.main()