import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'x264' doesn't work
out = cv2.VideoWriter('test1.mp4',fourcc, 8.0, size)  # 'False' for 1-ch instead of 3-ch for color


flag = cv2.imread('flag2.jpg')
def put_flag(flag, fc, x, y, w, h):
    flag_width = w
    flag_height = h

    img_width = flag_width + 1
    img_height = int(0.50 * flag_height) + 1

    flag = cv2.resize(flag, (img_width, img_height))

    for i in range(img_height):
        for j in range(img_width):
            for k in range(3):
                if flag[i][j][k] < 235:
                    fc[y + i - int(-0.20 * flag_height)][x + j][k] = flag[i][j][k]
    return fc

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw= mp.solutions.drawing_utils



while True:
    success, img = cap.read()
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx,cy), 7, (255,0,255), cv2.FILLED)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            img = put_flag(flag,img,100,100,150,150)
            cv2.putText(img, "Happy Independence Day!", (30,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)


    cv2.imshow("Image", img)
    out.write(img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    cv2.waitKey(1)