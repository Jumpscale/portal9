## God mode:
god mode allows you to access functionalities overriding the security schema.

To activate god mode:

 - Start the robot with god mode flag 
   ```bash
   zrobot server start -T http://github.com/zero-os/0-templates --god
   ```
 - Then get god token from robot to be able to access functionalities

   ```bash
   zrobot godtoken get
   ```
 - then using portal, set god token in client configurations
    - goto to [URL/ZRGrid/robots]
    - press Add Robot Button 
    - fill all data field and add God token you copied from above step in God token field
    - press Confirm button
    
 - or using Jumpscale, set god token in client configurations 
   ```bash
   cl = j.clients.zrobot.get('instance_name')
   cl.god_token_set('god_token')
   ```
Note: to access the robot in god mode, god mode flag must be set to `true` and you must provide the generated god token
