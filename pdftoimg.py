from pdf2image import convert_from_path
images = convert_from_path("./20211229174004184.pdf")
x = 0
for img in images:
    img.save('./pagess/{}.jpg'.format(x), 'JPEG')
    x+=1