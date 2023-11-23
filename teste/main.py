from __future__ import print_function
import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--image', default='image.png', help='Caminho da imagem')
args = ap.parse_args()

imagem = cv2.imread(args.image)
cv2.imshow("Original", imagem)

escala_de_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(escala_de_cinza, kernel, iterations=1)

dilation = cv2.dilate(erosion, kernel, iterations=1)

# Encontra bordas na imagem usando o método de detecção de bordas Canny
# Calcula os limiares inferior e superior usando sigma = 0.33
sigma = 0.33
v = np.median(dilation)
limite_inferior = int(max(0, (1.0 - sigma) * v))
limite_superior = int(min(255, (1.0 + sigma) * v))

bordas = cv2.Canny(dilation, limite_inferior, limite_superior)

contornos, _ = cv2.findContours(bordas, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)


def detectarForma(cnt):
    forma = 'desconhecida'
    peri = cv2.arcLength(cnt, True)
    vertices = cv2.approxPolyDP(cnt, 0.04 * peri, True)

    # Se a forma for um triângulo, ela terá 3 vértices
    if len(vertices) == 3:
        forma = 'triangulo'

    elif len(vertices) == 4:

        x, y, largura, altura = cv2.boundingRect(vertices)
        proporcao_aspecto = float(largura) / altura

        if proporcao_aspecto >= 0.95 and proporcao_aspecto <= 1.05:
            forma = "quadrado"
        else:
            forma = "retangulo"
    else:
        forma = "circulo"

    return forma

for i, contorno in enumerate(contornos):
    # Ignora contornos muito pequenos
    area = cv2.contourArea(contorno)
    if area < 100:
        continue

    M = cv2.moments(contorno)
    # A partir do momento, podemos calcular área, etc.
    # O centróide pode ser calculado da seguinte forma
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    # chama detectarForma para o contorno
    forma = detectarForma(contorno)

    # Desenha os contornos
    cv2.drawContours(imagem, [contorno], -1, (0, 255, 0), 2)

    cv2.putText(imagem, forma, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 2)

    cv2.imshow("Imagem", imagem)

cv2.waitKey(0)
cv2.destroyAllWindows()
