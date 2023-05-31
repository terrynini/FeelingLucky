import random

# External dependencies
import httpx
import ida_kernwin
import idaapi
import idautils


try:
    # Generate true randomness if we got a connection to the outside world
    drand_info = httpx.get("https://api.drand.sh/public/latest").json()
    seed = int(drand_info["randomness"], 16)
    random.seed(seed)
except httpx.ConnectError:
    # Use the default random seed otherwise
    pass


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
        idahome = idaapi.idadir("plugins/FeelingLucky")
        icon_data = open(idahome + "/dice_icon.png", "rb").read()
        act_icon = ida_kernwin.load_custom_icon(data=icon_data, format="png")
        action_desc = ida_kernwin.action_desc_t(
            "nini:FeelingLucky", "Trying your luck", LuckyHandler(), "Alt+Z", "Trying your luck", act_icon
        )

        ida_kernwin.register_action(action_desc)
        idaapi.attach_action_to_toolbar("AnalysisToolBar", "nini:FeelingLucky")

        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        pass

    def term(self):
        ida_kernwin.unregister_action("nini:FeelingLucky")


def PLUGIN_ENTRY():
    return LuckyPlugin()
