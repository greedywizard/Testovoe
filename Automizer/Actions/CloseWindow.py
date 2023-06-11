from Automizer.ExecEnvironment import ExecEnvironment
from selenium.webdriver.support import expected_conditions as EC


def CloseWindow(env: ExecEnvironment):
    win_count = env.Driver.window_handles.__len__()
    env.Driver.close()
    env.Wait.until(EC.number_of_windows_to_be(win_count - 1))
