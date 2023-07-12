from .main_menu_step import UB_MainMenuStep
from .enter_first_level_step import UB_EnterFirstLevelStep
from .skip_level_preview import UB_SkipLevelPreviewStep
from .wait_for_level_start import UB_WaitForLevelStartStep
from .platforming_level import UB_PlatformingLevelStep
from .ultraman_consts import ULTRAMAN_CONSTS

ultraman_generation_steps = [
    UB_MainMenuStep(),
    UB_EnterFirstLevelStep(),
    UB_SkipLevelPreviewStep("1-1"),
    UB_WaitForLevelStartStep("1-1"),
    #UB_PlatformingLevelStep("1-1", ULTRAMAN_CONSTS().LEVEL_WAYPOINTS['1-1']),
    UB_PlatformingLevelStep("1-1", [])
]