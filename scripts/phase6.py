import subprocess
import sys
import time
from subprocess import Popen, PIPE, STDOUT


def permute() -> list: 
    result = []
    for i in range(10101,65656):
        attempt = str(i)
        flag = False
        previous = -1
        for letter in attempt:
            if letter == previous or int(letter) > 5:
                flag = True
                break
            previous = letter
        if flag != True:
            result.append(attempt)
    return result


def main(exec_path: str, phases_path: str) -> None:
    charset = permute()
    for attempt in charset:
        p = Popen([exec_path, phases_path], stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
        stdout_data = p.communicate(input=f'4 {attempt[0]} {attempt[1]} {attempt[2]} {attempt[3]} {attempt[4]}\n')[0]
        print(stdout_data)
        if 'BOOM!!!' not in stdout_data:
            print(f'Success! -> {attempt}')
            break
        p.kill()


if __name__ == "__main__":
    exec_path,phases_path = sys.argv[1],sys.argv[2] if len(sys.argv) == 3 else sys.exit('Error: Wrong number of arguments')
    main(exec_path, phases_path)
