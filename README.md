# Pylogix Data Logger

This program uses the [Pylogix](https://github.com/dmroeder/pylogix) library to monitor tags on connected Allen-Bradley PLCs and log the data to a csv file.

Usage: 

`python logger.py -c {config_file.json} -f {output_file.csv}`

Example JSON config - comparison:
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
    "print_timestamp": 1
}
```

Example JSON config - periodic:
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
    "print_timestamp": 1
}
```

| JSON Config Field | Info |
| --- | --- |
| ip | Specify the IP address of the connected controller. |
| tags | List the PLC tags you want to log. Specify program name for program-scope tags.|
| headers | List headers for the output CSV file. |
| trigger_type | Options: "change", "periodic", "compare". |
| trigger_tag | When using "change" or "compare" trigger, specify the tag to monitor/compare. |
| period_time | When using "periodic" trigger, specify time in seconds between logs. |
| compare_condition | Specify when using "compare" trigger. Options: "grt", "geq", "les", "leq", "neq", "equ". |
| compare_cutoff | Value to compare the selected tag to. |
| print_timestamp | Enable (1) / Disable (0) timestamp field in output log. |

## Setup

1. Download & install [Python](https://www.python.org/downloads/) if you haven't already.
2. Run 'setup.bat' (Windows) or 'setup.sh' (Unix) to install dependencies.

Written by Ben DeWeerd.