#!/bin/bash

# Run command 1 in a new terminal window
# gnome-terminal -- sudo docker run -p 8080:8080 hapiproject/hapi:latest &

# Run command 2 in a new terminal window
gnome-terminal -- python3 central_server.py &

# Run command 3 in a new terminal window
gnome-terminal -- python3 hos_b_server.py &

# Run command 4 in a new terminal window
gnome-terminal -- python3 hospital_a.py &