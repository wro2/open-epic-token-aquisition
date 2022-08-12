This is a sample python library that can be used by someone with a valid client ID to aquire an access token via the Epic EHR "Open Epic" system. I am not affiliated with Epic in any way and this is a personal project for learning purposes only. 

Open Epic is a set of healthcare FHIR APIs available to healthcare organizations. A full list of documentation can be found at the following location. Epic also has a FHIR sandbox that can be accessed using this method.

Open Epic Site and Documentation: https://fhir.epic.com/

Steps to use this repository:

1. Install all of the project requirements using pip (pip install requests and pip install jwt).

2. You will need an application regsitered with Open Epic. You can go to fhir.epic.com and sign up, and register an application. 
   At that point you should have a "Client ID" for your applicaiton. You can use the non-production client ID for the Epic Sandbox.

3. Generate a encryption keypair to be signed using a JWT. You can use Open SSL for this. Upload the public key to your Epic Applicaiton.
   Epic has instructions here: https://fhir.epic.com/Documentation?docId=oauth2&section=Creating-Key-Pair

4. Create a folder in the same directory as the main.py named "keys" and place the private key you crated in this directory in a .pem file. You can rename the .pem to privatekey or edit the python script to use your path.

5. Update the main.py with your client ID and the OAuth endpoint you are trying to aquire a token from. This can be found from the FHIR Metadata endpoint if you are not sure where to authorize.

6. Execute the script! If everything goes well you should have an access token printed out in your terminal / command window and you can use that as a Bearer token in Postman or similar tool to access the FHIR enpoints your application has scope for.


Good luck!
