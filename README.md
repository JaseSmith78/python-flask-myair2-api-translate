# python-flask-myair2-api-translate 

## Things to note

Update the settings in myaircontrol.service to match your system 

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

> ### MIT License

> Copyright (c) [2019] [Jason Smith]

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

