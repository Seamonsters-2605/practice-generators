import sys
import queue
import threading
import remi
import remi.gui as gui

DASHBOARD_PORT = 5805

def hBoxWith(*args, **kwargs):
    box = gui.HBox(**kwargs)
    for widget in args:
        box.append(widget)
    return box

def vBoxWith(*args, **kwargs):
    box = gui.VBox(**kwargs)
    for widget in args:
        box.append(widget)
    return box

def startDashboard(robot, dashboardClass):
    appHolder = [None]

    appReadyEvent = threading.Event()
    def appCallback(app):
        appHolder[0] = app
        appReadyEvent.set()

    def startDashboardThread(robot, appCallback):
        if sys.argv[1] == 'sim':
            remi.start(dashboardClass, port=DASHBOARD_PORT, userdata=(robot, appCallback,))
        elif sys.argv[1] == 'depoly':
            pass
        elif sys.argv[1] == 'run': # run on robot
            remi.start(dashboardClass, start_browser=False,
                address='10.26.5.2', port=DASHBOARD_PORT, userdata=(robot, appCallback,))

    thread = threading.Thread(target=startDashboardThread,
                                args=(robot, appCallback))
    thread.daemon = True
    thread.start()
    print("Waiting for app to start...")
    appReadyEvent.wait()
    print("App started!")

    return appHolder[0]


class Dashboard(remi.App):

    def __init__(self, *args):
        self.eventQueue = queue.Queue()
        super(Dashboard, self).__init__(*args)

    def queuedEvent(self, eventF):
        def queueTheEvent(*args, **kwargs):
            def doTheEvent():
                print("Event:", eventF.__name__)
                eventF(*args, **kwargs)
            self.eventQueue.put(doTheEvent)
        return queueTheEvent

    def clearEvents(self):
        while not self.eventQueue.empty():
            self.eventQueue.get()

    def doEvents(self):
        while not self.eventQueue.empty():
            event = self.eventQueue.get()
            event()
