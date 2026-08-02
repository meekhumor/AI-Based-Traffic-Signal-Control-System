1. netedit [Make network file]
2. `python randomTrips.py -n intersection.net.xml -r intersection.rou.xml` [Make route file]
3. Change the path in `intersection.sumocfg`
4. `sumo-gui -c intersection.sumocfg` [Run the simulation]
5. `python train.py --train -e 50 -m model_name -s 500` [Train the network]
6. `python train.py -m model_name -s 500` [Run the trained model]

7. `netconvert --osm-files king_circle.osm -o king_circle.net.xml`


SUMO → DQN → ONNX → OpenVINO.

`ovc traffic_light_dqn.onnx --output_model optimized_model/traffic_light_dqn --input "input[1,6]"`