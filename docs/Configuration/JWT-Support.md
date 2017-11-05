## Portal JWT Authentication

It is possible to authenticate with you JWT token by passing the `Authorization` header.
Example Request:
```
curl -X POST -H 'Authorization:bearer eyJhbGciOiJFUzM4NCIsInR5cCI6IkpXVCJ9.eyJhenAiOiJjT2JQRHdJakE5anFYQUJZYUk2WVZOQXVaZXpHIiwiZXhwIjoxNTA5OTU5OTU2LCJpc3MiOiJpdHN5b3VvbmxpbmUiLCJyZWZyZXNoX3Rva2VuIjoid1FKNGhkVmg5bHRLMlZ2UWVkTHhhX0ZybTRyZiIsInNjb3BlIjpbInVzZXI6YWRtaW4iXSwidXNlcm5hbWUiOiJkZWJvZWNraiJ9.QJA4yExnQNmLCSVX3cDLAQ69-dTe-SHELwh4ZIpQy0YtMG0lLMTyzgIoisFn3g7qMo6_xEwsvNheNZLYi000RgDeh-6FLF2X7tGWyT29v93gergergergertycPos8LzmFWmF69' 'http://172.17.0.2:8200/restmachine/system/usermanager/whoami' 
```

###Adding support for a JWT provider



Example:
```
jwt:
  itsyouonline: MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAES5X8XrfKdx9gYayFITc89wad4usrk0n27MjiGYvqalizeSWTHEpnd7oea9IQ8T5oJjMVH5cc0H5tFSKilFFeh//wngxIyny66+Vq5t5B0V0Ehy01+2ceEon2Y0XDkIKv
  anotherpvoider: MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAESoX8XrfKdx9gYayFITc89wad4usrkjn27MjiGYvqalizeSWTHEpnd7oea9IQ8T5oJjMVH5cc0H5tFSKilFFeg/gwngxIyny66+Vq5t5B0V0Ehy01+2ceEon2Y0XDkIKv
```