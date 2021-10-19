import cv2
import numpy as np

# Medida das moedas em milimetros
diametro1Real = 27        # identificar pelas duas cores
diametro25Centavos = 25   # identificar pelo raio
diametro10Centavos = 20   # identificar pela raio
diametro5Centavos = 22    # identificar pela raio

# Definindo a razão das moedas com a de um real
razao25Centavos = diametro25Centavos / diametro1Real
razao10Centavos = diametro10Centavos / diametro1Real
razao5Centavos = diametro5Centavos / diametro1Real

# 

def main():
    
    # Definindo variaveis
    input = cv2.imread('moeda8.png')
    processado = input.copy() 
    output = input.copy()
    somaMoedas = 0
    
    (processado, output, somaMoedas, media1Real) = processar1Real(input, processado, output, somaMoedas)
    (processado, output, somaMoedas) = processar50Centavos(processado, output, somaMoedas)
    # (processado, output, somaMoedas) = processarRestante(processado, output, somaMoedas)

    # cv2.imshow("input", input)
    instrucoesFinais(processado, output, somaMoedas, media1Real)

    
def processar1Real(input, processado, output, somaMoedas):

    media1Real = 0;
    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 9)
    
    lower_range = np.array([0, 0, 0])
    upper_range = np.array([255, 102, 255])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    circles = cv2.HoughCircles(image=mask, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=40, maxRadius=100)

    detected_circles = np.uint16(np.around(circles))
    
    for (x, y, r) in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(processado, (x, y), r, (255, 0, 0), cv2.FILLED)
        somaMoedas += 1
        media1Real += float(r) 
    
    media1Real /= somaMoedas
    return processado, output, somaMoedas, media1Real
    
    
def processar50Centavos(processado, output, somaMoedas):
    
    hsv = cv2.cvtColor(processado, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 1)
    
    lower_range = np.array([0, 0, 0])
    upper_range = np.array([255, 60, 135])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    circles = cv2.HoughCircles(image=mask, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=40, maxRadius=100)

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
         
        for (x, y, r) in detected_circles[0, :]:
            cv2.circle(output, (x, y), r, (255, 255, 0), 3)
            cv2.circle(processado, (x, y), r, (255, 0, 0), cv2.FILLED)
            somaMoedas += 0.5

    return processado, output, somaMoedas
  
  
def processarRestante(input, processado, output, somaMoedas): 
    inputGray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(inputGray, 15)
    circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=45, maxRadius=100)
    
    detected_circles = np.uint16(np.around(circles))
    
    for (x, y, r) in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(output, (x, y), 2, (0, 255, 255), 3)
        cv2.putText(output, str(float(r)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1)

    return processado, output, somaMoedas
    
    
def instrucoesFinais(processado, output, somaMoedas, media1Real):
    cv2.imshow("processado", processado)
    cv2.putText(output, "Total: R$ " + str(somaMoedas), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)    
    cv2.putText(output, "Media de R$ 1: " + str(media1Real), (500, 50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)    
    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()