from container import Container


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Get container
    cont = Container()
    # Set selected value as one not in the range
    select = 100
    while select != "0":  # While to repeat until termination
        print("Select:")
        print("0) Exit")
        print("1) Motion Vectors")
        print("2) Create New BBB Container")
        print("3) Broadcasting Standard")
        print("4) Subtitles")
        print("5) Create Non-Broadcast Standard Video for option 3) Debugging")
        select = input()

        # Input options
        if select == "0":
            break
        elif select == "1":
            cont.motion_vectors()
        elif select == "2":
            cont.bbb_container()
        elif select == "3":
            cont.broadcast_standards()
        elif select == "4":
            cont.insert_subtitles()
        elif select == "5":
            cont.non_standard_video()
        else:
            print("Not an option!")
