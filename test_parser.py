from parser import Parser

if __name__ == "__main__":
    parser = Parser("file.txt")
    parser.parse()
    print("###parsing nb_drones:####")
    print(parser.nb_drones)
    print("###parsing zones :####")
    for z in parser.zones.values():
        print(z)
    
    print("###parsing connection:####")
    
    for c in parser.connections :
        print(c)
