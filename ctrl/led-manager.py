from mode_manager import network_mode_manager
import time
import os
from led_manager_settings import led_manager_settings
import argparse

# COMMAND is a full command, including possible arguments.
def make_lambda (command):
    return lambda : os.execv ("/bin/sh", ["/bin/sh", "-c", command])

def build_items (config):
    items = {}
    config_scripts = config.scripts ()
    if len (config_scripts) == 0:
        raise RuntimeError ("no scripts in config file")
    print ("Scripts:")
    for name in config_scripts:
        print ("  %s: %s" % (name, config_scripts[name]))
        items[name] = make_lambda (config_scripts[name])
    return items

def main ():
    # Process command line options.
    parser = argparse.ArgumentParser(description='Control LED scripts.')
    parser.add_argument('--config', help='config file to read', default=None)
    args = parser.parse_args()

    # Figure out the path to the config file, or look in the same
    # directory as the script for a default.
    config_path = args.config
    if config_path == None:
        exe_dir = os.path.abspath (os.path.dirname (__file__))
        config_path = os.path.join (exe_dir, "led-manager.conf")
    else:
        config_path = os.path.abspath (config_path)

    # Now start up the server.
    config = led_manager_settings (config_path)
    items = build_items (config)
    mm = network_mode_manager (config.port (), items, config.default ())
    print ("Listening on port %d for commands" % config.port ())
    mm.loop ()

main ()
