## osis 2 eve

goal
- upgrade osis to be based on even & sqlalchemy
- sqlalchemy can be used as database abstraction layer
- eve can be used as rest interface on top
- to have an osis compatible client so existing consumers don't need to be changed & macro's and other business logic works
- write documentation so we know how to extend this eve and how to e.g. add security
- test with mongodb & sqlite

todo
- create convertor to convert osis specs to sqlalchemy specs
    - http://docs.sqlalchemy.org/en/latest/core/metadata.html
- implement business logic in the sqlalchemy base classes (if there is any business logic)
- document the mountaintop repo the database structure used 
- define a std structure where the classes / specs are to be stored so our portal or even can find it
- use hrd as configuration language e.g. for connection string to database
- create code generation to generate swagger 2.0 specs from the eve structure
- create code generation to generate python client which is compatible with osis (if possible) client so portal does not need to be changed

macro's
- document the eve based grid macro's
- make sure the even based grid macro's have style in line with other macro's
- test the macro's 

why
- this will allow easier integration for 3e party with our database structure
- this will allow to use other databases e.g. sqlite under eve which will allow deployment for smaller environments 
