'''
This code is able to add patient, search patient, delete patient
'''

import json
import pprint
import requests
from flask import Flask
import time

getMyEHR_url = "http://127.0.0.1:5000/"
hospital_base = "http://127.0.0.1:5052/"
patient_consent_server = "http://127.0.0.1:9001/"

def store_admission(patient_id, start_time, end_time, reason):
        # complete_url = Patient.url + "Patient?_format=json"
        complete_url = f"http://localhost:8000/fhir/Encounter"

        payload = {
        "resourceType": "Encounter",
        "id": "example",
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "period": {
            "start": start_time,
            "end": end_time
        },
        "reasonCode": [
            {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "123456",
                            "display": reason
                        }
                    ]
                }
            ]
        }

        headers = {'Content-Type': 'application/json'}

        try:
            # Post the Encounter data
            response = requests.post(complete_url, headers=headers, json=payload)
            print("Response status code:", response.status_code)
            if response.status_code == 201:
                response_json = response.json()
                
                print("Encounter ID:", response_json.get("id"))

                # encounter_id = response_json.get("id")
                # encounter_data_url = f"http://localhost:8000/fhir/Encounter/{encounter_id}?_format=json"
                # encounter_response = requests.get(encounter_data_url)

                # if encounter_response.status_code == 200:
                #     encounter_data = encounter_response.json()
                #     print("Encounter data:", encounter_data)
                return response_json.get("id")
            

            else:
                print("Error:", response.text)
                return "Error: " + response.text
        except Exception as e:
            print("Exception occurred while posting Encounter data:", e)
            return "Error: " + str(e)

def send_request(url, header):
    try:
        print("Sending this as header : ", header)
        response = requests.request("GET", url, headers=header)
        if response.status_code == 200:
            print("GET request successfully sent!")
            print("\nResponse:", response.text) # Here it recieves all the details
        else:
            print("Failed to send GET request. Status code:", response.status_code)
    except requests.RequestException as e:
        print("Error:", e)
        
def send_login_request(username, password):
    '''
    Sends the Username and password as POST request to the server
    '''
    url = getMyEHR_url + 'login'
    payload = {}
    headers = {
        'username': username,
        'password': password
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status_code in [200, 201]):
        return response.text
    else:
        return response
    
def store_in_json(name, hash):
    with open("hashes.json", "r") as file:
        data = json.load(file)
    
    data[hash] = name
    print("SSSSSSSSSSSSSSSSS : ", data)
    
    with open("hashes.json", "w") as file:
        json.dump(data, file)
    
    print(" ------- Data Added ------ ")

import hashlib

def generate_hash_id(first_name, last_name, dob):
    """
    Generates a unique hash ID based on the provided first name, last name, and date of birth.
    
    Args:
        first_name (str): The person's first name.
        last_name (str): The person's last name.
        dob (str): The person's date of birth in the format "DD-MM-YYYY".
    
    Returns:
        str: The generated hash ID.
    """
    # Split the date of birth into its components
    year, month = dob.split("-")
    
    # Concatenate the components in the desired order
    input_string = f"{first_name.lower()}{last_name.lower()}{month}{year}"
    
    # Compute the SHA-256 hash and return the hexadecimal string
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    # Print the length of the hash ID
    print(f"The length of the hash ID is: {len(hash_id)}")
    
    return hash_id


class Patient:
    
    # url = "http://hapi.fhir.org/baseR4/"
    url = "http://localhost:8080/fhir/"
    central_server = "http://127.0.0.1:5000/"
    
    def __init__(self, name, age, height, weight, mobile, birthdate):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.mobile = mobile
        self.birthdate = birthdate

    def store(self):
        '''
        Implement this using API calls
        '''
        complete_url = Patient.url + "Patient?_format=json"
        payload = json.dumps({
          "resourceType": "Patient",
          "id": "example-patient",
          "name": [
            {
              "use": "official",
              "given": [
                self.name
            ]
            }
        ],
        "telecom": [
            {
            "system": "phone",
            "value": str(self.mobile),
            "use": "mobile"
            }
        ],
        "height": {
            "value": self.height,
            "unit": "cm",
            "system": "http://unitsofmeasure.org",
            "code": "cm"
        },
        "weight": {
            "value": self.weight,
            "unit": "kg",
            "system": "http://unitsofmeasure.org",
            "code": "kg"
        },
        "birthDate": "2005-10"
        })
        headers = {
          'Content-Type': 'application/json'
        }
        print("Complete URL check : ",complete_url)
        
        response = requests.request("POST", complete_url, headers=headers, data=payload)
        if(response.status_code == 201):
            return response.json()["id"]
        else:
            return "Error There"

    @staticmethod
    def search(name):
        '''
        Implement this using APIs
        '''
        import requests
        complete_url = Patient.url + "Patient?given=" + name + "&_include=*&_count=5&_pretty=true"

        payload = {}
        headers = {}

        response = requests.request("GET", complete_url, headers=headers, data=payload)
        if(response.json()["total"] > 0):
            list_of_patients = response.json()["entry"]
            for each_patient in list_of_patients :
                pprint.pprint(each_patient["resource"])
        else:
            print("----- No Patient Exists -----")

    @staticmethod
    def delete(id2):
        '''
        Implement this using APIs
        '''
        p_id = id2

        complete_url = Patient.url + "Patient/" + str(p_id) +"?_pretty=true"
        payload = {}
        headers = {}

        response = requests.request("DELETE", complete_url, headers=headers, data=payload)
        if(response.status_code == 200):
            print("------ COMPLETED DELETION --------")
        else:
            print("----- ERROR : Please provide correct Fields ------")

    @staticmethod
    def enter_new_patient():
        # Function to enter details of a new patient
        print("Entering details for a new patient...")
        hospital = input("Enter the Hospital Name : ")
        f_name = input("Enter the First Name of the Patient : ")
        l_name = input("Enter the second name of the Patient : ")
        age = int(input("Enter the Age : "))
        height = int(input("Enter the Height : "))
        weight = int(input("Enter the Weight : "))
        mobile = int(input("Enter the Mobile Number : "))
        birthdate = input("Enter Your Date of Birth in YYYY-MM : ")
        option = input("Do you want to share information in future (yes/no): ")
        name = f_name + l_name
        consent_url = patient_consent_server + "share-consent?name="+name+"&hospital="+hospital
        print(consent_url)
        payload = {}
        headers = {}
        response = requests.request("GET", consent_url, headers=headers, data=payload)
        print("response from patient : ", response.text)

        consent_id = ""
        if(response.text != "permission not given" and option == 'yes'):
            consent_id = response.text
        hash_key = generate_hash_id(f_name, l_name, birthdate) + consent_id
        patient = Patient(name, age, height, weight, mobile, birthdate)
        id2 = patient.store()
        print("---------------------------------------------")
        store_in_json(name, hash_key)
        if id2:
            print("----- Data Stored Successfully -----")
            print("Your ID : ", id2)

    @staticmethod
    def view_patient():
        # Function to view details of a specific patient
        print("Viewing details of a patient...")
        name_to_search = input("Please enter the Name that you want to search : ")
        Patient.search(name_to_search)
        print("------- SEARCH COMPLETED --------")

    @staticmethod
    def delete_patient_record():
        # Function to delete a patient's record
        print("Deleting a patient's record...")
        id2 = int(input("Enter the ID of the Patient : "))
        Patient.delete(id2)

    @staticmethod
    def get_patient_details():
        print("For Now, You can only access patients admission details")
        print("Please Enter the Patient Details to get his information")
        f_name = input("Enter First Name of the Patient : ")
        l_name = input("Enter the Last name of the Patient : ")
        dob = input("Enter the Data of birth YYYY-MM : ")
        name = generate_hash_id(f_name, l_name, dob)
        id_of_patient = input("Enter the Hospital ID (Port) : ")
        username = input("Enter Hospital Username : ")
        token = input("Enter the token generated after Login : ")
        print("----------- Waiting for Patient Consent -------------")
        consent_id = "" # Need to send request to the Patient Consent for retrieve
        consent_url = patient_consent_server + "retrive-consent?name="+f_name+l_name+"&hospital="+username
        payload = {}
        headers = {
          'username': 'susheelkrishna',
          'password': 'Doraemon',
          'Authorization': 'Bearer ddfdnjfhjfkd'
        }
        response = requests.request("GET", consent_url, headers=headers, data=payload)
        if(response.text != "permission not given"):
            consent_id = response.text

        name += consent_id
        params = {
        'patient': {name},
        'id': {id_of_patient},  # Assuming this is the hospital ID
        'username' : {username},
        'access_token' : {token}
        }
        response = requests.get(f"{Patient.central_server}/get-details", params=params)
        if response.status_code == 200:
            data = response.text
            print("Response from server:")
            print(data)
        else:
            print("Error:", response.status_code)
            
    @staticmethod
    def register_to_server():
        username = input("Enter the Username : ")
        password = input("Enter the password : ")
        port = input("Enter the IP address of hospital : ")
        
        url = "http://127.0.0.1:5000/register?username="+username+"&password="+password+"&port="+port
        print("Sending to URL : ", url)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        
    @staticmethod
    def Login_to_server():
        '''
        This Function sends post request to the getMyEHR server.
        Finally, it recieves the Message whether the Login is Succeeded
        '''
        print("-------- You are Now LOGGING IN -------")
        username = input("Enter the Username : ")
        password = input("Enter the Password : ")
        response = send_login_request(username, password)
        print("--------Response : Access_Token : {} --------", response)

    @staticmethod
    def add_admission():
        reason = input("Enter the reason : ")
        start_time = input("Enter the Start Time : ")
        end_time = input("Enter the End time : ")
        diet_preference = input("Enter the Diet preference : ")
        patient_id = input("Enter the Patient id : ")
        print("Will be implemented in future")

    @staticmethod
    def switch_case(option):
        # Switch case function to execute different actions based on user input
        switcher = {
            1: Patient.enter_new_patient,
            2: Patient.view_patient,
            3: Patient.delete_patient_record,
            4: Patient.get_patient_details,
            5: Patient.register_to_server,
            6: Patient.Login_to_server,
            7: Patient.add_admission
        }
        # Get the function corresponding to the user's input option
        selected_function = switcher.get(option, lambda: print("Invalid option"))
        # Execute the selected function
        selected_function()

options = int(input("""
Choose an Option from below :
1) Enter New Patient
2) View Patient in Local Server
3) Delete Patient Record
4) Get Details of the patient from other hospitals
5) Register my hospital to GetMyEHR
6) Login to getMyEHR
7) Add Admission Details

"""))

Patient.switch_case(options)
