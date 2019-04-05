import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2
import face_recognition
import numpy


def main():
    
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        container = av.open(drone.get_video_stream())

        process_this_frame = True
        face_locations = []

        while True:
            for frame in container.decode(video=0):

                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                small_frame = cv2.resize(numpy.array(frame.to_image()), (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                if process_this_frame:
                    face_locations = face_recognition.face_locations(rgb_small_frame)

                process_this_frame = not process_this_frame

                for (top,right,bottom, left) in face_locations:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2. imshow("Faces", image)

            if cv2.waitKey(1)&0xFF == ord('q'):
                break

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

