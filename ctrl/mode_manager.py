from multiprocessing import Process
import time
import asyncore
import socket
import sys
import psutil

def killtree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()

    if including_parent:
        parent.kill()

class mode_manager:
    def __init__ (self, modes, default = None):
        self._process = None
        self._modes = modes
        self._curr = None

        if (default):
            self.run (default)

    def __del__ (self):
        print ("cleaning up mode_manager")
        self.stop ()

    def modes (self):
        return self._modes.keys ()

    def stop (self):
        if (self._process and self._process.is_alive ()):
            # We can't call 'self._process.terminate ()' here as this
            # does not reliably kill any children of the process being
            # terminated.  Instead, manually kill all children.
            killtree (self._process.pid)
            self._process.join ()
            self._process = None
            self._curr = None

    def run (self, mode):
        print ("Run `%s`" % mode)
        if not mode in self._modes:
            raise RuntimeError ("invalid mode")
        print ("Starting: %s" % mode)
        self.stop ()
        self._process = Process (target=self._modes[mode])
        self._process.start ()
        self._curr = mode

    def current_mode (self):
        return self._curr

class network_mode_manager (mode_manager):

    def __init__ (self, port, modes, default = None):
        mode_manager.__init__ (self, modes, default)
        self._server = network_mode_manager.server ('localhost', port, self)

    def loop (self):
        asyncore.loop ()

    class handler (asyncore.dispatcher_with_send):

        def __init__ (self, sock, manager):
            asyncore.dispatcher_with_send.__init__ (self, sock)
            self._data = b''
            self._manager = manager

        def handle_read(self):
            data = self.recv(4)
            self._data += data
            #print ("Got: %s" % self._data)
            if (len (self._data) > 100):
                print ("too much data")
                self.close ()
                return
            try:
                i = self._data.index (b'\r\n')
            except ValueError:
                return
            else:
                pkt = self._data[:i].decode("utf-8")
                self._data = self._data[i+2:]
                if pkt == '?':
                    print ("Query")
                    modes = self._manager.modes ()
                    self.send (bytes ("%d\r\n" % len (modes), "utf-8"))
                    for m in (modes):
                        if m == self._manager.current_mode ():
                            pre = '>'
                        else:
                            pre = ' '
                        self.send (bytes ("%s%s\r\n" % (pre, m), "utf-8"))
                elif pkt[0] == '!':
                    mode = pkt[1:]
                    if mode == '':
                        print ("Stop")
                        self._manager.stop ()
                    else:
                        print ("Set: %s" % mode)
                        try:
                            self._manager.run (mode)
                            self.send (bytes ("OK\r\n", "utf-8"))
                        except RuntimeError:
                            print ("Invalid mode: %s" % mode)
                            self.send (bytes ("FAILED\r\n", "utf-8"))
                elif pkt == 'quit':
                    print ("Quit")
                    self._manager.stop ()
                    sys.exit (0)
                else:
                    print ("First '%c'" % pkt[0])
                    print ("Unknown: %s" % pkt)

    class server (asyncore.dispatcher):
        def __init__ (self, host, port, manager):
            asyncore.dispatcher.__init__ (self)
            self._manager = manager
            self.create_socket (socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr ()
            self.bind ((host, port))
            self.listen (5)

        def handle_accept (self):
            pair = self.accept ()
            if pair is None:
                return
            else:
                sock, addr = pair
                print('Incoming connection from %s' % repr (addr))
                handler = network_mode_manager.handler (sock, self._manager)

# Execute only if run as a script.
if __name__ == "__main__":

    def blah ():
        while True:
            print ("In blah!")
            time.sleep (1)

    def woof ():
        while True:
            print ("In woof!")
            time.sleep (1)

    def main ():
        xxxx = {
            "blah": blah,
            "woof": woof
        }
        mm = network_mode_manager (8080, xxxx)
        mm.loop ()

    main ()
