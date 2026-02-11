# Pylogix Data Logger

This program uses the [Pylogix](https://github.com/dmroeder/pylogix) library to monitor tags on connected Allen-Bradley PLCs and log the data to a csv file. It can trigger periodically or based on tag data.

## Setup

1. Download & install [Python](https://www.python.org/downloads/) if you haven't already. Make sure to add Python to path/environment variables during install.
2. Run 'setup.bat' (Windows) or 'setup.sh' (Unix) to install dependencies.

## Usage

1. Connect to the same network as the PLC (you can ping to verify)
2. Open a terminal in the same directory as `logger.py`
3. Run `python logger.py -c {path_to_config_file.json} -f {path_to_output_file.csv}`

## JSON Config
| Field | Info |
| --- | --- |
| ip | Specify the IP address of the connected controller. |
| tags | List the PLC tags you want to log. Specify program name for program-scope tags.|
| headers | List headers for the output CSV file. |
| trigger_type | Options: "change", "periodic", "compare", "rising", "falling". |
| trigger_tag | When using "change", "compare", "rising", or "falling" trigger, specify the tag to monitor/compare. |
| period_time | When using "periodic" trigger, specify time in seconds between logs. |
| compare_condition | Specify when using "compare" trigger. Options: "grt", "geq", "les", "leq", "neq", "equ". |
| compare_cutoff | Value to compare the selected tag to. |
| print_timestamp | Enable (1) / Disable (0) timestamp field in output log. |
| live_update | Enable (1) / Disable (0) live output updates. Live updates show data immediately but reduce performance. |

#### Example JSON config - comparison trigger:
```
{
    "ip": "10.240.10.102",
    "tags": [
        "AI_Z9_MB1_05_00",
        "AI_Z9_MB1_05_01",
        "AI_Z9_MB1_05_02",
        "AI_Z9_MB1_05_03"
    ],
    "headers": [
        "LRT1",
        "LRT2",
        "LRT3",
        "LRT4"
    ],
    "trigger_type": "compare",
    "trigger_tag": "AI_Z9_MB1_05_00",
    "period_time": 0,
    "compare_condition": "les",
    "compare_cutoff": 1866.5625,
    "print_timestamp": 1,
    "live_update": 0
}
```

#### Example JSON config - periodic trigger:
```
{
    "ip": "10.240.10.102",
    "tags": [
        "AI_Z9_MB1_05_00",
        "AI_Z9_MB1_05_01",
        "AI_Z9_MB1_05_02",
        "AI_Z9_MB1_05_03"
    ],
    "headers": [
        "LRT1",
        "LRT2",
        "LRT3",
        "LRT4"
    ],
    "trigger_type": "periodic",
    "trigger_tag": "",
    "period_time": 0.25,
    "compare_condition": "",
    "compare_cutoff": 0,
    "print_timestamp": 1,
    "live_update": 1
}
```

#### Example JSON config - program-scope tags:
```
{
    "ip": "10.240.10.102",
    "tags": [
        "Program:HMI.Trim_Banner_Title",
        "Program:HMI.Trim_Banner_Message"
    ],
    "headers": [
        "Title",
        "Message"
    ],
    "trigger_type": "change",
    "trigger_tag": "Program:HMI.Trim_Banner_Title",
    "period_time": 0,
    "compare_condition": "",
    "compare_cutoff": 0,
    "print_timestamp": 1,
    "live_update": 0
}
```

***

Written by Ben DeWeerd.