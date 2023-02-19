from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton
import slicer

class PointSelectionDialog(QDialog):
    def __init__(self, point_num):
        super().__init__()
        self.points = [None, None, None]  # Initialize the selected points to None
        self.point_num = point_num

        self.setWindowTitle(f"Point Selection Dialog (Point {point_num})")
        self.setLayout(QVBoxLayout())

        self.viewLabel = QLabel(f"Please select the start, middle, and end points for point {point_num} by clicking on them in the 3D view:")
        self.layout().addWidget(self.viewLabel)

        # Create radio buttons to select the current point to set
        self.buttonGroup = QGroupBox("Current point")
        self.buttonGroup.setLayout(QHBoxLayout())
        self.startButton = QRadioButton("Start")
        self.middleButton = QRadioButton("Middle")
        self.endButton = QRadioButton("End")
        self.startButton.setChecked(True)  # By default, set the start point
        self.buttonGroup.layout().addWidget(self.startButton)
        self.buttonGroup.layout().addWidget(self.middleButton)
        self.buttonGroup.layout().addWidget(self.endButton)
        self.layout().addWidget(self.buttonGroup)

        # Create a callback function that will be called when the user clicks in the 3D view
        self.callbackTag = slicer.app.layoutManager().threeDWidget(0).threeDView().AddObserver(slicer.vtkMRMLViewNode.CursorPositionChangeEvent, self.onCursorPositionChanged)

    def onCursorPositionChanged(self, caller, event):
        # When the user clicks in the 3D view, set the selected point and update the radio buttons
        current_point = None
        if self.startButton.isChecked():
            current_point = 0
        elif self.middleButton.isChecked():
            current_point = 1
        elif self.endButton.isChecked():
            current_point = 2

        if current_point is not None:
            self.points[current_point] = slicer.app.layoutManager().threeDWidget(0).threeDView().convertDeviceToXYZ(event.GetCursorPosition())
            self.updateRadioButtons()

    def updateRadioButtons(self):
        # Disable radio buttons for points that have already been set
        if self.points[0] is not None:
            self.startButton.setEnabled(False)
        if self.points[1] is not None:
            self.middleButton.setEnabled(False)
        if self.points[2] is not None:
            self.endButton.setEnabled(False)

    def getPoints(self):
        return self.points

# Create an empty list to store the selected points
selectedPoints = []

# Prompt the user to select three sets of start, middle, and end points
for i in range(1, 4):
    # Create a new instance of the PointSelectionDialog class and show it
    app = QApplication.instance() or QApplication([])
    dialog = PointSelectionDialog(i)
    dialog.exec_()

    # Get the selected points from the dialog and add them to the list
    selectedPoints.append(dialog.getPoints())

# Print the selected point coordinates
print("Selected points:", selectedPoints)

# Use the selected points to add curves to the Markups module
w = slicer.qSlicerMarkupsPlaceWidget()
w.setMRMLScene(slicer.mrmlScene)

for i, points in enumerate(selectedPoints):
    markupsNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsCurveNode")
    markupsNode.CreateDefaultDisplayNodes
