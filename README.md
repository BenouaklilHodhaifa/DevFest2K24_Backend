# Factory 86 Backend
This Django based backend is in charge of the data needs for the Factory 86 factory management application.
The repository structure is as follows:
- DevFest2k24_Backend/ : is the default folder created with the Django project. Its most important files are :
  - settings.py : sets the global settings of the project
  - urls.py : which acts a main url dispatcher, currently redirects all urls to the main/ app.
- main/ : is the main and single app of the Django project, the most important files and folders are :
  - models.py : defines the models that interface with the database tables such as StampingPress, PaintingRobot or AGV which all inherit form django.models.Model.
  - serializers.py : defines the class based serializers inherited from Django Rest Framework ModelSerializer. They allow to convert back and forth between complex Django Model instances and native python datatypes.
  - urls.py : which is the local url dispatcher for the main/ app. It contains the urls of the different endpoints and links them to the appropriate views.
  - views/ : this folder contains the views that will handle the requests. The views are separated into different python files according to their concerns :
    - sensors_loading.py : contains views that receive the POST requests from the sensors in order to load their data into the database. Each type of sensor has a dedicted view.
    - sensors_uploading.py : currently contains one view responsible for providing the logged sensors data to the front end.
    - account.py : contains the views responsible for managing account related operations such as account listing.
    - notification.py : for now only contains the view for retrieving the logged notifications in the database. The notifications are also sent in real time.
    - task.py : contains views in charge of the automatic task management logic such as getting a list of the (automatically) created tasks and changing tasks status to in progress or done.
    - team.py : these views handle the operator teams logic.
