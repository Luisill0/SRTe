import argparse
from typing import Dict, List, Tuple
from times import Timecode
from interfaces import SRTeArgs

description = 'Load and edit SRT files in Python. Edit dialogues, timecodes, and chunks order.'
parser = argparse.ArgumentParser(prog='SRTe', description=description ,epilog='by Luiz :)')
parser.add_argument('-V', '--verbose', help='Increase output verbosity', action='store_true', required=False)
parser.add_argument('-F', '--file', type=str, help='Path to SRT file to edit', metavar='path', required=False)
args:SRTeArgs = SRTeArgs(parser.parse_args())

def askUser(petition: str, numOptions: int) -> int:
    flag: bool = True
    option: int = -1
    while flag:
        option = int(input(petition))
        flag = not(option > 0 and option <= numOptions)
        if flag is True: print('Invalid option')
    return option  

def getFileName() -> str:
    fileName = args.file if args.file is not None else input('Enter the SRT file path:\n')
    if args.verbose: print('fileName: ', fileName) 
    return fileName

def getIncreaseDecrease() -> Tuple[int, Dict[int, int]]: 
    edit_option = askUser('Edit options:\n1) Increase time\n2) Decrease time\n', 2)
    edit_option_dict = { 1: 1, 2: -1 }
    return edit_option, edit_option_dict

def getTimeToEdit() -> Tuple[int, Dict[int, int]]:
    time_to_edit = askUser('1) Hours\n2) Minutes\n3) Seconds\n4) Miliseconds\n', 4)
    time_to_edit_dict = { 1: 60*60*1000, 2: 60*1000, 3: 1000, 4: 1 }
    return time_to_edit, time_to_edit_dict

def editSRTFile(fileName: str, ms_edit_amount: int) -> str:
    srtFile = open(fileName, 'r')
    newSRTFileName = ''.join(fileName.split('.')[:-1]) + '.new.srt'
    newSrtFile = open(newSRTFileName, 'w')
    for line in srtFile.readlines():
        newLines: List[str] = []
        if(line.__contains__('-->')):
            lineElements = line.split(maxsplit=2)
            ms_start = Timecode.getMS(lineElements[0])
            ms_end = Timecode.getMS(lineElements[2]) 

            new_ms_start = Timecode.getStr(ms_start + ms_edit_amount)
            new_ms_end = Timecode.getStr(ms_end + ms_edit_amount)
            newLines.append('{} ---> {}\n'.format(new_ms_start,new_ms_end))
        else:
            newLines.append(line)
        newSrtFile.writelines(newLines)
    newSrtFile.close()  
    return newSRTFileName  
            
            

if __name__=='__main__':
    fileName = getFileName()
    
    edit_option, edit_option_dict = getIncreaseDecrease()
    time_to_edit, time_to_edit_dict = getTimeToEdit()
    edit_amount = int(input('Enter time amount to {}:'.format(('increase' if edit_option == 1 else 'decrease'))))

    ms_edit_amount = time_to_edit_dict[time_to_edit] * edit_option_dict[edit_option] * edit_amount
    newFileName = editSRTFile(fileName, ms_edit_amount)
    print('Done!', 'the new file is {}'.format(newFileName) if args.verbose == True else '')  