import cv2
import dlib
import numpy as np
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input
import sys
import argparse

# Load mô hình đã huấn luyện
model_path = 'D:\\Py for data science\\final project\\autism\\realtime\\efficientNetB3_300_300_50.h5'
model = load_model(model_path)

# Tạo một bộ nhận diện khuôn mặt từ dlib
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("D:\\Py for data science\\final project\\autism\\realtime\\shape_predictor_81_face_landmarks (1).dat")



def predict_on_image(image_path):
 
    image = cv2.imread(image_path)
    faces = detector(image)

    for face in faces:
        # Tiền xử lý frame
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        cropped_face = image[y:y+h, x:x+w]

        resized_frame = cv2.resize(cropped_face, (300, 300))
        img = preprocess_input(resized_frame)
        img = np.expand_dims(img, axis=0)

        # Dự đoán
        prediction = model.predict(img)

        # Lấy chỉ số của giá trị lớn nhất
        CLASS_NAMES = ["Autistic", "Non_Autistic"]
        predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
        confidence = np.max(prediction[0])



        message = f'Result: {predicted_class} (Confidence: {confidence*100:.2f}%)'
        print(message)

        cv2.namedWindow('Autism Detection', cv2.WINDOW_AUTOSIZE)
        # Hiển thị kết quả trực tiếp lên ảnh
        text_position = (image.shape[1] - 200, 30)  # Đặt tọa độ x và y
        result_text = f'{predicted_class}: {confidence*100:.2f}%'
        cv2.putText(image, result_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Hiển thị hình ảnh
        cv2.imshow('Autism Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def predict_on_webcam():
    # Kết nối với camera hoặc webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()

        # Tìm khuôn mặt trong frame
        faces = detector(frame)

        for face in faces:
            # Tiền xử lý frame
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            cropped_face = frame[y:y+h, x:x+w]


            resized_frame = cv2.resize(cropped_face, (300, 300))
            img = preprocess_input(resized_frame)
            img = np.expand_dims(img, axis=0)

            # Dự đoán
            prediction = model.predict(img)
   
            
            CLASS_NAMES = ["Autistic", "Non_Autistic"]
            predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
            confidence = np.max(prediction[0])

        

            landmarks = landmark_predictor(frame, face)

            # Hiển thị "TEST AUTISM" ở giữa frame phía góc trái
            cv2.putText(frame, 'TEST AUTISM', (10, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), 1, cv2.LINE_AA)

            result_text = f'{predicted_class}: {confidence*100:.2f}%'
            cv2.putText(frame, result_text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 1, cv2.LINE_AA)

            
            # Vẽ các điểm landmark trên ảnh
            for i in range(81):
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

            # Nối các điểm trên mặt
            for i in range(81 - 1):
                x1, y1 = landmarks.part(i).x, landmarks.part(i).y
                x2, y2 = landmarks.part(i+1).x, landmarks.part(i+1).y
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
            
            # Tạo thông báo dựa trên kết quả
            message = "Ban hay nhanh chong den bac si kiem tra!" if np.argmax(prediction[0]) == 0 else "Xin chuc mung ban khong mac benh"

            # Hiển thị thông báo phía dưới
            cv2.putText(frame, message, (10, frame.shape[0] - 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 255), 1, cv2.LINE_AA)

        # Hiển thị frame
        cv2.imshow('Realtime Autism Detection', frame)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()



def main():
    parser = argparse.ArgumentParser(description='Autism Detection')
    parser.add_argument('--image', help='Path to the image file for prediction')
    args = parser.parse_args()

    if args.image:
        predict_on_image(args.image)
    else:
        predict_on_webcam()

if __name__ == "__main__":
    main()