import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import random

def initialize_firestore():
    """
    Create database connection
    """
    # Setup Google Cloud Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cs246-db-project-firebase-adminsdk-7clw1-06397866ff.json"

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'cs246-db-project',
    })

    # Get reference to database
    db = firestore.client()
    return db

def find_employee(db, id):
   """
   Finding the employee information in the database
   """
   result = db.collection("Employees").document(id).get()
   if result.exists:
      empInfo = result.to_dict()
      return empInfo
   else:
      return None

def update_emp(db, id, hoursTrained, trainedStatus):
   """
   Create or update an employee
   """
   trainingInfo = {"Hours Trained" : hoursTrained,
                   "Training Completed" : trainedStatus}

   db.collection("Employees").document(id).set(trainingInfo)

def delete_emp(db, id):
   """
   Delete a player
   """
   db.collection("Employees").document(id).delete()

def main():
   db = initialize_firestore()

   print()
   emp_id = input("Please enter employee id: ")

   quit_program = False
   while not quit_program:
      hours = find_employee(db, emp_id)
      empHoursTrained = hours["Hours Trained"]
      empCompletedTraining = hours["Training Completed"]
      print()
      print("Select Option:")
      print("t -- Add hours trained\n"
            "u -- Update training status\n"
            "c -- Check hours trained\n"
            "s -- Check training status\n"
            "a -- Add employee\n"
            "d -- Delete employee\n"
            "e -- Exit\n")
      option = input(">>> ")
      if option == "t":
         trainingHours = int(input("Hours to add: "))
         trainingHours += empHoursTrained
         update_emp(db, emp_id, trainingHours, empCompletedTraining)
      elif option == "u":
         isTrained = input("Is training complete? (y/n): ")
         if isTrained == "y":
            update_emp(db, emp_id, empHoursTrained, True)
         else:
            update_emp(db, emp_id, empHoursTrained, False)
      elif option == "c":
         print("Hours Trained: {}".format(empHoursTrained))
      elif option == "s":
         print("Training Complete? {}".format(empCompletedTraining))
      elif option == "a":
         newID = input("What is the new employee ID? ")
         update_emp(db, newID, 0, False)
      elif option == "d":
         delete_emp(db, emp_id)
         print("Employee {} deleted".format(emp_id))
         quit_program = True
      elif option == "e":
         quit_program = True

if __name__ == "__main__":
   main()