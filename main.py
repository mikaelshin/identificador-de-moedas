import cv2
import numpy as np

# Medida das moedas em milimetros
diametro1Real = 27        # identificar pelas duas cores
diametro50Centavos = 23   # identificar pela cor 
diametro25Centavos = 25   # identificar pelo raio
diametro10Centavos = 20   # identificar pela raio
diametro5Centavos = 22    # identificar pela raio

# Definindo a razão das moedas com a de um real
razao25Centavos = diametro25Centavos / diametro1Real
razao10Centavos = diametro10Centavos / diametro1Real
razao5Centavos = diametro5Centavos / diametro1Real

def detectar1Real():
    img = cv2.imread('moeda8.png')
    output = img.copy()
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 9)
    
    lower_range = np.array([0,0,0])
    upper_range = np.array([255,102,255])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    circles = cv2.HoughCircles(image=mask, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=40, maxRadius=100)

    detected_circles = np.uint16(np.around(circles))
    
    for (x, y, r) in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(output, (x, y), 2, (0, 255, 255), 3)
        cv2.putText(output, str(float(r)), (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,0), 1)
    
    cv2.imshow("mask", output)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def main():
    detectar1Real()
    # img = cv2.imread('moeda6.png')
    # output = img.copy()

    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(imgGray, 15)
    # circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=45, maxRadius=100)
    
    # detected_circles = np.uint16(np.around(circles))
    
    # for (x, y, r) in detected_circles[0, :]:
    #     # if(diametro >= diametro10Centavos-2 and diametro <= diametro1Real+2):
    #     cv2.circle(output, (x, y), r, (0, 255, 0), 3)
    #     cv2.circle(output, (x, y), 2, (0, 255, 255), 3)
    #     cv2.putText(output, str(float(r)), (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,0), 1)
    

    # cv2.imshow("output", output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
