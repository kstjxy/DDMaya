# DDMayaPlugin.py

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

# Plugin Name
kPluginCmdName = "DDMayaPlugin"

def createDDMayaWindow(*args):
    """
    Create a window that matches the Direct Delta Mush Skinning Tool UI
    as shown in the provided screenshot.
    """
    window_name = "DDMayaWin"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create window
    window = cmds.window(window_name, 
                         title="Direct Delta Mush Skinning Tool",
                         widthHeight=(300, 200), 
                         sizeable=False)

    # Main layout
    main_layout = cmds.columnLayout(adjustableColumn=True)

    # Top buttons row
    cmds.rowLayout(nc=2, adjustableColumn=2, columnWidth2=[140, 140])
    cmds.button(label="Apply DDM Skinning", 
                width=140, 
                command=lambda _: cmds.warning("Apply DDM Skinning pressed (stub)!"))
    cmds.button(label="Reset to Default", 
                width=140,
                command=lambda _: resetDefaults())
    cmds.setParent('..')  # End rowLayout

    # Parameter Adjustments frame
    cmds.frameLayout(label="Parameter Adjustments:", collapsable=False, marginWidth=5, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True)

    # Smoothing Strength (λ)
    global smoothing_strength_slider
    smoothing_strength_slider = cmds.floatSliderGrp(label="Smoothing Strength (λ)",
                                                    field=True,
                                                    minValue=0.0, maxValue=100.0, 
                                                    value=20.0, 
                                                    step=0.1)
    # Rotation Blend (α)
    global rotation_blend_slider
    rotation_blend_slider = cmds.floatSliderGrp(label="Rotation Blend (α)",
                                                field=True,
                                                minValue=0.0, maxValue=1.0,
                                                value=0.5,
                                                step=0.01)
    # Translation Blend (κ)
    global translation_blend_slider
    translation_blend_slider = cmds.floatSliderGrp(label="Translation Blend (κ)",
                                                   field=True,
                                                   minValue=0.0, maxValue=1.0,
                                                   value=0.1,
                                                   step=0.01)
    # Per-Vertex Weights
    cmds.rowLayout(nc=2, adjustableColumn=1, columnWidth2=[130, 80])
    cmds.text(label="Per-Vertex Weights:")
    cmds.button(label="Edit", 
                command=lambda _: cmds.warning("Edit Per-Vertex Weights (stub)!"))
    cmds.setParent('..')  # End rowLayout

    # Enable Real-Time Preview
    cmds.checkBox(label="Enable Real-Time Preview", 
                  value=False, 
                  changeCommand=lambda x: cmds.warning("Preview toggled to: %s" % x))

    cmds.setParent('..')  # End columnLayout
    cmds.setParent('..')  # End frameLayout

    # Output Settings label (placeholder)
    cmds.text(label="Output Settings:", align="left")

    cmds.showWindow(window)


def resetDefaults():
    """
    Resets the UI controls to their default values.
    """
    # Just sets the sliders to example defaults. 
    # You could add more logic or additional controls as needed.
    cmds.floatSliderGrp(smoothing_strength_slider, edit=True, value=20.0)
    cmds.floatSliderGrp(rotation_blend_slider, edit=True, value=0.5)
    cmds.floatSliderGrp(translation_blend_slider, edit=True, value=0.1)
    cmds.warning("All parameters reset to default values.")


def createDDMayaMenu():
    """
    Creates a new main menu in Maya’s menu bar called 'DDMaya',
    with a single item to open our UI window.
    """
    # If menu already exists, remove it (to avoid duplicates).
    if cmds.menu("DDMayaMenu", exists=True):
        cmds.deleteUI("DDMayaMenu", menu=True)

    main_menu = cmds.menu("DDMayaMenu", 
                          label="DDMaya", 
                          parent="MayaWindow", 
                          tearOff=True)
    cmds.menuItem(label="Open Direct Delta Mush Skinning Tool", 
                  parent=main_menu, 
                  command=createDDMayaWindow)


#----------------------------------------------------------
#  PLUGIN INITIALIZATION / UNINITIALIZATION
#----------------------------------------------------------

class DDMayaPlugin(ompx.MPxCommand):
    """
    A dummy command to tie our Python code into Maya’s plugin system.
    """
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(self, args):
        pass


def cmdCreator():
    return ompx.asMPxPtr(DDMayaPlugin())


def initializePlugin(mobject):
    """
    This function is called when the plugin is loaded into Maya.
    """
    mplugin = ompx.MFnPlugin(mobject, "YourNameOrCompany", "1.0", "Any")
    try:
        # Register command (not strictly necessary if we're just using it for the menu/UI)
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        om.MGlobal.displayError("Failed to register command: %s" % kPluginCmdName)
        raise

    # Create the DDMaya menu
    createDDMayaMenu()
    om.MGlobal.displayInfo("DDMayaPlugin loaded. 'DDMaya' menu created.")


def uninitializePlugin(mobject):
    """
    This function is called when the plugin is unloaded from Maya.
    """
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        om.MGlobal.displayError("Failed to deregister command: %s" % kPluginCmdName)

    # Remove the menu if it exists
    if cmds.menu("DDMayaMenu", exists=True):
        cmds.deleteUI("DDMayaMenu")

    om.MGlobal.displayInfo("DDMayaPlugin unloaded.")
