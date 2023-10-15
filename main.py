from PIL import Image


# me di cuenta demasiado tarde que la imagen que uso para validar es RGBA y no RGB
# pero todavia me sale discrepancia comparando con el resultado que da openCV
def rgbToHSV(rgbImage):
    width, height = rgbImage.size
    hsvImage = Image.new('HSV', (width, height))
    h = 0

    for x in range(width):
        for y in range(height):
            r, g, b = rgbImage.getpixel((x, y))
            r, g, b = r / 255.0, g / 255.0, b / 255.0

            cmax = max(r, g, b)
            cmin = min(r, g, b)
            diff = cmax - cmin  # El valor de la diferencia o delta

            if cmax == cmin:
                h = 0
            # Dependiendo del maximo va aplicando segun la formula
            elif cmax == r:
                h = (60 * ((g - b) / diff) + 360) % 360
            elif cmax == g:
                h = (60 * ((b - r) / diff) + 120) % 360
            elif cmax == b:
                h = (60 * ((r - g) / diff) + 240) % 360
            if cmax == 0:
                s = 0
            else:
                s = (diff / cmax) * 100
            v = cmax * 100
            # Va juntando los pixeles convertidoes en una nueva imagen
            hsvImage.putpixel((x, y), (int(h), int(s), int(v)))

    return hsvImage


# Esto es mas simple y se pudo con un match case basico
def hsvToRGB(hsv_image):
    width, height = hsv_image.size
    rgb_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            h, s, v = hsv_image.getpixel((x, y))
            h, s, v = h / 360.0, s / 100.0, v / 100.0

            if s == 0:
                r, g, b = v, v, v
            else:
                h *= 6.0
                i = int(h)
                f = h - i
                p = v * (1 - s)
                q = v * (1 - s * f)
                t = v * (1 - s * (1 - f))

                match i:
                    case 0:
                        r, g, b = v, t, p
                    case 1:
                        r, g, b = q, v, p
                    case 2:
                        r, g, b = p, v, t
                    case 3:
                        r, g, b = p, q, v
                    case 4:
                        r, g, b = t, p, v
                    case _:
                        r, g, b = v, p, q

            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            rgb_image.putpixel((x, y), (r, g, b))

    return rgb_image


def convertHSVToRGB(input_image_path, output_image_path):
    rgb_image = Image.open(input_image_path)
    hsv_image = rgbToHSV(rgb_image)
    rgb_image = hsvToRGB(hsv_image)
    rgb_image.save(output_image_path)


if __name__ == '__main__':
    input_image_path = "./Images/Cars.png"
    output_hsv_image_path = "resultado_hsv.png"
    output_rgb_image_path = "CarsRgb.jpg"

    # Convertir imagen RGB a HSV y guardarla
    rgb_image = Image.open(input_image_path)
    rgb_image = rgb_image.convert('RGB')  # Se supone que convierte de rgba a hsv
    hsv_image = rgbToHSV(rgb_image)
    hsv_image.show("HSV")
    # Convertir imagen HSV de nuevo a RGB y guardarla
    rgb_image = hsvToRGB(hsv_image)
    rgb_image.show("RGB")
    rgb_image.save(output_rgb_image_path)
