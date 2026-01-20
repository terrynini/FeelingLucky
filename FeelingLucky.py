import random
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import ida_kernwin
import idaapi
import idautils
import os

class LuckyHandler(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)
    def activate(self, ctx):
        functions = idautils.Functions()
        function_ea = random.choice(list(functions))
        return idaapi.jumpto(function_ea)
    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS

class LuckyPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_PROC
    comment = "This plugin does nothing useful"
    help = "Good luck!"
    wanted_name = "FeelingLucky"

    def init(self):
        PLUGIN_DIR = os.path.dirname(__file__)
        ICON_PATH  = os.path.join(PLUGIN_DIR, "dice_icon.png")
        icon_data = open(ICON_PATH, "rb").read()
        act_icon = ida_kernwin.load_custom_icon(data=icon_data, format="png")
        action_desc = ida_kernwin.action_desc_t(
            'nini:FeelingLucky',
            'Trying your luck',
            LuckyHandler(),
            'Alt+Z',
            'Trying your luck',
            act_icon
        )

        ida_kernwin.register_action(action_desc)
        idaapi.attach_action_to_toolbar("AnalysisToolBar", 'nini:FeelingLucky')

        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        pass

    def term(self):
        ida_kernwin.unregister_action("nini:FeelingLucky")

def PLUGIN_ENTRY():
    return LuckyPlugin() 
