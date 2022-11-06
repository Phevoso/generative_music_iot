import argparse

def parse_args():

    parser = argparse.ArgumentParser(description='Type the I.P of the MQTT server.') 

    parser.add_argument( '-i', '--ip_adress', type=str, help='The I.P of the MQTT server.', required=True)
    parser.add_argument('-c', '--client_name', type=str, help="Pass the client's name.")
    parser.add_argument('-t', '--topic', type=str, help="MQTT topic to publish the data.")
    parser.add_argument('-u', '--username', type=str, help="Type the MQTT username.")
    parser.add_argument('-p', '--password', type=str, help="Type the MQTT password.")
    parser.add_argument('-m' '--mongo_client_key', type=str, help="Insert the MongoDB client key")

    args = parser.parse_args()
    return args