from flask import Flask, request, send_file, jsonify
import face_recognition
import pandas as pd
import os

# existing_data =  pd.read_csv('face_embeddings.csv')

app = Flask(__name__)

@app.route('/generate_embeddings', methods=['POST'])
def generate_embeddings():
    
    global existing_data
    ###### Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'})
    if 'id' not in request.form:
        return jsonify({'error': 'No employee ID found'})

    ###### get file and id
    file = request.files['file']
    emp_id = request.form['id']
    emp_id_to_check = int(emp_id)
    emp_id_exists = None
    
    ###### Check if the file has a valid content type (MIME type)
    if not file or not file.content_type.startswith('image/'):
        return jsonify({'error': 'Invalid image file'})

    CSV_FILE_PATH = 'face_embeddings.csv'
    # Check if the CSV file exists
    if os.path.isfile(CSV_FILE_PATH):
        # If the file exists, load existing data from the CSV file
        existing_data = pd.read_csv(CSV_FILE_PATH)
        ###### Check if emp_id_to_check exists in the DataFrame
        emp_id_exists = emp_id_to_check in existing_data['emp_id'].values
        print('checking ************', emp_id_exists,emp_id_to_check )
        print('checking ***********',  type(existing_data['emp_id'].values[0]))
        print('checking ***********',  type(emp_id_to_check))
    
    else:
        # If the file doesn't exist, create a new DataFrame with columns 'emp_id' and 'Embedding'
        existing_data = pd.DataFrame(columns=['emp_id', 'Embedding'])
    
    
    ###### if ID Exists 
    if emp_id_exists:
        print(f"emp_id {emp_id_to_check} exists in the DataFrame.")
        return jsonify({'status': 'error', 'message': f"emp_id {emp_id_to_check} already exists"})

    ###### if ID Not Exists 
    else:
        print(f"emp_id {emp_id_to_check} does not exist in the DataFrame.")
        

        ###### Detection Face and make embeddings
        try:
            # Load the image with faces
            image = face_recognition.load_image_file(file)
    
            # Find all face locations in the image
            face_locations = face_recognition.face_locations(image)
    
            # Check if at least one face is found in the image
            if len(face_locations) > 0:
                # Compute face embeddings for all detected faces
                face_encodings = face_recognition.face_encodings(image, face_locations)
    
                # Convert the face embeddings to a list of strings
                face_encodings_str = [", ".join(map(str, encoding)) for encoding in face_encodings]
                # Append the new embeddings to the existing data
                # new_embeddings = [{"emp_id": emp_id, "Embedding": encoding} for i, encoding in enumerate(face_encodings_str)]
                # print(new_embeddings)
                existing_data = pd.concat([existing_data, pd.DataFrame([{"emp_id": emp_id, "Embedding": encoding} 
                                                                        for i, encoding in enumerate(face_encodings_str)])], ignore_index=True)
    
                # Save the updated embeddings back to the CSV file
                existing_data.to_csv(CSV_FILE_PATH, index=False)
    
                return jsonify({
                    'status': 'success', 
                    'message': f'Embeddings of Employee id {emp_id} added and saved successfully.'})
    
            else:
                return jsonify({'status': 'error', 'message': 'No faces found in the image.'})
        
        
        ###### When getting error in Face Detection and embeddings making
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})


@app.route('/upload', methods=['POST'])
def upload_file():
    global existing_data
    
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    ###### Check if the file has a valid content type (MIME type)
    if not file or not file.content_type.startswith('image/'):
        return jsonify({'error': 'Invalid image file'})

    # # Save the uploaded image to a temporary directory
    # # You can customize the path where you want to save it
    # file.save('uploaded_image.jpg')

    # Load the image you want to match
    incoming_image = face_recognition.load_image_file(file)
    incoming_embedding = face_recognition.face_encodings(incoming_image)
    
    # Check if a face embedding was computed for the incoming image
    if len(incoming_embedding) > 0:
        incoming_embedding = incoming_embedding[0]  # Take the first (and likely only) embedding
        CSV_FILE_PATH = 'face_embeddings.csv'
        # Check if the CSV file exists
        if os.path.isfile(CSV_FILE_PATH):
            # If the file exists, load existing data from the CSV file
            existing_data = pd.read_csv(CSV_FILE_PATH)
            # Iterate through the existing data and compare embeddings
            match_found = False
            matched_employee_id = None
            for idx, row in existing_data.iterrows():
                existing_embedding = eval(row['Embedding'])  # Convert the string back to a list

                # Compare the embeddings using face_recognition's compare_faces
                results = face_recognition.compare_faces([existing_embedding], incoming_embedding)
                if results[0]:
                    match_found = True
                    matched_employee_id = row['emp_id']  # Store the matched employee ID
                    break

            if match_found:
                print('************* Face Matched')
                response_data = {
                    'match_status': 'image matched',
                    'success': True
                }
                    
            else:
                print('************* Face Not Matched')
                response_data = {
                    'match_status': 'image not match',
                    'success': False
                }
        else:
            print('************* file does not exist')
            response_data = {
                    'match_status': 'file does not exist',
                    'success': False
                }

    else:
        response_data = {'error': 'No face detected in the incoming image.'}

    return jsonify(response_data)



if __name__ == '__main__':
    app.run()
