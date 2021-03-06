import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/application_logs"


def get_all(isamAppliance, file_path='', recursive='yes', flat_details=None, check_mode=False, force=False):
    """
    Retrieving the contents of a directory from the application log files area

    flat_details - takes 'yes' or 'no'
    """
    return isamAppliance.invoke_get("Retrieving the contents of a directory from the application log files area",
                                    "{0}/{1}/{2}".format(uri, file_path,
                                                         tools.create_query_string(
                                                             recursive=recursive,
                                                             flat_details=flat_details)))


def get(isamAppliance, file_path, length=None, start=None, check_mode=False, force=False):
    """
    Retrieving the contents of a file from the application log files area
    """
    return isamAppliance.invoke_get("Retrieving the contents of a file from the application log files area",
                                    "{0}/{1}{2}".format(uri, file_path,
                                                         tools.create_query_string(
                                                             length=length,
                                                             start=start)))


def clear(isamAppliance, file_id, check_mode=False, force=False):
    """
    Clearing a log file
    """
    delete_required = False
    if force is False:
        try:
            ret_obj = get(isamAppliance, file_id, length=1, start=1)
            delete_required = True  # Exception thrown if the file is empty
        except:
            pass

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Clearing a log file",
                "{0}/{1}?action=clear".format(uri, file_id))

    return isamAppliance.create_return_object()


def delete(isamAppliance, file_id, check_mode=False, force=False):
    """
    Deleting a log file
    """
    if force is False:
        try:
            ret_obj = get(isamAppliance, file_id, length=1, start=1)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a log file",
                "{0}/{1}?action=delete".format(uri, file_id))

    return isamAppliance.create_return_object()


def export_file(isamAppliance, file_path, filename, check_mode=False, force=False):
    """
    Downloading a file from the file application log files area
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Downloading a file from the file application log files area",
                "{0}/{1}?type=File".format(uri, file_path),
                filename, no_headers=True)

    return isamAppliance.create_return_object()
