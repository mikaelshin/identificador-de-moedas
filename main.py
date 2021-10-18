import numpy as np
import cv2

# Medida das moedas em milimetros
umReal = 27
cinquentaCentavos = 23
vinteCincoCentavos = 25
dezCentavos = 20
cincoCentavos = 22

# Definindo a razão das moedas com a de um real
razaoCinquentaCentavos = cinquentaCentavos / umReal
razaoVinteCincoCentavos = vinteCincoCentavos / umReal
razaoDezCentavos = dezCentavos / umReal
razaoCincoCentavos = cincoCentavos / umReal

def main():
    img = cv2.imread('moeda8menor.png')
    output = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(imgGray, 17)
    circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=75)
    
    detected_circles = np.uint16(np.around(circles))
    for (x, y, r) in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(output, (x, y), 2, (0, 255, 255), 3)
        cv2.putText(output, str(int(r*2/5)), (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,0), 1)
    

    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()