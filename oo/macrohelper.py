"""
Basic class implements global Constants and Functions in StarBasic
Makes writing macroses with python more comfortable
Takes XSCRIPTCONTEXT or ComponentContext to generate all other objects, so it can  be
used inside macroses and from remote procs


"""


import uno
import logging
log = logging.getLogger(__name__)

class StarBasicGlobals:
    def __init__(self, context):
        self._givenctx = context
        self._preload()

    def _preload(self):
        c = self._givenctx
        if hasattr(c, 'getDesktop'):  # context is XSCRIPTCONTEXT
            self.StarDesktop = c.getDesktop
            self.GetDefaultContext = c.getComponentContext
            self.ThisComponent = c.getDocument()
        elif hasattr(c, 'ServiceManager'):  # context is StarOffice.ComponentContext
            self.StarDesktop = c.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", c)
            self.GetDefaultContext = lambda: c
            self.ThisComponent = self.StarDesktop.getCurrentComponent()
        assert self.StarDesktop, "bad context, init failed"

        self._ctx = self.GetDefaultContext()
        self.GetProcessServiceManager = self._ctx.getServiceManager
        self._smgr = self.GetProcessServiceManager()
    
    def CreateUnoService(self, uri, *args):
        if len(args):
            return self._smgr.createInstanceWithArgumentsAndContext(uri,
                    args, self._ctx)
        return self._smgr.createInstanceWithContext(uri, self._ctx)
    def CreateUnoStruct(self, uri, *args):
        return uno.createUnoStruct(uri, *args)

    def CreateUnoDialog(self, uri):
        dp = self._smgr.createInstanceWithContext(
                "com.sun.star.DialogProvider", self._ctx)
        return dp.createDialog(
                "vnd.sun.star.script:{uri}?location=user".format(uri=uri))

    def InputBox(self, message, title=""):
        """ Create simple imput dialog programaticaly"""
        from summerfield.SortedDict import SortedDict
        parent = self.StarDesktop.getCurrentFrame().getContainerWindow()
        toolkit = parent.getToolkit()
        dialog = self._smgr.createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialog", self._ctx)
        dialogModel = self._smgr.createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialogModel", self._ctx)
        dialog.setModel(dialogModel)
        modelDict = SortedDict()
        modelDict['Name'] = 'InputBox'
        modelDict['Title'] = title
        # we also should prescribe Width, Height, X and YPosition
        dialogModel.setPropertyValues(tuple(modelDict.keys()),
                tuple(modelDict.values()))


        # now lets print in the message as simple label
        label = dialogModel.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
        modelDict.clear()
        modelDict['Name'] = "Message"
        modelDict['PositionX'] = 5
        modelDict['PositionY'] = 5
        modelDict['Width'] = 100
        modelDict['Height'] = 8

        label.setPropertyValues(tuple(modelDict.keys()), tuple(modelDict.values()))
        log.debug("label is %s", label)
        dialogModel.insertByName("Message", label)
        control = dialog.getControl("Message")
        log.debug("control is %s", control)
        control.setText(message)
        
       




        dialog.createPeer(toolkit, parent)
        dialog.execute()
        dialog.dispose()


        

    

        
    def MsgBox(self, message, title="", message_type="infobox", buttons=1):
        """ Show message in message box. """
        parent = self.StarDesktop.getCurrentFrame().getContainerWindow()
        toolkit = parent.getToolkit()
        older_imple = self._check_method_parameter(
                "com.sun.star.awt.XMessageBoxFactory", "createMessageBox",
                1, "com.sun.star.awt.Rectangle")
        if older_imple:
            from com.sun.star.awt import Rectangle
            msgbox = toolkit.createMessageBox(
                parent, Rectangle(), message_type, buttons, title, message)
        else:
            message_type = uno.getConstantByName("com.sun.star.awt.MessageBoxType." + {
                "messbox": "MESSAGEBOX", "infobox": "INFOBOX",
                "warningbox": "WARNINGBOX", "errorbox": "ERRORBOX",
                "querybox": "QUERYBOX"}[message_type])
            msgbox = toolkit.createMessageBox(
                parent, message_type, buttons, title, message)
        n = msgbox.execute()
        msgbox.dispose()
        return n

    def _check_method_parameter(self, interface_name, method_name, param_index, param_type):
        """ Check the method has specific type parameter at the specific position. """
        cr = self.CreateUnoService("com.sun.star.reflection.CoreReflection")
        try:
            idl = cr.forName(interface_name)
            m = idl.getMethod(method_name)
            if m:
                info = m.getParameterInfos()[param_index]
                return info.aType.getName() == param_type
        except:
            pass
        return False

