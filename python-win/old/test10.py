from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GRect, GOval

window = GWindow()
rect = GRect(200, 100)  # A rectangle 200 pixels wide and 100 pixels tall.
oval = GOval(
    100, 50
)  # An oval whose bounding box is 100 pixels wide and 50 pixels tall.
oval.filled = True
window.add(
    rect, x=20, y=40
)  # Add the rectangle to the graphical window 20 pixels from the left and 40 pixels from the top.
window.add(
    oval, x=40, y=20
)  # Add the oval to the graphical window 20 pixels from the left and 40 pixels from the top.
