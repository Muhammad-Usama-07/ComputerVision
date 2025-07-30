# VideoCap_ClipExtract

## Run the project

Step # 01
  clone the repo, open cmd in projects's folder

Step # 02 (hit these command in cmd)

  pip install -r requirements.txt
  
  uvicorn api:app --reload
  
Step # 02

  it will open the fastapi's swagger with default address http://127.0.0.1:8000

## Task 01

  For task 01 i have made and endpoint i fastapi called "input_video", which take video file as input and save that video file in a folder, after that, it will extract caption from video's frame after every 2 second and the save the data with caption and it's corresponding timestamp of the video in a csv file

### Data extracted from video

![image](https://github.com/user-attachments/assets/d08c4c9e-5e9a-41de-b831-e08f3c475972)

## Task 02

  In task 02, made and endpoint i fastapi called "user_input", which take a sentence/text as input from the user, after that, it will match the user's query with the saved captions from csv file and than slice the video paths according to the timestamp of the captions and will return the detailed respose.
  
### Reponse of the endpoint

![image](https://github.com/user-attachments/assets/cac9f7d2-9c1e-4f0c-8aa4-6359322a8b83)

### Output after user's query

![image](https://github.com/user-attachments/assets/8fc597c5-09c3-48ea-b419-54880c178a8d)

## Project's Requirements

  OS: windows 10
  
  python version: 3.11.5


