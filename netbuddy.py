# Python 3.8.2
# Written by Dylan Halladay
# NetBuddy - Network tools and troubleshooting

"""How to import:

   from netbuddy import NetBuddy

   ---

   NetBuddy's code is contained entirely in one class, which isn't very pythonic.
   There are a few reasons I did it this way:

   - Readability:  This structure allows all of NetBuddy's methods, exceptions, and variables
                   to be contained in a single structure

   - Importing:    The single, all-encompassing structure makes imports of NetBuddy extreme simple,
                   as opposed to having to import all these things separately

   - Organization: Having all the code in a single file makes things easier if this module is
                   added to another project in the future """

from os import name
from subprocess import check_output, CalledProcessError
import requests  # You may need 'python -m pip install requests'


class NetBuddy:
    """Class to provide a simple-to-use interface for network
       troubleshooting and tools. For help, run NetBuddy.help()"""

    active = False  # True if start() has run and quit() hasn't, False otherwise

    class NetBuddyException(BaseException):
        """Base exception class for all NetBuddy exceptions. Useful to handle all
           NetBuddy errors while still seeing others."""

    class NotStartedException(NetBuddyException):
        """Thrown if a method is called before a session is started."""
        pass

    class NotWindowsException(NetBuddyException):
        """Thrown if device is not running Windows, as this program
           was not designed for other platforms."""
        pass

    class MissingCommandException(NetBuddyException):
        """Thrown if a command is not found. This error should be very rare,
           as the commands that might throw this are bundled with Windows."""
        pass

    class QuestionableException(NetBuddyException):
        """Thrown for states that should be unreachable. If you get this error,
           I wish you luck.

           Information about the error is in the traceback."""
        pass

    def __init__(self):
        """Instantiation is supported but unnecessary. It just calls the start() method.

           To use NetBuddy without instantiation, just replace the instace with the class:

           NetBuddy.start()

           instead of:

           x.start()"""
        self.start()

    @staticmethod
    def ensure_session_active():
        """Shortcut to ensure a session is active, throws error if not."""
        if not NetBuddy.active:
            raise NetBuddy.NotStartedException("No session active, use NetBuddy.start() first")

    @staticmethod
    def start():
        """Import modules, check platform, check for commands, etc.
           Required before running any other method except quit()."""
        if NetBuddy.active:
            print("A session is already active. To quit, use NetBuddy.quit().")
        else:
            print("Session starting...")
            print("Checking platform...")
            if name != 'nt':
                raise NetBuddy.NotWindowsException("This program is only supported on Windows.")

            print("Looking for required commands...")
            if not check_output(['ping', '/?']):
                raise NetBuddy.MissingCommandException("Missing command 'ping'. This is unexpected for Windows devices.")

            NetBuddy.active = True
            print("Session started. Run NetBuddy.help() for options.")

    @staticmethod
    def quit():
        """Clean exit."""
        NetBuddy.active = False
        print("Session ended.")

    @staticmethod
    def help():
        """Display a list of options."""
        print("NetBuddy by Dylan Halladay                                                           ")
        print("'NetBuddy' has been omitted from the beginning of these items for readability.       ")
        print("For example, to start a session, use NetBuddy.start(), not just .start()             ")
        print("All options and methods print to screen and return False upon failure                ")
        print("Options: ----------------------------------------------------------------------------")
        print("-- .start()                       : Start NetBuddy session, required for all methods ")
        print("-- .quit()                        : Cleanly quits NetBuddy session                   ")
        print("-- .help()                        : Display this screen                              ")
        print("Methods: ----------------------------------------------------------------------------")
        print("-- .test_connection()             : Test if your device is online (alias: test)      ")
        print("-- .ping(address)                 : Ping a URL or IP address                         ")
        print("-- .measure_ping()                : Measure your ping (alias: measure)               ")
        print("-- .send(data, url)               : Send data to a URL or IP address                 ")
        print("-- .get_my_IP                     : Get this device's IP address                     ")
        print("-- .get_my_hostname               : Get this device's hostname                       ")
        print("-- .get_hostname(address)         : Get the hostnames of the specified device        ")
        print("-- .get_IPs                       : Get the IP of every device on this network       ")
        print("-- .get_hostnames                 : Get the hostname of every device on this network ")
        print("Data: -------------------------------------------------------------------------------")
        print("-- .active                        = True if a session is active, otherwise False     ")
        print("Exceptions: -------------------------------------------------------------------------")
        print("-- .NetBuddyException             - Base class for all following exceptions          ")
        print("-- .NotStartedException           - Tried to use a method before starting session    ")
        print("-- .NotWindowsException           - Device platform is not Windows (unsupported)     ")
        print("-- .MissingCommandException       - Required command was not found                   ")
        print("How to import: ----------------------------------------------------------------------")
        print("from netbuddy import NetBuddy                                                        ")

    @staticmethod
    def test_connection():
        """Test if this device is connected to the internet."""
        NetBuddy.ensure_session_active()

        success_count = 0
        test_count = 4

        print("Running 4 tests:")
        try:
            check_output(['ping', '-n', '2', '-l', '32', 'www.google.com'])
        except CalledProcessError:
            print("-- Test 1 failed.\t(www.google.com)")
        else:
            success_count += 1
            print("-- Test 1 passed.\t(www.google.com)")

        try:
            check_output(['ping', '-n', '2', '-l', '32', 'twitter.com'])
        except CalledProcessError:
            print("-- Test 2 failed.\t(twitter.com)")
        else:
            success_count += 1
            print("-- Test 2 passed.\t(twitter.com)")

        try:
            check_output(['ping', '-n', '2', '-l', '32', 'www.python.org'])
        except CalledProcessError:
            print("-- Test 3 failed.\t(www.python.org)")
        else:
            success_count += 1
            print("-- Test 3 passed.\t(www.python.org)")

        try:
            check_output(['ping', '-n', '2', '-l', '32', 'github.com'])
        except CalledProcessError:
            print("-- Test 4 failed.\t(github.com)")
        else:
            success_count += 1
            print("-- Test 4 passed.\t(github.com)")

        success_rate = int(100*(success_count/test_count))
        print("%s/%s tests passed (%s%%)" % (success_count, test_count, success_rate))
        if not success_rate > 0:
            return False

    @staticmethod
    def test():
        """Alias"""
        return NetBuddy.test_connection()

    @staticmethod
    def ping(address):
        """Ping a URL or IP address, return reply or False."""
