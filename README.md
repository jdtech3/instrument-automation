# instrument-automation
Various scripts for automating UTAT's lab gear

## AutoMetrology

[`autometrology`](./autometrology) also lives here: a WIP Python wrapper library for our instruments. Currently maintained by [Joe Dai](https://github.com/jdtech3).

Currently includes drivers for:
  * Keithley 2380-120-60 Electronic DC Load
  * Korad KA3005P DC Power Supply

***Note:*** _drivers do not aim to be feature complete wrappers, but rather only common commands are implemented!_

## Contributing 
To keep code neat, please run the following commands before pushing changes (run `pip3 install -U -r requirements.dev.txt` to install tools):
```
black . && isort . && flake8
```
This will reformat according to PEP8, and alert of any issues that can't be automatically resolved. 

---

*This project is licensed under the MIT license. For more information, please see [LICENSE](./LICENSE).*
