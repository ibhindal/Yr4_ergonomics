#Source: https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html
# Instructions:
# Open Slicer>Open Python Console

import slicer
w=slicer.qSlicerMarkupsPlaceWidget()

w.setMRMLScene(slicer.mrmlScene)

markupsNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsCurveNode")

w.setCurrentNode(slicer.mrmlScene.GetNodeByID(markupsNode.GetID()))

# Hide all buttons and only show place button
w.buttonsVisible=False
w.placeButton().show()
w.show()

placeModePersistence = 1
slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
