"""
This module implements a library that uses reflection to dynamically load
modules, classes, etc.
"""
# Import modules
import traceback
from importlib import import_module


def import_mod(name, pkg=None):
    """
    Import a module using reflection.
    inputs:
    - name: module name (e.g. cv2)
    - pkg:  package address (e.g. pkg_name.subpkg_name)
    outputs:
    - ret: imported module (None, if exception occurs)
    """
    # Initialize
    ret = None
    if pkg is None:
        pkg_str = " "
    else:
        pkg_str = " in package {} ".format(pkg)

    # Import the module
    try:
        ret = import_module(name, pkg)
        if __debug__:
            output = "Success! Module {}".format(name) + pkg_str + "imported."
    except ImportError:
        output = "Fail! Module {}".format(name) + pkg_str + "not imported."
        if __debug__:
            traceback.print_stack()
            traceback.print_exc()
    finally:
        if __debug__ or ret is None:
            print output

    return ret

def get_attr(name, obj):
    """
    Get an attribute for an object such as a class, a function, etc.
    inputs:
    - name: attribute of the module (e.g. class or function name, etc.)
    - obj:  object (e.g. module resp. output from import_mod)
    outputs:
    - ret: attribute of the object (None, if exception occurs)
    """
    # Initialize
    ret = None

    # Get the attribute
    try:
        ret = getattr(obj, name)
        if __debug__:
            output = "Success! Attribute {} in object {} found.".format(name, obj)
    except TypeError:
        output = "Fail! Attribute {} in object {} not found.".format(name, obj)
        if __debug__:
            traceback.print_stack()
            traceback.print_exc()
    finally:
        if __debug__ or ret is None:
            print output

    return ret

def set_attr(name, obj, value):
    """
    set an attribute in an object such as a class, a function, etc.
    inputs:
    - name:  attribute of the module (e.g. class or function name, etc.)
    - obj:   object (e.g. module resp. output from import_mod)
    - value: new value for the object to be set
    outputs:
    -
    """
    setattr(obj, name, value)


# Test the library
if __name__ == "__main__":
    # Import nonexisting module
    BLA_MOD = import_mod(".bla", "pkg.sub_pkg")
    assert BLA_MOD is None

    # Import test module
    TEST_MOD = import_mod(".test_ref", "pkg.sub_pkg")
    assert TEST_MOD is not None

    # Get non existent attribute
    TEST_ATTR = get_attr(TEST_MOD, "nonExistent")
    assert TEST_ATTR is None

    # Get test class
    TEST_ATTR = get_attr("testClass", TEST_MOD)
    TEST_CLASS = TEST_ATTR()
    TEST_CLASS.printout()
    assert TEST_CLASS.text == "This is a test."

    # Set an attribute correctly
    set_attr("text", TEST_CLASS, "This is a text set through reflection.")
    TEST_CLASS.printout()
    COMP = TEST_CLASS.text == "This is a text set through reflection."
    assert COMP is True

    # Import ROS Pose message
    GEOMETRY_MSGS = import_mod("._Pose", "geometry_msgs.msg")
    POSE = get_attr("Pose", GEOMETRY_MSGS)
    POSE_MSG = POSE()
    POSE_MSG.position.x = 1
    POSE_MSG.position.y = 2
    POSE_MSG.position.z = 3
    POSE_MSG.orientation.x = 4
    POSE_MSG.orientation.y = 5
    POSE_MSG.orientation.z = 6
    POSE_MSG.orientation.w = 7
    print POSE_MSG

    # Import the protobuf
    POSE_PROTO_MOD = import_mod("._Pose_pb2", "protobuf")
    POSE_PROTO = get_attr("Pose", POSE_PROTO_MOD)
    POSE_OBJ = POSE_PROTO()
