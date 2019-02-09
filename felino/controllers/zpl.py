import zpl
from zpl import label
l = label(65,60)
height = 0
l.origin(0,0)
l.write_text("Problem?", char_height=10, char_width=8, line_width=60,
justification='C')
l.endorigin()

height += 13
image_width = 55
l.origin((l.width-image_width)/2, height)
image_height = l.write_graphic(Image.open('trollface-large.png'),
image_width)
l.endorigin()

l.origin(0, height+image_height)
l.write_text('Happy Troloween!', char_height=5, char_width=4,
line_width=60,
             justification='C')
l.endorigin()

print(l.dumpZPL())
l.preview()