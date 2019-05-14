# python-flask-myair2-api-translate| 

## MyAirControl API

### Basic API calls

| Call                     | Description                  | Example                                      | 
| ------------------------ | ---------------------------- | -------------------------------------------- | 
| http://pi-3:8000         | base address                 | *this text*                                  |
| /api/getSetTemp          | get the setpoint temp        | 00.0                                         |
| /api/getActTemp          | get the actual temp          | 00.0                                         |
| /api/setTemp             | set the setpoint temp        | 00.0                                         |
| /api/getMode             | get the current running mode | [C,H,F]                                      |
| /api/setMode             | set the running mode         | [C,H,F]                                      |
| /api/getRunning          | get power on / off           | [1,0]                                        |
| /api/setRunning          | set power on / off           | [1,0]                                        |
| /api/getZone/x           | get x zone                   | x = 1..8 name: XXXX open: [1,0] percent: 000 |
| /api/setZone/x/onoff/y   | set x zone on/off            | x = 0..8 y = [1,0]                           |
| /api/setZone/x/percent/y | set x zone percent           | x = 0..8 y = 0..100                          |


