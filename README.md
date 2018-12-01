## ssh筆記
- mongo admin
  -  映射mongo admin 到http://127.0.0.1:7777 `ssh -o "ExitOnForwardFailure yes" -NL 127.0.0.1:7777:localhost:60005 35.201.215.113` 
  -  連線位置:`mongodb://db:27017/`
- mongo 
  - 映射mongo db 到本機 `ssh -o "ExitOnForwardFailure yes" -NL 127.0.0.1:27017:localhost:27017 35.201.215.113`
