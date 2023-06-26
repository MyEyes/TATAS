from .main_menu_step import UB_MainMenuStep
from .enter_first_level_step import UB_EnterFirstLevelStep
from .skip_level_preview import UB_SkipLevelPreviewStep

ultraman_generation_steps = [
    UB_MainMenuStep(),
    UB_EnterFirstLevelStep(),
    UB_SkipLevelPreviewStep("1-1")
]