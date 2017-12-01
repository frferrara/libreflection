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
        pkg_str = " in package %s "

    # Import the module
    try:
        ret = import_module(name, pkg)
        output = "Success! Module %s" + pkg_str + "imported."
    except ImportError:
        output = "Fail! Module %s" + pkg_str + "not imported."
        traceback.print_stack()
        traceback.print_exc()
    finally:
        if pkg is None:
            print output %name
        else:
            print output %(name, pkg)

    return ret

def get_attr(name, mod):
    """
    Get an attribute for a module such as a class, a function, etc.
    inputs:
    - name: attribute of the module (e.g. class or function name, etc.)
    - mod:  module (e.g. output from import_mod)
    outputs:
    - ret: attribute of the module (None, if exception occurs)
    """
    # Initialize
    ret = None

    # Get the attribute
    try:
        ret = getattr(mod, name)
        output = "Success! Attribute %s in module %s found."
    except TypeError:
        output = "Fail! Attribute %s in module %s not found."
        traceback.print_stack()
        traceback.print_exc()
    finally:
        print output %(name, mod)

    return ret


# Test the library
if __name__ == "__main__":
    # Import nonexisting module
    BLA_MOD = import_mod(".bla", "pkg.sub_pkg")

    # Import test module
    TEST_MOD = import_mod(".test_ref", "pkg.sub_pkg")

    # Get non existent attribute
    TEST_ATTR = get_attr(TEST_MOD, "nonExistent")

    # Get test class
    TEST_ATTR = get_attr("testClass", TEST_MOD)
    TEST_CLASS = TEST_ATTR()
    TEST_CLASS.printout()

    # Import ROS Pose message
    GEOMETRY_MSGS = import_mod("geometry_msgs")
