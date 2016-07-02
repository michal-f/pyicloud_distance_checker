import subprocess
import threading
import settings

class SoundThread(threading.Thread):
    """
    Sound information player (PyICloud distance checker project)
    input params: level, type
    """

    def __init__(self, level, type):
        threading.Thread.__init__(self)
        self.level = level
        self.type = type

    def run(self):
        self.process_sound()

    def process_sound(self):
        output = subprocess.Popen(["python", "sound_player.py", self.level, self.type],
                                  # cwd="/home/theta/",
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        stdout, stderr = output.communicate()
        if settings.DEBUGGING:
            print stdout
            print stderr


def play(level, type):
    sound_thread = SoundThread(level, type)
    sound_thread.start()


if __name__ == "__main__":
    print ">!!SOUND PROCESSOR TEST!!<"
    play("0", "distance")
    play("1", "distance")
    play("2", "distance")
    play("3", "distance")
    play("4", "distance")
    play("5", "distance")
    play("6", "distance")
    play("7", "distance")
    play("8", "distance")
    play("9", "distance")
    play("10", "distance")
    play("0", "speed")
    play("1", "speed")
    play("2", "speed")
    play("3", "speed")
    play("4", "speed")
    play("5", "speed")
    play("6", "speed")
    print ">!! EXITING SOUND PROCESSOR!!<"
