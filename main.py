import cv2
import numpy as np

# Medida das moedas em milimetros
diametro1Real = 27        
diametro25Centavos = 25   # identificar pelo raio
diametro10Centavos = 20   # identificar pela raio
diametro5Centavos = 22    # identificar pela raio

# Definindo a razão das moedas com a de um real
razao25Centavos = diametro25Centavos / diametro1Real
razao10Centavos = diametro10Centavos / diametro1Real
razao5Centavos = diametro5Centavos / diametro1Real

def main():
    
    input = cv2.imread('moeda4.png')
    
    (processado, output, somaMoedas, media1Real) = processar1Real(input, processado=input.copy(), 
                                                                  output=input.copy(), somaMoedas=0)
    (processado, output, somaMoedas) = processar50Centavos(processado, output, somaMoedas)
    (output, somaMoedas) = processarRestante(processado, output, somaMoedas, media1Real)
    instrucoesFinais(output, somaMoedas)

    
def processar1Real(input, processado, output, somaMoedas):
    
    media1Real = 0;
    hsv = cv2.medianBlur(cv2.cvtColor(input, cv2.COLOR_BGR2HSV), 9)
    
    mascara = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([255, 102, 255]))
    circulos = cv2.HoughCircles(image=mascara, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                                param1=50, param2=30, minRadius=40, maxRadius=100)

    circulosDetectados = np.uint16(np.around(circulos))
    
    for (x, y, raio) in circulosDetectados[0, :]:
        cv2.circle(output, (x, y), raio, (0, 140, 255), 3)
        k = raio + 8
        processado[y-k: y+k, x-k: x+k] = cv2.blur(processado[y-k: y+k, x-k: x+k], (199, 199))
        cv2.putText(output, "R$ 1.00", (x - 50, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
        somaMoedas += 1
        media1Real += float(raio) 

    media1Real /= somaMoedas
    return processado, output, somaMoedas, media1Real
    
    
def processar50Centavos(processado, output, somaMoedas):
    
    hsv = cv2.medianBlur(cv2.cvtColor(processado, cv2.COLOR_BGR2HSV), 1)
    
    mascara = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([255, 60, 135]))
    circulos = cv2.HoughCircles(image=mascara, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                                param1=50, param2=30, minRadius=40, maxRadius=100)

    if circulos is not None:
        circulosDetectados = np.uint16(np.around(circulos))
         
        for (x, y, raio) in circulosDetectados[0, :]:
            cv2.circle(output, (x, y), raio, (255, 255, 255), 3)
            k = raio + 8 #constante
            processado[y-k: y+k, x-k: x+k] = cv2.blur(processado[y-k: y+k, x-k: x+k], (199, 199))
            cv2.putText(output, "R$ 0.50", (x - 45, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
            somaMoedas += 0.5
    
    return processado, output, somaMoedas
  
  
def processarRestante(processado, output, somaMoedas, media1Real): 
    
    gray = cv2.medianBlur(cv2.cvtColor(processado, cv2.COLOR_BGR2GRAY), 15)
    circulos = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                                param1=50, param2=30, minRadius=45, maxRadius=100)
    
    circulosDetectados = np.uint16(np.around(circulos))
    
    for (x, y, raio) in circulosDetectados[0, :]:
        
        razao = float(round(raio/media1Real, 2))
        
        # 25 Centavos, se:    0.98 >= razao >= 0.86
        if (razao25Centavos + 0.06) >= razao >= (razao25Centavos - 0.06):
            somaMoedas += 0.25
            cv2.circle(output, (x, y), raio, (0, 0, 0), 3)
            cv2.putText(output, "R$ 0.25", (x - 45, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
        
        # 5 Centavos, se:      0.86 > razao >= 0.80 
        elif (razao5Centavos + 0.05) > razao >= (razao5Centavos - 0.01):
            somaMoedas += 0.05
            cv2.circle(output, (x, y), raio, (123, 0, 0), 3)
            cv2.putText(output, "R$ 0.05", (x - 45, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
            
        # 10 Centavos, se:      0.80 > razao >= 0.67   
        elif (razao10Centavos + 0.06) > razao >= (razao10Centavos - 0.07):
            somaMoedas += 0.10
            cv2.circle(output, (x, y), raio, (123, 0, 123), 3)
            cv2.putText(output, "R$ 0.10", (x - 45, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
    
    return output, somaMoedas
    
    
def instrucoesFinais(output, somaMoedas):
    
    cv2.putText(output, "Total: R$ " + str("%.2f" %somaMoedas), 
                (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 1)    
    cv2.imshow("output", output)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()