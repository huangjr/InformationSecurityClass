from PIL import Image

# ppmPicture="./car.ppm"
# im = Image.open("./car_jpg.jpg")
# im.save(ppmPicture)

ppmPicture = "./test.ppm"
im = Image.open(ppmPicture)
im.save('./test.png', "png")