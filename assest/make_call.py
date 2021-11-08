import freeswitch
from uuid import uuid4

def fsapi(session, stream, env, args):
    freeswitch.consoleLog("info", "Executando uma chamada. Parametros: {0}...\n".format(args))
    
    _args = args.split()
    
    dial_string, destination, process_id, timeout, amount = _args
    
    context = 'default'
    extension = 'automatic_call'
    amount = int(amount)
    

    dialplan = "XML"    
    for i in range(amount): 
        uniqueid = uuid4()
        variables = '{origination_uuid=%s,CALL_ID=%s,DESTINATION=%s,PROCESS_ID=%s,ignore_early_media=true,sip_sticky_contact=true,absolute_codec_string=PCMA}[leg_timeout=%s]' % (uniqueid, uniqueid, destination, process_id, timeout)

        command = "bgapi originate {0}{1} {2} {3} {4}".format(variables, str(dial_string),  str(extension), str(dialplan), str(context))
        
        freeswitch.consoleLog("info", "FullDial" + str(command) + "\n")
        new_api = freeswitch.API()
        new_api.executeString(command)