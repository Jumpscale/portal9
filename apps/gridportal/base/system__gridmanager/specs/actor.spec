[actor] @dbtype:mem,fs
    """
    gateway to grid
    """    
    method:getProcessStats
        """     
        ask the right processmanager on right node to get the information
        """
        var:nid int,,id of node 
        var:domain str,,optional domain name for process @tags: optional
        var:name str,,optional name for process @tags: optional
        result:json

    method:getProcessesActive
        """     
        ask the right processmanager on right node to get the info 
        output all relevant info (no stat info for that we have getProcessStats)
        """
        var:nid int,,id of node (if not specified goes to all nodes and aggregates) @tags: optional
        var:name str,,optional name for process name (part of process name) @tags: optional
        var:domain str,,optional name for process domain (part of process domain) @tags: optional
        result:json

    method:getJob
        """
        gets relevant info of job (also logs)
        can be used toreal time return job info
        """
        var:id str,,find based on id @tags: optional
        var:includeloginfo bool,,True,if true fetch all logs of job & return as well @tags: optional
        var:includechildren bool,,True,if true look for jobs which are children & return that info as well @tags: optional

    method:getNodeSystemStats
        """     
        ask the right processmanager on right node to get the information about node system
        """
        var:nid int,,id of node
        result:json

    method:getStatImage
        """     
        get png image as binary format
        comes from right processmanager
        """
        var:statKey str,,e.g. n1.disk.mbytes.read.sda1.last
        var:width int,,500, @tags: optional
        var:height int,,200, @tags: optional
        result:binary

    method:getNodes
        """     
        list found nodes 
        """
        var:id str,,find based on id @tags: optional
        var:gid int,,find nodes for specified grid @tags: optional
        var:name str,,match on text in name @tags: optional
        var:roles str,,match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.) @tags: optional
        var:ipaddr str,,comma separated list of ip addr to match against @tags: optional
        var:macaddr str,,comma separated list of mac addr to match against @tags: optional
        var:active bool,,True,is the node still active @tags: optional
        var:peer_stats int,,id of node which has stats for this node @tags: optional
        var:peer_log int,,id of node which has logs (e.g. transactionlogs) for this node @tags: optional
        var:peer_backup int,,id of node which has backups for this node @tags: optional
        var:lastcheckFrom str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckFrom  (-4d means 4 days ago) @tags: optional
        var:lastcheckTo str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find nodes with lastcheckTo  (-4d means 4 days ago) @tags: optional
        result:list(list)

    method:getMachines
        """     
        list found machines 
        """
        result:list(list)
        var:id str,,find based on id @tags: optional
        var:otherid str,,find based on 2nd id @tags: optional
        var:gid int,,find nodes for specified grid @tags: optional
        var:nid int,,find nodes for specified node @tags: optional
        var:name str,,match on text in name @tags: optional
        var:description str,,match on text in name @tags: optional
        var:state str,,STARTED,STOPPED,RUNNING,FROZEN,CONFIGURED,DELETED @tags: optional
        var:roles str,,match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.) @tags: optional
        var:ipaddr str,,comma separated list of ip addr to match against @tags: optional
        var:macaddr str,,comma separated list of mac addr to match against @tags: optional
        var:active bool,,True,is the machine still active @tags: optional
        var:cpucore int,,find based on nr cpucore @tags: optional
        var:mem int,,find based on mem in MB @tags: optional
        var:type str,,KVM or LXC @tags: optional
        var:lastcheckFrom str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find machines with lastcheckFrom  (-4d means 4 days ago) @tags: optional
        var:lastcheckTo str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find machines with lastcheckTo  (-4d means 4 days ago) @tags: optional

    method:getDisks
        """     
        list found disks (are really partitions) 
        """
        result:list(list)
        var:id str,,find based on id @tags: optional
        var:gid int,,find disks for specified grid @tags: optional
        var:nid int,,find disks for specified node @tags: optional
        var:fs str,,ext4;xfs;... @tags: optional
        var:sizeFrom int,,in MB @tags: optional
        var:sizeTo int,,in MB @tags: optional
        var:freeFrom int,,in MB @tags: optional
        var:freeTo int,,in MB @tags: optional        
        var:mounted bool,,is disk mounted @tags: optional
        var:ssd bool,,is disk an ssd @tags: optional
        var:path str,,match on part of path e.g. /dev/sda @tags: optional
        var:model str,,match on part of model @tags: optional
        var:description str,,match on part of description @tags: optional
        var:mountpoint str,,match on part of mountpoint @tags: optional
        var:type str,,type e.g. BOOT DATA CACHE @tags: optional
        var:active bool,,True,is the disk still active @tags: optional        
        var:lastcheckFrom str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disks with lastcheckFrom  (-4d means 4 days ago) @tags: optional
        var:lastcheckTo str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find disk with lastcheckTo  (-4d means 4 days ago) @tags: optional

    method:getVDisks
        """     
        list found vdisks (virtual disks like qcow2 or sections on fs as used by a container or virtual machine) 
        """
        result:list(list)
        var:machineid int,,to which machine is the vdisk attached @tags: optional
        var:id str,,find based on id @tags: optional
        var:gid int,,find vdisks for specified grid @tags: optional
        var:nid int,,find vdisks for specified node @tags: optional
        var:disk_id int,,find disk which hosts this disk @tags: optional
        var:fs str,,ext4;xfs;... @tags: optional
        var:sizeFrom int,,in MB @tags: optional
        var:sizeTo int,,in MB @tags: optional
        var:freeFrom int,,in MB @tags: optional
        var:freeTo int,,in MB @tags: optional        
        var:sizeondiskFrom int,,in MB @tags: optional
        var:sizeondiskTo int,,in MB @tags: optional        
        var:mounted bool,,is disk mounted @tags: optional
        var:path str,,match on part of path e.g. /dev/sda @tags: optional
        var:description str,,match on part of description @tags: optional
        var:mountpoint str,,match on part of mountpoint @tags: optional
        var:role str,,type e.g. BOOT DATA CACHE @tags: optional
        var:type str,,type e.g. QCOW2 FS @tags: optional
        var:order int,,when more vdisks linked to a vmachine order of linkage @tags: optional
        var:devicename str,,if known device name in vmachine @tags: optional
        var:backup bool,,is this a backup image @tags: optional
        var:backuplocation str,,where is backup stored (tag based notation) @tags: optional
        var:backuptime int,,epoch when was backup taken @tags: optional
        var:backupexpiration int,,when does backup needs to expire @tags: optional
        var:active bool,,True,is the disk still active @tags: optional  
        var:lastcheckFrom str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckFrom  (-4d means 4 days ago) @tags: optional
        var:lastcheckTo str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find vdisks with lastcheckTo  (-4d means 4 days ago) @tags: optional

    method:getLogs
        """     
        interface to get log information
        #result:json array
        """
        var:id str,,find based on id @tags: optional
        var:level int,,level between 1 & 9; all levels underneath are found e.g. level 9 means all levels @tags: optional
        var:category str,,match on multiple categories; are comma separated @tags: optional
        var:text str,,match on text in body @tags: optional 
        var:from_ str,-1h,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs from date specified  (-4d means 4 days ago) @tags: optional
        var:to str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find logs to date specified  @tags: optional
        var:jid int,,find logs for specified jobid @tags: optional
        var:nid int,,find logs for specified node @tags: optional
        var:gid int,,find logs for specified grid @tags: optional
        var:pid int,,find logs for specified process (on grid level) @tags: optional
        var:tags str,,comma separted list of tags/labels @tags: optional

        
    method:getJobs
        """     
        interface to get job information
        #result:json array
        """
        var:id str,,find based on id @tags: optional
        var:from_ str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs from date specified  (-4d means 4 days ago) @tags: optional
        var:to str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find jobs to date specified  @tags: optional
        var:nid int,,find jobs for specified node @tags: optional
        var:gid int,,find jobs for specified grid @tags: optional
        var:parent str,,find jobs which are children of specified parent @tags: optional
        var:roles str,,match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.) @tags: optional
        var:state str,,OK;ERROR;... @tags: optional
        var:organization str,, @tags: optional
        var:name str,, @tags: optional
        var:description str,, any description when asked for the job @tags: optional
        var:category str,,category in dot notation
        var:source str,, who asked for the job is free text @tags: optional


    method:getErrorconditions
        """     
        interface to get errorcondition information (eco)
        #result:json array
        """
        var:id str,,find based on id @tags: optional
        var:level int,,level between 1 & 3; all levels underneath are found e.g. level 3 means all levels @tags: optional
        var:descr str,,match on text in descr @tags: optional  
        var:descrpub str,,match on text in descrpub @tags: optional
        var:from_ str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find ecos from date specified  (-4d means 4 days ago) @tags: optional
        var:to str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find ecos to date specified  @tags: optional
        var:nid int,,find ecos for specified node @tags: optional
        var:gid int,,find ecos for specified grid @tags: optional
        var:category str,,match on multiple categories; are comma separated @tags: optional
        var:tags str,,comma separted list of tags/labels @tags: optional
        var:type int,,  optional unique type id for eco @tags: optional
        var:jid int,,find ecos for specified job @tags: optional

    method:getAudits
        """
        interface to get audit
        #result:json array
        """
        var:id str,,find based on id @tags: optional
        var:nid int,,find alerts for specified node @tags: optional
        var:gid int,,find alerts for specified grid @tags: optional
        var:status_code str,,find audits based on their status code  @tags: optional
        var:user str,,find audits for specified user @tags: optional
        var:from_time str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they happened first (-4d means 4 days ago) @tags: optional
        var:to_time str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they happened first  @tags: optional

    method:getAlerts
        """     
        interface to get alert (is optionally the result of an eco)
        #result:json array
        """
        var:level int,,level between 1 & 3; all levels underneath are found e.g. level 3 means all levels, 1:critical, 2:warning, 3:info @tags: optional
        var:descr str,,match on text in descr @tags: optional  
        var:descrpub str,,match on text in descrpub @tags: optional
        var:id str,,find based on id @tags: optional

        var:nid int,,find alerts for specified node @tags: optional
        var:gid int,,find alerts for specified grid @tags: optional
        var:category str,,match on multiple categories; are comma separated  @tags: optional
        var:tags str,,comma separted list of tags/labels @tags: optional
        var:state str,,NEW ALERT CLOSED @tags: optional
        var:from_inittime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they happened first (-4d means 4 days ago) @tags: optional
        var:to_inittime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they happened first  @tags: optional
        var:from_lasttime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they happened last  (-4d means 4 days ago) @tags: optional
        var:to_lasttime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they happened last  @tags: optional
        var:from_closetime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts from date specified when they were closed  (-4d means 4 days ago) @tags: optional
        var:to_closetime str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find alerts to date specified when they were closed  @tags: optional
        var:nrerrorconditions int,,nr of times errorcondition happened @tags: optional
        var:errorcondition str,,errorcondition(s) which caused this alert @tags: optional


    method:getProcesses
        """     
        list processes , are the grid unique processes (not integrated with processmanager yet)
        """
        var:id str,,find based on id @tags: optional
        var:name str,,match on text in name @tags: optional
        var:nid int,,find logs for specified node @tags: optional
        var:gid int,,find logs for specified grid @tags: optional        
        var:from_ str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes from date specified  (-4d means 4 days ago) @tags: optional
        var:to str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes to date specified @tags: optional
        var:active bool,,True,is the process still active @tags: optional
        var:aysdomain str,, AYS domain of process @tags: optional
        var:aysname str,, AYS name of process @tags: optional
        var:instance str,, instance of process @tags: optional
        var:systempid int,, pid on the system of process @tags: optional
        var:lastcheckFrom str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes with lastcheckFrom  (-4d means 4 days ago) @tags: optional
        var:lastcheckTo str,,-4d;-4w;-4m;-1h;-1s  d=day w=week m=month s=sec  find processes with lastcheckTo  (-4d means 4 days ago) @tags: optional
        result:list(list)

    method:getGrids
        """     
        list grids
        """
        result:list(list)


    method:getJumpscripts
        """
        calls internally the agentcontroller
        return: lists the jumpscripts with main fields (organization, name, category, descr)
        """
        var:organization str,,find jumpscripts @tags: optional
        var:active bool,,is session active or not @tags: optional
        
    method:getJumpscript
        """
        calls internally the agentcontroller to fetch detail for 1 jumpscript
        """
        var:organization str,,
        var:name str,,

    method:getAgentControllerSessions
        """
        calls internally the agentcontroller
        """ 
        var:roles str,,match on comma separated list of roles (subsets also ok e.g. kvm.  would match all roles starting with kvm.) @tags: optional
        var:nid int,,find for specified node (on which agents are running which have sessions with the agentcontroller) @tags: optional
        var:active bool,,is session active or not @tags: optional

    method:getAgentControllerActiveJobs
        """
        calls internally the agentcontroller
        list jobs now running on agentcontroller
        """


