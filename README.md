# _ShadowHashTools_

_Description: ShadowHashTools: Generate, Manipulate and Embed ShadowHash Data_

####First Extract a hash to use 

1. `sudo ./EXTRACT_USER_HASH.py -p password`
_or_
2. `sudo ./EXTRACT_USER_HASH.py -p ~/Desktop/passwordList.txt`

Durring the extract proccess the NT and CRAM-MD5 hashes are removed. These types of hashes are considered insecure. If the desired user is sharing files using SMB you will have to re-enter the user's password in the Sharing Menu to re-enable the NT hashes. 

####Next We will inject the hash
1. `sudo ./INJECT_USER_HASH.py -u shortname -p hash`

_Example_

2. `sudo ./INJECT_USER_HASH.py -u user1 -p 62706c6973743030d101025f101453414c5445442d5348413531322d50424b444632d303040506070857656e74726f70795473616c745a697465726174696f6e734f1080913776ab988b1b979ad58eb72a9b4e64c0e346eae10d0a8fb13a4c4a18ee96c4bdc289299304dc5e9b928d9494ecc2dfa20772d5cbdfee58495fdbee550982345637ac6152cfee4ad56f202ff032f4b2a59333e285a0998b0a50d020dd4c284b1ad9705343ccbf0b5d0259b0376c75ceecb9f05263e1478b8c176e4f5009f54f4f102047ca31ccf4a7a24e40343964789ff5abc2ce97195e33fc9f5dad8caf5dd1b994116073080b2229313641c4e700000000000001010000000000000009000000000000000000000000000000ea`

## License

 Copyright 2014 Thomas Burgin.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
