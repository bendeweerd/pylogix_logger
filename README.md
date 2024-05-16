# Pylogix Data Logger

This program uses the [Pylogix](https://github.com/dmroeder/pylogix) library to monitor tags on connected Allen-Bradley PLCs and log the data to a csv file.

Example usage: 

`python logger.py -c {config_file.json} -f {output_file.csv}`

Example JSON config:
```
{
    "ip": "10.240.10.102",
    "tags": [
        "AI_Z9_MB1_05_00",
        "AI_Z9_MB1_05_01",
        "Program:HMI.SelectedPartData_Title"
    ],
    "headers": [
        "LRT1",
        "LRT2",
        "Selected Part"
    ],
    "trigger_type": "periodic",
    "trigger_tag": "",
    "period_time": 1.0,
    "print_timestamp": 1
}
```

| Field | Info |
| --- | --- |
| ip | Specify the IP address of the connected controller. |
| tags | List the PLC tags you want to log. Specify program name for program-scope tags.|
| headers | List headers for the output CSV file. |
| trigger_type | Options: "change", "periodic" |
| trigger_tag | When using "change" trigger, specify the tag to monitor for changes. |
| period_time | When using "periodic" trigger, specify time in seconds between logs. |
| print_timestamp | Enable (1) / Disable (0) timestamp field in output log. |

## Setup

1. Download & install [Python](https://www.python.org/downloads/) if you haven't already.
2. Run 'setup.bat' (Windows) or 'setup.sh' (Unix) to install dependencies.

Written by Ben DeWeerd.