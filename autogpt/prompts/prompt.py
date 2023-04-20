from colorama import Fore

from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.logs import logger
from autogpt.prompts.generator import PromptGenerator
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()


def build_default_prompt_generator() -> PromptGenerator:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "~4000字的短期记忆限制。你的短期记忆是短暂的，所以立即将重要信息保存到文件中."
    )
    prompt_generator.add_constraint(
        "如果你不确定你以前是如何做某事的，或者想要回忆过去的事情，想想类似的事件会帮助你思考."
    )
    prompt_generator.add_constraint("没有用户协助")
    prompt_generator.add_constraint(
        '只使用双引号中列出的命令，例如"命令名称"'
    )
    prompt_generator.add_constraint('必须用中文回答')

    # Define the command list
    commands = [
        ("Do Nothing", "do_nothing", {}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
    ]

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        "上网搜索和收集信息。"
    )
    prompt_generator.add_resource("使用内存长期管理。")
    prompt_generator.add_resource(
        "GPT-3.5支持的代理，用于简单任务的委托。"
    )
    prompt_generator.add_resource("输出文件.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        "不断地回顾和分析你的行为，以确保你发挥出了最好的能力。"
    )
    prompt_generator.add_performance_evaluation(
        "经常建设性地自我批评你的整体行为。"
    )
    prompt_generator.add_performance_evaluation(
        "反思过去的决定和策略，以完善你的方法。"
    )
    prompt_generator.add_performance_evaluation(
        "每个命令都有成本，所以要聪明和高效。以最少的步骤完成任务为目标。"
    )
    prompt_generator.add_performance_evaluation("把所有代码输出到文件")
    return prompt_generator


def construct_main_ai_config() -> AIConfig:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("Name :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("Role :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("Goals:", Fore.GREEN, f"{config.ai_goals}")
    elif config.ai_name:
        logger.typewriter_log(
            "欢迎回来! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
Continue (y/n): """
        )
        if should_continue.lower() == "n":
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save(CFG.ai_settings_file)

    return config
