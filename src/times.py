from typing import List

class Timecode:
    @staticmethod
    def getMS(timecode: str) -> int:
        times: List[str] = timecode.split(':')
        return Timecode.__timecodeStrToMs(times)

    @staticmethod
    def getStr(ms: int) -> str:
        return Timecode.__msToTimecodeStr(ms)

    @staticmethod
    def __timecodeStrToMs(times: List[str]) -> int:
        ms = int(times[0]) * 60 * 60 * 1000 + int(times[1]) * 60 * 1000 # hours + minutes
        # split again because SRT uses a comma (,) to separate seconds and miliseconds
        seconds_ms: List[str] = times[2].split(',')
        ms += int(seconds_ms[0]) * 1000 # seconds
        ms += int(seconds_ms[1]) # miliseconds
        return ms    

    @staticmethod
    def __msToTimecodeStr(ms: int) -> str:
        if ms < 0: return '00:00:00,00'
        hours = ms // (60*60*1000)
        ms %= (60*60*1000)
        minutes = ms // (60*1000)
        ms %= (60*1000)
        seconds = ms // 1000
        miliseconds = ms % 1000
        return '{}{}:{}:{},{}'.format('0' if hours < 10 else '', hours, minutes, seconds, miliseconds)